from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('V1.23 · afiches y sonidos finales','V1.24 · proximidad cilíndrica de afiches',1)

old="""    function updatePosterInteraction(){
      if(posterOverlayOpen || P.dead){ posterPrompt.style.display='none'; return; }
      let best=null, bestD=Infinity;
      for(const poster of posters){
        const dx=poster.position.x-P.pos.x;
        const dy=poster.position.y-(P.pos.y+.65);
        const dz=poster.position.z-P.pos.z;
        const d=dx*dx+dy*dy+dz*dz;
        if(isPosterFrontFacing(poster) && d<bestD){bestD=d;best=poster;}
      }
      nearbyPoster=(best && bestD<2.25) ? best : null; // about 1.5 m
      posterPrompt.textContent=isMobileUI?'Pulsa aquí para ampliar':'Pulsa F para ampliar';
      posterPrompt.style.display=nearbyPoster?'block':'none';
    }
"""
new="""    function updatePosterInteraction(){
      if(posterOverlayOpen || P.dead){ posterPrompt.style.display='none'; return; }
      let best=null, bestHorizontalD=Infinity;
      const maxHorizontalD2=2.25; // 1.5 m radius in X/Z
      const maxVerticalDelta=3.0; // tall cylinder so floor-level players can reach high posters
      for(const poster of posters){
        const dx=poster.position.x-P.pos.x;
        const dy=poster.position.y-(P.pos.y+.65);
        const dz=poster.position.z-P.pos.z;
        const horizontalD2=dx*dx+dz*dz;
        if(Math.abs(dy)<=maxVerticalDelta && isPosterFrontFacing(poster) && horizontalD2<bestHorizontalD){
          bestHorizontalD=horizontalD2;
          best=poster;
        }
      }
      nearbyPoster=(best && bestHorizontalD<maxHorizontalD2) ? best : null;
      posterPrompt.textContent=isMobileUI?'Pulsa aquí para ampliar':'Pulsa F para ampliar';
      posterPrompt.style.display=nearbyPoster?'block':'none';
    }
"""
if old not in s:
    raise SystemExit('poster interaction block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched V1.24 cylindrical poster proximity')
