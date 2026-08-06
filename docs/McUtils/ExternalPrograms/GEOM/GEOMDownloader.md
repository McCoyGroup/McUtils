## <a id="McUtils.ExternalPrograms.GEOM.GEOMDownloader">GEOMDownloader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L584)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L584?message=Update%20Docs)]
</div>

Downloads and extracts the GEOM `rdkit_folder` archive.

By default, fetches the whole dataset via its Dataverse persistentId
(returned as a zip wrapping rdkit_folder.tar.gz, which is unwrapped
automatically). If `file_id` is given, downloads that file directly
instead (skips the wrapping zip step; known value for
rdkit_folder.tar.gz is "4327252").

from geom_downloader import GEOMDownloader

downloader = GEOMDownloader(out_dir="./geom_data")
extracted_dir = downloader.download()

# or via direct file id, skipping the dataset-bundle zip:
downloader = GEOMDownloader(out_dir="./geom_data", file_id="4327252")
extracted_dir = downloader.download()







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
PERSISTENT_ID: str
SERVER_URL: str
CHUNK_SIZE: int
RDKIT_DATA_ID: int
```
<a id="McUtils.ExternalPrograms.GEOM.GEOMDownloader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, out_dir: 'str | Path', persistent_id: 'str' = None, server_url: 'str' = None, file_id: 'Optional[str]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L610)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L610?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMDownloader.download" class="docs-object-method">&nbsp;</a> 
```python
download(self, keep_archive: 'bool' = False, skip_download: 'bool' = False) -> 'Path': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMDownloader.py#L749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMDownloader.py#L749?message=Update%20Docs)]
</div>
Download (unless skip_download) and extract the GEOM archive.

Returns the path to the extracted `rdkit_folder` directory.
 </div>
</div>












---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/GEOM/GEOMDownloader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/GEOM/GEOMDownloader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/GEOM/GEOMDownloader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/GEOM/GEOMDownloader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L584?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>