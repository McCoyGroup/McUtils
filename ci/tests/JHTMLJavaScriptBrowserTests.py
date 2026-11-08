"""Browser integration tests; Playwright and Plotly are optional test dependencies."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import json
import os
from pathlib import Path
import unittest

from McUtils.Jupyter.JHTML import HTML, JHTML, JSVar, JSState
from McUtils.Jupyter.Apps import Card, Slider, Selector, Checkbox
from McUtils.Readouts import ReadoutSection, ReadoutTable, ReadoutPlot
from McUtils.Readouts.Renderers.HTML import HTMLReadoutRenderer


@_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
class JavaScriptBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
            import plotly
        except ImportError:
            raise unittest.SkipTest('Playwright and Plotly are optional browser test dependencies')
        cls.plotly_js = Path(plotly.__file__).with_name('package_data') / 'plotly.min.js'
        cls.x3dom_js = Path(__import__('McUtils').__file__).parent / 'Jupyter/resources/x3dom-full.js'
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={'width': 1100, 'height': 850})
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('https://cdn.plot.ly/**', lambda route: route.fulfill(path=str(self.plotly_js), content_type='application/javascript'))
        self.page.route('https://www.x3dom.org/download/**', self.x3dom_route)

    def x3dom_route(self, route):
        if route.request.url.endswith('.js'):
            route.fulfill(path=str(self.x3dom_js), content_type='application/javascript')
        else:
            route.fulfill(body='', content_type='text/css')

    def tearDown(self):
        self.page.close()
        self.assertEqual(self.errors, [])

    def load(self, html, scopes=1):
        self.page.set_content(html)
        # FragmentResult.html intentionally contains declarations only; its host
        # provides the shared library. Full document exports already include it.
        if not self.page.evaluate('Boolean(window.McUtilsJS)'):
            self.page.add_script_tag(content=JSState.javascript_source())
        self.page.wait_for_function("n => document.querySelectorAll('[data-mcjs-status=ready][data-mcjs-state]').length === n", arg=scopes)

    def test_controls_share_state_and_rendered_copies_stay_independent(self):
        value = JSVar('value', initial=1, kind='integer', min=0, max=2)
        enabled = JSVar('enabled', initial=True, kind='boolean')
        panel = Card([Slider(value, range=(0,2,1)), Selector(value, options=[('zero',0),('one',1),('two',2)]),
                      Checkbox(enabled), JHTML.Span(bind={'text': value}),
                      JHTML.Button('action', bind={'enabled': enabled})], state=JSState(value,enabled))
        self.load(panel.to_html(create_body=False) + panel.to_html(create_body=False), scopes=2)
        roots = self.page.locator('[data-mcjs-state]')
        roots.nth(0).locator('select').select_option('2')
        self.page.wait_for_function("document.querySelector('[data-mcjs-state]').controller.get('value') === 2")
        self.assertEqual(roots.nth(0).locator('input[type=range]').input_value(), '2')
        self.assertEqual(roots.nth(0).locator('span').inner_text(), '2')
        self.assertEqual(roots.nth(1).locator('input[type=range]').input_value(), '1')
        roots.nth(0).locator('input[type=checkbox]').uncheck()
        self.assertTrue(roots.nth(0).locator('button').is_disabled())
        self.page.evaluate("window.saved=document.querySelector('[data-mcjs-state]').controller;window.host=window.saved.root;window.host.remove()")
        self.page.wait_for_function('window.saved.disposed')
        self.page.evaluate('document.body.append(window.host)')
        self.page.wait_for_function('window.host.controller && !window.host.controller.disposed')
        self.assertEqual(self.page.evaluate("window.host.controller.get('value')"), 1)

    def test_invalid_batch_is_atomic_and_disposed_scope_rejects_writes(self):
        a = JSVar('a', initial=1, kind='integer', min=0, max=2, nullable=False)
        b = JSVar('b', initial=1, kind='integer', min=0, max=2, nullable=False)
        self.load(JSState(a,b).to_html(JHTML.Input(type='range', min='0', max='2', bind={'value': a})))
        result = self.page.evaluate('''() => {
          const state=document.querySelector('[data-mcjs-state]').controller;
          let failed=false;try {state.patch({a:2,b:10});}catch{failed=true;}
          const snapshot=state.snapshot();state.dispose();
          let closed=false;try{state.set('a',0);}catch{closed=true;}
          return {failed,closed,snapshot};
        }''')
        self.assertEqual(result, {'failed': True, 'closed': True, 'snapshot': {'a':1,'b':1}})

    def test_plotly_and_table_selection_and_zoom_persistence(self):
        from McUtils.Plots import ScatterPlot
        sample = JSVar('sample', initial=1, kind='integer')
        plot = ScatterPlot([0,1,2], [0,2,1], backend='plotly', plot_style={'customdata': [0,1,2]})
        panel = ReadoutSection(
            ReadoutTable({'id': [2,0,1], 'energy': [1,0,2]}, row_key='id', bind={'selection': sample}),
            ReadoutPlot(plot, bind={'selection': sample}), state=JSState(sample))
        html = HTMLReadoutRenderer().render_fragment_result(panel).html
        self.load(html + html, scopes=2)
        self.page.wait_for_function('document.querySelectorAll(".js-plotly-plot").length === 2')
        roots = self.page.locator('[data-mcjs-state]')
        roots.nth(0).locator('tr[data-mcjs-key="2"]').click()
        self.page.wait_for_function('document.querySelector(".js-plotly-plot").data[0].selectedpoints[0] === 2')
        self.assertEqual(roots.nth(1).evaluate("el => el.controller.get('sample')"), 1)
        self.page.evaluate("Plotly.relayout(document.querySelector('.js-plotly-plot'), {'xaxis.range':[.2,1.8]})")
        self.page.locator('.js-plotly-plot').nth(0).locator('.point').nth(1).click(force=True)
        self.page.wait_for_function("document.querySelector('[data-mcjs-state]').controller.get('sample') === 1")
        self.page.wait_for_function('document.querySelector(".js-plotly-plot").data[0].selectedpoints[0] === 1')
        self.assertEqual(self.page.locator('.js-plotly-plot').nth(0).evaluate('el => el.layout.xaxis.range'), [.2,1.8])
        self.assertEqual(roots.nth(0).locator('tr[aria-selected=true]').get_attribute('data-mcjs-key'), '1')
        self.assertEqual(self.page.locator('script[src^="https://cdn.plot.ly/"]').count(), 1)
        if os.environ.get('MCUTILS_JS_SCREENSHOT'):
            self.page.screenshot(path=os.environ['MCUTILS_JS_SCREENSHOT'], full_page=True)

    def test_plot_remains_visible_through_repeated_table_and_slider_updates(self):
        from McUtils.Plots import ScatterPlot
        sample = JSVar('sample', initial=1, kind='integer')
        visible = JSVar('visible', initial=True, kind='boolean')
        plot = ScatterPlot([0,1,2],[0,2,1],backend='plotly',
                           plot_style={'customdata':[0,1,2]}, image_size=[650,350])
        panel = ReadoutSection(
            Card([Slider(sample,range=(0,2,1)),Checkbox(visible)]),
            ReadoutTable({'id':[2,0,1]},row_key='id',bind={'selection':sample}),
            ReadoutPlot(plot,bind={'selection':sample,'visible':visible}),
            state=JSState(sample,visible))
        self.load(HTMLReadoutRenderer().render_fragment_result(panel).html)
        graph = self.page.locator('.js-plotly-plot')
        self.page.wait_for_function("document.querySelector('.js-plotly-plot')?.data?.[0]?.selectedpoints?.[0] === 1")
        def assert_visible(sample):
            self.page.wait_for_function("sample => document.querySelector('.js-plotly-plot')?.data?.[0]?.selectedpoints?.[0] === sample",arg=sample)
            self.assertGreater(graph.bounding_box()['width'],100)
            self.assertTrue(graph.is_visible())
            self.assertEqual(graph.locator('.point').count(),3)
            self.assertTrue(self.page.locator('input[type=checkbox]').is_checked())
        for sample in [0,1,2,0,2,1,0,1]:
            self.page.locator('tr[data-mcjs-key="{}"]'.format(sample)).click()
            assert_visible(sample)
        slider = self.page.locator('input[type=range]')
        for key,sample in [('Home',0),('ArrowRight',1),('ArrowRight',2),('ArrowLeft',1),('Home',0)]:
            slider.focus()
            slider.press(key)
            assert_visible(sample)
        self.page.set_viewport_size({'width':400,'height':850})
        assert_visible(0)
        self.assertLessEqual(graph.bounding_box()['width'],400)

    def test_native_psience_mode_and_playback_controls(self):
        try:
            from Psience.Molecools import Molecule
            import numpy as np
        except ImportError:
            self.skipTest('Psience is optional')
        molecule = Molecule(['H','H'], [[0,0,0],[1.4,0,0]], bonds=[(0,1,1)])
        scene = molecule.animate_mode([0,1], modes=np.eye(6)[:,:2], mass_scale=False,
                        backend='x3d', allow_adjustments=True, include_save_buttons=False,
                        animation_options={'running':False})
        mode = JSVar('mode', initial=0, kind='integer')
        phase = JSVar('phase', initial=.25, kind='number', min=0, max=1)
        scene.js_bind = {'mode': mode, 'fraction': phase}
        html = JSState(mode,phase).to_html(scene.to_widget(),
                  JHTML.Input(type='range', min='0', max='1', step='.01', id='phase', bind={'value': phase}))
        self.load(html)
        self.page.wait_for_function("document.querySelector('.mcutils-x3d-component')?.controller?.getState().fraction === .25")
        self.page.locator('[data-role=mode]').select_option('1')
        self.page.wait_for_function("document.querySelector('[data-mcjs-state]').controller.get('mode') === 1")
        self.page.locator('#phase').focus()
        self.page.locator('#phase').press('ArrowRight')
        self.page.wait_for_function("document.querySelector('.mcutils-x3d-component').controller.getState().fraction === .26")
        self.page.locator('[data-role=playback-next]').click()
        self.page.wait_for_function("document.querySelector('[data-mcjs-state]').controller.get('phase') > .26")

    def test_bridge_javascript_uses_activehtml_model_contract_without_echo(self):
        try:
            import ipywidgets
        except ImportError:
            self.skipTest('ipywidgets is optional')
        from McUtils.Jupyter.Apps import Var,VarBridge,VariableNamespace
        python_var = Var('sample',namespace=VariableNamespace(),value=1)
        sample = JSVar('sample',initial=0,kind='integer')
        state = JSState(sample,bridges=[VarBridge(python_var,sample)])
        wrapper = state.to_widget(mode='widget')
        try:
            handlers = wrapper.elem.jsHandlers
            self.load('<div id="transport">'+state.to_html(JHTML.Input(type='range',min='0',max='4',bind={'value':sample}))+'</div>')
            self.page.evaluate('''source => {
              window.sent=[];
              window.transport={el:document.querySelector('#transport'),callHandler:async()=>{},model:{send:message=>sent.push(message)}};
              return new Function('event','widget','context',source)({},transport,{});
            }''', handlers['mcjs_init'])
            self.page.locator('input').focus()
            self.page.locator('input').press('ArrowRight')
            self.page.wait_for_function('sent.length === 1')
            self.assertEqual(self.page.evaluate('sent[0].detail'), {'name':'sample','value':2})
            self.page.evaluate('''source => new Function('event','widget','context',source)(
              {content:{name:'sample',value:4}},transport.model,{})''', handlers['mcjs_set'])
            self.page.wait_for_function("document.querySelector('input').value === '4'")
            self.assertEqual(self.page.evaluate('sent.length'), 1)
            self.page.evaluate("document.querySelector('#transport').remove()")
            self.page.wait_for_function('transport.model.__mcjs_states.size === 0')
        finally:
            wrapper.elem.close()


if __name__ == '__main__':
    unittest.main()
