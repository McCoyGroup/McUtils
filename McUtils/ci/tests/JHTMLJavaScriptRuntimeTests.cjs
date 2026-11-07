/* Contract tests against Python-rendered interfaces; jsdom does not replace browser QA. */
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {JSDOM,ResourceLoader,VirtualConsole} = require('jsdom');
const fixtures = JSON.parse(fs.readFileSync(process.env.MCUTILS_JS_FIXTURES, 'utf8'));
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
async function until(predicate) {
  for (let i=0;i<400;i++) { if (predicate()) return; await pause(5); }
  assert.fail('Runtime update timed out');
}
function load(html, setup) {
  const dom = new JSDOM(html, {runScripts:'outside-only',pretendToBeVisual:true});
  dom.window.eval(fixtures.runtime);
  setup?.(dom.window);
  for (const root of dom.window.document.querySelectorAll('[data-mcjs-state]')) dom.window.McUtilsJS.mount(root);
  return dom;
}
const plain = value => JSON.parse(JSON.stringify(value));

test('existing controls synchronize typed values without sharing rendered instances', async () => {
  const dom=load(fixtures.controls+fixtures.controls),w=dom.window;
  try {
    const [a,b]=w.document.querySelectorAll('[data-mcjs-state]');
    const select=a.querySelector('select');
    select.value='2';select.dispatchEvent(new w.Event('change',{bubbles:true}));
    await until(()=>a.querySelector('span').textContent==='2');
    assert.equal(a.controller.get('value'),2);
    assert.equal(a.querySelector('input[type=range]').value,'2');
    assert.equal(b.controller.get('value'),1);
    const box=a.querySelector('input[type=checkbox]');box.checked=false;
    box.dispatchEvent(new w.Event('input',{bubbles:true}));
    await until(()=>a.querySelector('button').disabled);
    const saved=a.controller;a.remove();await until(()=>saved.disposed);
    w.document.body.append(a);w.McUtilsJS.mount(a);
    assert.equal(a.controller.get('value'),1);
  } finally { dom.window.close(); }
});

test('state batches are atomic, snapshots are copies, and notifications are batched',async()=>{
  const dom=load(fixtures.controls),w=dom.window;
  try {
    const state=w.document.querySelector('[data-mcjs-state]').controller;
    let calls=0;state.subscribe(()=>calls++);
    assert.throws(()=>state.patch({value:2,enabled:100}));
    assert.equal(state.get('value'),1);
    const snapshot=state.snapshot();snapshot.value=0;
    assert.equal(state.get('value'),1);
    state.patch({value:2,enabled:false});await until(()=>calls===1);
    state.set('value',2);await pause(10);assert.equal(calls,1);
    state.dispose();assert.throws(()=>state.set('value',0));
  }finally{dom.window.close();}
});

test('custom component adapters register before their initial bindings mount',async()=>{
  const dom=load(fixtures.extension),w=dom.window;
  try{
    const root=w.document.querySelector('[data-mcjs-state]');
    assert.equal(root.querySelector('span').textContent,'Mode 1');
    root.controller.set('value',2);await until(()=>root.querySelector('span').textContent==='Mode 2');
  }finally{dom.window.close();}
});

test('table and Plotly adapter coordinate stable keys and release their resources',async()=>{
  let purges=0,click;
  const dom=load(fixtures.plot,w=>{
    w.Plotly={
      async newPlot(el,data,layout){el.data=data;el.layout=layout;el.on=(event,fn)=>{click=fn;};el.removeListener=()=>{click=null;};},
      async react(el,data,layout){el.data=data;el.layout=layout;},
      purge(){purges++;}
    };
  });const w=dom.window;
  try{
    const root=w.document.querySelector('[data-mcjs-state]');
    const graph=[...root.querySelectorAll('[data-mcjs-bind]')].find(el=>JSON.parse(el.getAttribute('data-mcjs-bind')).adapter==='plotly');
    await until(()=>typeof click==='function');
    root.querySelector('tr[data-mcjs-key="2"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>graph.data[0].selectedpoints[0]===2);
    assert.equal(root.controller.get('sample'),2);
    click({points:[{curveNumber:0,pointNumber:0,customdata:0}]});
    await until(()=>root.querySelector('tr[aria-selected=true]')?.getAttribute('data-mcjs-key')==='0');
    await until(()=>graph.data[0].selectedpoints[0]===0);
    assert.equal(graph.layout.uirevision,'mcutils');
    root.controller.set('sample',null);await until(()=>graph.data[0].selectedpoints===null);
    root.controller.dispose();assert.equal(purges,1);assert.equal(click,null);
  }finally{dom.window.close();}
});

test('actual Plotly preserves plot width through repeated table and slider updates',
  {skip: !process.env.MCUTILS_PLOTLY_JS}, async()=>{
  const dom=load(fixtures.responsive,w=>{
    w.TextEncoder=TextEncoder;w.TextDecoder=TextDecoder;
    w.URL.createObjectURL=()=>'';
    // jsdom supplies DOM/SVG but no layout or canvas text measurement. Model
    // intrinsic sizing of a percentage-width child in an auto-width figure;
    // Plotly's real responsive renderer supplies the changing svg-container.
    w.HTMLCanvasElement.prototype.getContext=()=>({measureText:s=>({width:String(s).length*7})});
    w.SVGElement.prototype.getBBox=function(){return{x:0,y:0,width:(this.textContent||'').length*7,height:12};};
    const graph=[...w.document.querySelectorAll('[data-mcjs-bind]')].find(el=>JSON.parse(el.getAttribute('data-mcjs-bind')).adapter==='plotly');
    const px=value=>/^\d+(?:\.\d+)?px$/.test(value||'') ? parseFloat(value) : 0;
    Object.defineProperty(graph,'clientWidth',{get(){
      return px(graph.style.width) || px(graph.parentElement.style.width) || px(graph.querySelector('.svg-container')?.style.width);
    }});
    Object.defineProperty(graph,'clientHeight',{get(){return px(graph.style.height);}});
    w.eval(fs.readFileSync(process.env.MCUTILS_PLOTLY_JS,'utf8'));
  }),w=dom.window;
  try{
    const root=w.document.querySelector('[data-mcjs-state]');
    const graph=[...root.querySelectorAll('[data-mcjs-bind]')].find(el=>JSON.parse(el.getAttribute('data-mcjs-bind')).adapter==='plotly');
    await until(()=>graph._fullLayout && graph.data?.[0].selectedpoints?.[0]===1);
    const settle=async sample=>{
      await until(()=>graph.data?.[0].selectedpoints?.[0]===sample);
      assert.ok(graph.clientWidth>100,'The plot lost its width after selecting sample '+sample);
      assert.equal(graph.hidden,false);
      assert.equal(root.controller.get('visible'),true);
      assert.equal(graph.querySelectorAll('.point').length,3);
    };
    for(const sample of [0,1,2,0,2,1,0,1]){
      root.querySelector('tr[data-mcjs-key="'+sample+'"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
      await settle(sample);
    }
    const slider=root.querySelector('input[type=range]');
    for(const sample of [2,1,0,1,2,0]){
      slider.value=String(sample);slider.dispatchEvent(new w.Event('input',{bubbles:true}));
      await settle(sample);
    }
  }finally{w.close();}
});

test('X3D adapter waits for controllers and routes native updates in both directions',async()=>{
  const dom=load(fixtures.scene),w=dom.window;
  try{
    const root=w.document.querySelector('[data-mcjs-state]');
    const component=root.querySelector('.mcutils-x3d-component');
    const current={modeIndex:0,fraction:0};
    component.controller={selectMode(value){current.modeIndex=value;},seek(value){current.fraction=value;}};
    await until(()=>current.fraction===.25);
    root.controller.set('mode',1);await until(()=>current.modeIndex===1);
    component.dispatchEvent(new w.CustomEvent('scanchange',{detail:{modeIndex:0,fraction:.7}}));
    await until(()=>root.controller.get('fraction')===.7);
    assert.equal(root.controller.get('mode'),0);
  }finally{dom.window.close();}
});

test('bridge handlers use the ActiveHTMLWidgets model contract and suppress echoes',async()=>{
  assert.ok(fixtures.bridge,'Generate bridge fixtures with optional widget dependencies installed');
  const dom=load('<div id="transport">'+fixtures.bridge.html+'</div>'),w=dom.window;
  try{
    const messages=[];
    const widget={el:w.document.querySelector('#transport'),callHandler:async()=>{},model:{send:message=>messages.push(plain(message))}};
    const compile=source=>new w.Function('event','widget','context',source);
    await compile(fixtures.bridge.handlers.mcjs_init)({},widget,{});
    const input=widget.el.querySelector('input');
    input.value='2';input.dispatchEvent(new w.Event('input',{bubbles:true}));
    await until(()=>messages.length===1);
    assert.deepEqual(messages[0].detail,{name:'bridge',value:2});
    compile(fixtures.bridge.handlers.mcjs_set)({content:{name:'bridge',value:4}},widget.model,{});
    await until(()=>input.value==='4');
    assert.equal(messages.length,1);
    widget.el.remove();await until(()=>widget.model.__mcjs_states.size===0);
  }finally{dom.window.close();}
});

function automatic(html, assets={}, prepare) {
  const requests=[],errors=[];
  class Assets extends ResourceLoader {
    fetch(url) {
      requests.push(url);
      if(Object.hasOwn(assets,url))return Promise.resolve(Buffer.from(assets[url]));
      return Promise.reject(new Error('Unexpected external asset: '+url));
    }
  }
  const console=new VirtualConsole();console.on('jsdomError',error=>errors.push(error.message));
  const dom=new JSDOM(html,{url:'https://host.example.test/readout.html',runScripts:'dangerously',
    resources:new Assets(),pretendToBeVisual:true,virtualConsole:console,beforeParse:prepare});
  return {dom,w:dom.window,requests,errors};
}
const cdn='https://cdn.example.test/revision/McUtils/Jupyter/';
function cdnAssets() {
  return {
    [cdn+'JHTML/resources/javascript.js']:fixtures.entry,
    [cdn+'Apps/resources/native.js']:fixtures.native_js,
    [cdn+'Apps/resources/native.css']:fixtures.native_css,
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js':fixtures.bootstrap_js,
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css':fixtures.bootstrap_css
  };
}

test('one footer bundle automatically mounts independent WebComponents and owns their lifetime',async()=>{
  const {w,requests,errors}=automatic(fixtures.inline_multiple);
  try{
    await until(()=>[...w.document.querySelectorAll('mcui-state')].every(root=>root.controller));
    const [a,b]=w.document.querySelectorAll('mcui-state');
    assert.ok(a&&b);assert.equal(w.document.querySelectorAll('#mcutils-apps-native-js').length,1);
    assert.equal(w.document.querySelectorAll('script').length,1);
    const slider=a.querySelector('input[type=range]');slider.value='2';
    slider.dispatchEvent(new w.Event('input',{bubbles:true}));
    await until(()=>a.controller.get('value')===2);
    assert.equal(b.controller.get('value'),1);
    const saved=a.controller;a.remove();await until(()=>saved.disposed);
    w.document.body.append(a);await until(()=>a.controller&&!a.controller.disposed);
    assert.equal(a.controller.get('value'),1);
    assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);
  }finally{w.close();}
});

test('a single CDN entry activates the existing native UI and dynamically inserted state scopes',async()=>{
  const {w,requests,errors}=automatic(fixtures.cdn_native,cdnAssets());
  try{
    await until(()=>w.document.querySelector('mcui-state')?.controller);
    const scope=w.document.querySelector('mcui-state');
    const tabs=scope.querySelectorAll('[data-mcui-toggle=tab]');
    assert.equal(tabs.length,2);
    tabs[1].dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>tabs[1].getAttribute('aria-selected')==='true');
    const accordion=scope.querySelector('[data-mcui-toggle=collapse]');
    const previous=accordion.getAttribute('aria-expanded');
    accordion.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>accordion.getAttribute('aria-expanded')!==previous);
    const clone=scope.cloneNode(true);scope.after(clone);
    await until(()=>clone.controller);
    clone.controller.set('value',2);await until(()=>clone.querySelector('span').textContent==='2');
    assert.equal(scope.controller.get('value'),1);
    assert.deepEqual(requests.sort(),[cdn+'JHTML/resources/javascript.js',cdn+'Apps/resources/native.js',cdn+'Apps/resources/native.css'].sort());
    assert.deepEqual(errors,[]);
  }finally{w.close();}
});

test('explicit Bootstrap uses the shared entry point, real tab controls, and tooltip cleanup',
  {skip:!fixtures.bootstrap_js},async()=>{
  const {w,requests,errors}=automatic(fixtures.cdn_bootstrap,cdnAssets());
  try{
    await until(()=>w.document.querySelector('mcui-state')?.controller);
    const root=w.document.querySelector('mcui-bootstrap');
    const tabs=root.querySelectorAll('[data-bs-toggle=tab]');
    tabs[1].dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>tabs[1].classList.contains('active'));
    const tooltip=w.document.createElement('button');
    tooltip.setAttribute('data-bs-toggle','tooltip');tooltip.title='Details';root.append(tooltip);
    await until(()=>w.bootstrap.Tooltip.getInstance(tooltip));
    const instance=w.bootstrap.Tooltip.getInstance(tooltip);assert.ok(instance);
    tooltip.remove();await until(()=>!w.bootstrap.Tooltip.getInstance(tooltip));
    const slider=root.querySelector('input[type=range]');slider.value='2';
    slider.dispatchEvent(new w.Event('input',{bubbles:true}));
    await until(()=>root.querySelector('mcui-state').controller.get('value')===2);
    assert.equal(requests.filter(url=>url.endsWith('bootstrap.bundle.min.js')).length,1);
    assert.equal(requests.filter(url=>url.endsWith('/native.js')).length,1);
    assert.equal(requests.filter(url=>url.endsWith('/native.css')).length,0);
    assert.deepEqual(errors,[]);
  }finally{w.close();}
});

test('a host can load the CDN entry in its head before any state markup',async()=>{
  const script=fixtures.cdn_native.match(/<script[^>]*id="mcutils-apps-native-js"[^>]*><\/script>/)[0];
  const html=fixtures.cdn_native.replace(script,'').replace('</head>',script+'</head>');
  const {w,errors}=automatic(html,cdnAssets());
  try{
    await until(()=>w.document.querySelector('mcui-state')?.controller);
    const root=w.document.querySelector('mcui-state');
    assert.equal(root.querySelector('input[type=range]').value,'1');
    root.controller.set('value',2);await until(()=>root.querySelector('input[type=range]').value==='2');
    assert.deepEqual(errors,[]);
  }finally{w.close();}
});

test('offline Readout embeds real Plotly once and performs no asset requests on selection',async()=>{
  const {w,requests,errors}=automatic(fixtures.offline_native,{},w=>{
    w.TextEncoder=TextEncoder;w.TextDecoder=TextDecoder;w.URL.createObjectURL=()=>'';
    w.HTMLCanvasElement.prototype.getContext=()=>({measureText:s=>({width:String(s).length*7})});
    w.SVGElement.prototype.getBBox=function(){return{x:0,y:0,width:(this.textContent||'').length*7,height:12};};
  });
  try{
    const root=w.document.querySelector('mcui-state');
    const graph=[...root.querySelectorAll('[data-mcjs-bind]')].find(el=>JSON.parse(el.getAttribute('data-mcjs-bind')).adapter==='plotly');
    await until(()=>graph.data?.[0].selectedpoints?.[0]===1);
    root.querySelector('tr[data-mcjs-key="2"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>graph.data[0].selectedpoints[0]===2);
    assert.equal(root.controller.get('sample'),2);
    assert.equal(w.document.querySelectorAll('#mcutils-plotly-js').length,1);
    assert.equal(w.document.querySelectorAll('#mcutils-apps-native-js').length,1);
    assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);
  }finally{w.close();}
});

test('offline explicit Bootstrap embeds its dependencies and makes no requests',
  {skip:!fixtures.offline_bootstrap},async()=>{
  const {w,requests,errors}=automatic(fixtures.offline_bootstrap);
  try{
    await until(()=>w.document.querySelector('mcui-state')?.controller);
    const tabs=w.document.querySelectorAll('[data-bs-toggle=tab]');
    tabs[1].dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
    await until(()=>tabs[1].classList.contains('active'));
    assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);
  }finally{w.close();}
});
