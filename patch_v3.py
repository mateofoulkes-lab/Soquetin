from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'Pattern not found: {label}')
    s = s.replace(old, new, 1)

rep("""    function buildWallWithOpeningHorizontal(z, x1, x2, openCenter, openW=1.2, t=.3, h=5){
      const leftEnd=openCenter-openW/2, rightStart=openCenter+openW/2;
      if(leftEnd>x1) wallSegment((x1+leftEnd)/2,z,leftEnd-x1,t,h);
      if(x2>rightStart) wallSegment((rightStart+x2)/2,z,x2-rightStart,t,h);
      boxMesh('lintel',openCenter,3.7,z,openW,2.6,t,wallMat,true,true);
    }

    function buildWallWithOpeningsHorizontal(z, x1, x2, centers, openW=1.2, t=.3, h=5){
      const intervals=centers.map(c=>[c-openW/2,c+openW/2]).sort((a,b)=>a[0]-b[0]);
      let cur=x1;
      for(const [a,b] of intervals){
        if(a>cur) wallSegment((cur+a)/2,z,a-cur,t,h);
        boxMesh('lintel',(a+b)/2,3.7,z,b-a,2.6,t,wallMat,true,true);
        cur=b;
      }
      if(cur<x2) wallSegment((cur+x2)/2,z,x2-cur,t,h);
    }""",
"""    function buildWallWithOpeningHorizontal(z, x1, x2, openCenter, openW=1.2, t=.3, h=5){
      const leftEnd=openCenter-openW/2, rightStart=openCenter+openW/2;
      if(leftEnd>x1) wallSegment((x1+leftEnd)/2,z,leftEnd-x1,t,h);
      if(x2>rightStart) wallSegment((rightStart+x2)/2,z,x2-rightStart,t,h);
      boxMesh('lintel',openCenter,3.7,z,openW,2.6,t,wallMat,true,true);
      addFloorRect(openCenter,z,openW,.9,0,floorMat,true);
    }

    function buildWallWithOpeningsHorizontal(z, x1, x2, centers, openW=1.2, t=.3, h=5){
      const intervals=centers.map(c=>[c-openW/2,c+openW/2]).sort((a,b)=>a[0]-b[0]);
      let cur=x1;
      for(const [a,b] of intervals){
        if(a>cur) wallSegment((cur+a)/2,z,a-cur,t,h);
        boxMesh('lintel',(a+b)/2,3.7,z,b-a,2.6,t,wallMat,true,true);
        addFloorRect((a+b)/2,z,b-a,.9,0,floorMat,true);
        cur=b;
      }
      if(cur<x2) wallSegment((cur+x2)/2,z,x2-cur,t,h);
    }""", 'door thresholds')

rep("""    const OUT_L=-10.5, OUT_R=10.5;
    const Z_START_FRONT=11.0;
    const Z_CHALLENGE_SOUTH=3.0;
    const Z_PIT_SOUTH=0.0;
    const Z_PIT_NORTH=-6.0;
    const Z_CHALLENGE_NORTH=-9.0;
    const Z_COMMON_NORTH=-16.0;
    const Z_FINAL_NORTH=-24.0;
    const ROOM_CENTERS=[-7.0,0,7.0];
    const ROOM_W=7.0;
    const FINAL_W=7.5;
    const OPEN_W=1.2;
    const H=5, T=.3;""",
"""    const OUT_L=-10.5, OUT_R=10.5;
    const ROOM_CENTERS=[-7.0,0,7.0];
    const ROOM_W=7.0;
    const FINAL_W=7.5;
    const OPEN_W=1.2;
    const H=5, T=.3;
    const TILE_SIZE=(ROOM_W-.3)/5;
    const Z_START_FRONT=13.0;
    const Z_CHALLENGE_SOUTH=5.0;
    const Z_PIT_SOUTH=0.0;
    const Z_PIT_NORTH=Z_PIT_SOUTH-(TILE_SIZE*6);
    const Z_CHALLENGE_NORTH=Z_PIT_NORTH-5.0;
    const Z_COMMON_NORTH=Z_CHALLENGE_NORTH-7.0;
    const Z_FINAL_NORTH=Z_COMMON_NORTH-8.0;""", 'map dimensions')

s = s.replace('keep a 3 m "vereda" before and after each jumping zone.', 'keep a 5 m "vereda" before and after each jumping zone.', 1)

rep("""    const lava = new THREE.Mesh(new THREE.PlaneGeometry(21.0,6.4,1,1),lavaMat);
    lava.rotation.x=-Math.PI/2; lava.position.set(0,-10,-3); scene.add(lava);
    const lavaGlow = new THREE.PointLight(0xff3b0a,45,22,2); lavaGlow.position.set(0,-7,-3); scene.add(lavaGlow);""",
"""    const lava = new THREE.Mesh(new THREE.PlaneGeometry(21.0,Math.abs(Z_PIT_NORTH-Z_PIT_SOUTH)+.6,1,1),lavaMat);
    lava.rotation.x=-Math.PI/2; lava.position.set(0,-10,(Z_PIT_SOUTH+Z_PIT_NORTH)/2); scene.add(lava);
    const lavaGlow = new THREE.PointLight(0xff3b0a,45,24,2); lavaGlow.position.set(0,-7,(Z_PIT_SOUTH+Z_PIT_NORTH)/2); scene.add(lavaGlow);""", 'lava dimensions')

rep("""    function addLetterRoom(cx, letters, roomIndex) {
      challengeZones.push({minX:cx-2.5,maxX:cx+2.5,minZ:-6,maxZ:0,kind:'tiles'});
      for(let r=0;r<6;r++) for(let c=0;c<5;c++){
        const x=cx-2+c, z=-5.5+r;
        const id=`r${roomIndex}-${r}-${c}`;
        const mat=new THREE.MeshStandardMaterial({map:tileTexture(letters[r][c]),roughness:.9});
        const mesh=boxMesh('tile-'+id,x,-.08,z,.98,.16,.98,mat,false,true);
        const isSafe=safe.has(`${r},${c}`);
        if(isSafe) supportRects.push({minX:x-.49,maxX:x+.49,minZ:z-.49,maxZ:z+.49,y:0,type:'safeTile',id});
        else breakTiles.push({id,mesh,minX:x-.49,maxX:x+.49,minZ:z-.49,maxZ:z+.49,broken:false,t:0,baseY:-.08});
      }
    }""",
"""    function addLetterRoom(cx, letters, roomIndex) {
      const half=TILE_SIZE/2;
      const innerW=ROOM_W-.3;
      challengeZones.push({minX:cx-innerW/2,maxX:cx+innerW/2,minZ:Z_PIT_NORTH,maxZ:Z_PIT_SOUTH,kind:'tiles'});
      for(let r=0;r<6;r++) for(let c=0;c<5;c++){
        const x=cx-innerW/2+half+c*TILE_SIZE;
        const z=Z_PIT_NORTH+half+r*TILE_SIZE;
        const id=`r${roomIndex}-${r}-${c}`;
        const mat=new THREE.MeshStandardMaterial({map:tileTexture(letters[r][c]),roughness:.9});
        const mesh=boxMesh('tile-'+id,x,-.08,z,TILE_SIZE,.16,TILE_SIZE,mat,false,true);
        const isSafe=safe.has(`${r},${c}`);
        const edge=half-.012;
        if(isSafe) supportRects.push({minX:x-edge,maxX:x+edge,minZ:z-edge,maxZ:z+edge,y:0,type:'safeTile',id});
        else breakTiles.push({id,mesh,minX:x-edge,maxX:x+edge,minZ:z-edge,maxZ:z+edge,broken:false,t:0,baseY:-.08});
      }
    }""", 'letter room grid')

rep("""    function addColumnRoom(cx) {
      challengeZones.push({minX:cx-2.5,maxX:cx+2.5,minZ:-6,maxZ:0,kind:'columns'});
      for(let r=0;r<6;r++) for(let c=0;c<5;c++){
        if(!safe.has(`${r},${c}`)) continue;
        const x=cx-2+c, z=-5.5+r;
        const h=10;
        const columnMats=[darkSideMat,darkSideMat,columnTopMat,darkSideMat,darkSideMat,darkSideMat];
        const mesh=boxMesh(`column-${r}-${c}`,x,-5,z,.98,h,.98,columnMats,false,true);
        supportRects.push({minX:x-.49,maxX:x+.49,minZ:z-.49,maxZ:z+.49,y:0,type:'column'});
      }
    }""",
"""    function addColumnRoom(cx) {
      const half=TILE_SIZE/2;
      const innerW=ROOM_W-.3;
      challengeZones.push({minX:cx-innerW/2,maxX:cx+innerW/2,minZ:Z_PIT_NORTH,maxZ:Z_PIT_SOUTH,kind:'columns'});
      for(let r=0;r<6;r++) for(let c=0;c<5;c++){
        if(!safe.has(`${r},${c}`)) continue;
        const x=cx-innerW/2+half+c*TILE_SIZE;
        const z=Z_PIT_NORTH+half+r*TILE_SIZE;
        const h=10;
        const columnMats=[darkSideMat,darkSideMat,columnTopMat,darkSideMat,darkSideMat,darkSideMat];
        const mesh=boxMesh(`column-${r}-${c}`,x,-5,z,TILE_SIZE,h,TILE_SIZE,columnMats,false,true);
        const edge=half-.012;
        supportRects.push({minX:x-edge,maxX:x+edge,minZ:z-edge,maxZ:z+edge,y:0,type:'column'});
      }
    }""", 'column room grid')

rep("""    const warm = [ [-7,4.15,7], [0,4.15,7], [7,4.15,7], [-7,4.15,-3], [0,4.15,-3], [7,4.15,-3], [-7,4.15,-12.5], [0,4.15,-12.5], [7,4.15,-12.5], [0,4.15,-20] ];""",
"""    const warm = [
      [-7,4.15,9], [0,4.15,9], [7,4.15,9],
      [-7,4.15,(Z_PIT_SOUTH+Z_PIT_NORTH)/2], [0,4.15,(Z_PIT_SOUTH+Z_PIT_NORTH)/2], [7,4.15,(Z_PIT_SOUTH+Z_PIT_NORTH)/2],
      [-7,4.15,(Z_CHALLENGE_NORTH+Z_COMMON_NORTH)/2], [0,4.15,(Z_CHALLENGE_NORTH+Z_COMMON_NORTH)/2], [7,4.15,(Z_CHALLENGE_NORTH+Z_COMMON_NORTH)/2],
      [0,4.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2]
    ];""", 'light positions')

rep("pos:new THREE.Vector3(0,.02,8.2)", "pos:new THREE.Vector3(0,.02,10.2)", 'spawn position')
rep("spawn:new THREE.Vector3(0,.02,8.2)", "spawn:new THREE.Vector3(0,.02,10.2)", 'spawn reset')

rep("""      P.vel.y=5.9;
      P.vel.x=dir.x*4.0; P.vel.z=dir.z*4.0;""",
"""      // Dos losetas quedan apenas al alcance de un salto muy bueno.
      P.vel.y=4.5;
      P.vel.x=dir.x*3.0; P.vel.z=dir.z*3.0;""", 'big jump impulse')
rep("const targetSpeed=P.bigJumpUsed?4.0:3.25;", "const targetSpeed=P.bigJumpUsed?3.0:3.25;", 'big jump air speed')

p.write_text(s, encoding='utf-8')
print('index.html patched successfully')
