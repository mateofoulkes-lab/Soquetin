from pathlib import Path
p=Path('texture-editor.html')
s=p.read_text(encoding='utf-8')

old="const saved=JSON.parse(localStorage.getItem('soquetinTextureOverrides')||'{}');"
new="let saved={};"
if old not in s: raise SystemExit('saved declaration not found')
s=s.replace(old,new,1)

anchor="let hovered=null, lastAB='';\n"
insert="""let hovered=null, lastAB='';

// A/B export starts from the known-good stable table. Versioned migration avoids
// carrying the previous experimental B-only localStorage into the new mixer.
const AB_MIX_VERSION='2';
if(localStorage.getItem('soquetinABMixVersion')!==AB_MIX_VERSION){
  saved=JSON.parse(JSON.stringify(TEXTURE_TABLE_A));
  localStorage.setItem('soquetinABMixVersion',AB_MIX_VERSION);
  localStorage.setItem('soquetinTextureOverrides',JSON.stringify(saved));
}else{
  try{saved=JSON.parse(localStorage.getItem('soquetinTextureOverrides')||'{}')}catch(e){saved={}}
  if(!Object.keys(saved).length) saved=JSON.parse(JSON.stringify(TEXTURE_TABLE_A));
}
"""
if anchor not in s: raise SystemExit('AB anchor not found')
s=s.replace(anchor,insert,1)

old_apply="""function applyAB(table,label){
  if(!hovered)return;
  const state=tableStateFor(hovered,table);
  if(!state.objectCfg && !state.faceCfg){lastAB=`${label}: sin entrada para esta superficie`;refreshABStatus();return;}
  const mats=prepareMeshMaterials(hovered.mesh);
  if(state.objectCfg) for(const mat of mats) cfgApply(mat,state.objectCfg);
  if(state.faceCfg) cfgApply(mats[hovered.face]||mats[0],state.faceCfg);
  selected=hovered;
  lastAB=`${label} aplicada${state.objectCfg?' · objeto':''}${state.faceCfg?' · cara '+hovered.face:''}`;
  loadSelected(); refreshABStatus();
}"""
new_apply="""function applyAB(table,label){
  if(!hovered)return;
  const state=tableStateFor(hovered,table);
  const base=objectKey(hovered.mesh).replace(/#object$/,'');
  const objectK=base+'#object', faceK=base+'#face'+hovered.face;
  const stable=tableStateFor(hovered,TEXTURE_TABLE_A);

  // If the chosen table has no explicit entry, A means restore/remove any B-only
  // override for this target; B simply reports that there is nothing to apply.
  if(!state.objectCfg && !state.faceCfg){
    if(table===TEXTURE_TABLE_A){
      if(!stable.objectCfg) delete saved[objectK];
      if(!stable.faceCfg) delete saved[faceK];
      updateOutput();
      lastAB=`${label}: restaurada a base estable`;
    }else lastAB=`${label}: sin entrada para esta superficie`;
    refreshABStatus();return;
  }

  const mats=prepareMeshMaterials(hovered.mesh);
  if(state.objectCfg){
    for(const mat of mats) cfgApply(mat,state.objectCfg);
    saved[objectK]=JSON.parse(JSON.stringify(state.objectCfg));
  }else if(table===TEXTURE_TABLE_A && !stable.objectCfg){
    delete saved[objectK];
  }
  if(state.faceCfg){
    cfgApply(mats[hovered.face]||mats[0],state.faceCfg);
    saved[faceK]=JSON.parse(JSON.stringify(state.faceCfg));
  }else if(table===TEXTURE_TABLE_A && !stable.faceCfg){
    delete saved[faceK];
  }

  selected=hovered;
  updateOutput();
  lastAB=`${label} aplicada y GUARDADA${state.objectCfg?' · objeto':''}${state.faceCfg?' · cara '+hovered.face:''}`;
  loadSelected(); refreshABStatus();
}"""
if old_apply not in s: raise SystemExit('applyAB block not found')
s=s.replace(old_apply,new_apply,1)

s=s.replace('<button id="reset" class="secondary">Restaurar selección</button>', '<button id="reset" class="secondary">Restaurar selección</button>\n    <button id="resetMix" class="secondary">REINICIAR MEZCLA DESDE A ESTABLE</button>',1)

anchor2="$('copy').onclick=async()=>{"
reset_code="""$('resetMix').onclick=()=>{
  saved=JSON.parse(JSON.stringify(TEXTURE_TABLE_A));
  localStorage.setItem('soquetinTextureOverrides',JSON.stringify(saved));
  updateOutput();
  lastAB='mezcla reiniciada desde A estable';
  refreshABStatus();
};
"""
if anchor2 not in s: raise SystemExit('copy anchor not found')
s=s.replace(anchor2,reset_code+anchor2,1)

p.write_text(s,encoding='utf-8')
print('A/B selections now persist into exported mixed table')
