"""Build small, self-contained SVG assets for the GitHub profile.

Usage: python scripts/build_profile.py
Requires fontTools. The README uses static SVGs at every motion preference.
The previous GIF remains an unused legacy asset.
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

CORE = [
    ('python', 'Python', '#3776AB'),
    ('sql', 'SQL', '#5180C0'),
    ('pandas', 'pandas', '#150458'),
    ('postgresql', 'PostgreSQL', '#336791'),
]
SUPPORT = [
    ('ANALYTICS', '#A94311', ['NumPy · GeoPandas', 'scikit-learn · Matplotlib']),
    ('BACKEND / DB', '#28745F', ['FastAPI · SQLAlchemy', 'Pydantic · Alembic']),
    ('WEB / DELIVERY', '#745A91', ['React · TypeScript', 'Docker · GitHub Actions']),
]


def paper(width, height):
    return '''<defs>
<linearGradient id="paper" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".6" stop-color="#FFFDF8"/><stop offset="1" stop-color="#FFF1E0"/></linearGradient>
<linearGradient id="coin" x2=".2" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#FAFBFD"/></linearGradient>
</defs>''' + rect(1, 1, width-2, height-2, 'url(#paper)', '#F0E3D4', 28)


def core_tool(item, x, y, width):
    name, label, color = item
    b = rect(x, y, width, 78, '#FFF7EB', '#F2D8B9', 18)
    b += f'<circle cx="{x+39}" cy="{y+39}" r="29" fill="url(#coin)" stroke="#EDDCC7"/>'
    # Keep the original self-contained technology logos and coin motif.
    b += f'<g transform="translate({x+39} {y+39}) scale(.74)">' + icon(name, 0, 0, color) + '</g>'
    size = 25 if label != 'PostgreSQL' else (21 if width < 240 else 23)
    b += text(label, x+79, y+48, size, INK, True)
    return b


def stack(mobile=False):
    w, h = (520, 624) if mobile else (1120, 380)
    b = paper(w, h)
    b += text('TECH', 32, 49, 30, INK, True, -.6)
    b += text('STACK', 132, 49, 30, ORANGE, True, -.6)
    b += sparkle(w-42, 39, 10)
    b += text('CORE', 34, 87, 17, '#A94311', True, 1)
    for i, item in enumerate(CORE):
        x = 28 + (i % 2)*238 if mobile else 32 + i*266
        y = 104 + (i // 2)*91 if mobile else 108
        b += core_tool(item, x, y, 226 if mobile else 250)
    if mobile:
        for i, (label, accent, lines) in enumerate(SUPPORT):
            y = 310 + i*106
            b += f'<path d="M32 {y-20}H488" stroke="#EEE2D4"/>'
            b += text(label, 34, y+4, 17, accent, True, .5)
            for j, line in enumerate(lines):
                b += text(line, 34, y+35+j*29, 23, INK)
    else:
        for i, (label, accent, lines) in enumerate(SUPPORT):
            y = 240 + i*53
            b += f'<path d="M32 {y-28}H1088" stroke="#EEE2D4"/>'
            b += text(label, 34, y, 17, accent, True, .6)
            b += text(' · '.join(lines), 284, y, 23, INK)
    description = 'Core: Python, SQL, pandas, PostgreSQL. ' + '; '.join(
        label + ': ' + ' · '.join(lines) for label, _, lines in SUPPORT
    ) + '. Static artwork; no animation.'
    svg('tech-stack-mobile.svg' if mobile else 'tech-stack.svg', w, h,
        'SSG-SAK — Core, Analytics, Backend and Delivery', description, b)


def label_text(s, x, y, size, fill=INK, bold=False, spacing=0):
    # Native text preserves Korean accessibility and uses the reader's CJK font.
    family = "Arial, 'Noto Sans CJK KR', 'Noto Sans KR', 'Malgun Gothic', sans-serif"
    weight = 700 if bold else 400
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{spacing}" fill="{fill}">'
            f'{escape(s)}</text>')


PROJECTS = [
    ('golden-time', 'GOLDEN TIME', 'PERSONAL · GIS / WEB SERVICE',
     ['대구 150개 행정동 의료 접근성 분석', 'GIS 정책 비교와 탐색 서비스 구현'],
     'Python · GeoPandas · FastAPI',
     '<path d="M56 38v36M38 56h36" stroke="#EE6B22" stroke-width="6" stroke-linecap="round"/>'),
    ('ev-safecharge', 'EV SAFECHARGE', 'TEAM · MY ROLE: DATA / PIPELINE',
     ['충전 데이터 정의·품질·전처리 담당', '가용률·피처·라벨 기준 설계'],
     'Python · pandas · EDA',
     '<path d="M60 34L44 59h14l-6 19 20-29H58z" fill="#EE6B22"/>'),
    ('golden-data-lab', 'GOLDEN DATA LAB', 'PERSONAL · REPRODUCIBLE ANALYTICS',
     ['소매 매출·청년 인구이동 분석 2건', 'SQL 추출부터 통계·KPI·대시보드까지'],
     'SQL · PostgreSQL · Python',
     '<path d="M39 70V54h8v16zm15 0V44h8v26zm15 0V35h8v35z" fill="#EE6B22"/>'),
    ('factoryhr', 'FACTORYHR LITE', 'PERSONAL · FULL-STACK / HR',
     ['직원·근태 관리 DB·API·화면 구현', 'DB 무결성 검증과 역할별 권한 분리'],
     'PostgreSQL · FastAPI · Next.js',
     '<path d="M38 72V49l12 7V45l12 7V38h13v34z" fill="none" stroke="#EE6B22" stroke-width="4" stroke-linejoin="round"/>'),
]


def project_cards():
    for key, title, kind, lines, technologies, symbol in PROJECTS:
        b = '''<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#FFFDF9"/><stop offset="1" stop-color="#FFF0DC"/></linearGradient></defs>'''
        b += rect(1, 5, 538, 210, 'url(#bg)', '#F0D3B5', 22)
        b += '<circle cx="56" cy="56" r="30" fill="#FFF7ED" stroke="#F5B77A"/>' + symbol
        b += label_text(title, 103, 49, 26, '#C24915', True)
        b += label_text(kind, 103, 76, 14.5, '#795E4B', True, .4)
        b += '<path d="M489 48l10 8-10 8" fill="none" stroke="#D65C1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        b += '<path d="M30 99H510" stroke="#EED8C1"/>'
        for j, line in enumerate(lines):
            b += label_text(line, 30, 133+j*30, 22)
        b += label_text(technologies, 30, 194, 18, '#795E4B')
        svg('project-'+key+'.svg', 540, 220, title,
            kind + '. ' + '. '.join(lines) + '. ' + technologies, b)


if __name__ == '__main__':
    banner()
    stack()
    stack(mobile=True)
    project_cards()
    for name in ['ssg-sak-banner.svg', 'tech-stack.svg', 'tech-stack-mobile.svg']:
        p = OUT/name
        print(name, p.stat().st_size, 'bytes')
