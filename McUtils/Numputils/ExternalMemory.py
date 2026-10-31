"""External integer sort/unique and mapped sparse matrix storage."""
from pathlib import Path
import tempfile
import os
import functools
import numpy as np

__all__ = ['external_unique', 'save_sparse_matrix', 'load_sparse_matrix']


def _merge(left, lp, right, rp, out, positions):
    i=j=k=0
    while i<len(left) or j<len(right):
        which=-1
        if i==len(left):which=1
        elif j==len(right):which=0
        else:
            for col in range(left.shape[1]):
                if left[i,col]<right[j,col]:which=0;break
                if left[i,col]>right[j,col]:which=1;break
        if which<0:
            for col in range(out.shape[1]):out[k,col]=left[i,col]
            positions[k]=min(lp[i],rp[j]);i+=1;j+=1
        elif which==0:
            for col in range(out.shape[1]):out[k,col]=left[i,col]
            positions[k]=lp[i];i+=1
        else:
            for col in range(out.shape[1]):out[k,col]=right[j,col]
            positions[k]=rp[j];j+=1
        k+=1
    return k


@functools.lru_cache(maxsize=1)
def _merge_function():
    # Keep NumPy-only McUtils imports independent of the optional accelerator.
    try:
        from numba import njit
    except ImportError:
        return _merge
    return njit(cache=True)(_merge)


def _close_mapping(array):
    mapping=getattr(array,'_mmap',None)
    if mapping is not None and not mapping.closed:mapping.close()


def _sorted_runs(arrays, root, chunk_size, mappings):
    runs=[];offset=0;width=None;ndim=None;buffer=None;filled=0
    def emit(block, origin):
        keys,positions=np.unique(block,axis=0,return_index=True)
        path=root/f'run_{len(runs)}'
        np.save(str(path)+'_keys.npy',keys)
        np.save(str(path)+'_positions.npy',positions+origin)
        runs.append((path,len(keys)))
    for array in arrays:
        array=np.asanyarray(array)
        # NumPy gives [] a floating dtype. Empty chunks contain no keys to
        # validate; retain their vector/row shape without coercing any values.
        if array.ndim in [1,2] and len(array)==0:
            array=np.empty(array.shape,dtype=np.int64)
        if array.ndim not in [1,2] or array.dtype.kind not in 'iu':
            raise TypeError('external unique requires integer vectors or row arrays')
        if array.dtype.kind=='u' and array.size and array.max()>np.iinfo(np.int64).max:
            raise OverflowError('external unique keys must fit signed int64')
        if ndim is None:
            ndim=array.ndim;width=1 if ndim==1 else array.shape[1]
            buffer=np.empty((chunk_size,width),dtype=np.int64)
        if array.ndim!=ndim or (ndim==2 and array.shape[1]!=width):
            raise ValueError('all external unique inputs must have the same row shape')
        start=0
        while start<len(array):
            count=min(chunk_size-filled,len(array)-start)
            buffer[filled:filled+count]=array[start:start+count].reshape(-1,width)
            filled+=count;start+=count
            if filled==chunk_size:
                emit(buffer,offset);offset+=filled;filled=0
    if filled:emit(buffer[:filled],offset)
    del buffer
    generation=0
    while len(runs)>1:
        merged=[]
        for pair in range(0,len(runs),2):
            if pair+1==len(runs):merged.append(runs[pair]);continue
            (a,na),(b,nb)=runs[pair:pair+2]
            ak=np.load(str(a)+'_keys.npy',mmap_mode='r')[:na]
            ap=np.load(str(a)+'_positions.npy',mmap_mode='r')[:na]
            bk=np.load(str(b)+'_keys.npy',mmap_mode='r')[:nb]
            bp=np.load(str(b)+'_positions.npy',mmap_mode='r')[:nb]
            path=root/f'merge_{generation}_{pair}'
            out=np.lib.format.open_memmap(str(path)+'_keys.npy',mode='w+',dtype=np.int64,shape=(na+nb,width))
            pos=np.lib.format.open_memmap(str(path)+'_positions.npy',mode='w+',dtype=np.int64,shape=(na+nb,))
            mappings.extend([ak,ap,bk,bp,out,pos])
            size=int(_merge_function()(ak,ap,bk,bp,out,pos));out.flush();pos.flush()
            for array in [ak,ap,bk,bp,out,pos]:_close_mapping(array)
            del ak,ap,bk,bp,out,pos
            for old in [a,b]:
                for suffix in ['_keys.npy','_positions.npy']:Path(str(old)+suffix).unlink()
            merged.append((path,size))
        runs=merged;generation+=1
    if not runs:return np.empty((0,width or 1),dtype=np.int64),np.empty(0,dtype=np.int64),ndim or 1
    path,size=runs[0]
    keys=np.load(str(path)+'_keys.npy',mmap_mode='r')[:size]
    positions=np.load(str(path)+'_positions.npy',mmap_mode='r')[:size]
    mappings.extend([keys,positions])
    return keys,positions,ndim


def external_unique(arrays, *, sort=True, return_index=False, return_values=True, chunk_size=262144,
                    directory=None, output_file=None):
    """Deduplicate integer inputs using sorted disk runs and pairwise merges.

    ``sort=False`` preserves first-occurrence order across the input stream.
    The final output is an ordinary array, or a mapped .npy when output_file
    is supplied. No inverse array or concatenated copy of all inputs is made.
    """
    if chunk_size<1:raise ValueError('chunk_size must be positive')
    if isinstance(arrays,np.ndarray):arrays=[arrays]
    if directory is not None:Path(directory).mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory,prefix='external_unique_') as work:
        mappings=[]
        try:
            root=Path(work)
            keys,positions,ndim=_sorted_runs(arrays,root,int(chunk_size),mappings)
            if not sort and len(keys):
                ordered=root/'stable';ordered.mkdir()
                records=((np.column_stack((positions[i:i+chunk_size],keys[i:i+chunk_size]))
                          if return_values else positions[i:i+chunk_size,None])
                         for i in range(0,len(keys),chunk_size))
                stable,_,_=_sorted_runs(records,ordered,int(chunk_size),mappings)
                positions=stable[:,0]
                if return_values:keys=stable[:,1:]
            shape=(len(keys),) if ndim==1 else keys.shape
            if not return_values:
                if output_file is not None:raise ValueError('output_file requires return_values=True')
                values=None
            elif output_file is None:
                values=np.array(keys,copy=True).reshape(shape)
            else:
                path=Path(output_file);path.parent.mkdir(parents=True,exist_ok=True)
                values=np.lib.format.open_memmap(path,mode='w+',dtype=np.int64,shape=shape)
                for i in range(0,len(keys),chunk_size):values[i:i+chunk_size]=keys[i:i+chunk_size].reshape((-1,)+shape[1:])
                values.flush()
            first=np.array(positions,copy=True) if return_index else None
            return (values,first) if return_index else values
        finally:
            # Close before removing files: unlinking an open mmap leaves NFS
            # .nfs files that can prevent TemporaryDirectory from cleaning up.
            for array in mappings:_close_mapping(array)


def save_sparse_matrix(file, matrix):
    """Save CSR components without densifying or building a whole byte string."""
    from .Sparse import SparseArray
    if matrix.ndim != 2:raise ValueError('mapped sparse storage requires a matrix')
    if isinstance(matrix,SparseArray):matrix=matrix.data
    matrix=matrix.tocsr(copy=False)
    # NumPy writes zip members in bounded buffers; use uncompressed members
    # so the existing McUtils archive reader can map their data offsets.
    path=Path(file);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.npz',delete=False) as stream:
            temporary=Path(stream.name)
        np.savez(temporary,data=matrix.data,indices=matrix.indices,indptr=matrix.indptr,
                 shape=np.asarray(matrix.shape,dtype=np.int64))
        os.replace(temporary,path)
    finally:
        if temporary is not None and temporary.exists():temporary.unlink()


def load_sparse_matrix(file, *, mode='r'):
    """Load a native SparseArray retaining mapped CSR component buffers."""
    import scipy.sparse as sp
    from .Sparse import SparseArray
    from .Serialization import load_npz_memmap
    archive=load_npz_memmap(file,mode=mode)
    matrix=sp.csr_matrix((archive['data'],archive['indices'],archive['indptr']),
                         shape=tuple(archive['shape']),copy=False)
    result=SparseArray.from_data(matrix,cache_block_data=False)
    # Keep the archive owner alive for at least as long as the sparse wrapper.
    result._mapped_archive=archive
    return result
