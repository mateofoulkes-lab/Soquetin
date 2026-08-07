from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'Pattern not found: {label}')
    s=s.replace(old,new,1)

# Expose Three scene to the parallel texture editor (same-origin iframe only).
rep("""    document.body.prepend(renderer.domElement);

    const clock = new THREE.Clock();""",
"""    document.body.prepend(renderer.domElement);

    // Same-origin hook used only by texture-editor.html. It does not change gameplay.
    window.__SOQUETIN_EDITOR__ = { THREE, scene, camera, renderer };

    const clock = new THREE.Clock();""", 'editor hook')

# Replace symmetric final room dimensions with a room extended 2 m to the right.
rep("""    const ROOM_W=7.0;
    const FINAL_W=7.5;
    const OPEN_W=1.2;""",
"""    const ROOM_W=7.0;
    const FINAL_W=7.5;
    const FINAL_LEFT=-FINAL_W/2;
    const FINAL_RIGHT=FINAL_W/2+2.0;
    const FINAL_CENTER=(FINAL_LEFT+FINAL_RIGHT)/2;
    const FINAL_TOTAL_W=FINAL_RIGHT-FINAL_LEFT;
    const OPEN_W=1.2;""", 'final room constants')

rep("""    addFloorRect(0, (Z_COMMON_NORTH+Z_FINAL_NORTH)/2, FINAL_W-.3, Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH)-.3, 0);""",
"""    addFloorRect(FINAL_CENTER, (Z_COMMON_NORTH+Z_FINAL_NORTH)/2, FINAL_TOTAL_W-.3, Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH)-.3, 0);""", 'final floor')

rep("""    // Final corridor walls
    wallSegment(-FINAL_W/2,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,T,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH),H);
    wallSegment(FINAL_W/2,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,T,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH),H);
    wallSegment(0,Z_FINAL_NORTH,FINAL_W+T,T,H);""",
"""    // Final room: 2 m deeper toward the player's right side.
    // The doorway stays where it was, so the Instagram clue is hidden until you turn right.
    wallSegment(FINAL_LEFT,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,T,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH),H);
    wallSegment(FINAL_RIGHT,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,T,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH),H);
    wallSegment(FINAL_CENTER,Z_FINAL_NORTH,FINAL_TOTAL_W+T,T,H);""", 'final walls')

rep("""    boxMesh('ceiling',0,H+0.12,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,FINAL_W+.3,.24,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH)+.3,ceilMat,false,true);""",
"""    boxMesh('ceiling',FINAL_CENTER,H+0.12,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,FINAL_TOTAL_W+.3,.24,Math.abs(Z_FINAL_NORTH-Z_COMMON_NORTH)+.3,ceilMat,false,true);""", 'final ceiling')

rep("""    insta.position.set(FINAL_W/2-.165,2.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2); insta.rotation.y=-Math.PI/2; scene.add(insta);""",
"""    insta.position.set(FINAL_RIGHT-.165,2.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2); insta.rotation.y=-Math.PI/2; scene.add(insta);""", 'instagram position')

p.write_text(s,encoding='utf-8')
