from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('V1.19 · splash + nombre nuevo','V1.20 · ajuste UV en superficies equivalentes',1)

anchor="""    function applyHardcodedTextureOverrides(){\n      scene.traverse(mesh=>{\n        if(!mesh?.isMesh || !mesh.geometry || !mesh.material)return;\n        const base=textureObjectBaseKey(mesh);\n        const objectCfg=SOQUETIN_TEXTURE_OVERRIDES[`${base}#object`];\n        const faceKeys=Object.keys(SOQUETIN_TEXTURE_OVERRIDES).filter(k=>k.startsWith(`${base}#face`));\n        if(!objectCfg && faceKeys.length===0)return;\n        const mats=ensurePerFaceMaterials(mesh);\n        if(objectCfg){\n          for(const mat of mats) applyTextureOverrideToMaterial(mat,objectCfg);\n        }\n        for(const key of faceKeys){\n          const idx=Number(key.split('#face')[1]);\n          const mat=mats[idx]||mats[0];\n          applyTextureOverrideToMaterial(mat,SOQUETIN_TEXTURE_OVERRIDES[key]);\n        }\n      });\n    }\n"""
replacement=anchor+"""

    // Propagate the user's hand-tuned UV settings only to genuinely similar
    // architectural surfaces. Explicit overrides always win. Gameplay meshes
    // (lava, tiles, columns) are deliberately excluded.
    function boxDims(mesh){
      const p=mesh.geometry?.parameters||{};
      return {w:Number(p.width)||0,h:Number(p.height)||0,d:Number(p.depth)||0};
    }
    function dimSimilarity(a,b){
      const rel=(x,y)=>Math.abs(x-y)/Math.max(.001,Math.max(x,y));
      return Math.max(rel(a.w,b.w),rel(a.h,b.h),rel(a.d,b.d));
    }
    function collectExplicitTextureSources(name){
      const out=[];
      scene.traverse(mesh=>{
        if(!mesh?.isMesh || mesh.name!==name)return;
        const base=textureObjectBaseKey(mesh);
        const objectCfg=SOQUETIN_TEXTURE_OVERRIDES[`${base}#object`]||null;
        const faces={};
        for(const [key,cfg] of Object.entries(SOQUETIN_TEXTURE_OVERRIDES)){
          if(key.startsWith(`${base}#face`)) faces[Number(key.split('#face')[1])]=cfg;
        }
        if(objectCfg || Object.keys(faces).length) out.push({mesh,dims:boxDims(mesh),objectCfg,faces});
      });
      return out;
    }
    function hasExplicitTextureOverride(mesh){
      const base=textureObjectBaseKey(mesh);
      return Object.keys(SOQUETIN_TEXTURE_OVERRIDES).some(k=>k.startsWith(base+'#'));
    }
    function applyInheritedTextureCfg(mesh,src){
      const mats=ensurePerFaceMaterials(mesh);
      if(src.objectCfg) for(const mat of mats) applyTextureOverrideToMaterial(mat,src.objectCfg);
      for(const [idxText,cfg] of Object.entries(src.faces)){
        const idx=Number(idxText), mat=mats[idx]||mats[0];
        applyTextureOverrideToMaterial(mat,cfg);
      }
    }
    function applySimilarArchitectureTextureOverrides(){
      const wallSources=collectExplicitTextureSources('wall');
      const floorSources=collectExplicitTextureSources('floor');
      scene.traverse(mesh=>{
        if(!mesh?.isMesh || !mesh.geometry || !mesh.material)return;
        const name=mesh.name;
        if(name!=='wall' && name!=='floor' && name!=='ceiling')return;
        if(hasExplicitTextureOverride(mesh))return;
        const dims=boxDims(mesh);
        const sources=name==='wall'?wallSources:floorSources;
        let best=null,bestScore=Infinity;
        for(const src of sources){
          const score=dimSimilarity(dims,src.dims);
          if(score<bestScore){bestScore=score;best=src;}
        }
        // Copy exact hand-tuned transformations only when dimensions are close.
        if(best && bestScore<=.16){
          applyInheritedTextureCfg(mesh,best);
          mesh.userData.textureInheritedFrom=textureObjectBaseKey(best.mesh);
          return;
        }
        // Ceilings have no hand-tuned source. Use the repeat density inferred
        // from the two corrected broad floor slabs (~0.17 repeats per metre),
        // but do not invent positional offsets or rotation.
        if(name==='ceiling'){
          const cfg={repeatU:Math.max(.1,dims.w*.17),repeatV:Math.max(.1,dims.d*.17),offsetU:0,offsetV:0,rotation:0};
          const mats=ensurePerFaceMaterials(mesh);
          for(const mat of mats) applyTextureOverrideToMaterial(mat,cfg);
          mesh.userData.textureInheritedFrom='floor-density-0.17';
        }
      });
    }
"""
if anchor not in s: raise SystemExit('texture function anchor not found')
s=s.replace(anchor,replacement,1)

s=s.replace('    applyHardcodedTextureOverrides();','    applyHardcodedTextureOverrides();\n    applySimilarArchitectureTextureOverrides();',1)

p.write_text(s,encoding='utf-8')
print('patched V1.20 texture propagation')
