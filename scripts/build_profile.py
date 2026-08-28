"""Build small, self-contained SVG assets for the GitHub profile.

Usage: python scripts/build_profile.py
Requires fontTools. PROFILE_FONT_DIR may point to a DejaVu Sans font folder.
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

def banner():
    b='''<style>
.orbit { transform-origin:925px 191px; animation:orbit 28s linear infinite; }
.twinkle { animation:twinkle 4s ease-in-out infinite; }
.glint { animation:glint 9s linear infinite; }
@keyframes orbit { to { transform:rotate(360deg); } }
@keyframes twinkle { 0%,100% { opacity:.3; } 50% { opacity:1; } }
@keyframes glint { 0% { transform:translateX(0); } 65%,100% { transform:translateX(1520px); } }
@media (prefers-reduced-motion:reduce) { .orbit,.twinkle,.glint { animation:none; } .glint { display:none; } }
</style><defs>
<linearGradient id="paper" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".6" stop-color="#FFF9F1"/><stop offset="1" stop-color="#FFE5C7"/></linearGradient>
<linearGradient id="orange" x2="1" y2="1"><stop stop-color="#F88732"/><stop offset="1" stop-color="#E75118"/></linearGradient>
<linearGradient id="ball" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFF1DF"/></linearGradient>
<linearGradient id="glint"><stop stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#DCA97C" opacity=".24"/></pattern>
<clipPath id="clip"><rect x="1" y="1" width="1118" height="398" rx="26"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="1120" height="400" fill="url(#paper)"/>
<rect x="610" width="510" height="400" fill="url(#dots)"/>
<path d="M694 -30L508 430H574L760 -30Z" fill="#FFFFFF" opacity=".5"/>
<circle cx="935" cy="207" r="188" fill="none" stroke="#F5D8BA"/>
<circle cx="935" cy="207" r="157" fill="none" stroke="#F4C69E" stroke-dasharray="3 10"/>
<path d="M770 283Q865 376 1045 286" fill="none" stroke="#F8B878" stroke-width="2"/>
</g>'''
    b+=rect(1,1,1118,398,'none','#F0DCC7',26)
    b+=pill('DATA ANALYTICS  /  BUILDER',44,34,300)
    b+=text('SSG-SAK',40,173,92,INK,True,spacing=-4)
    b+=text('DATA. SYSTEMS.',44,231,37,ORANGE,True,-.7)
    b+=text('DECISIONS.',44,278,37,ORANGE,True,-.7)
    b+=text('From a clear question to a working product.',46,318,19,MUTED)
    b+='<path d="M46 350H588" stroke="#EEDAC5"/><path d="M46 350H169" stroke="#F27629" stroke-width="3"/>'
    b+=text('PYTHON  /  SQL  /  DATA QUALITY  /  WEB',46,378,14,MUTED,True,1)
    # Baseball identity from the original profile, redrawn on warm white.
    b+='<g transform="translate(925 191) rotate(-18)">'
    b+='<ellipse cy="116" rx="96" ry="13" fill="#DEB995" opacity=".2"/>'
    b+='<circle r="112" fill="url(#ball)" stroke="#F1CBA9" stroke-width="2"/>'
    b+='<circle cx="-22" cy="-26" r="77" fill="#FFFFFF" opacity=".5"/>'
    for sign in [-1,1]:
        x=sign*61
        b+=f'<path d="M{x} -88Q{sign*4} 0 {x} 88" fill="none" stroke="#EA6A2B" stroke-width="3"/>'
        for j in range(-4,5):
            yy=j*18
            xx=sign*(32.5+28.5*(yy/88)**2)
            b+=f'<path d="M{xx-7} {yy-4}l14 8" stroke="#ED7131" stroke-width="3" stroke-linecap="round"/>'
    b+='</g>'
    b+=rect(735,52,126,46,'#FFFFFF','#F1D8BF',12)+text('SQL',769,82,22,INK,True)
    b+=rect(969,275,116,46,'#FFFFFF','#F1D8BF',12)+text('API',1000,305,22,INK,True)
    b+=pill('SF GIANTS + HANWHA EAGLES',760,347,310,'#FFFFFF',MUTED,13)
    b+=sparkle(735,213,14)+sparkle(1054,66,12)+sparkle(1080,228,7,'#F4AC50')
    b+='<g class="orbit"><circle cx="806" cy="91" r="4" fill="#F47A2D"/></g>'
    b+='<g class="twinkle" opacity=".7">'+sparkle(1064,137,7)+'</g>'
    b+='<g clip-path="url(#clip)"><rect class="glint" x="-220" y="0" width="150" height="400" fill="url(#glint)" opacity=".26"/></g>'
    svg('ssg-sak-banner.svg',1120,400,'SSG-SAK — Data, Systems, Decisions','Bright ivory and orange profile banner. Data analytics, data quality and full-stack projects. San Francisco Giants and Hanwha Eagles fan.',b)

def card(name,num,title,kind,lines,highlight,stack,accent,light,icon):
    b=rect(1,1,538,274,'#FFFFFF','#E5E8EB',22)
    b+=rect(1,1,538,66,light,rx=22)+rect(1,40,538,27,light,rx=0)
    b+=text(num,23,42,19,accent,True)+text(kind,66,41,14,accent,True,1)
    b+=text(title,24,108,29,INK,True,-.7)
    for i,line in enumerate(lines): b+=text(line,25,148+i*28,19,MUTED)
    b+=pill(highlight,24,195,460,light,accent,14)
    b+=text(stack,25,253,14,MUTED)
    b+=f'<g transform="translate(480 20)" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
    svg(name,540,276,title,kind+'. '+' '.join(lines)+'. '+highlight+'. '+stack,b)

def stack():
    b=rect(1,1,1118,688,'#FFFCF8','#F0DDC9',24)
    b+=text('THE TOOLKIT',30,55,30,INK,True,-.6)+text('Used in projects. Organized by purpose.',32,84,17,MUTED)
    b+=pill('2026.08',955,29,126,'#FFF0E2',ORANGE,16)
    panels=[
        (26,111,'01','DATA & ANALYTICS','#EA6A25','#FFF0E3',
         [('Python','SQL','pandas'),('NumPy','GeoPandas','scikit-learn'),('Jupyter','Matplotlib','seaborn')]),
        (575,111,'02','FRONTEND','#3376BD','#ECF5FF',
         [('Next.js','React','TypeScript'),('Tailwind','TanStack Query','Recharts'),('React Hook Form','Zod','Zustand')]),
        (26,365,'03','BACKEND & DATABASE','#188573','#EBF8F4',
         [('FastAPI','Pydantic','SQLAlchemy'),('PostgreSQL','SQLite','Alembic'),('ReportLab','Gemini API','httpx')]),
        (575,365,'04','TEST & DELIVERY','#8A5BB1','#F5EFFB',
         [('Pytest','Vitest','Playwright'),('Git','GitHub Actions','Docker Compose'),('Render','GitHub Pages','CI')])
    ]
    for x,y,num,label,color,light,rows in panels:
        b+=rect(x,y,519,232,'#FFFFFF','#E8E4DE',18)
        b+=rect(x+1,y+1,517,52,light,rx=17)+rect(x+1,y+35,517,19,light,rx=0)
        b+=text(num,x+18,y+34,17,color,True)+text(label,x+58,y+34,18,color,True)
        b+=f'<circle cx="{x+491}" cy="{y+27}" r="4" fill="{color}"/>'
        for ri,row in enumerate(rows):
            for ci,label in enumerate(row):
                xx=x+17+ci*165; yy=y+71+ri*48
                b+=rect(xx,yy,155,37,'#FBFCFD','#E9ECF0',9)
                size=14 if len(label)>12 else 16
                b+=text(label,xx+10,yy+25,size,INK,True)
    b+=text('DEEPENING NEXT',33,646,15,ORANGE,True,1)
    b+=text('Advanced SQL  /  Power BI  /  Statistical analysis',225,646,18,MUTED)
    b+=text('Technology names indicate project use, not equal proficiency in every tool.',33,675,14,MUTED)
    svg('tech-stack.svg',1120,690,'SSG-SAK — Project Toolkit','Project-used technologies across data analytics, frontend, backend and databases, testing and delivery. Learning focus: advanced SQL, Power BI and statistical analysis. Tool use does not imply equal proficiency.',b)

def footer():
    b=rect(1,1,1118,100,'#FFF7EC','#F1DFC9',20)
    b+=text('DEFINE IT. CHECK IT. SHIP IT.',28,47,25,INK,True)
    b+=text('Clear metrics. Traceable data. Working products.',29,77,17,MUTED)
    b+=sparkle(1060,48,16)+sparkle(1025,69,7,'#EFAB4E')
    svg('profile-footer.svg',1120,102,'Define it. Check it. Ship it.','Clear metrics. Traceable data. Working products.',b)

banner()
card('project-factoryhr.svg','01','FactoryHR Lite','NEW / FULL-STACK',
     ['HR operations, data validation,','KPI dashboards and PDF / CSV reports.'],
     'PERSONAL PROJECT  /  SYNTHETIC DEMO DATA',
     'Next.js  /  FastAPI  /  PostgreSQL','#C85219','#FFF0E3',
     '<rect width="29" height="28" rx="4"/><path d="M7 20V14m7 6V8m7 12V11"/>')
card('project-golden.svg','02','Daegu Golden Time','PUBLIC DATA / GIS',
     ['Emergency-care access and','policy scenario analysis in Daegu.'],
     '150 DISTRICTS  /  POLICY SIMULATION',
     'Python  /  GeoPandas  /  React','#AA711B','#FFF6DE',
     '<path d="M14 29S3 18 3 10a11 11 0 0 1 22 0c0 8-11 19-11 19Z"/><circle cx="14" cy="10" r="4"/>')
card('project-ev.svg','03','EV SafeCharge','TEAM / DATA ROLE 01',
     ['Data quality, time-aware processing,','features and model-ready datasets.'],
     'MY ROLE: DATA  /  SCORING & UI: TEAM',
     'Python  /  pandas  /  Parquet  /  Pytest','#197C70','#EAF8F3',
     '<path d="M17 0L3 17h10l-2 13 17-19H17Z"/>')
card('project-lab.svg','04','Golden Data Lab','IN PROGRESS / ANALYTICS',
     ['Retail customer and revenue analysis.','From SQL extraction to reproducibility.'],
     'CASE 01 IN PROGRESS  /  CASE 02 PLANNED',
     'PostgreSQL  /  Python  /  Jupyter','#496BBC','#EEF3FF',
     '<path d="M9 0h12m-9 0v10L2 27q-1 3 3 3h22q4 0 2-3L18 10V0M8 20h16"/>')
stack()
footer()
if '--gif' in sys.argv:
    import subprocess
    import tempfile
    from PIL import Image, ImageDraw, ImageFilter
    with tempfile.TemporaryDirectory() as td:
        png=Path(td)/'stack.png'
        subprocess.run(['inkscape',str(OUT/'tech-stack.svg'),'--export-type=png',f'--export-filename={png}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        base=Image.open(png).convert('RGBA')
        frames=[]
        anchors=[(26,111),(575,111),(26,365),(575,365)]
        palette=base.convert('RGB').quantize(colors=96)
        for frame in range(60):
            overlay=Image.new('RGBA',base.size,(0,0,0,0))
            draw=ImageDraw.Draw(overlay)
            for j,(x,y) in enumerate(anchors):
                phase=(frame/60-j/4)%1
                if phase<.62:
                    head=x+22+int(phase/.62*473)
                    for tail in range(65):
                        xx=head-tail
                        if xx<x+20: continue
                        alpha=int((1-tail/65)*200)
                        draw.line((xx,y+2,xx,y+2),fill=(255,143,48,alpha),width=3)
                    draw.ellipse((head-2,y,head+2,y+4),fill=(255,210,141,230))
            glow=overlay.filter(ImageFilter.GaussianBlur(4))
            rgb=Image.alpha_composite(Image.alpha_composite(base,glow),overlay).convert('RGB')
            frames.append(rgb.quantize(palette=palette,dither=Image.Dither.NONE))
        frames[0].save(OUT/'tech-stack.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=1)
        assert (OUT/'tech-stack.gif').stat().st_size<1_000_000
        print(f'tech-stack.gif: {(OUT/"tech-stack.gif").stat().st_size:,} bytes; 60 frames')
for p in sorted(OUT.glob('*.svg')):
    print(f'{p.name}: {p.stat().st_size:,} bytes')
