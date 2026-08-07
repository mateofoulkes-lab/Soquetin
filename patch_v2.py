from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new):
    global s
    if old not in s:
        raise SystemExit(f'No se encontro bloque esperado: {old[:120]!r}')
    s = s.replace(old, new)

rep('renderer.toneMappingExposure = 1.15;', 'renderer.toneMappingExposure = 1.32;')
rep("const darkSideMat = new THREE.MeshStandardMaterial({color:0x302c25,roughness:1});",
    "const darkSideMat = new THREE.MeshStandardMaterial({color:0x3a342b,roughness:1});\n    const columnTopMat = new THREE.MeshStandardMaterial({map:texFloor,color:0xeadfbd,roughness:.82,emissive:0x2b2110,emissiveIntensity:.18});")

rep('''    const OUT_L=-9.3, OUT_R=9.3;
    const Z_START_FRONT=8.0;
    const Z_CHALLENGE_SOUTH=1.2;
    const Z_PIT_SOUTH=0.0;
    const Z_PIT_NORTH=-6.0;
    const Z_CHALLENGE_NORTH=-7.2;
    const Z_COMMON_NORTH=-12.8;
    const Z_FINAL_NORTH=-19.0;
    const ROOM_CENTERS=[-6.2,0,6.2];
    const ROOM_W=6.2;
    const FINAL_W=6.2;''', '''    const OUT_L=-10.5, OUT_R=10.5;
    const Z_START_FRONT=11.0;
    const Z_CHALLENGE_SOUTH=3.0;
    const Z_PIT_SOUTH=0.0;
    const Z_PIT_NORTH=-6.0;
    const Z_CHALLENGE_NORTH=-9.0;
    const Z_COMMON_NORTH=-16.0;
    const Z_FINAL_NORTH=-24.0;
    const ROOM_CENTERS=[-7.0,0,7.0];
    const ROOM_W=7.0;
    const FINAL_W=7.5;''')
rep('// keep a 1.2 m "vereda" before and after each jumping zone.', '// keep a 3 m "vereda" before and after each jumping zone.')
rep('for(const x of [-3.1,3.1]) wallSegment', 'for(const x of [-3.5,3.5]) wallSegment')
rep('new THREE.PlaneGeometry(18.6,6.4,1,1)', 'new THREE.PlaneGeometry(21.0,6.4,1,1)')

rep('''        const mesh=boxMesh(`column-${r}-${c}`,x,-5,z,.98,h,.98,darkSideMat,false,true);
        mesh.material = new THREE.MeshStandardMaterial({map:texFloor,roughness:.95});''', '''        const columnMats=[darkSideMat,darkSideMat,columnTopMat,darkSideMat,darkSideMat,darkSideMat];
        const mesh=boxMesh(`column-${r}-${c}`,x,-5,z,.98,h,.98,columnMats,false,true);''')

rep("posterOnHorizontalWall(-3.4,2.0,Z_CHALLENGE_SOUTH+.001", "posterOnHorizontalWall(-3.9,2.0,Z_CHALLENGE_SOUTH+.001")
rep("posterOnHorizontalWall(3.4,2.0,Z_CHALLENGE_SOUTH+.001", "posterOnHorizontalWall(3.9,2.0,Z_CHALLENGE_SOUTH+.001")
rep("posterOnHorizontalWall(-2.45,2.0,Z_COMMON_NORTH+.001", "posterOnHorizontalWall(-2.8,2.0,Z_COMMON_NORTH+.001")

rep('scene.add(new THREE.HemisphereLight(0xc6ad82,0x20140d,1.12));', 'scene.add(new THREE.HemisphereLight(0xd8c49c,0x2b1b10,1.5));')
rep('const warm = [ [-6.2,4.15,4.6], [0,4.15,4.6], [6.2,4.15,4.6], [-6.2,4.15,-3], [0,4.15,-3], [6.2,4.15,-3], [-6.2,4.15,-9.8], [0,4.15,-9.8], [6.2,4.15,-9.8], [0,4.15,-15.9] ];',
    'const warm = [ [-7,4.15,7], [0,4.15,7], [7,4.15,7], [-7,4.15,-3], [0,4.15,-3], [7,4.15,-3], [-7,4.15,-12.5], [0,4.15,-12.5], [7,4.15,-12.5], [0,4.15,-20] ];')
rep('const l=new THREE.PointLight(0xffb45d,8.6,9.5,2);', 'const l=new THREE.PointLight(0xffbb68,11.5,12.5,2);')
rep('dungeonLights.push({light:l, base:8.6,', 'dungeonLights.push({light:l, base:11.5,')

rep('pos:new THREE.Vector3(0,.02,5.8), vel:new THREE.Vector3(),', 'pos:new THREE.Vector3(0,.02,8.2), vel:new THREE.Vector3(),')
rep('spawn:new THREE.Vector3(0,.02,5.8)', 'spawn:new THREE.Vector3(0,.02,8.2), bigJumpUsed:false')

rep('''    function tryBigJump(){
      if(P.dead || !P.grounded) return;
      const dir=inputVector();
      if(dir.lengthSq()<.01) dir.set(-Math.sin(P.camYaw),0,-Math.cos(P.camYaw));
      dir.normalize();
      P.vel.y=5.7;
      P.vel.x=dir.x*3.75; P.vel.z=dir.z*3.75;
      P.grounded=false; P.squash=1;
    }''', '''    function tryBigJump(){
      // El salto grande puede interrumpir inmediatamente un saltito automatico.
      // Solo se permite uno hasta volver a tocar una superficie.
      if(P.dead || P.bigJumpUsed) return;
      const dir=inputVector();
      if(dir.lengthSq()<.01) dir.set(-Math.sin(P.camYaw),0,-Math.cos(P.camYaw));
      dir.normalize();
      P.vel.y=5.9;
      P.vel.x=dir.x*4.0; P.vel.z=dir.z*4.0;
      P.grounded=false; P.bigJumpUsed=true; P.squash=1;
    }''')

rep('P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.squash=.4;',
    'P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;')

rep('''      // automatic "Worms-like" little hops while moving
      if(P.grounded){
        P.autoHopTimer-=dt;
        if(hasInput && P.autoHopTimer<=0){
          dir.normalize();
          P.vel.y=2.35;
          const hopSpeed=2.75;
          P.vel.x=THREE.MathUtils.lerp(P.vel.x,dir.x*hopSpeed,.72);
          P.vel.z=THREE.MathUtils.lerp(P.vel.z,dir.z*hopSpeed,.72);
          P.grounded=false; P.autoHopTimer=0; P.squash=.52;
        } else if(!hasInput) {
          P.vel.x*=Math.pow(.32,dt); P.vel.z*=Math.pow(.32,dt);
        }
      } else if(hasInput) {
        // directional control in air
        dir.normalize();
        const air=5.6*dt;
        P.vel.x=THREE.MathUtils.lerp(P.vel.x,dir.x*3.25,Math.min(1,air*.72));
        P.vel.z=THREE.MathUtils.lerp(P.vel.z,dir.z*3.25,Math.min(1,air*.72));
      }''', '''      // Movimiento a saltitos: al soltar la direccion NO hay inercia ni patinaje.
      // Mientras se mantiene una direccion, los saltitos se encadenan al aterrizar.
      if(!hasInput){
        P.vel.x=0; P.vel.z=0;
      }

      if(P.grounded){
        P.bigJumpUsed=false;
        P.autoHopTimer-=dt;
        if(hasInput && P.autoHopTimer<=0){
          dir.normalize();
          P.vel.y=2.35;
          const hopSpeed=2.9;
          P.vel.x=dir.x*hopSpeed;
          P.vel.z=dir.z*hopSpeed;
          P.grounded=false; P.autoHopTimer=0; P.squash=.52;
        }
      } else if(hasInput) {
        // Control direccional inmediato en el aire.
        dir.normalize();
        const targetSpeed=P.bigJumpUsed?4.0:3.25;
        const air=Math.min(1,7.0*dt);
        P.vel.x=THREE.MathUtils.lerp(P.vel.x,dir.x*targetSpeed,air);
        P.vel.z=THREE.MathUtils.lerp(P.vel.z,dir.z*targetSpeed,air);
      }''')

p.write_text(s, encoding='utf-8')
print('index.html actualizado')
