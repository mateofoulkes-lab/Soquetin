from pathlib import Path
import re

idx=Path('index.html').read_text(encoding='utf-8')
ed=Path('texture-editor.html').read_text(encoding='utf-8')

m=re.search(r'    const SOQUETIN_TEXTURE_OVERRIDES = (\{.*?\n    \});',idx,re.S)
if not m: raise SystemExit('stable texture table not found')
table_a=m.group(1)

table_b=r'''{
  "floor@0,-0.12,9#face2":{"scope":"face","repeatU":3.5,"repeatV":1.15,"offsetU":0,"offsetV":0,"rotation":0},
  "floor@0,-0.12,2.5#face2":{"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-1,"offsetV":-1,"rotation":0},
  "floor@7,-0.12,2.5#face2":{"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-0.82,"offsetV":0,"rotation":0},
  "lintel@7,3.7,-13.04#face0":{"scope":"face","repeatU":4.35,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@7,3.7,-13.04#face4":{"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0,"offsetV":0.09,"rotation":0},
  "lintel@7,3.7,-13.04#face5":{"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0.07,"offsetV":-0.03,"rotation":0},
  "lintel@0,3.7,-13.04#face0":{"scope":"face","repeatU":0.1,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@0,3.7,-13.04#face5":{"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.06,"offsetV":-0.04,"rotation":0},
  "lintel@-7,3.7,-13.04#face0":{"scope":"face","repeatU":1.75,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@-7,3.7,-13.04#face5":{"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.07,"offsetV":-0.04,"rotation":0},
  "wall@-5.55,2.5,-20.04#face0":{"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-5.55,2.5,-20.04#object":{"scope":"object","repeatU":3.5,"repeatV":5.05,"offsetU":0.78,"offsetV":0,"rotation":0},
  "wall@5.55,2.5,-20.04#object":{"scope":"object","repeatU":2.85,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@0,3.7,-20.04#object":{"scope":"object","repeatU":0.35,"repeatV":2.65,"offsetU":-0.11,"offsetV":0.22,"rotation":0},
  "floor@0,-0.12,-16.54#object":{"scope":"object","repeatU":3.5,"repeatV":1.35,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
  "floor@7,-0.12,-10.54#object":{"scope":"object","repeatU":1.15,"repeatV":0.75,"offsetU":0,"offsetV":1.63,"rotation":0},
  "floor@-7,-0.12,-10.54#object":{"scope":"object","repeatU":1.2,"repeatV":0.75,"offsetU":-1.12,"offsetV":0.03,"rotation":0},
  "lintel@0,3.7,-20.04#face5":{"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.02,"offsetV":0.22,"rotation":0},
  "wall@5.75,2.5,-24.04#face0":{"scope":"face","repeatU":2,"repeatV":2.6,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@5.75,2.5,-24.04#face1":{"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@1,2.5,-28.04#face4":{"scope":"face","repeatU":3.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-3.75,2.5,-24.04#face0":{"scope":"face","repeatU":2.55,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "floor@1,-0.12,-24.04#face2":{"scope":"face","repeatU":1.55,"repeatV":1.45,"offsetU":-0.14,"offsetV":0.01,"rotation":0},
  "wall@-3.5,2.5,-13.04#face0":{"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,-13.04#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "wall@3.5,2.5,-13.04#face0":{"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,-13.04#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.07,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,5#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@3.5,2.5,5#face0":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,5#face0":{"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":-0.07,"offsetV":0,"rotation":0},
  "wall@3.5,2.5,5#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-1.77,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,5#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "lintel@0,3.7,-13.04#face4":{"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":-0.74,"offsetV":-0.04,"rotation":0},
  "wall@3.5,2.5,-13.04#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "lintel@-7,3.7,-13.04#face4":{"scope":"face","repeatU":0.55,"repeatV":2.6,"offsetU":-0.93,"offsetV":0.08,"rotation":0},
  "wall@5.55,2.5,-20.04#face1":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0}
}'''

# Add styling/status box.
ed=ed.replace('  #mode{position:absolute;left:14px;top:14px;background:#17130eee;padding:8px 12px;border:1px solid #ffffff2c;border-radius:8px;font-size:12px;font-weight:800;pointer-events:none}',
'''  #mode{position:absolute;left:14px;top:14px;background:#17130eee;padding:8px 12px;border:1px solid #ffffff2c;border-radius:8px;font-size:12px;font-weight:800;pointer-events:none}
  #abStatus{position:absolute;left:14px;top:54px;background:#000d;padding:9px 12px;border:1px solid #ffffff2c;border-radius:8px;font:700 11px ui-monospace,monospace;pointer-events:none;white-space:pre-line;max-width:520px}''',1)
ed=ed.replace('<div id="mode">MODO: MIRAR</div>','<div id="mode">MODO: MIRAR</div>\n    <div id="abStatus">A/B: apuntá una superficie en modo SELECCIONAR</div>',1)
ed=ed.replace('WASD + mouse para recorrer\n<span class="key">V</span> alterna MIRAR / SELECCIONAR','WASD + mouse para recorrer\n<span class="key">V</span> MIRAR / SELECCIONAR · <span class="key">A</span> ESTABLE · <span class="key">B</span> NUEVA',1)
ed=ed.replace('En modo seleccionar, hacé clic directamente sobre la cara que querés corregir. Los cambios se ven <b>en vivo</b>.','En modo seleccionar, apuntá una cara con el cursor. <b>A</b> aplica la tabla estable y <b>B</b> la tanda nueva para esa superficie. También podés hacer clic para editarla manualmente. Los cambios se ven <b>en vivo</b>.',1)

anchor="const saved=JSON.parse(localStorage.getItem('soquetinTextureOverrides')||'{}');\n"
insert=f'''const saved=JSON.parse(localStorage.getItem('soquetinTextureOverrides')||'{{}}');

// A/B snapshots: A is the current stable table; B is the candidate batch.
const TEXTURE_TABLE_A = {table_a};
const TEXTURE_TABLE_B = {table_b};
let hovered=null, lastAB='';
'''
if anchor not in ed: raise SystemExit('saved anchor missing')
ed=ed.replace(anchor,insert,1)

# Insert helpers before pickAt.
anchor='function pickAt(clientX,clientY){\n'
helpers=r'''function cfgApply(mat,cfg){
  if(!mat?.map || !cfg)return;
  const tex=mat.map;
  tex.wrapS=tex.wrapT=api.THREE.RepeatWrapping;
  tex.repeat.set(cfg.repeatU,cfg.repeatV);
  tex.offset.set(cfg.offsetU,cfg.offsetV);
  tex.center.set(.5,.5);
  tex.rotation=cfg.rotation*Math.PI/180;
  tex.needsUpdate=true;
}
function hitAt(clientX,clientY){
  if(!api || !canvas || mode!=='select')return null;
  const THREE=api.THREE, rect=canvas.getBoundingClientRect();
  const x=((clientX-rect.left)/rect.width)*2-1, y=-((clientY-rect.top)/rect.height)*2+1;
  const ray=new THREE.Raycaster(); ray.setFromCamera(new THREE.Vector2(x,y),api.camera);
  const hits=ray.intersectObjects(api.scene.children,true).filter(h=>h.object?.isMesh && h.object.visible);
  for(const hit of hits){
    const fi=hit.face?.materialIndex??0, mat=isolateMaterialForFace(hit.object,fi);
    if(mat)return {mesh:hit.object,face:fi,mat,key:surfaceKey(hit.object,fi)};
  }
  return null;
}
function tableStateFor(sel,table){
  if(!sel)return {objectCfg:null,faceCfg:null};
  const base=objectKey(sel.mesh).replace(/#object$/,'');
  return {objectCfg:table[base+'#object']||null,faceCfg:table[base+'#face'+sel.face]||null};
}
function refreshABStatus(){
  if(!hovered){$('abStatus').textContent='A/B: apuntá una superficie en modo SELECCIONAR';return;}
  const a=tableStateFor(hovered,TEXTURE_TABLE_A), b=tableStateFor(hovered,TEXTURE_TABLE_B);
  const mark=s=>(s.objectCfg||s.faceCfg)?'SÍ':'—';
  $('abStatus').textContent=`${hovered.key}\nA · ESTABLE: ${mark(a)}    B · NUEVA: ${mark(b)}${lastAB?'\nÚLTIMA: '+lastAB:''}`;
}
function applyAB(table,label){
  if(!hovered)return;
  const state=tableStateFor(hovered,table);
  if(!state.objectCfg && !state.faceCfg){lastAB=`${label}: sin entrada para esta superficie`;refreshABStatus();return;}
  const mats=prepareMeshMaterials(hovered.mesh);
  if(state.objectCfg) for(const mat of mats) cfgApply(mat,state.objectCfg);
  if(state.faceCfg) cfgApply(mats[hovered.face]||mats[0],state.faceCfg);
  selected=hovered;
  lastAB=`${label} aplicada${state.objectCfg?' · objeto':''}${state.faceCfg?' · cara '+hovered.face:''}`;
  loadSelected(); refreshABStatus();
}
function hoverAt(clientX,clientY){hovered=hitAt(clientX,clientY);refreshABStatus();}

'''
if anchor not in ed: raise SystemExit('pick anchor missing')
ed=ed.replace(anchor,helpers+anchor,1)

# Simplify pickAt to reuse hitAt while preserving behavior.
start=ed.index('function pickAt(clientX,clientY){')
end=ed.index('\nfunction loadSelected(){',start)
ed=ed[:start]+'''function pickAt(clientX,clientY){
  const hit=hitAt(clientX,clientY);
  if(hit){selected=hit;hovered=hit;loadSelected();refreshABStatus();return;}
  $('sel').textContent='No encontré una superficie con textura debajo del cursor.';
}
'''+ed[end:]

# Replace parent key handler to add A/B.
old="document.addEventListener('keydown',e=>{if(e.code==='KeyV' && !['INPUT','TEXTAREA'].includes(e.target.tagName)){e.preventDefault();toggleMode();}});"
new="""document.addEventListener('keydown',e=>{
  if(['INPUT','TEXTAREA'].includes(e.target.tagName))return;
  if(e.code==='KeyV'){e.preventDefault();toggleMode();return;}
  if(mode==='select' && e.code==='KeyA'){e.preventDefault();applyAB(TEXTURE_TABLE_A,'A · ESTABLE');return;}
  if(mode==='select' && e.code==='KeyB'){e.preventDefault();applyAB(TEXTURE_TABLE_B,'B · NUEVA');return;}
});"""
if old not in ed: raise SystemExit('parent key handler missing')
ed=ed.replace(old,new,1)

# Add iframe key handlers and mouse hover.
old="d.addEventListener('keydown',e=>{if(e.code==='KeyV'){e.preventDefault();e.stopPropagation();toggleMode();}},true);\n  if(canvas){canvas.addEventListener('click',e=>{if(mode!=='select')return;e.preventDefault();e.stopImmediatePropagation();pickAt(e.clientX,e.clientY);},true)}"
new="""d.addEventListener('keydown',e=>{
    if(e.code==='KeyV'){e.preventDefault();e.stopPropagation();toggleMode();return;}
    if(mode==='select' && e.code==='KeyA'){e.preventDefault();e.stopPropagation();applyAB(TEXTURE_TABLE_A,'A · ESTABLE');return;}
    if(mode==='select' && e.code==='KeyB'){e.preventDefault();e.stopPropagation();applyAB(TEXTURE_TABLE_B,'B · NUEVA');return;}
  },true);
  if(canvas){
    canvas.addEventListener('mousemove',e=>{if(mode==='select')hoverAt(e.clientX,e.clientY)},true);
    canvas.addEventListener('click',e=>{if(mode!=='select')return;e.preventDefault();e.stopImmediatePropagation();pickAt(e.clientX,e.clientY);},true)
  }"""
if old not in ed: raise SystemExit('iframe handlers missing')
ed=ed.replace(old,new,1)

Path('texture-editor.html').write_text(ed,encoding='utf-8')
print('patched texture editor with A/B comparison mode')