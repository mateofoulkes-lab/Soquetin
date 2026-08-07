from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

marker="""    const columnTopMat = new THREE.MeshStandardMaterial({map:texFloor,color:0xeadfbd,roughness:.82,emissive:0x2b2110,emissiveIntensity:.18});
"""

block=r'''    const columnTopMat = new THREE.MeshStandardMaterial({map:texFloor,color:0xeadfbd,roughness:.82,emissive:0x2b2110,emissiveIntensity:.18});

    // ------------------------------------------------------------
    // HARDCODED TEXTURE OVERRIDES — PART 1
    // Exported from texture-editor.html. Object settings are applied first;
    // face settings then override the matching face when both exist.
    // ------------------------------------------------------------
    const SOQUETIN_TEXTURE_OVERRIDES = {
      "wall@0,2.5,13#face0":{"scope":"face","repeatU":18.65,"repeatV":17.55,"offsetU":3.36,"offsetV":3.18,"rotation":95},
      "floor@0,-0.12,9#face2":{"scope":"face","repeatU":2.5,"repeatV":1.1,"offsetU":0,"offsetV":0,"rotation":0},
      "floor@0,-0.12,9#face0":{"scope":"face","repeatU":9.3,"repeatV":22.65,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
      "wall@0,2.5,13#face5":{"scope":"face","repeatU":7.05,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-10.5,2.5,-3.52#face0":{"scope":"face","repeatU":12.7,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-9.05,2.5,5#object":{"scope":"object","repeatU":1.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-9.05,2.5,5#face0":{"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-1.75,"offsetV":0,"rotation":0},
      "lintel@-7,3.7,5#face4":{"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":0,"offsetV":-0.42,"rotation":0},
      "wall@-3.5,2.5,5#face0":{"scope":"face","repeatU":2,"repeatV":3.1,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-3.5,2.5,5#object":{"scope":"object","repeatU":1.95,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
      "lintel@-7,3.7,5#face5":{"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":0.01,"offsetV":0.08,"rotation":0},
      "floor@-7,-0.12,2.5#face2":{"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-0.81,"offsetV":0,"rotation":0},
      "floor@-7,-0.12,5#face2":{"scope":"face","repeatU":3.95,"repeatV":17.25,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@10.5,2.5,-3.52#object":{"scope":"object","repeatU":9.3,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@9.05,2.5,5#object":{"scope":"object","repeatU":0.8,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "lintel@7,3.7,5#object":{"scope":"object","repeatU":0.45,"repeatV":2.65,"offsetU":0.03,"offsetV":-0.03,"rotation":0},
      "wall@3.5,2.5,5#object":{"scope":"object","repeatU":2,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
      "lintel@0,3.7,5#object":{"scope":"object","repeatU":0.4,"repeatV":2.6,"offsetU":0.03,"offsetV":0.08,"rotation":0},
      "wall@3.5,2.5,-4.02#object":{"scope":"object","repeatU":5.35,"repeatV":5.05,"offsetU":0.71,"offsetV":0,"rotation":0},
      "floor@0,-0.12,9#object":{"scope":"object","repeatU":3.65,"repeatV":1.4,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
      "floor@0,-0.12,2.5#object":{"scope":"object","repeatU":1.1,"repeatV":0.8,"offsetU":-1.31,"offsetV":0.07,"rotation":0},
      "wall@-3.5,2.5,-4.02#object":{"scope":"object","repeatU":5.35,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0}
    };

    function textureCoord(v){ return Number(Number(v).toFixed(2)); }
    function textureObjectBaseKey(mesh){
      const p=mesh.position;
      return `${mesh.name||'mesh'}@${textureCoord(p.x)},${textureCoord(p.y)},${textureCoord(p.z)}`;
    }
    function ensurePerFaceMaterials(mesh){
      const groups=mesh.geometry?.groups||[];
      const maxIndex=Math.max(0,...groups.map(g=>g.materialIndex||0));
      if(!Array.isArray(mesh.material) && maxIndex>0){
        const base=mesh.material;
        mesh.material=Array.from({length:maxIndex+1},()=>base.clone());
      } else if(!Array.isArray(mesh.material)) {
        mesh.material=mesh.material.clone();
      }
      return Array.isArray(mesh.material)?mesh.material:[mesh.material];
    }
    function applyTextureOverrideToMaterial(mat,cfg){
      if(!mat?.map)return;
      if(!mat.userData._hardcodedTextureClone){
        mat.map=mat.map.clone();
        mat.userData._hardcodedTextureClone=true;
      }
      const tex=mat.map;
      tex.wrapS=tex.wrapT=THREE.RepeatWrapping;
      tex.repeat.set(cfg.repeatU,cfg.repeatV);
      tex.offset.set(cfg.offsetU,cfg.offsetV);
      tex.center.set(.5,.5);
      tex.rotation=cfg.rotation*Math.PI/180;
      tex.needsUpdate=true;
    }
    function applyHardcodedTextureOverrides(){
      scene.traverse(mesh=>{
        if(!mesh?.isMesh || !mesh.geometry || !mesh.material)return;
        const base=textureObjectBaseKey(mesh);
        const objectCfg=SOQUETIN_TEXTURE_OVERRIDES[`${base}#object`];
        const faceKeys=Object.keys(SOQUETIN_TEXTURE_OVERRIDES).filter(k=>k.startsWith(`${base}#face`));
        if(!objectCfg && faceKeys.length===0)return;
        const mats=ensurePerFaceMaterials(mesh);
        if(objectCfg){
          for(const mat of mats) applyTextureOverrideToMaterial(mat,objectCfg);
        }
        for(const key of faceKeys){
          const idx=Number(key.split('#face')[1]);
          const mat=mats[idx]||mats[0];
          applyTextureOverrideToMaterial(mat,SOQUETIN_TEXTURE_OVERRIDES[key]);
        }
      });
    }
'''

if 'HARDCODED TEXTURE OVERRIDES — PART 1' not in s:
    if marker not in s:
        raise SystemExit('material marker not found')
    s=s.replace(marker,block,1)

call_marker="""    // ------------------------------------------------------------
    // PLAYER
    // ------------------------------------------------------------
"""
call_block="""    // Apply exported UV/repeat settings after all dungeon geometry is built.
    applyHardcodedTextureOverrides();

    // ------------------------------------------------------------
    // PLAYER
    // ------------------------------------------------------------
"""
if 'applyHardcodedTextureOverrides();' not in s:
    if call_marker not in s:
        raise SystemExit('player marker not found')
    s=s.replace(call_marker,call_block,1)

p.write_text(s,encoding='utf-8')
