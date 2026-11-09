"""External integer sort/unique and mapped sparse matrix storage."""
from pathlib import Path
import tempfile
from ..Devutils.FileHelpers import atomic_file
import os
import functools
import time
from contextlib import ExitStack
import numpy as np

__all__ = ['MappedArrayFlushBuffer', 'external_unique', 'save_sparse_matrix', 'load_sparse_matrix', 'release_mapped_pages']


class MappedArrayFlushBuffer:
    """Bound pending writeback of disposable mapped files, without owning maps.

    ``defer(array)`` records its file identity and closes no mappings. Call
    ``discard(path)`` before deleting a consumed temporary file. Remaining
    files are synced oldest first when either queue limit is exceeded, or
    all at once by ``flush()``. No descriptors, arrays or mappings are retained.

    Limits count file sizes, not dirty pages or resident memory. The OS can
    write pages independently; this is not a RAM limit. Caller-owned final
    outputs should still be flushed explicitly at their persistence boundary.
    """
    def __init__(self, max_bytes=256*1024**2, max_files=64):
        for name, value in [('max_bytes', max_bytes), ('max_files', max_files)]:
            if (value is None and name == 'max_bytes'):
                continue
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
                raise ValueError('{} must be positive integer{}'.format(name, ' bytes or None' if name == 'max_bytes' else ''))
        import threading
        self.max_bytes = None if max_bytes is None else int(max_bytes)
        self.max_files = int(max_files)
        self._pending = {}
        self._pending_bytes = 0
        self._lock = threading.RLock()
        self._closed = False
        self._metrics = dict(enqueued_files=0, enqueued_bytes=0, flushed_files=0,
                             flushed_bytes=0, discarded_files=0, discarded_bytes=0,
                             flush_seconds=0., peak_pending_bytes=0, peak_pending_files=0)

    @staticmethod
    def _path(array_or_path):
        return Path(os.path.abspath(os.fspath(getattr(array_or_path, 'filename', array_or_path))))

    def defer(self, array):
        """Queue a shared writable file mapping before its owner closes it."""
        if not isinstance(array, np.memmap) or array.mode not in ('r+', 'w+'):
            raise TypeError('deferred writeback requires a shared writable NumPy memmap')
        with self._lock:
            if self._closed:
                raise RuntimeError('flush buffer is closed')
            path = self._path(array)
            stat = path.stat()
            identity = (stat.st_dev, stat.st_ino)
            previous = self._pending.get(path)
            if previous is not None:
                if previous[:2] != identity:
                    raise RuntimeError('pending mapped file was replaced: {}'.format(path))
                self._pending_bytes -= previous[2]
            else:
                self._metrics['enqueued_files'] += 1
                self._metrics['enqueued_bytes'] += stat.st_size
            self._pending[path] = identity + (stat.st_size,)
            self._pending_bytes += stat.st_size
            self._metrics['peak_pending_bytes'] = max(self._metrics['peak_pending_bytes'], self._pending_bytes)
            self._metrics['peak_pending_files'] = max(self._metrics['peak_pending_files'], len(self._pending))
            while (len(self._pending) > self.max_files or
                   (self.max_bytes is not None and self._pending_bytes > self.max_bytes)):
                self._flush_one(next(iter(self._pending)))

    def _flush_one(self, path):
        device, inode, size = self._pending[path]
        started = time.perf_counter()
        try:
            with open(path, 'rb') as stream:
                stat = os.fstat(stream.fileno())
                if (stat.st_dev, stat.st_ino) != (device, inode):
                    raise RuntimeError('pending mapped file was replaced: {}'.format(path))
                # A whole-file sync includes pages from already-closed shared
                # mappings, without recreating mappings or retaining buffers.
                getattr(os, 'fdatasync', os.fsync)(stream.fileno())
        finally:
            self._metrics['flush_seconds'] += time.perf_counter() - started
        del self._pending[path]
        self._pending_bytes -= size
        self._metrics['flushed_files'] += 1
        self._metrics['flushed_bytes'] += size

    def flush(self):
        """Synchronously write back every still-pending file; propagate errors."""
        with self._lock:
            for path in list(self._pending):
                self._flush_one(path)

    def discard(self, path, *, recursive=False):
        """Forget consumed temporary files; never unlink or close their owners."""
        path = self._path(path)
        with self._lock:
            paths = ([p for p in self._pending if p == path or path in p.parents]
                     if recursive else [path] if path in self._pending else [])
            for p in paths:
                size = self._pending.pop(p)[2]
                self._pending_bytes -= size
                self._metrics['discarded_files'] += 1
                self._metrics['discarded_bytes'] += size

    def snapshot(self):
        with self._lock:
            return dict(self._metrics, pending_files=len(self._pending), pending_bytes=self._pending_bytes,
                        max_bytes=self.max_bytes, max_files=self.max_files, closed=self._closed)

    def close(self):
        with self._lock:
            if not self._closed:
                self.flush()
                self._closed = True

    def __enter__(self):
        if self._closed:
            raise RuntimeError('flush buffer is closed')
        return self

    def __exit__(self, *exc):
        self.close()

    def __getstate__(self):
        with self._lock:
            if self._pending:
                raise TypeError('cannot serialize pending mapped-file writeback')
            return dict(max_bytes=self.max_bytes, max_files=self.max_files, closed=self._closed)

    def __setstate__(self, state):
        self.__init__(state['max_bytes'], state['max_files'])
        self._closed = state['closed']


def release_mapped_pages(array, *, writeback=True):
    """Release resident pages without closing a mapping or invalidating views.

    Flush writable data first unless the caller has already done so. This is
    OS advice, not a hard RAM/cache cap; unsupported platforms return False.
    """
    import mmap
    current = array
    while current is not None and not isinstance(current, mmap.mmap):
        mapping = getattr(current, '_mmap', None)
        current = mapping if mapping is not None else getattr(current, 'base', None)
    if current is None or current.closed:
        return False
    if not hasattr(current, 'madvise') or not hasattr(mmap, 'MADV_DONTNEED'):
        return False
    if writeback:
        current.flush()
    current.madvise(mmap.MADV_DONTNEED)
    return True


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
            if positions is not None:positions[k]=min(lp[i],rp[j])
            i+=1;j+=1
        elif which==0:
            for col in range(out.shape[1]):out[k,col]=left[i,col]
            if positions is not None:positions[k]=lp[i]
            i+=1
        else:
            for col in range(out.shape[1]):out[k,col]=right[j,col]
            if positions is not None:positions[k]=rp[j]
            j+=1
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


def _sorted_runs(arrays, root, chunk_size, mappings, *, track_positions=True, flush_buffer=None):
    # One run per binary level. Merge equal-sized groups of input chunks as
    # they arrive, so repeated keys are removed before every run is spilled.
    pending=[];offset=0;width=None;ndim=None;buffer=None;filled=0;serial=0

    def new_path(kind):
        nonlocal serial
        path=root/f'{kind}_{serial}';serial+=1
        return path

    def merge_runs(left, right):
        (a,na),(b,nb)=left,right
        path=new_path('merge')
        with ExitStack() as opened:
            def own(array):
                opened.callback(_close_mapping,array)
                return array
            ak=own(np.load(str(a)+'_keys.npy',mmap_mode='r')[:na])
            ap=own(np.load(str(a)+'_positions.npy',mmap_mode='r')[:na]) if track_positions else None
            bk=own(np.load(str(b)+'_keys.npy',mmap_mode='r')[:nb])
            bp=own(np.load(str(b)+'_positions.npy',mmap_mode='r')[:nb]) if track_positions else None
            out=own(np.lib.format.open_memmap(str(path)+'_keys.npy',mode='w+',dtype=np.int64,shape=(na+nb,width)))
            pos=(own(np.lib.format.open_memmap(str(path)+'_positions.npy',mode='w+',dtype=np.int64,shape=(na+nb,)))
                 if track_positions else None)
            size=int(_merge_function()(ak,ap,bk,bp,out,pos))
            if flush_buffer is None:
                out.flush()
                if pos is not None:pos.flush()
            else:
                # Both consumed runs can be forgotten before a size-triggered
                # writeback. Their contents have already reached the new run.
                for old in [a,b]:
                    flush_buffer.discard(str(old)+'_keys.npy')
                    if track_positions:flush_buffer.discard(str(old)+'_positions.npy')
                flush_buffer.defer(out)
                if pos is not None:flush_buffer.defer(pos)
        del ak,ap,bk,bp,out,pos
        for old in [a,b]:
            for suffix in (['_keys.npy','_positions.npy'] if track_positions else ['_keys.npy']):
                Path(str(old)+suffix).unlink()
        return path,size

    def emit(block, origin):
        if track_positions:
            keys,positions=np.unique(block,axis=0,return_index=True)
        elif width == 1:
            # Scalar IDs need neither structured row sorting nor stable argsort.
            keys=np.unique(block[:,0]).reshape(-1,1)
        else:
            keys=np.unique(block,axis=0)
        path=new_path('run')
        np.save(str(path)+'_keys.npy',keys)
        if track_positions:np.save(str(path)+'_positions.npy',positions+origin)
        run=(path,len(keys));level=0
        while level<len(pending) and pending[level] is not None:
            run=merge_runs(pending[level],run)
            pending[level]=None;level+=1
        if level==len(pending):pending.append(run)
        else:pending[level]=run

    for array in arrays:
        array=np.asanyarray(array)
        # Empty chunks still establish the input row shape without keys to
        # validate; preserve the existing integer-vector/row API.
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
    # Smaller levels are the newest tail chunks. Fold those first, putting
    # each older level on the left: the same ragged balanced tree as before.
    result=None
    for run in pending:
        if run is not None:result=run if result is None else merge_runs(run,result)
    if result is None:
        return (np.empty((0,width or 1),dtype=np.int64),
                np.empty(0,dtype=np.int64) if track_positions else None,ndim or 1)
    path,size=result
    keys=np.load(str(path)+'_keys.npy',mmap_mode='r')[:size]
    mappings.append(keys)
    positions=None
    if track_positions:
        positions=np.load(str(path)+'_positions.npy',mmap_mode='r')[:size]
        mappings.append(positions)
    return keys,positions,ndim


def external_unique(arrays, *, sort=True, return_index=False, return_values=True, chunk_size=262144,
                    directory=None, output_file=None, flush_buffer=None):
    """Deduplicate integer inputs using sorted disk runs and pairwise merges.

    ``sort=False`` preserves first-occurrence order across the input stream.
    The final output is an ordinary array, or a mapped .npy when output_file
    is supplied. No inverse array or concatenated copy of all inputs is made.
    With ``flush_buffer`` intermediate disposable merge files defer writeback;
    consumed files are removed from its queue. The final ``output_file`` is
    always flushed before return. None preserves immediate intermediate flushes.
    """
    if chunk_size<1:raise ValueError('chunk_size must be positive')
    if isinstance(arrays,np.ndarray):arrays=[arrays]
    if directory is not None:Path(directory).mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory,prefix='external_unique_') as work:
        mappings=[]
        try:
            root=Path(work)
            keys,positions,ndim=_sorted_runs(arrays,root,int(chunk_size),mappings,
                                             track_positions=not sort or return_index,flush_buffer=flush_buffer)
            if not sort and len(keys):
                ordered=root/'stable';ordered.mkdir()
                records=((np.column_stack((positions[i:i+chunk_size],keys[i:i+chunk_size]))
                          if return_values else positions[i:i+chunk_size,None])
                         for i in range(0,len(keys),chunk_size))
                stable,_,_=_sorted_runs(records,ordered,int(chunk_size),mappings,
                                         track_positions=False,flush_buffer=flush_buffer)
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
            if flush_buffer is not None:
                # Only our owned disposable directory is retired. A shared
                # caller buffer may still own unrelated pending files.
                flush_buffer.discard(root,recursive=True)
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
    with atomic_file(path,'wb',fsync=False,keep_mode=False) as stream:
        np.savez(stream,data=matrix.data,indices=matrix.indices,indptr=matrix.indptr,
                 shape=np.asarray(matrix.shape,dtype=np.int64))


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
