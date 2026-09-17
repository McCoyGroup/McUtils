## <a id="McUtils.Plots.X3DInterface.X3D">X3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L132?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
defaults: dict
xite_options: dict
X_ITE_JS: str
X3DOM_JS: str
X3DOM_CSS: str
MATHJAX_CDN: str
```
<a id="McUtils.Plots.X3DInterface.X3D.get_new_id" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_new_id(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L144?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate a fresh `x3d-`-prefixed id.
  - `:returns`: `str`
    > the id


<a id="McUtils.Plots.X3DInterface.X3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *children, id=None, dynamic_loading=True, use_xite=False, xite_options=None, x3dom_path=None, x3dom_css_path=None, include_mathjax=False, recording_options=None, include_export_button=False, include_record_button=False, include_view_settings_button=False, preload_scripts=None, onload_scripts=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L155?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the top-level X3D scene container: its children, size, resource paths, and
the optional export/record/view-settings UI and MathJax/loader scripting.
  - `children`: `Any`
    > the scene's child objects
  - `id`: `Any`
    > the DOM id (auto-generated if omitted)
  - `dynamic_loading`: `bool`
    > load the X3DOM runtime dynamically
  - `x3dom_path`: `Any`
    > an override path/URL for the X3DOM JS
  - `x3dom_css_path`: `Any`
    > an override path/URL for the X3DOM CSS
  - `include_mathjax`: `bool`
    > include MathJax for text rendering
  - `recording_options`: `dict | None`
    > options for the screen recorder
  - `include_export_button`: `bool`
    > include the image-export button
  - `include_record_button`: `bool`
    > include the screen-record button
  - `include_view_settings_button`: `bool`
    > include the view-settings button
  - `preload_scripts`: `Any`
    > scripts to run before the scene loads
  - `onload_scripts`: `Any`
    > scripts to run once the scene loads
  - `opts`: `Any`
    > extra scene options (e.g. width/height)


<a id="McUtils.Plots.X3DInterface.X3D.get_export_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_export_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L232?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the JavaScript that exports the scene canvas to a PNG and triggers a download.
  - `id`: `str`
    > the scene DOM id
  - `:returns`: `str`
    > the export script


<a id="McUtils.Plots.X3DInterface.X3D.get_ready_check_expression" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_ready_check_expression(cls, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L254?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the JavaScript predicate `rasterize` polls (via Playwright's
`wait_for_function`) to find out whether X3DOM has actually
started rendering the scene with the given wrapper `id`, instead
of sleeping a fixed amount of time and hoping it was enough.

Each `<x3d>` element gets its own `Runtime` object -- attached
directly to that DOM element as `.runtime`, *not* reachable through
`x3dom.canvases[...]` -- whose `.isReady` flips `true` on the
first animation-frame tick once the WebGL backend is set up (right
before that frame actually renders). Reading it back off the
element like this, rather than installing our own hook such as a
custom `x3dom.runtime.ready`, is also what makes this robust to
`to_widget()`/`to_html()` sometimes emitting the x3dom `<script>`
tag twice on the same page (harmless for X3DOM itself, but it
re-runs that script's top-level `var x3dom = {...}` and so would
silently wipe out any hook installed between the two runs).
  - `id`: `str`
    > the scene's wrapper element id (`X3D.id`)
  - `:returns`: `str`
    > the ready-check predicate, as the body of a Playwright
    `wait_for_function` expression


<a id="McUtils.Plots.X3DInterface.X3D.get_view_settings_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_view_settings_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L291?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the JavaScript that reads the current view matrix and writes it into the view-matrix output field.
  - `id`: `str`
    > the scene DOM id
  - `:returns`: `str`
    > the script


<a id="McUtils.Plots.X3DInterface.X3D.parse_view_matrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_view_matrix(cls, vs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L319?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a serialized X3DOM view matrix into `{position, orientation}` viewpoint
options (inverting the matrix and extracting the rotation angle/axis).
  - `vs`: `Any`
    > the view matrix (JSON string or array)
  - `:returns`: `dict`
    > the viewpoint options


<a id="McUtils.Plots.X3DInterface.X3D.get_record_screen_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_record_screen_script(self, id, polling_rate=30, recording_duration=2, video_format='video/webm'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L341)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L341?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the JavaScript that records the scene canvas to a video and triggers a download.
  - `id`: `str`
    > the scene DOM id
  - `polling_rate`: `int`
    > the capture frame rate
  - `recording_duration`: `float`
    > the recording length in seconds
  - `video_format`: `str`
    > the recording MIME type
  - `:returns`: `str`
    > the recording script


<a id="McUtils.Plots.X3DInterface.X3D.set_animation_duration_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
set_animation_duration_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L395)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L395?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the JavaScript that reads the duration input and stores it on the canvas.
  - `id`: `str`
    > the scene DOM id
  - `:returns`: `str`
    > the script


<a id="McUtils.Plots.X3DInterface.X3D.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, dynamic_loading=None, include_export_button=None, include_record_button=None, include_view_settings_button=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L469?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the scene to an interactive X3DOM widget (cached), wiring up the loader
scripts and any export/record/view-settings UI.
  - `dynamic_loading`: `bool | None`
    > load the runtime dynamically
  - `include_export_button`: `bool | None`
    > include the export button
  - `include_record_button`: `bool | None`
    > include the record button
  - `include_view_settings_button`: `bool | None`
    > include the view-settings button
  - `:returns`: `_`
    > the widget


<a id="McUtils.Plots.X3DInterface.X3D.to_html" class="docs-object-method">&nbsp;</a> 
```python
to_html(self, *base_elems, header_elems=None, dynamic_loading=False, include_export_button=None, include_record_button=None, **header_info): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L618)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L618?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap the scene widget in a full HTML document (with the X3DOM CSS/JS in the head).
  - `base_elems`: `Any`
    > extra body elements
  - `header_elems`: `list | None`
    > extra head elements
  - `dynamic_loading`: `bool`
    > load the runtime dynamically
  - `include_export_button`: `bool | None`
    > include the export button
  - `include_record_button`: `bool | None`
    > include the record button
  - `header_info`: `Any`
    > extra head attributes
  - `:returns`: `_`
    > the HTML document


<a id="McUtils.Plots.X3DInterface.X3D.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L674)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L674?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the scene widget's MIME bundle for rich display.
  - `:returns`: `dict`
    > the MIME bundle


<a id="McUtils.Plots.X3DInterface.X3D.to_x3d" class="docs-object-method">&nbsp;</a> 
```python
to_x3d(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L684)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L684?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the scene to its `<x3d>` DOM element, formatting the size and rendering each child.
  - `:returns`: `_`
    > the X3D element


<a id="McUtils.Plots.X3DInterface.X3D.display" class="docs-object-method">&nbsp;</a> 
```python
display(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L710)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L710?message=Update%20Docs)]
</div>
**LLM Docstring**

Display the scene widget.


<a id="McUtils.Plots.X3DInterface.X3D.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L718)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L718?message=Update%20Docs)]
</div>
**LLM Docstring**

Display the scene, enabling dynamic loading when in a Jupyter environment.


<a id="McUtils.Plots.X3DInterface.X3D.dump" class="docs-object-method">&nbsp;</a> 
```python
dump(self, file, write_html=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L728)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L728?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the scene to a file, as full HTML or as bare X3D.
  - `file`: `Any`
    > the destination file
  - `write_html`: `bool`
    > write full HTML (vs bare X3D)
  - `opts`: `Any`
    > extra write options
  - `:returns`: `_`
    > the write result


<a id="McUtils.Plots.X3DInterface.X3D.rasterize" class="docs-object-method">&nbsp;</a> 
```python
rasterize(self, file, image_format='png', width=None, height=None, device_scale_factor=1, background=None, transparent=None, timeout=15000, executable_path=None, channel=None, browser_args=None, keep_html=False, ready_timeout_action='warn'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L746?message=Update%20Docs)]
</div>
**LLM Docstring**

Render this scene to a raster image. This builds the page X3DOM
needs (the margin reset, the optional background, `to_html`'s own
CSS/JS embedding) and hands the actual headless-browser work off
to that page's own `HTML.XMLElement.rasterize` -- the generic
rasterizer any JHTML element now has -- passing it this scene's
own X3DOM-specific "is it actually on screen yet" check
(`get_ready_check_expression`) as its `ready_function`, and the
rendered `<canvas>` (not the `<x3d>` tag itself, whose own CSS
layout box is not what you'd expect, or the whole page/viewport)
as what to screenshot.
  - `file`: `Any`
    > destination; a path, a writable/bytes-like buffer
    (e.g. `io.BytesIO()`), or `None` to get a new `io.BytesIO` back
  - `image_format`: `str`
    > `"png"` or `"jpg"`/`"jpeg"`
  - `width`: `Any`
    > viewport width; defaults to the scene's own configured width
  - `height`: `Any`
    > viewport height; defaults to the scene's own configured height
  - `background`: `Any`
    > an HTML background color to give the page
    before the scene loads (mostly invisible once the scene's own
    canvas covers it; a convenience for callers that already have
    a `facecolor`-style option lying around)
  - `transparent`: `Any`
    > if truthy, take the screenshot with
    `omit_background=True` so a transparent page background can
    come through as alpha (the WebGL canvas' own pixels are
    unaffected unless the scene itself renders with a transparent
    background)
  - `timeout`: `int`
    > milliseconds to wait for the scene-ready signal
    before giving up and capturing whatever is currently rendered
  - `executable_path`: `Any`
    > forwarded to `resolve_chromium_launch_kwargs`
  - `channel`: `Any`
    > forwarded to `resolve_chromium_launch_kwargs`
  - `browser_args`: `Any`
    > extra Chromium command-line flags; defaults to
    `DEFAULT_RASTERIZE_ARGS` (a software-WebGL config that works
    headless without a GPU)
  - `keep_html`: `bool`
    > if truthy, don't delete the intermediate HTML
    file/directory (useful for debugging what got rendered)
  - `ready_timeout_action`: `str`
    > `"warn"` (default, via the `warnings`
    module), `"raise"`, or `"ignore"` -- what to do if the
    scene-ready signal doesn't fire within `timeout`
  - `:returns`: `_`
    > `file` if given (the path or buffer passed in), otherwise
    a new `io.BytesIO` holding the image


<a id="McUtils.Plots.X3DInterface.X3D.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L828)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L828?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the scene's child objects.
  - `:returns`: `list`
    > the children
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L132?message=Update%20Docs)   
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