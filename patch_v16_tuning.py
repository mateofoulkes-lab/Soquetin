from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
"Prototipo V1.5:":"Prototipo V1.6:",
"Recuperador de password de Soquetin · V1.5":"Recuperador de password de Soquetin · V1.6",
"renderer.toneMappingExposure = 1.68;":"renderer.toneMappingExposure = 1.38;",
"scene.add(new THREE.HemisphereLight(0xe8d7b5,0x3a2618,2.25));":"scene.add(new THREE.HemisphereLight(0xdcc8a3,0x302014,1.65));",
"new THREE.PointLight(0xffc77a,16.5,14.5,2);":"new THREE.PointLight(0xffbd6c,12.5,13.0,2);",
"dungeonLights.push({light:l, base:16.5,":"dungeonLights.push({light:l, base:12.5,",
"P.vel.y=4.5;":"P.vel.y=4.03;",
"const dist=3.9;":"const dist=4.4;",
"addFloorRect(openCenter,z,openW,.9,0,floorMat,true);":"addFloorRect(openCenter,z,openW,.9,-.01,floorMat,true);",
"addFloorRect((a+b)/2,z,b-a,.9,0,floorMat,true);":"addFloorRect((a+b)/2,z,b-a,.9,-.01,floorMat,true);"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing: {a}')
    s=s.replace(a,b)

# Add a character-only fill light using Three.js layers.
needle="    const visualRoot=new THREE.Group(); playerRoot.add(visualRoot);\n"
if needle not in s:
    raise SystemExit('visualRoot needle missing')
insert="""    const visualRoot=new THREE.Group(); playerRoot.add(visualRoot);\n\n    // Character-only fill light: layer 1 is enabled on the camera/model,\n    // while dungeon geometry remains only on layer 0.\n    camera.layers.enable(1);\n    const playerFillLight=new THREE.PointLight(0xffe0b0,3.2,4.0,2);\n    playerFillLight.position.set(0,1.25,-1.15);\n    playerFillLight.layers.set(1);\n    playerRoot.add(playerFillLight);\n"""
s=s.replace(needle,insert,1)

needle2="""        if(obj.isMesh){\n          obj.castShadow=true;\n          obj.receiveShadow=true;\n        }\n"""
if needle2 not in s:
    raise SystemExit('model traverse needle missing')
replace2="""        if(obj.isMesh){\n          obj.castShadow=true;\n          obj.receiveShadow=true;\n          obj.layers.enable(1);\n        }\n"""
s=s.replace(needle2,replace2,1)

p.write_text(s,encoding='utf-8')
print('patched V1.6')
