"""Apps presentation isolation and Readout widget/layout regression tests."""
import os
os.environ.setdefault('MPLBACKEND','Agg')
import unittest,json
from html.parser import HTMLParser
try:
    import ipywidgets as widgets
except ImportError:
    widgets=None
from McUtils.Jupyter import (JHTML,AppTheme,App,Card,Grid,Flex,Button,Dropdown,Tabs,Accordion,
                             Readout,ReadoutText,ReadoutFields,ReadoutSection,ReadoutGrid,
                             ReadoutPanel,ReadoutFlex,ReadoutWidget,as_readout_node)

class Markup(HTMLParser):
    def __init__(self,text):
        super().__init__();self.elements=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.elements.append((tag,dict(attrs)))

class HTMLWidget:
    def __init__(self):self.calls=0
    def to_widget(self):
        self.calls+=1
        return JHTML.HTML.Div('Arbitrary object',id='arbitrary-object')
class KernelWidget:
    def __init__(self):self.calls=0;self.widget=widgets.Button(description='Live')
    def to_widget(self):self.calls+=1;return self.widget

def models(root):
    result=[];seen=set()
    def visit(obj):
        if hasattr(obj,'elem'):obj=obj.elem
        if not isinstance(obj,widgets.Widget) or id(obj) in seen:return
        seen.add(id(obj));result.append(obj)
        for child in getattr(obj,'children',()):visit(child)
    visit(root);return result

@unittest.skipIf(widgets is None,'live widget tests need ipywidgets')
class ThemeTests(unittest.TestCase):
    def test_native_default_and_explicit_bootstrap(self):
        layout=Grid([[Card('Body',header='Header'),Button('Go')]],column_width=['2fr','1fr'])
        native=layout.to_static_html().tostring()
        self.assertIn('mcui-card-header',native);self.assertIn('grid-template-columns:2fr 1fr',native)
        self.assertNotIn('cdn.jsdelivr',native);self.assertNotIn('context.bootstrap',native)
        explicit=layout.to_static_html(ui_theme='bootstrap').tostring()
        self.assertIn('bootstrap@5.1.3',explicit);self.assertIn('class="card"',explicit)
        self.assertNotIn('mcutils-apps-native-css',explicit)
        self.assertNotIn('jquery',explicit)
    def test_theme_scope_is_restored_on_exception(self):
        with self.assertRaises(RuntimeError):
            with AppTheme('bootstrap'):
                self.assertEqual(AppTheme.current().name,'bootstrap');raise RuntimeError()
        self.assertEqual(AppTheme.current().name,'native')
        with self.assertRaises(ValueError):AppTheme('unknown')
    def test_app_theme_alias_and_layout_export(self):
        for name in ('native','bootstrap'):
            app=App(body=Card('Content',header='Card'),header='App',capture_output=False,theme=name)
            html=app.to_static_html().tostring()
            self.assertEqual('bootstrap@5.1.3' in html,name=='bootstrap')
            self.assertEqual(app.to_readout().ui_theme,name)
    def test_callbacks_and_widget_identity(self):
        called=[];button=Button('Run',action=lambda *args:called.append('run'))
        first=button.to_widget();self.assertIs(first,button.to_widget())
        raw=button._widget_cache
        raw.elem._handle(None,{'type':'click'},[])
        self.assertEqual(called,['run'])
        self.assertIn(raw.elem,models(first))
        html=button.to_static_html().tostring()
        self.assertIn('data-requires-kernel="true"',html);self.assertIn('disabled=',html)
    def test_frontend_source_is_shared_between_widgets(self):
        one=Card('One').to_widget();two=Card('Two').to_widget()
        self.assertIs(one.elem.jsAPI,two.elem.jsAPI)
    def test_native_navigation_descriptors(self):
        for component in [Dropdown('Menu',{'Item':None}),Tabs({'One':'First','Two':'Second'}),Accordion({'Section':'Content'})]:
            html=component.to_static_html().tostring()
            self.assertNotIn('data-bs-',html);self.assertIn('data-mcui-',html)
            self.assertNotIn('context.bootstrap',html)
    def test_grid_spans_infer_exact_tracks(self):
        grid=Grid([[Grid.Item('Span',row_span=2,col_span=2)]])
        self.assertEqual((grid.rows,grid.cols),(2,2))
        html=grid.to_static_html().tostring()
        self.assertIn('grid-row-end:span 2',html);self.assertIn('repeat(2, auto)',html)

@unittest.skipIf(widgets is None,'live widget tests need ipywidgets')
class ReadoutTests(unittest.TestCase):
    def test_arbitrary_html_widget_is_lazy_and_cached(self):
        obj=HTMLWidget();readout=Readout(obj)
        self.assertIsInstance(readout.children[0],ReadoutWidget);self.assertEqual(obj.calls,0)
        self.assertIn('arbitrary-object',readout.to_html());self.assertIn('Arbitrary object',readout.to_html())
        readout.to_widget();self.assertEqual(obj.calls,1)
    def test_live_widget_is_not_stringified_or_replaced(self):
        obj=KernelWidget();readout=Readout(obj)
        rendered=readout.to_widget()
        self.assertIn(obj.widget,models(rendered));self.assertEqual(obj.calls,1)
        self.assertIn('requires a live Python kernel',readout.to_html());self.assertEqual(obj.calls,1)
        obj.widget.description='Changed';self.assertEqual(obj.widget.description,'Changed')
    def test_widget_fallback(self):
        readout=Readout(ReadoutWidget(KernelWidget(),fallback=ReadoutText('Static alternative')))
        self.assertIn('Static alternative',readout.to_html());self.assertIn('Static alternative',readout.to_text())
    def test_callable_widget_is_not_called_as_a_factory(self):
        class CallableWidget(HTMLWidget):
            def __call__(self):raise AssertionError('called as factory')
        self.assertIn('Arbitrary object',Readout(CallableWidget()).to_html())
    def test_widget_cycles_raise(self):
        class Cycle:
            def to_widget(self):return self
        with self.assertRaisesRegex(ValueError,'Cycle'):Readout(Cycle()).to_widget()
    def test_semantic_grid_retains_values_for_all_exports(self):
        left=ReadoutFields({'left':[1,2]},id='left-values')
        right=ReadoutFields({'right':[3,4]},id='right-values')
        layout=Grid([[Card(left,header='Left'),Card(right,header='Right')]],column_width=['3fr','2fr'])
        readout=Readout(layout,title='Results')
        self.assertIsInstance(readout.children[0],ReadoutGrid)
        values=readout.to_json();self.assertIn('1',values);self.assertIn('4',values)
        html=readout.to_html();self.assertIn('grid-template-columns:3fr 2fr',html)
        self.assertEqual(html.count('id="mcutils-apps-native-css"'),1)
        self.assertEqual(html.count('id="mcutils-apps-native-js"'),1)
        self.assertIn('Left',readout.to_text());self.assertTrue(readout.to_pptx())
    def test_grid_responsive_and_invalid_spans(self):
        readout=Readout(ReadoutGrid([[Grid.Item('Wide',row_span=2),'Side']],collapse_below=900))
        self.assertIn('@media(max-width:900px)',readout.to_html())
        with self.assertRaises(ValueError):ReadoutGrid([[Grid.Item('Invalid',row_span=0)]])
    def test_flex_adapter_and_node_widget(self):
        node=as_readout_node(Flex([ReadoutText('A'),ReadoutText('B')],direction='column',wrap='nowrap'))
        self.assertIsInstance(node,ReadoutFlex)
        self.assertIn('flex-direction:column',Readout(node).to_html())
        self.assertIsNotNone(node.to_widget())
    def test_layout_theme_is_inherited(self):
        panel=ReadoutPanel(Button('Action'),header='Theme',ui_theme='bootstrap')
        html=Readout(panel).to_html()
        button=next(attrs for tag,attrs in Markup(html).elements if tag=='button')
        self.assertTrue({'btn','btn-primary'} <= set(button.get('class','').split()))
        self.assertNotIn('mcui-button',html)


import asyncio
from McUtils.Jupyter import (AppTheme,Button,Card,Grid,Flex,Slider,VariableNamespace,Var,
                            Readout,ReadoutFields,ReadoutPanel,ReadoutWidget,ReadoutGrid,
                            as_readout_node,ReadoutScene,Popover,Tooltip)

@unittest.skipIf(widgets is None,'live widget tests need ipywidgets')
class ProtocolTests(unittest.TestCase):
    def test_raw_ipywidgets_are_accepted(self):
        widget=widgets.Button(description='Raw')
        readout=Readout(widget)
        self.assertIsInstance(readout.children[0],ReadoutWidget)
        self.assertIn(widget,models(readout.to_widget()))
    def test_control_values_remain_linked(self):
        namespace=VariableNamespace.create('ui-isolation-tests')
        var=Var('level',namespace=namespace,value=.25)
        slider=Slider(var,min=0,max=1,step=.01)
        root=slider.to_widget();self.assertEqual(slider.value,.25)
        var.value=.75;self.assertAlmostEqual(float(slider.value),.75)
        self.assertIs(root,slider.to_widget())
        self.assertIn(slider._widget_cache.elem,models(root))
    def test_explicit_context_is_retained(self):
        with AppTheme('bootstrap'):card=Card('Saved')
        self.assertEqual(card.ui_theme,'bootstrap')
        self.assertIn('bootstrap@5.1.3',card.to_static_html().tostring())
        self.assertEqual(AppTheme.current().name,'native')
        from McUtils.Jupyter import ReadoutFlex
        with AppTheme('bootstrap'):
            panel=ReadoutPanel('Saved panel')
            grid=ReadoutGrid([['Saved grid']])
            flex=ReadoutFlex('Saved flex')
        for layout in (panel,grid,flex):
            self.assertEqual(layout.ui_theme,'bootstrap')
            self.assertIn('bootstrap@5.1.3',Readout(layout).to_html())
    def test_theme_contexts_do_not_leak_between_tasks(self):
        theme=AppTheme('bootstrap')
        async def task(name):
            with theme if name=='bootstrap' else AppTheme(name):
                await asyncio.sleep(0)
                return AppTheme.current().name
        async def run():return await asyncio.gather(task('bootstrap'),task('native'),task('bootstrap'))
        self.assertEqual(asyncio.run(run()),['bootstrap','native','bootstrap'])
        self.assertEqual(AppTheme.current().name,'native')
    def test_flex_item_placement_is_preserved(self):
        flex=Flex([Flex.Item(ReadoutFields({'left':1}),grow=2,order=1,basis='20rem'),Flex.Item('Right',shrink=0)],direction='row',style={'gap':'12px'})
        html=Readout(flex).to_html()
        for text in ['flex-grow:2','order:1','flex-basis:20rem','flex-shrink:0','gap:12px']:
            self.assertIn(text,html)
    def test_bootstrap_hooks_do_not_require_frontend_bootstrap_context(self):
        tooltip=Tooltip(Button('Tip'),title='Title')
        with AppTheme('bootstrap'):
            root=tooltip.to_widget()
        handles=tooltip._widget_cache.elem.jsHandlers
        self.assertTrue(handles)
        self.assertTrue(all('context.bootstrap' not in value for value in handles.values()))
        self.assertTrue(any('window.bootstrap' in value for value in handles.values()))
    def test_scenes_keep_their_specific_adapter(self):
        from McUtils.Plots import X3D,X3DScene,X3DSphere
        scene=X3D(X3DScene(X3DSphere([0,0,0],radius=.5)),include_mathjax=False)
        self.assertIsInstance(as_readout_node(scene),ReadoutScene)
        readout=Readout(ReadoutGrid([[scene,'Details']]))
        html=readout.to_html(x3dom_path='inline')
        self.assertIn('<x3d',html.lower());self.assertIn('<sphere',html.lower())
        self.assertNotIn('bootstrap@',html)
        self.assertIsNotNone(readout.to_widget())
    def test_viewport_is_a_real_meta_attribute(self):
        meta=next(attrs for tag,attrs in Markup(Readout('Hello').to_html()).elements if tag=='meta' and attrs.get('name')=='viewport')
        self.assertIn('width=device-width',meta['content'])
        self.assertNotIn('style',meta)

    def test_grid_attributes_and_breakpoint_survive_adapter(self):
        grid=Grid([['Left','Right']],id='my-grid',cls='custom-layout',collapse_below=700)
        html=Readout(grid).to_html()
        self.assertIn('id="my-grid"',html);self.assertIn('custom-layout',html)
        self.assertIn('@media(max-width:700px)',html)
        self.assertIn('@media(max-width:700px)',grid.to_static_html().tostring())
        for bad in (0,-1,float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):Grid([['A']],collapse_below=bad).to_static_html()

    def test_app_context_is_reentrant_and_restores_state(self):
        from McUtils.Jupyter import App
        before=list(App._app_stack)
        app=App(body='Body',capture_output=False,ui_theme='bootstrap')
        with app:
            self.assertEqual(AppTheme.current().name,'bootstrap')
            with app:self.assertEqual(app._stack_depth,2)
            self.assertEqual(app._stack_depth,1)
        self.assertEqual(app._stack_depth,0)
        self.assertEqual(App._app_stack,before)
        self.assertEqual(AppTheme.current().name,'native')
        app.to_static_html()
        self.assertEqual(App._app_stack,before)

    def test_ipython_html_result_has_a_standalone_representation(self):
        from IPython.display import HTML
        class DisplayObject:
            def to_widget(self):return HTML('<strong id="ipy-html">Portable HTML</strong>')
        self.assertIn('id="ipy-html"',Readout(DisplayObject()).to_html())

    def test_existing_progress_updates_retain_the_bar(self):
        from McUtils.Jupyter import Progress
        progress=Progress(25)
        root=progress.to_widget()
        progress.bar.add_styles(width='75%')
        self.assertEqual(progress.bar.style['width'],'75%')
        self.assertIn(progress.container.elem,models(root))
        self.assertIs(root,progress.to_widget())

    def test_panel_and_flex_attributes_survive_adapter(self):
        card=Card('Body',header='Heading',id='named-card',cls='custom-card',style={'width':'20rem'})
        flex=Flex([card],id='named-flex',cls='custom-flex')
        html=Readout(flex).to_html()
        for text in ('id="named-flex"','id="named-card"','custom-card','custom-flex','width:20rem'):
            self.assertIn(text,html)

    def test_explicit_zero_grid_positions_are_rejected(self):
        for placement in ({'row':0},{'col':0},{'row_span':0},{'col_span':0}):
            with self.assertRaises(ValueError):ReadoutGrid([[Grid.Item('Cell',**placement)]])

    def test_custom_layout_keeps_generic_widget_protocol(self):
        from McUtils.Jupyter import Layout
        class CustomLayout(Layout):
            Item=Flex.Item
            def get_layout_styles(self,**opts):return {'display':'block'}
        layout=CustomLayout(['Content'])
        node=as_readout_node(layout)
        self.assertIsInstance(node,ReadoutWidget)
        self.assertIs(node.get_widget(),layout.to_widget())


class WebComponentTests(unittest.TestCase):
    def test_apps_and_readouts_emit_native_custom_elements(self):
        layout=Grid([[Card('Body',header='Header',footer='Footer'),Flex(['A','B'])]])
        for html in (layout.to_static_html().tostring(),Readout(layout).to_html()):
            tags={tag for tag,attrs in Markup(html).elements}
            self.assertTrue({'mcui-grid','mcui-flex','mcui-panel','mcui-panel-header',
                             'mcui-panel-body','mcui-panel-footer'} <= tags)
        bootstrap=Markup(layout.to_static_html(ui_theme='bootstrap').tostring())
        self.assertFalse(any(tag.startswith('mcui-') for tag,attrs in bootstrap.elements))

    def test_interactive_components_emit_their_own_custom_elements(self):
        from McUtils.Jupyter import Opener,Carousel,Tooltip,Popover
        cases=[(Tabs({'One':'A'}),'mcui-tabs'),(Accordion({'One':'A'}),'mcui-accordion'),
               (Opener({'One':'A'}),'mcui-opener'),(Dropdown('Actions',{'Go':None}),'mcui-dropdown'),
               (Carousel(['A','B']),'mcui-carousel'),(Tooltip(Button('Tip'),title='Help'),'mcui-tooltip'),
               (Popover(Button('More'),body='Details'),'mcui-popover')]
        for component,expected in cases:
            with self.subTest(expected=expected):
                self.assertIn(expected,{tag for tag,attrs in Markup(component.to_static_html().tostring()).elements})

    @unittest.skipIf(widgets is None,'live widgets need ipywidgets')
    def test_tooltip_keeps_the_original_callback_model(self):
        from McUtils.Jupyter import Tooltip
        calls=[]
        button=Button('Action',action=lambda *args:calls.append('called'))
        tooltip=Tooltip(button,title='Help')
        root=tooltip.to_widget()
        raw=button._widget_cache.elem
        self.assertIn(raw,models(root))
        self.assertEqual(tooltip._widget_cache.elem.tagName,'mcui-tooltip')
        raw._handle(None,{'type':'click'},[])
        self.assertEqual(calls,['called'])

    @unittest.skipIf(widgets is None,'live widgets need ipywidgets')
    def test_custom_events_use_the_existing_python_callback_bridge(self):
        events=[]
        tabs=Tabs({'One':'A','Two':'B'},event_handlers={'mcui:select':lambda event,widget:events.append(event)})
        root=tabs.to_widget()
        raw=tabs._widget_cache.elem
        self.assertEqual(raw.tagName,'mcui-tabs')
        self.assertIn(raw,models(root))
        self.assertIn('detail',raw.eventPropertiesDict['mcui:select']['fields'])
        self.assertTrue(raw.eventPropertiesDict['mcui:select']['propagate'])
        raw._handle(None,{'type':'mcui:select','detail':{'value':'two'}},[])
        self.assertEqual(events[0]['detail']['value'],'two')


class StandaloneLayoutTests(unittest.TestCase):
    def test_static_layout_does_not_require_ipywidgets(self):
        import subprocess,sys,tempfile
        code="""
import sys,importlib.abc
class NoWidgets(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='ipywidgets' or fullname.startswith('ipywidgets.'):
            raise ModuleNotFoundError('deliberately unavailable ipywidgets')
sys.meta_path.insert(0,NoWidgets())
from McUtils.Jupyter import App,Card,Grid,Readout,ReadoutFields
app=App(body=Card('Body',header='Header'),capture_output=False)
html=app.to_static_html().tostring()
assert 'mcui-card' in html and 'cdn.jsdelivr' not in html
assert not App._app_stack
readout=Readout(Grid([[ReadoutFields({'n':3})]]))
assert 'N' in readout.to_html()
"""
        environment=dict(os.environ,PYTHONPATH=os.pathsep.join(sys.path),PYTHONDONTWRITEBYTECODE='1')
        with tempfile.TemporaryDirectory() as directory:
            process=subprocess.run([sys.executable,'-c',code],cwd=directory,env=environment,text=True,capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr)

if __name__=='__main__':
    unittest.main(verbosity=2)
