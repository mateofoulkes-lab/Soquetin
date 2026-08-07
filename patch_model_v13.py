from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("<div id=\"title\">Recuperador de password de Soquetin · V1.2</div>","<div id=\"title\">Recuperador de password de Soquetin · V1.3</div><div id=\"modelStatus\" style=\"position:absolute;left:18px;top:58px;padding:6px 9px;background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.14);border-radius:8px;font:700 11px ui-monospace,monospace;color:#ffd88a\">MODELO: CARGANDO…</div>")
s=s.replace("Prototipo V1.2:","Prototipo V1.3:")
s=s.replace("import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';","import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';\n    import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';")
old="""    gltfLoader.setDRACOLoader(dracoLoader);\n    gltfLoader.setMeshoptDecoder(MeshoptDecoder);\n    gltfLoader.load(SOQUETIN_MODEL_URL,(gltf)=>{\n"""
new="""    gltfLoader.setDRACOLoader(dracoLoader);\n    gltfLoader.setMeshoptDecoder(MeshoptDecoder);\n    const ktx2Loader=new KTX2Loader();\n    ktx2Loader.setTranscoderPath('https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/libs/basis/');\n    ktx2Loader.detectSupport(renderer);\n    gltfLoader.setKTX2Loader(ktx2Loader);\n    const modelStatus=document.getElementById('modelStatus');\n    gltfLoader.load(SOQUETIN_MODEL_URL,(gltf)=>{\n"""
if old not in s: raise SystemExit('loader setup block not found')
s=s.replace(old,new,1)
s=s.replace("      visualRoot.remove(body);\n      visualRoot.add(model);","      visualRoot.remove(body);\n      visualRoot.add(model);\n      if(modelStatus){modelStatus.textContent='MODELO: OK · GLB';modelStatus.style.color='#9dff9d';}",1)
s=s.replace("      if(status){ status.textContent='Error cargando Soquetin: '+(err?.message||err); status.style.color='#ff9b7a'; }","      const msg=(err?.message||String(err));\n      if(status){ status.textContent='Error cargando Soquetin: '+msg; status.style.color='#ff9b7a'; }\n      if(modelStatus){modelStatus.textContent='MODELO ERROR: '+msg;modelStatus.style.color='#ff8f78';}",1)
p.write_text(s,encoding='utf-8')
