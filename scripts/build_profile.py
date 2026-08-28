"""Build small, self-contained SVG assets for the GitHub profile.

Usage: python scripts/build_profile.py [--gif]
Requires fontTools; --gif also requires Pillow and Inkscape.
PROFILE_FONT_DIR may point to a DejaVu Sans font folder.
No remote images, scripts, tracking pixels or generated contribution statistics.
"""
from pathlib import Path
from html import escape
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT_DIR = Path(os.environ.get('PROFILE_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
FONTS = {False: TTFont(FONT_DIR / 'DejaVuSans.ttf'), True: TTFont(FONT_DIR / 'DejaVuSans-Bold.ttf')}
INK = '#263348'
MUTED = '#586579'
ORANGE = '#EE621D'

def text(s, x, y, size=20, fill=INK, bold=False, spacing=0):
    font = FONTS[bold]
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    units = font['head'].unitsPerEm
    scale = size / units
    offset = 0
    pieces = []
    for c in s:
        glyph = glyphs[cmap.get(ord(c), '.notdef')]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        d = pen.getCommands()
        if d:
            pieces.append(f'<path transform="translate({offset:.2f} 0)" d="{d}"/>')
        offset += glyph.width + spacing / scale
    return f'<g aria-label="{escape(s, quote=True)}" fill="{fill}" transform="translate({x} {y}) scale({scale:.7f} {-scale:.7f})">' + ''.join(pieces) + '</g>'

def rect(x,y,w,h,fill,stroke='none',rx=18,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'

def pill(s,x,y,w,fill='#FFF0E2',color='#A94311',size=15):
    return rect(x,y,w,32,fill,rx=16)+text(s,x+14,y+22,size,color,True)

def sparkle(x,y,size=10,color=ORANGE):
    return f'<path d="M{x} {y-size} Q{x+2} {y-2} {x+size} {y} Q{x+2} {y+2} {x} {y+size} Q{x-2} {y+2} {x-size} {y} Q{x-2} {y-2} {x} {y-size}Z" fill="{color}"/>'

def svg(name,w,h,title,desc,body):
    result=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
{body}
</svg>'''
    (OUT/name).write_text(result,encoding='utf-8')

import json
import re
import subprocess
import tempfile
from xml.etree import ElementTree as ET

LOGOS=json.loads((ROOT/'scripts/logo_sources.json').read_text())
ET.register_namespace('', 'http://www.w3.org/2000/svg')

def centered(s,x,y,size=16,color=INK,bold=True):
    font=FONTS[bold]
    glyphs=font.getGlyphSet()
    cmap=font.getBestCmap()
    width=sum(glyphs[cmap.get(ord(c),'.notdef')].width for c in s)*size/font['head'].unitsPerEm
    return text(s,round(x-width/2,2),y,size,color,bold)

def icon(name,x,y,color):
    if name in LOGOS:
        raw=LOGOS[name]
        for ident in re.findall(r'id="([^"]+)"',raw):
            raw=raw.replace('id="'+ident+'"','id="'+name+'-'+ident+'"').replace('#'+ident, '#'+name+'-'+ident)
        root=ET.fromstring(raw)
        root.set('x',str(x-25));root.set('y',str(y-25))
        root.set('width','50');root.set('height','50')
        if 'viewBox' not in root.attrib:root.set('viewBox','0 0 128 128')
        root.set('fill',color)
        return ET.tostring(root,encoding='unicode')
    shapes={
        'sql':'<ellipse cx="24" cy="10" rx="18" ry="7"/><path d="M6 10v28c0 10 36 10 36 0V10M6 23c0 10 36 10 36 0"/>',
        'recharts':'<path d="M5 5v37h40M12 34l10-13 10 4 10-16"/><circle cx="22" cy="21" r="3"/><circle cx="32" cy="25" r="3"/>',
        'alembic':'<path d="M17 3h14M20 3v16L7 41q-2 5 4 5h26q6 0 4-5L28 19V3M14 33h20"/>',
        'reportlab':'<path d="M10 2h21l9 9v34H10ZM30 2v12h10M17 22h16M17 29h16M17 36h10"/>',
        'githubpages':'<rect x="3" y="6" width="42" height="36" rx="4"/><path d="M3 16h42M20 23l-7 6 7 6m8-12 7 6-7 6"/>'}
    return f'<g transform="translate({x-24} {y-24})" fill="none" stroke="{color}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">{shapes[name]}</g>'

def banner():
    b='''<defs>
<linearGradient id="paper" x2="1" y2="1"><stop stop-color="#FFFDF9"/><stop offset=".6" stop-color="#FFF5E6"/><stop offset="1" stop-color="#FFE1BC"/></linearGradient>
<linearGradient id="type" x2="1" y2=".4"><stop stop-color="#F68B36"/><stop offset="1" stop-color="#E6531B"/></linearGradient>
<linearGradient id="ball" x2=".8" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFF2DF"/></linearGradient>
<clipPath id="outer"><rect width="1120" height="240" rx="28"/></clipPath>
</defs>
<g clip-path="url(#outer)"><rect width="1120" height="240" fill="url(#paper)"/>
<path d="M720-40L515 290M780-40L575 290" stroke="#FFF" stroke-width="24" opacity=".6"/>
<circle cx="944" cy="121" r="164" fill="none" stroke="#F5C897"/>
<circle cx="944" cy="121" r="132" fill="none" stroke="#EEB782" stroke-dasharray="2 10"/>
<path d="M54 194H510" stroke="#EDCBA7"/><path d="M54 194H170" stroke="#EE7625" stroke-width="3"/>
</g>'''
    b+=text('SSG-SAK',48,159,108,'url(#type)',True,-5)
    b+='<g transform="translate(939 120) rotate(-20)"><circle cy="7" r="90" fill="#EDC69F" opacity=".25"/><circle r="89" fill="url(#ball)" stroke="#EFCCA7" stroke-width="2"/>'
    for side in [-1,1]:
        b+=f'<path d="M{side*48} -72Q{side*2} 0 {side*48} 72" fill="none" stroke="#ED762F" stroke-width="2.5"/>'
        for j in range(-4,5):
            yy=j*14;xx=side*(24+24*(yy/72)**2)
            b+=f'<path d="M{xx-6} {yy-3}l12 6" stroke="#ED762F" stroke-width="2.5" stroke-linecap="round"/>'
    b+='</g>'+sparkle(788,123,17)+sparkle(1066,56,11)+sparkle(1079,187,8)
    b+=rect(1,1,1118,238,'none','#F2DAC0',28)
    svg('ssg-sak-banner.svg',1120,240,'SSG-SAK','SSG-SAK, orange wordmark and baseball on an ivory background.',b)

ROWS=[
 ('DATA & ANALYTICS','#D97427',[
 ('python','Python','#3776AB'),('sql','SQL','#5180C0'),('pandas','pandas','#150458'),('numpy','NumPy','#4DABCF'),
 ('geopandas','GeoPandas','#139B63'),('scikitlearn','scikit-learn','#F89939'),('jupyter','Jupyter','#F37726'),('matplotlib','Matplotlib','#297FC7')]),
 ('FRONTEND','#4488C2',[
 ('nextjs','Next.js','#222222'),('react','React','#49ADCC'),('typescript','TypeScript','#3178C6'),('tailwindcss','Tailwind CSS','#38BDF8'),
 ('tanstack','TanStack|Query','#E77833'),('reacthookform','React Hook|Form','#EC5990'),('zod','Zod','#3E67B1'),('recharts','Recharts','#25A6A0')]),
 ('BACKEND & REPORTS','#399A7F',[
 ('fastapi','FastAPI','#009688'),('pydantic','Pydantic','#E92063'),('sqlalchemy','SQLAlchemy','#D32F2F'),('postgresql','PostgreSQL','#336791'),
 ('sqlite','SQLite','#2683BE'),('alembic','Alembic','#AA693E'),('reportlab','ReportLab','#3E70B6'),('googlegemini','Gemini','#7662DE')]),
 ('TEST & DELIVERY','#9273BB',[
 ('docker','Docker|Compose','#2496ED'),('git','Git','#F05032'),('githubactions','GitHub|Actions','#2088FF'),('pytest','Pytest','#2D93A3'),
 ('vitest','Vitest','#7CB420'),('playwright','Playwright','#2EAD33'),('render','Render','#242D35'),('githubpages','GitHub|Pages','#68788C')])
]

def stack():
    b='''<defs>
<linearGradient id="paper" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".6" stop-color="#FFFDF8"/><stop offset="1" stop-color="#FFF1E0"/></linearGradient>
<linearGradient id="coin" x2=".2" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#FAFBFD"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#F7B977" stop-opacity=".23"/><stop offset="1" stop-color="#F7B977" stop-opacity="0"/></radialGradient>
</defs>'''
    b+=rect(1,1,1118,818,'url(#paper)','#F0E3D4',28)
    b+='<ellipse cx="1060" cy="70" rx="230" ry="100" fill="url(#halo)"/>'
    b+=text('TECH',38,64,38,INK,True,-1)+text('STACK',164,64,38,ORANGE,True,-1)
    b+=sparkle(1065,48,13)+sparkle(1037,66,6,'#EFAB4E')
    for ri,(label,accent,items) in enumerate(ROWS):
        top=110+ri*174
        b+=text(label,39,top+10,16,accent,True,1.2)
        b+=f'<path d="M340 {top+5}H1080" stroke="#EDE8E0"/><circle cx="1080" cy="{top+5}" r="3" fill="{accent}" opacity=".6"/>'
        for ci,(name,label,color) in enumerate(items):
            x=84+ci*136;y=top+74
            b+=f'<ellipse cx="{x}" cy="{y+42}" rx="37" ry="8" fill="#D9C9BA" opacity=".15"/>'
            b+=f'<circle cx="{x}" cy="{y}" r="45" fill="none" stroke="{accent}" opacity=".12"/><circle cx="{x}" cy="{y}" r="41" fill="url(#coin)" stroke="#E9E7E2"/>'
            b+=f'<path d="M{x-25} {y-32}Q{x} {y-45} {x+25} {y-32}" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
            b+=icon(name,x,y,color)
            labels=label.split('|')
            for li,line in enumerate(labels):
                b+=centered(line,x,y+68+li*19,15 if len(line)>11 else 16,INK,True)
    b+=f'<path d="M38 799H1082" stroke="#F0E5D8"/>'
    svg('tech-stack.svg',1120,820,'SSG-SAK Tech Stack','; '.join(name.replace('|',' ') for _,_,items in ROWS for _,name,_ in items),b)

def gif():
    from PIL import Image,ImageDraw,ImageFilter
    with tempfile.TemporaryDirectory() as td:
        png=Path(td)/'stack.png'
        subprocess.run(['inkscape',str(OUT/'tech-stack.svg'),'--export-type=png',f'--export-filename={png}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        base=Image.open(png).convert('RGBA')
        palette=base.convert('RGB').quantize(colors=128)
        frames=[]
        for frame in range(48):
            overlay=Image.new('RGBA',base.size,(0,0,0,0));d=ImageDraw.Draw(overlay)
            for row in range(4):
                phase=(frame/48-row*.18)%1
                head=350+int(phase*710);y=115+row*174
                for tail in range(100):
                    x=head-tail
                    if x<342:continue
                    d.line((x,y,x,y),fill=(245,156,63,int((1-tail/100)*200)),width=2)
                d.ellipse((head-2,y-2,head+2,y+2),fill=(255,201,126,240))
            glow=overlay.filter(ImageFilter.GaussianBlur(4))
            out=Image.alpha_composite(Image.alpha_composite(base,glow),overlay).convert('RGB')
            frames.append(out.quantize(palette=palette,dither=Image.Dither.NONE))
        frames[0].save(OUT/'tech-stack.gif',save_all=True,append_images=frames[1:],duration=110,loop=0,disposal=1,optimize=True)
        assert (OUT/'tech-stack.gif').stat().st_size<1_000_000
        print('GIF:',(OUT/'tech-stack.gif').stat().st_size,'bytes /',len(frames),'frames')

banner()
stack()
if '--gif' in sys.argv:gif()
for name in ['ssg-sak-banner.svg','tech-stack.svg']:
    p=OUT/name
    print(name,p.stat().st_size,'bytes')
