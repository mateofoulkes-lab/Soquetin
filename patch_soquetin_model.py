from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace("    import * as THREE from 'three';\n", "    import * as THREE from 'three';\n    import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js';\n")

old='''    const playerRoot=new THREE.Group(); scene.add(playerRoot);\n    const body=new THREE.Mesh(new THREE.BoxGeometry(.44,1.12,.44),new THREE.MeshStandardMaterial({color:0xe2d2a2,roughness:.72}));\n    body.castShadow=true; body.receiveShadow=true; body.position.y=.56; playerRoot.add(body);\n    const face=new THREE.Mesh(new THREE.PlaneGeometry(.28,.22),new THREE.MeshBasicMaterial({color:0x1a1814}));\n    face.position.set(0,.73,-.221); face.rotation.y=Math.PI; body.add(face);\n    const eyeMat=new THREE.MeshBasicMaterial({color:0xece6d7});\n    for(const ex of [-.065,.065]){\n      const e=new THREE.Mesh(new THREE.CircleGeometry(.028,12),eyeMat); e.position.set(ex,.035,.002); face.add(e);\n    }\n'''

new='''    const playerRoot=new THREE.Group(); scene.add(playerRoot);\n    // Visual content lives under a base pivot at the character's feet.\n    // This lets squash/stretch deform the model without changing the collider.\n    const visualRoot=new THREE.Group(); playerRoot.add(visualRoot);\n\n    // Simple fallback while the GLB loads (or if it ever fails).\n    const body=new THREE.Mesh(new THREE.BoxGeometry(.44,1.12,.44),new THREE.MeshStandardMaterial({color:0xe2d2a2,roughness:.72}));\n    body.castShadow=true; body.receiveShadow=true; body.position.y=.56; visualRoot.add(body);\n    const face=new THREE.Mesh(new THREE.PlaneGeometry(.28,.22),new THREE.MeshBasicMaterial({color:0x1a1814}));\n    face.position.set(0,.73,-.221); face.rotation.y=Math.PI; body.add(face);\n    const eyeMat=new THREE.MeshBasicMaterial({color:0xece6d7});\n    for(const ex of [-.065,.065]){\n      const e=new THREE.Mesh(new THREE.CircleGeometry(.028,12),eyeMat); e.position.set(ex,.035,.002); face.add(e);\n    }\n\n    const SOQUETIN_MODEL_URL='3354c2e8-ca8b-4056-87f9-db61cd76f25d.glb';\n    const CHARACTER_VISUAL_HEIGHT=1.12;\n    const gltfLoader=new GLTFLoader();\n    gltfLoader.load(SOQUETIN_MODEL_URL,(gltf)=>{\n      const model=gltf.scene;\n      model.updateMatrixWorld(true);\n      const box=new THREE.Box3().setFromObject(model);\n      const size=new THREE.Vector3();\n      const center=new THREE.Vector3();\n      box.getSize(size); box.getCenter(center);\n      const scale=size.y>0 ? CHARACTER_VISUAL_HEIGHT/size.y : 1;\n      model.scale.setScalar(scale);\n      model.updateMatrixWorld(true);\n\n      // Recompute after scaling, then center horizontally and place the feet/base at y=0.\n      const scaledBox=new THREE.Box3().setFromObject(model);\n      const scaledCenter=new THREE.Vector3();\n      scaledBox.getCenter(scaledCenter);\n      model.position.x -= scaledCenter.x;\n      model.position.z -= scaledCenter.z;\n      model.position.y -= scaledBox.min.y;\n\n      model.traverse(obj=>{\n        if(obj.isMesh){\n          obj.castShadow=true;\n          obj.receiveShadow=true;\n        }\n      });\n\n      visualRoot.remove(body);\n      visualRoot.add(model);\n    },undefined,(err)=>{\n      console.warn('No se pudo cargar el Soquetin GLB; se mantiene el cubo provisional.',err);\n    });\n'''

if old not in s:
    raise SystemExit('player block not found')
s=s.replace(old,new,1)

old2='''      body.scale.set(sxz,sy,sxz);\n      body.position.y=.56*sy;\n      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;\n'''
new2='''      visualRoot.scale.set(sxz,sy,sxz);\n      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;\n'''
if old2 not in s:
    raise SystemExit('squash block not found')
s=s.replace(old2,new2,1)

p.write_text(s,encoding='utf-8')
print('patched')
