# <a id="McUtils.Scaffolding">McUtils.Scaffolding</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides development utilities.
Each utility attempts to be almost entirely standalone (although there is
a small amount of cross-talk within the packages).
In order of usefulness, the design is:
1. `Logging` provides a flexible logging interface where the log data can be
reparsed and loggers can be passed around
2. `Serializers`/`Checkpointing` provides interfaces for writing/loading data
to file and allows for easy checkpoint loading
3. `Jobs` provides simpler interfaces for running jobs using the existing utilities
4. `CLIs` provides simple command line interface helpers

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[Cache](McUtils/McUtils/Scaffolding/Caches/Cache.md)   
</div>
   <div class="col" markdown="1">
[MaxSizeCache](McUtils/McUtils/Scaffolding/Caches/MaxSizeCache.md)   
</div>
   <div class="col" markdown="1">
[ObjectRegistry](McUtils/McUtils/Scaffolding/Caches/ObjectRegistry.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PseudoPickler](McUtils/McUtils/Scaffolding/Serializers/PseudoPickler.md)   
</div>
   <div class="col" markdown="1">
[BaseSerializer](McUtils/McUtils/Scaffolding/Serializers/BaseSerializer.md)   
</div>
   <div class="col" markdown="1">
[JSONSerializer](McUtils/McUtils/Scaffolding/Serializers/JSONSerializer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[NumPySerializer](McUtils/McUtils/Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[NDarrayMarshaller](McUtils/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[HDF5Serializer](McUtils/McUtils/Scaffolding/Serializers/HDF5Serializer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[YAMLSerializer](McUtils/McUtils/Scaffolding/Serializers/YAMLSerializer.md)   
</div>
   <div class="col" markdown="1">
[ModuleSerializer](McUtils/McUtils/Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[Schema](McUtils/McUtils/Scaffolding/Schema/Schema.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[LogParser](McUtils/McUtils/Scaffolding/Logging/LogParser.md)   
</div>
   <div class="col" markdown="1">
[Checkpointer](McUtils/McUtils/Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[CheckpointerKeyError](McUtils/McUtils/Scaffolding/Checkpointing/CheckpointerKeyError.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[DumpCheckpointer](McUtils/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[JSONCheckpointer](McUtils/McUtils/Scaffolding/Checkpointing/JSONCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[NumPyCheckpointer](McUtils/McUtils/Scaffolding/Checkpointing/NumPyCheckpointer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HDF5Checkpointer](McUtils/McUtils/Scaffolding/Checkpointing/HDF5Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[DictCheckpointer](McUtils/McUtils/Scaffolding/Checkpointing/DictCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[NullCheckpointer](McUtils/McUtils/Scaffolding/Checkpointing/NullCheckpointer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PersistenceLocation](McUtils/McUtils/Scaffolding/Persistence/PersistenceLocation.md)   
</div>
   <div class="col" markdown="1">
[PersistenceManager](McUtils/McUtils/Scaffolding/Persistence/PersistenceManager.md)   
</div>
   <div class="col" markdown="1">
[ResourceManager](McUtils/McUtils/Scaffolding/Persistence/ResourceManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[BaseObjectManager](McUtils/McUtils/Scaffolding/ObjectBackers/BaseObjectManager.md)   
</div>
   <div class="col" markdown="1">
[FileBackedObjectManager](McUtils/McUtils/Scaffolding/ObjectBackers/FileBackedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Config](McUtils/McUtils/Scaffolding/Configurations/Config.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ParameterManager](McUtils/McUtils/Scaffolding/Configurations/ParameterManager.md)   
</div>
   <div class="col" markdown="1">
[Job](McUtils/McUtils/Scaffolding/Jobs/Job.md)   
</div>
   <div class="col" markdown="1">
[JobManager](McUtils/McUtils/Scaffolding/Jobs/JobManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CLI](McUtils/McUtils/Scaffolding/CLIs/CLI.md)   
</div>
   <div class="col" markdown="1">
[CommandGroup](McUtils/McUtils/Scaffolding/CLIs/CommandGroup.md)   
</div>
   <div class="col" markdown="1">
[Command](McUtils/McUtils/Scaffolding/CLIs/Command.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/__init__.py#L1?message=Update%20Docs)   
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