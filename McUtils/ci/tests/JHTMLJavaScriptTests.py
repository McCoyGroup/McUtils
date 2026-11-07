"""Portable state, existing controls, and explicit widget-transport integration."""
import importlib.abc
import json
import os
from pathlib import Path
from html.parser import HTMLParser
import subprocess
import sys
import unittest
from unittest import mock

from McUtils.Jupyter.JHTML import HTML, JHTML, JSVar, JSState, JSBinding
from McUtils.Jupyter.Apps import App, Card, Slider, Selector, Checkbox, VariableDisplay, FunctionDisplay, Tabs, Accordion
from McUtils.Readouts import Readout, ReadoutSection, ReadoutTable, ReadoutPlot, TabularData
from McUtils.Readouts.Renderers.HTML import HTMLReadoutRenderer


class JavaScriptDeclarationTests(unittest.TestCase):
    def test_initial_values_are_copies_and_not_live_values(self):
        initial = {'items': [1]}
        variable = JSVar('sample', initial=initial)
        initial['items'].append(2)
        self.assertEqual(variable.initial, {'items': [1]})
        variable.initial['items'].append(3)
        self.assertEqual(variable.initial, {'items': [1]})
        with self.assertRaises(AttributeError):
            variable.value = 2

    def test_validation_at_serialization_boundary(self):
        variable = JSVar('sample', initial=1, kind='integer', min=0, max=2, nullable=False)
        for invalid in (True, 1.5, -1, 3, None, float('nan'), object()):
            with self.subTest(invalid=invalid), self.assertRaises((ValueError, TypeError)):
                variable.validate(invalid)
        with self.assertRaises(ValueError):
            JSVar('bad name')
        with self.assertRaises(TypeError):
            JSState(variable, script=lambda: None)

    def test_scope_identity_and_duplicate_names(self):
        a, b = JSVar('sample', initial=1), JSVar('sample', initial=2)
        with self.assertRaises(ValueError):
            JSState(a, b)
        with self.assertRaises(ValueError):
            JSState(a).to_html(JHTML.Input(bind={'value': b}))
        with self.assertRaises(TypeError):
            JSBinding('sample')

    def test_unknown_properties_and_direction_are_rejected(self):
        variable = JSVar('sample')
        with self.assertRaises(ValueError):
            JSState.bind_element(HTML.Div(), {'unknown': variable})
        with self.assertRaises(ValueError):
            JSState.bind_element(HTML.Div(), {'text': JSBinding(variable, 'both')})

    def test_display_support_and_python_function_boundary(self):
        variable = JSVar('sample', initial=1)
        html = Card(VariableDisplay(variable),state=JSState(variable)).to_html()
        self.assertIn('data-mcjs-bind', html)
        with self.assertRaisesRegex(TypeError, 'VarBridge'):
            FunctionDisplay(lambda sample: sample, [variable])

    def test_nested_scopes_are_independent(self):
        outer, inner = JSVar('sample', initial=1), JSVar('sample', initial=2)
        child = JHTML.Div(JHTML.Input(bind={'value': inner}), state=JSState(inner))
        html = JSState(outer).to_html(child, JHTML.Input(bind={'value': outer}))
        self.assertEqual(html.count('data-mcjs-state='), 2)

    def test_existing_components_export_without_widget_dependencies(self):
        code = r'''
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('IPython','ipywidgets','ipyevents') or '.ActiveHTMLWidget' in fullname:
            raise ImportError('intentionally unavailable: ' + fullname)
sys.meta_path.insert(0, Block())
from McUtils.Jupyter.Apps import App,Card,Slider,Selector,Checkbox,JSVar,JSState
a=JSVar('a',initial=1);b=JSVar('b',initial=True)
app=App(body=Card([Slider(a,range=(0,2,.1)),Selector(a,options=[('one',1),('two',2)]),Checkbox(b)]),state=JSState(a,b))
html=app.to_html()
assert 'data-mcjs-state' in html and 'data-mcjs-bind' in html
assert not any(name.split('.')[0] in ('IPython','ipywidgets','ipyevents') for name in sys.modules)
'''
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', NUMBA_DISABLE_JIT='1')
        result = subprocess.run([sys.executable, '-c', code], env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_table_requires_unique_stable_keys(self):
        sample = JSVar('sample', initial=0)
        for table in (ReadoutTable({'x': [0,1]}, bind={'selection': sample}),
                      ReadoutTable({'x': [0,0]}, row_key='x', bind={'selection': sample})):
            with self.assertRaises(ValueError):
                HTMLReadoutRenderer().render_fragment(table)

    def test_readout_keeps_plotly_interactive(self):
        from McUtils.Plots import Plot
        sample = JSVar('sample', initial=1)
        plot = Plot([0,1], [0,2], backend='plotly', plot_style={'customdata': [0,1]})
        readout = ReadoutSection(ReadoutTable({'id': [0,1]}, row_key='id', bind={'selection': sample}),
                                ReadoutPlot(plot, bind={'selection': sample}), state=JSState(sample))
        html = HTMLReadoutRenderer().render_fragment_result(readout).html
        self.assertIn('&quot;adapter&quot;:&quot;plotly&quot;', html)
        self.assertIn('data-mcjs-key', html)
        gaps = Plot([0,1],[0,float('nan')], backend='plotly')
        gap_element = gaps.figure.to_jhtml()
        manifest = json.loads(gap_element.elems[0].attrs['data-mcjs-bind'])
        self.assertEqual(manifest['options']['figure']['data'][0]['y'], [0,None])
        with self.assertRaises(ValueError):
            HTMLReadoutRenderer().render_fragment(ReadoutPlot(plot, interactive=False, bind={'selection': sample}))


class VarBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import ipywidgets
        except ImportError:
            raise unittest.SkipTest('ipywidgets is optional')

    def make_bridge(self, direction='both', initialize='python'):
        from McUtils.Jupyter.Apps import Var, VarBridge, VariableNamespace
        python_var = Var('sample', namespace=VariableNamespace(), value=3)
        js_var = JSVar('sample', initial=1, kind='integer')
        bridge = VarBridge(python_var, js_var, direction=direction, initialize_from=initialize)
        state = JSState(js_var, bridges=[bridge])
        return python_var, js_var, state

    def test_bridge_uses_existing_transport_and_cleans_up(self):
        python_var, js_var, state = self.make_bridge()
        wrapper = state.to_widget(mode='widget')
        messages = []
        wrapper.call = lambda method, **content: messages.append((method, content))
        try:
            self.assertEqual(state.to_dict()['variables'][0]['initial'], 3)
            wrapper.handle_event({'type': 'mcjs:bridge', 'detail': {'name': 'sample', 'value': 2}})
            self.assertEqual(python_var.value, 2)
            self.assertEqual(messages[-1], ('mcjs_set', {'name': 'sample', 'value': 2}))
            python_var.value = 4
            self.assertEqual(messages[-1][1]['value'], 4)
        finally:
            wrapper.elem.close()
        self.assertEqual(len(python_var.callbacks), 0)

    def test_bridge_directions_and_html_export(self):
        for direction in ('python_to_js','js_to_python'):
            python_var, js_var, state = self.make_bridge(direction)
            wrapper = state.to_widget(mode='widget')
            messages = []
            wrapper.call = lambda *args, **kwargs: messages.append((args, kwargs))
            try:
                wrapper.handle_event({'type': 'mcjs:bridge', 'detail': {'name': 'sample', 'value': 2}})
                self.assertEqual(python_var.value, 3 if direction == 'python_to_js' else 2)
                python_var.value = 4
                self.assertEqual(bool(messages), direction == 'python_to_js')
            finally:
                wrapper.elem.close()
            html = state.to_html(HTML.Input())
            self.assertNotIn('mcjs_init', html)
            self.assertNotIn('widget.model', html)
            self.assertIn('data-mcjs-state', html)


class RuntimeExportTests(unittest.TestCase):
    url = 'https://cdn.example.test/revision/McUtils/Jupyter/JHTML/resources/javascript.js'

    @staticmethod
    def markup(html):
        class Parser(HTMLParser):
            def __init__(self):
                super().__init__();self.tags=[]
            def handle_starttag(self, tag, attrs):
                self.tags.append((tag,dict(attrs)))
        parser=Parser();parser.feed(html)
        return parser.tags

    def panel(self, **options):
        value=JSVar('value',initial=1)
        return Card(Slider(value,range=(0,2,1)),state=JSState(value),**options)

    def test_scopes_are_declarative_and_readout_inlines_one_footer_library(self):
        scope=JSState(JSVar('value',initial=1)).to_widget()
        self.assertEqual(scope.tag,'mcui-state')
        self.assertNotIn('<script',scope.tostring())
        html=Readout(self.panel(),self.panel()).to_html()
        tags=self.markup(html)
        self.assertEqual(sum(tag=='mcui-state' for tag,_ in tags),2)
        scripts=[attrs for tag,attrs in tags if tag=='script']
        self.assertEqual([attrs.get('id') for attrs in scripts],['mcutils-apps-native-js'])
        self.assertGreater(html.index('<script'),html.rindex('</mcui-state>'))
        self.assertNotIn('onload=',html)

    def test_url_load_is_shared_by_apps_jhtml_and_readouts(self):
        for html in (self.panel().to_html(javascript_path=self.url),
                     JHTML.to_html(self.panel(),javascript_path=self.url),
                     Readout(self.panel(),self.panel()).to_html(javascript_path=self.url)):
            with self.subTest(export=html[:50]):
                scripts=[a for tag,a in self.markup(html) if tag=='script']
                self.assertEqual([a.get('src') for a in scripts],[self.url])
                self.assertNotIn('class McuiState',html)

    def test_cdn_selector_uses_installed_identity_and_offline_never_verifies(self):
        identity=JSState.runtime_info()
        with mock.patch.object(JSState,'cdn_url',return_value=identity['script']) as resolve:
            html=Readout(self.panel()).to_html(javascript_path='cdn')
            self.assertIn('src="'+identity['script']+'"',html)
            self.assertIn('data-mcui-runtime="'+identity['tag']+'"',html)
            self.assertTrue(resolve.called)
        with mock.patch.object(JSState,'cdn_url',side_effect=AssertionError('offline must not contact CDN')):
            html=Readout(self.panel(javascript_path='cdn')).to_html(javascript_path='cdn',offline=True)
            self.assertIn('class McuiState',html)
            self.assertNotIn('src="'+identity['script']+'"',html)

    def test_per_scope_url_and_export_override(self):
        value=JSVar('value',initial=1)
        scope=JSState(value,javascript_path=self.url).to_widget()
        html=Readout(scope).to_html()
        self.assertIn('src="'+self.url+'"',html)
        self.assertIn('class McuiState',Readout(scope).to_html(javascript_path='inline'))
        other=JSState(value,javascript_path='other.js').to_widget()
        with self.assertRaisesRegex(ValueError,'multiple'):
            Readout(scope,other).to_html()
        self.assertIn('src="'+self.url+'"',Readout(Tabs({'One':'A'},javascript_path=self.url)).to_html())

    def test_theme_controls_and_bootstrap_dependency_policy(self):
        native=self.panel().to_html(javascript_path=self.url)
        explicit=self.panel(ui_theme='bootstrap').to_html(javascript_path=self.url)
        self.assertIn('mcui-range',native)
        self.assertIn('form-range',explicit)
        native_attrs=[a for _,a in self.markup(native)]
        explicit_tags=self.markup(explicit)
        self.assertFalse(any('bootstrap@' in a.get('src','')+a.get('href','') for a in native_attrs))
        self.assertTrue(any('bootstrap@' in a.get('src','') for _,a in explicit_tags))
        self.assertTrue(any(tag=='mcui-bootstrap' for tag,_ in explicit_tags))

    @unittest.skipUnless(importlib.util.find_spec('ipywidgets'),'ipywidgets is optional')
    def test_widget_api_is_shared_per_theme_and_runtime_path(self):
        from McUtils.Jupyter.Apps import AppTheme
        with AppTheme.rendering(javascript_path=self.url):
            one=AppTheme.current().javascript_api()
            two=AppTheme.current().javascript_api()
            self.assertIs(one,two)
            self.assertIn(self.url,AppTheme.current().initializer())
        self.assertIsNot(one,AppTheme.current().javascript_api())

    @unittest.skipUnless(importlib.util.find_spec('ipywidgets'),'ipywidgets is optional')
    def test_direct_widget_scope_attaches_existing_shared_ui_api(self):
        value=JSVar('value',initial=1)
        widget=JSState(value,javascript_path=self.url).to_widget(mode='widget')
        try:
            self.assertIsNotNone(widget.elem.jsAPI)
            self.assertIn(self.url,widget.javascript_handles.elem.jsHandlers['mcui_mount'])
        finally:
            widget.elem.close()

    def test_offline_plotly_is_embedded_once_and_forces_inline_ui(self):
        from McUtils.Plots import ScatterPlot
        plot=ScatterPlot([0,1],[0,1],backend='plotly')
        readout=Readout(ReadoutPlot(plot),ReadoutPlot(plot),self.panel())
        html=readout.to_html(offline=True,javascript_path=self.url)
        tags=self.markup(html)
        self.assertFalse(any(a.get('src') or a.get('href') for tag,a in tags if tag in ('script','link')))
        ids=[a.get('id') for _,a in tags]
        self.assertEqual(ids.count('mcutils-plotly-js'),1)
        self.assertEqual(ids.count('mcutils-apps-native-js'),1)
        self.assertGreater(html.index('id="mcutils-plotly-js"'),html.rindex('</figure>'))

    def test_fragment_reports_host_runtime_without_inline_scope_scripts(self):
        result=HTMLReadoutRenderer(javascript_path=self.url).render_fragment_result(self.panel().to_readout())
        self.assertIn('mcutils-ui',result.needs)
        self.assertEqual(result.runtime['mcutils-ui']['script'],self.url)
        self.assertNotIn('<script',result.html)
        self.assertEqual(sum('id="mcutils-apps-native-js"' in item for item in result.head),1)

    def test_offline_x3d_uses_one_local_runtime_and_no_dynamic_loader(self):
        from McUtils.Plots import X3D,X3DScene,X3DSphere
        from McUtils.Readouts import ReadoutScene
        scene=X3D(X3DScene(X3DSphere([0,0,0],radius=.5)),include_mathjax=False)
        readout=Readout(ReadoutScene(html=scene),ReadoutScene(html=scene))
        html=readout.to_html(offline=True)
        tags=self.markup(html)
        self.assertEqual(sum(a.get('id')=='mcutils-x3dom-js' for _,a in tags),1)
        self.assertFalse(any(a.get('src') or a.get('href') for tag,a in tags if tag in ('script','link')))
        fragment=readout.to_html_fragment(offline=True)
        self.assertTrue(fragment.runtime['x3dom']['inline'])


def runtime_fixtures():
    """Render real Python interfaces for the optional Node/jsdom contract tests."""
    from McUtils.Plots import ScatterPlot
    value = JSVar('value', initial=1, kind='integer', min=0, max=2, nullable=False)
    enabled = JSVar('enabled', initial=True, kind='boolean')
    state = JSState(value, enabled)
    controls = Card([Slider(value, range=(0,2,1)), Selector(value, options=[('zero',0),('one',1),('two',2)]),
                     Checkbox(enabled), JHTML.Span(bind={'text': value}),
                     JHTML.Button('action', bind={'enabled': enabled})], state=state)
    sample = JSVar('sample', initial=1, kind='integer')
    plot = ScatterPlot([0,1,2], [0,2,1], backend='plotly', plot_style={'customdata':[0,1,2]})
    panel = ReadoutSection(ReadoutTable({'id':[2,0,1]}, row_key='id', bind={'selection':sample}),
                           ReadoutPlot(plot, bind={'selection':sample}), state=JSState(sample))
    fraction = JSVar('fraction', initial=.25)
    mode = JSVar('mode', initial=0)
    scene = JSState.bind_element(HTML.Div(HTML.Div(cls='mcutils-x3d-component')),
                                 {'mode':mode,'fraction':fraction},adapter='x3d')
    result = dict(controls=controls.to_html(create_body=False),
                  plot=HTMLReadoutRenderer().render_fragment_result(panel).html,
                  scene=JSState(mode,fraction).to_html(scene),
                  runtime=JSState.javascript_source(),
                  identity=JSState.runtime_info(),
                  widget_inline_loader=JSState.runtime_loader(),
                  widget_cdn_loader=JSState.runtime_loader(RuntimeExportTests.url),
                  entry=JSState.javascript_source(include_ui=False),
                  native_js=Path(__import__('McUtils').__file__).parent.joinpath('Jupyter/Apps/resources/native.js').read_text(),
                  native_css=JSState.native_css())
    visible = JSVar('visible', initial=True, kind='boolean')
    responsive = ReadoutSection(
        Card([Slider(sample, range=(0,2,1)), Checkbox(visible)]),
        ReadoutTable({'id':[2,0,1]}, row_key='id', bind={'selection':sample}),
        ReadoutPlot(plot, bind={'selection':sample,'visible':visible}),
        state=JSState(sample,visible))
    result['responsive'] = HTMLReadoutRenderer().render_fragment_result(responsive).html
    JSState.register_adapter('test-label', {'value':'in'})
    label = JSState.bind_element(HTML.Span(), {'value':value},adapter='test-label')
    result['extension'] = JSState(value,script="McUtilsJS.registerAdapter('test-label',ctx=>ctx.input('value',value=>{ctx.element.textContent='Mode '+value;}));").to_html(label)
    try:
        from McUtils.Jupyter.Apps import Var,VarBridge,VariableNamespace
        p = Var('bridge',namespace=VariableNamespace(),value=1)
        v = JSVar('bridge',initial=0,kind='integer')
        state = JSState(v,bridges=[VarBridge(p,v)])
        wrapper = state.to_widget(mode='widget')
        try:
            result['bridge'] = dict(html=state.to_html(JHTML.Input(type='range',min='0',max='4',bind={'value':v})),
                                    handlers=wrapper.elem.jsHandlers)
        finally:
            wrapper.elem.close()
    except ImportError:
        pass
    url=RuntimeExportTests.url
    for theme in ('native','bootstrap'):
        panel=Card([Tabs({'One':Slider(value,range=(0,2,1)),'Two':'Second'}),
                    Accordion({'Section':'Details'}),JHTML.Span(bind={'text':value})],
                   state=JSState(value),ui_theme=theme)
        result['cdn_'+theme]=panel.to_html(javascript_path=url)
    result['inline_multiple']=Readout(controls,controls).to_html()
    result['offline_native']=Readout(responsive).to_html(offline=True)
    bootstrap=os.environ.get('MCUTILS_BOOTSTRAP_ASSETS')
    if bootstrap:
        assets={'bootstrap_script':str(Path(bootstrap)/'js/bootstrap.bundle.min.js'),
                'bootstrap_stylesheet':str(Path(bootstrap)/'css/bootstrap.min.css')}
        result['offline_bootstrap']=Readout(panel).to_html(offline=True,asset_paths=assets)
        result['bootstrap_js']=Path(assets['bootstrap_script']).read_text()
        result['bootstrap_css']=Path(assets['bootstrap_stylesheet']).read_text()
    return result


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixtures':
        Path(sys.argv[2]).write_text(json.dumps(runtime_fixtures()))
    else:
        unittest.main()
