from pathlib import Path
import re

idxp=Path('index.html')
edp=Path('texture-editor.html')
idx=idxp.read_text(encoding='utf-8')
ed=edp.read_text(encoding='utf-8')

# 1) Make current game texture mix the new A baseline in texture editor.
m=re.search(r'    const SOQUETIN_TEXTURE_OVERRIDES = (\{.*?\n    \});', idx, re.S)
if not m:
    raise SystemExit('current game texture table not found')
current_table=m.group(1)
ed2,n=re.subn(r'const TEXTURE_TABLE_A = \{.*?\n    \};', 'const TEXTURE_TABLE_A = '+current_table, ed, count=1, flags=re.S)
if n!=1:
    raise SystemExit(f'TEXTURE_TABLE_A replacement count={n}')
ed=ed2
# Reset mixer once so localStorage starts from the new current baseline.
ed=ed.replace("const AB_MIX_VERSION='2';", "const AB_MIX_VERSION='3';", 1)

# 2) Jump rocking only when the jump was launched with directional input.
old="""      animPhase:'idle', animTime:0, animLaunchVy:2.35, tiltDeg:0, tiltPivotY:0, animStartTilt:0, animStartPivot:0,
      spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false"""
new="""      animPhase:'idle', animTime:0, animLaunchVy:2.35, tiltDeg:0, tiltPivotY:0, animStartTilt:0, animStartPivot:0, jumpTiltActive:false,
      spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false"""
if old not in idx:
    raise SystemExit('P animation state anchor not found')
idx=idx.replace(old,new,1)

old="""    function beginJumpTilt(launchVy){
      P.animPhase='takeoff';
      P.animTime=0;
      P.animLaunchVy=Math.max(.1,launchVy);
      P.animStartTilt=P.tiltDeg;
      P.animStartPivot=P.tiltPivotY;
    }
    function beginLandingTilt(){
      P.animPhase='land';
      P.animTime=0;
      P.animStartTilt=P.tiltDeg;
      P.animStartPivot=P.tiltPivotY;
    }"""
new="""    function beginJumpTilt(launchVy){
      P.jumpTiltActive=true;
      P.animPhase='takeoff';
      P.animTime=0;
      P.animLaunchVy=Math.max(.1,launchVy);
      P.animStartTilt=P.tiltDeg;
      P.animStartPivot=P.tiltPivotY;
    }
    function beginLandingTilt(){
      if(!P.jumpTiltActive){
        P.animPhase='idle';
        applyCharacterTilt(0,0);
        return;
      }
      P.animPhase='land';
      P.animTime=0;
      P.animStartTilt=P.tiltDeg;
      P.animStartPivot=P.tiltPivotY;
    }"""
if old not in idx:
    raise SystemExit('jump tilt functions anchor not found')
idx=idx.replace(old,new,1)

old="""        if(P.animTime>=.16){ P.animPhase='idle'; applyCharacterTilt(0,0); }"""
new="""        if(P.animTime>=.16){ P.animPhase='idle'; P.jumpTiltActive=false; applyCharacterTilt(0,0); }"""
if old not in idx:
    raise SystemExit('settle anchor not found')
idx=idx.replace(old,new,1)

old="""      const dir=inputVector();
      if(dir.lengthSq()<.01) dir.set(-Math.sin(P.camYaw),0,-Math.cos(P.camYaw));
      dir.normalize();
      // Dos losetas quedan apenas al alcance de un salto muy bueno.
      P.vel.y=4.433;
      P.vel.x=dir.x*3.0; P.vel.z=dir.z*3.0;
      P.grounded=false; P.bigJumpUsed=true; P.squash=1;
      beginJumpTilt(4.433);
      playSfx('jump',.82);"""
new="""      const dir=inputVector();
      const jumpHasDirection=dir.lengthSq()>=.01;
      if(!jumpHasDirection) dir.set(-Math.sin(P.camYaw),0,-Math.cos(P.camYaw));
      dir.normalize();
      // Dos losetas quedan apenas al alcance de un salto muy bueno.
      P.vel.y=4.433;
      P.vel.x=dir.x*3.0; P.vel.z=dir.z*3.0;
      P.grounded=false; P.bigJumpUsed=true; P.squash=1;
      if(jumpHasDirection){
        beginJumpTilt(4.433);
      }else{
        P.jumpTiltActive=false;
        P.animPhase='idle';
        applyCharacterTilt(0,0);
      }
      playSfx('jump',.82);"""
if old not in idx:
    raise SystemExit('tryBigJump anchor not found')
idx=idx.replace(old,new,1)

idxp.write_text(idx,encoding='utf-8')
edp.write_text(ed,encoding='utf-8')
print('updated texture editor A baseline and disabled rocking for stationary big jumps')
