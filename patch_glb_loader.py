from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('''    "imports": {\n      "three": "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js"\n    }''','''    "imports": {\n      "three": "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js",\n      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/"\n    }''')
s=s.replace("    import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js';","    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';\n    import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';\n    import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';")
s=s.replace("    const gltfLoader=new GLTFLoader();","    const gltfLoader=new GLTFLoader();\n    const dracoLoader=new DRACOLoader();\n    dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/libs/draco/gltf/');\n    gltfLoader.setDRACOLoader(dracoLoader);\n    gltfLoader.setMeshoptDecoder(MeshoptDecoder);")
s=s.replace("      console.warn('No se pudo cargar el Soquetin GLB; se mantiene el cubo provisional.',err);","      console.warn('No se pudo cargar el Soquetin GLB; se mantiene el cubo provisional.',err);\n      const status=document.getElementById('status');\n      if(status){ status.textContent='Error cargando Soquetin: '+(err?.message||err); status.style.color='#ff9b7a'; }")
p.write_text(s,encoding='utf-8')
print('patched GLB loader')