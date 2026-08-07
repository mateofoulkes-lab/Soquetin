from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
repls={
"Prototipo V1.4:":"Prototipo V1.5:",
"Recuperador de password de Soquetin · V1.4":"Recuperador de password de Soquetin · V1.5",
"renderer.toneMappingExposure = 1.32;":"renderer.toneMappingExposure = 1.68;",
"scene.add(new THREE.HemisphereLight(0xd8c49c,0x2b1b10,1.5));":"scene.add(new THREE.HemisphereLight(0xe8d7b5,0x3a2618,2.25));",
"new THREE.PointLight(0xffbb68,11.5,12.5,2);":"new THREE.PointLight(0xffc77a,16.5,14.5,2);",
"dungeonLights.push({light:l, base:11.5,":"dungeonLights.push({light:l, base:16.5,",
"const CHARACTER_VISUAL_HEIGHT=1.12;":"const CHARACTER_VISUAL_HEIGHT=0.896;"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing: {a}')
    s=s.replace(a,b)
needle="      model.position.y -= scaledBox.min.y;\n"
if needle not in s:
    raise SystemExit('model placement needle missing')
s=s.replace(needle, needle+"      // Este GLB viene orientado al reves respecto del forward del jugador.\n      model.rotation.y += Math.PI;\n",1)
p.write_text(s,encoding='utf-8')
print('patched V1.5')
