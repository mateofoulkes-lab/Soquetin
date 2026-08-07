from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
repls={
"Prototipo V1.9:":"Prototipo V1.10:",
"Recuperador de password de Soquetin · V1.9":"Recuperador de password de Soquetin · V1.10",
"const smokeGeo=new THREE.SphereGeometry(.12,8,6);":"const smokeGeo=new THREE.SphereGeometry(.085,8,6);",
"opacity:.68,depthWrite:false":"opacity:.42,depthWrite:false",
"const k=.85+Math.random()*1.15;":"const k=.70+Math.random()*.85;",
"life:1.0+Math.random()*.65,vx:(Math.random()-.5)*.16,vz:(Math.random()-.5)*.16,vy:.34+Math.random()*.24":"life:.85+Math.random()*.50,vx:(Math.random()-.5)*.14,vz:(Math.random()-.5)*.14,vy:.68+Math.random()*.34",
"p.mesh.material.opacity=.68*(1-q);":"p.mesh.material.opacity=.42*(1-q);",
"p.mesh.scale.multiplyScalar(1+dt*1.15);":"p.mesh.scale.multiplyScalar(1+dt*.75);"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing token: {a}')
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
print('patched V1.10 smoke')
