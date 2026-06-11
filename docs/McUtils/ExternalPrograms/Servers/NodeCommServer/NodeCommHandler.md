## <a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler">NodeCommHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L142?message=Update%20Docs)]
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
DEFAULT_CONNECTION_FILE_ENV_VAR: NoneType
MultiprocessingServerContext: MultiprocessingServerContext
client_class: NodeCommClient
```
<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.handle" class="docs-object-method">&nbsp;</a> 
```python
handle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L144?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.handle_json_request" class="docs-object-method">&nbsp;</a> 
```python
handle_json_request(self, message: bytes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L162?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.setup_env" class="docs-object-method">&nbsp;</a> 
```python
setup_env(self, env): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L180?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.method_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@property
method_dispatch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L183?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.dispatch_request" class="docs-object-method">&nbsp;</a> 
```python
dispatch_request(self, request: dict, env: dict): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L187?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_methods" class="docs-object-method">&nbsp;</a> 
```python
get_methods(self) -> 'dict[str,method]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer/NodeCommHandler.py#L222?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_valid_port" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_valid_port(git_port, min_port=4000, max_port=65535): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L226?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.get_default_connection" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_connection(cls, port=None, hostname='localhost', session_var='SESSION_ID'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L235?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.serialize_connection" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
serialize_connection(cls, connection, mode): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L253?message=Update%20Docs)]
</div>
Build a JSON-serializable dict describing the connection.


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.write_connection_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
write_connection_file(cls, connection_file, connection, mode): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L264?message=Update%20Docs)]
</div>
Write the connection details out as JSON for clients to consume.


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.read_connection_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
read_connection_file(cls, connection_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L274?message=Update%20Docs)]
</div>
Read connection details written by `start_server` and return a
connection spec usable by a client (tuple for TCP, str path for Unix).


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.start_server" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
start_server(cls, connection=None, port=None, connection_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L288)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L288?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.parse_kwargs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_kwargs(cls, extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L343?message=Update%20Docs)]
</div>
Convert leftover ``--`` tokens into a kwargs dict.

Supports ``--key value``, ``--key=value``, and bare ``--flag`` (-> True).
Values are run through JSON parsing for automatic type conversion, so
``--count 3`` yields ``{'count': 3}`` and ``--name foo`` yields
``{'name': 'foo'}``.


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.build_arg_parser" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_arg_parser(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L372)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L372?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.resolve_connection" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_connection(cls, socket=None, host='localhost', port=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L414)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L414?message=Update%20Docs)]
</div>
Pick a connection spec from CLI options.

Priority: --socket (Unix) > --host/--port (TCP) > class defaults.


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.main" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
main(cls, argv=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L426?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.resolve_roots" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_roots(cls, base, roots=None, allowed_domains=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L471)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L471?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.create_server_package" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_server_package(cls, hostpath, package_name=None, overwrite=False, dependency_paths=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L483?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.start_multiprocessing_server" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
start_multiprocessing_server(cls, connection=None, port=None, timeout=3, connection_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L533)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L533?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Servers.NodeCommServer.NodeCommHandler.client_request" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
client_request(cls, *args, client_class=None, connection=None, connection_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L542?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Servers/NodeCommServer.py#L142?message=Update%20Docs)   
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