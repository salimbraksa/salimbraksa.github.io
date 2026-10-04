"""Sync selected-work.json into both static pages. Run: python3 scripts/sync-content.py
Descriptions support Markdown paragraphs, bold, italic, code, and links.
Static HTML keeps file:// previews and search/share crawlers working.
"""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parent.parent

def markdown(text):
    def inline(value):
        value=html.escape(value)
        value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
        value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
        value=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',value)
        def link(m):
            url=html.unescape(m[2])
            return '<a href="'+html.escape(url,quote=True)+'">'+m[1]+'</a>' if url.startswith(('https://','http://','mailto:')) else m[1]
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,value)
    return ''.join('<p>'+inline(p.strip()).replace('\n','<br>')+'</p>' for p in re.split(r'\n\s*\n',text) if p.strip())

def card(p):
    esc=lambda v:html.escape(str(v),quote=True)
    rating=max(0,min(5,float(p['rating'])))
    storefront={'us':'US','sa':'Saudi Arabian','gb':'UK'}.get(p.get('ratingStorefront'),'')
    iconClass=' moment-app-icon' if p['id']=='moment' else ''
    identity=f'''<div class="app-identity"><img class="app-icon featured-icon{iconClass}" src="{esc(p['icon'])}" alt="" width="48" height="48"><div class="app-heading"><div class="eyebrow">{esc(p['appName'])}</div><div class="app-rating"><span class="rating" aria-label="{rating:.1f} out of 5 stars on the {storefront} App Store"><span class="rating-stars" aria-hidden="true"><span>★★★★★</span><span class="rating-fill" style="width:{rating*20}%">★★★★★</span></span><span class="rating-number">{rating:.1f}</span></span><a class="app-link" href="{esc(p['appStoreUrl'])}" aria-label="{esc(p['appName'])} on the App Store">App Store ↗</a></div></div></div>'''
    tags='<div class="tags">'+''.join('<span>'+esc(t)+'</span>' for t in p['technologies'])+'</div>'
    if p.get('video'):
        media=f'''<div class="demo-device recorded-device"><video controls playsinline preload="metadata" poster="{esc(p.get('poster') or '')}" aria-label="{esc(p['appName'])} demo" style="aspect-ratio:auto"><source src="{esc(p['video'])}" type="video/mp4"></video></div>'''
    else:
        media=f'''<div class="demo-device"><div class="device-notch" aria-hidden="true"></div><div class="demo-placeholder"><span class="eyebrow">{esc(p['appName'])}</span><strong>Demo coming soon</strong><p>{esc(p['projects'][0]['title'])}</p></div></div>'''
    if len(p['projects']) == 1:
        project = p['projects'][0]
        content = '<h3>'+esc(project['title'])+'</h3>'+markdown(p['appDescription'])+markdown(project['description'])
    else:
        content = markdown(p['appDescription'])+''.join('<section class="card-project"><h3>'+esc(project['title'])+'</h3>'+markdown(project['description'])+'</section>' for project in p['projects'])
    return '<article class="project demo-project"><div class="copy">'+identity+content+tags+'</div><div class="visual device-demo">'+media+'</div></article>'

projects=json.loads((ROOT/'content/selected-work.json').read_text())['projects']
for name in ('index.html','layout-draft.html'):
    path=ROOT/name
    source=path.read_text()
    matches=list(re.finditer(r'<article class="project demo-project">.*?</article>',source,re.S))
    if not matches: raise ValueError('Selected-work cards not found in '+name)
    source=source[:matches[0].start()]+''.join(card(p) for p in projects)+source[matches[-1].end():]
    path.write_text(source)
print('Synced selected-work.json into both pages.')
