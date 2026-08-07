from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
"Prototipo V1.6:":"Prototipo V1.7:",
"Recuperador de password de Soquetin · V1.6":"Recuperador de password de Soquetin · V1.7"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing version token: {a}')
    s=s.replace(a,b)

# Remove the character-only fill light/layer setup from V1.6.
old="""    // Character-only fill light: layer 1 is enabled on the camera/model,\n    // while dungeon geometry remains only on layer 0.\n    camera.layers.enable(1);\n    const playerFillLight=new THREE.PointLight(0xffe0b0,3.2,4.0,2);\n    playerFillLight.position.set(0,1.25,-1.15);\n    playerFillLight.layers.set(1);\n    playerRoot.add(playerFillLight);\n"""
if old not in s:
    raise SystemExit('character fill block missing')
s=s.replace(old,'',1)

# Remove layer opt-in from model meshes, and brighten the model material itself instead.
old2="""        if(obj.isMesh){\n          obj.castShadow=true;\n          obj.receiveShadow=true;\n          obj.layers.enable(1);\n        }\n"""
new2="""        if(obj.isMesh){\n          obj.castShadow=true;\n          obj.receiveShadow=false;\n\n          // Brighten only Soquetin itself. This does NOT emit light into the scene.\n          // Clone materials so the GLB remains isolated from any shared material state.\n          const mats=Array.isArray(obj.material)?obj.material:[obj.material];\n          const adjusted=mats.map(mat=>{\n            if(!mat) return mat;\n            const m=mat.clone();\n            if('emissive' in m){\n              m.emissive = new THREE.Color(0x2a2118);\n              m.emissiveIntensity = 0.38;\n            }\n            if('roughness' in m && Number.isFinite(m.roughness)) m.roughness=Math.min(1,m.roughness+.05);\n            m.needsUpdate=true;\n            return m;\n          });\n          obj.material=Array.isArray(obj.material)?adjusted:adjusted[0];\n        }\n"""
if old2 not in s:
    raise SystemExit('model traverse block missing')
s=s.replace(old2,new2,1)

# Configure room lights for inexpensive dynamic shadow use. Keep them normally non-shadowing;
# only the nearest one will be enabled each frame.
old3="""      const l=new THREE.PointLight(0xffbd6c,12.5,13.0,2);\n      l.position.set(x,y,z); l.castShadow=false; scene.add(l);\n      dungeonLights.push({light:l, base:12.5, phase:Math.random()*Math.PI*2, speed:.75+Math.random()*.55});\n"""
new3="""      const l=new THREE.PointLight(0xffbd6c,12.5,13.0,2);\n      l.position.set(x,y,z);\n      l.castShadow=false;\n      l.shadow.mapSize.set(384,384);\n      l.shadow.camera.near=.15;\n      l.shadow.camera.far=14;\n      l.shadow.bias=-0.0025;\n      l.shadow.normalBias=.025;\n      scene.add(l);\n      dungeonLights.push({light:l, base:12.5, phase:Math.random()*Math.PI*2, speed:.75+Math.random()*.55});\n"""
if old3 not in s:
    raise SystemExit('dungeon light block missing')
s=s.replace(old3,new3,1)

# Add helper before player block. It keeps only the closest room light shadow-enabled.
needle="""    // Apply exported UV/repeat settings after all dungeon geometry is built.\n    applyHardcodedTextureOverrides();\n\n    // ------------------------------------------------------------\n    // PLAYER\n"""
insert="""    // Apply exported UV/repeat settings after all dungeon geometry is built.\n    applyHardcodedTextureOverrides();\n\n    let activeShadowLight=-1;\n    function updateCharacterShadowLight(){\n      if(!dungeonLights.length || typeof P==='undefined') return;\n      let best=-1, bestD=Infinity;\n      for(let i=0;i<dungeonLights.length;i++){\n        const lp=dungeonLights[i].light.position;\n        const dx=lp.x-P.pos.x, dz=lp.z-P.pos.z;\n        const d=dx*dx+dz*dz;\n        if(d<bestD){ bestD=d; best=i; }\n      }\n      if(best===activeShadowLight) return;\n      if(activeShadowLight>=0) dungeonLights[activeShadowLight].light.castShadow=false;\n      activeShadowLight=best;\n      if(activeShadowLight>=0) dungeonLights[activeShadowLight].light.castShadow=true;\n    }\n\n    // ------------------------------------------------------------\n    // PLAYER\n"""
if needle not in s:
    raise SystemExit('player section needle missing')
s=s.replace(needle,insert,1)

# Call shadow selection each frame after player position has been updated.
# Locate the visual transform line which is already in the animation loop.
needle2="""      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;\n"""
replacement2="""      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;\n      updateCharacterShadowLight();\n"""
if needle2 not in s:
    raise SystemExit('player transform line missing')
s=s.replace(needle2,replacement2,1)

p.write_text(s,encoding='utf-8')
print('patched V1.7 character brightness/shadows')
