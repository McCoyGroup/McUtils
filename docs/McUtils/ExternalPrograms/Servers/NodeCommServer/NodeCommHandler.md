## <a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler">NodeCommHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L141?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
TCP_SERVER: NodeCommTCPServer
UNIX_SERVER: NodeCommUnixServer
DEFAULT_CONNECTION: tuple
DEFAULT_PORT_ENV_VAR: NoneType
DEFAULT_SOCKET_ENV_VAR: NoneType
MultiprocessingServerContext: MultiprocessingServerContext
client_class: NodeCommClient
```
<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.handle" class="docs-object-method">&nbsp;</a> 
```python
handle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L143?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.handle_json_request" class="docs-object-method">&nbsp;</a> 
```python
handle_json_request(self, message: bytes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L161)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L161?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.setup_env" class="docs-object-method">&nbsp;</a> 
```python
setup_env(self, env): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L179?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.method_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@property
method_dispatch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.dispatch_request" class="docs-object-method">&nbsp;</a> 
```python
dispatch_request(self, request: dict, env: dict): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L186?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_methods" class="docs-object-method">&nbsp;</a> 
```python
get_methods(self) -> 'dict[str,method]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L221)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L221?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_valid_port" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_valid_port(git_port, min_port=4000, max_port=65535): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L225)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L225?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_default_connection" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_connection(cls, port=None, hostname='localhost', session_var='SESSION_ID'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L234?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.start_server" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
start_server(cls, connection=None, port=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L250?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.start_multiprocessing_server" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
start_multiprocessing_server(cls, connection=None, port=None, timeout=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L292?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.client_request" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
client_request(cls, *args, client_class=None, connection=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L298?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L141?message=Update%20Docs)   
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