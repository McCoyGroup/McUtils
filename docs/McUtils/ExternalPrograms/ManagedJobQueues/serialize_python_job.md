# <a id="McUtils.ExternalPrograms.ManagedJobQueues.serialize_python_job">serialize_python_job</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L526)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L526?message=Update%20Docs)]
</div>

```python
serialize_python_job(func, *args, serializer='json', deserializer=None, serialization_mode=None, template='run_sbatch_python.py', path_modifications=None, script_file='run_{job_name}_{id}.py', job_name=None, id=None, state_string=None, post_processor='print', cleanup=False, function_args=None, function_kwargs=None, **kwargs): 
```
**LLM Docstring**

Serialize function arguments, pickle and base64-encode the callable and optional post-processor, substitute them into a Python runner template, and return a `FileBackedIO` for the generated script.
  - `func`: `object`
    > the Python callable executed by the generated runner

  - `serializer`: `object`
    > serializer instance, registered serializer name, or callable

  - `deserializer`: `object`
    > deserializer name or callable embedded in the generated script

  - `serialization_mode`: `object`
    > whether generated code uses McUtils serializer dispatch or an explicit function

  - `template`: `object`
    > runner-template text or template filename

  - `path_modifications`: `object`
    > paths inserted into the generated runner’s import search path

  - `script_file`: `object`
    > format string for the generated Python filename

  - `job_name`: `object`
    > scheduler-visible job name

  - `id`: `object`
    > explicit generated-script identifier

  - `state_string`: `object`
    > pre-serialized argument state

  - `post_processor`: `object`
    > callable or named post-processing expression for the result

  - `cleanup`: `object`
    > whether the generated runner removes its files after execution

  - `function_args`: `object`
    > explicit positional arguments to serialize

  - `function_kwargs`: `object`
    > explicit keyword arguments to serialize

  - `args`: `object`
    > positional command or function arguments

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `dev.FileBackedIO`
    > serialize function arguments, pickle and base64-encode the callable and optional post-processor, substitute them into a Python runner template, and return a `FileBackedIO` for the generated script.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/serialize_python_job.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/serialize_python_job.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/serialize_python_job.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/serialize_python_job.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L526?message=Update%20Docs)   
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