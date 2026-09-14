"""Build the static, Jekyll-compatible homepage from _data/homepage.json.

No third-party packages needed. Run after editing content or the HTML template.
The same HTML can be previewed without installing Ruby/Jekyll.
"""
import argparse
import html
import json
import shutil
from pathlib import Path
from string import Template
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MEDIA = '/assets/media/'


def esc(value):
    return html.escape(str(value), quote=True)


def authors(item):
    return ', '.join(f'<strong>{esc(name)}</strong>' if name == 'Yiran Zhang' else esc(name)
                     for name in item.get('authors', []))


def venue(item):
    return ' · '.join(esc(item[key]) for key in ('venue', 'year') if item.get(key))


def figure(item):
    return f'''<a class="figure-link" href="{MEDIA}{item['id']}-full.jpg" data-zoom
      aria-label="Enlarge figure: {esc(item['title'])}">
      <img src="{MEDIA}{item['id']}.webp" alt="{esc(item['title'])} — research overview"
        loading="lazy" decoding="async" width="1100" height="700">
      <span class="figure-hint" aria-hidden="true">Enlarge ↗</span>
    </a>'''


def video(item):
    if item.get('youtube'):
        watch = f"https://www.youtube.com/watch?v={item['youtube']}"
        # No third-party request until the visitor explicitly plays the demo.
        poster = (f'<img src="{MEDIA}{item["id"]}.webp" alt="" loading="lazy" decoding="async">'
                  if item.get('figure') else '<span class="video-placeholder" aria-hidden="true">Shutoko Highway<br>Driving & interaction</span>')
        return f'''<div class="video-stage" data-youtube="{esc(item['youtube'])}" data-title="{esc(item['title'])}">
          <a class="play-demo" href="{watch}" data-play-youtube aria-label="Play video: {esc(item['title'])}">
            {poster}<span class="play-label"><span aria-hidden="true">▶</span> Play demo</span>
          </a>
        </div>'''
    return f'''<video class="local-demo" controls playsinline loop preload="none"
      poster="{MEDIA}{item['video']}.webp" width="426" height="240"
      aria-label="{esc(item['title'])} demonstration">
      <source src="{MEDIA}{item['video']}.mp4" type="video/mp4">
      <a href="{MEDIA}{item['video']}.mp4">Watch the demonstration</a>
    </video>'''


def media(item):
    has_figure = bool(item.get('figure'))
    has_video = bool(item.get('youtube') or item.get('video'))
    if has_figure and has_video:
        uid = item['id']
        return f'''<div class="media-switcher" data-media-switcher>
          <div class="media-tabs" role="tablist" aria-label="Media for {esc(item['title'])}" hidden>
            <button type="button" role="tab" id="{uid}-figure-tab" aria-selected="true" aria-controls="{uid}-figure" data-panel="{uid}-figure">Figure</button>
            <button type="button" role="tab" id="{uid}-demo-tab" aria-selected="false" aria-controls="{uid}-demo" tabindex="-1" data-panel="{uid}-demo">Demo</button>
          </div>
          <div id="{uid}-figure" class="media-panel" role="tabpanel" aria-labelledby="{uid}-figure-tab">{figure(item)}</div>
          <div id="{uid}-demo" class="media-panel" role="tabpanel" aria-labelledby="{uid}-demo-tab">{video(item)}</div>
        </div>'''
    return figure(item) if has_figure else video(item)


def links(item):
    result = []
    if item.get('paper'):
        result.append(f'<a href="{esc(item["paper"])}">Paper <span aria-hidden="true">↗</span></a>')
    if item.get('youtube'):
        result.append(f'<a href="https://www.youtube.com/watch?v={esc(item["youtube"])}">Video <span aria-hidden="true">↗</span></a>')
    if item.get('video'):
        result.append(f'<a href="{MEDIA}{item["video"]}.mp4">Video <span aria-hidden="true">↗</span></a>')
    return '<div class="work-links">' + ''.join(result) + '</div>' if result else ''


def row(item):
    title = esc(item['title'])
    author_line = f'<p class="authors">{authors(item)}</p>' if item.get('authors') else ''
    highlight = f'<strong>{esc(item["highlight"])}</strong> ' if item.get('highlight') else ''
    summary = f'<p class="work-summary">{highlight}{esc(item["summary"])}</p>' if item.get('summary') else ''
    return f'''<article class="work" id="{item['id']}" aria-labelledby="{item['id']}-title">
      <div class="work-media">{media(item)}</div>
      <div class="work-text">
        <p class="work-category">{esc(item['category'])}</p>
        <h3 id="{item['id']}-title">{title}</h3>
        {author_line}
        <p class="venue">{venue(item)}</p>
        {summary}{links(item)}
      </div>
    </article>'''


def publication(item):
    title = esc(item['title'])
    if item.get('paper'):
        title = f'<a href="{esc(item["paper"])}">{title}</a>'
    return f'<li><h3>{title}</h3><p class="authors">{authors(item)}</p><p class="venue">{venue(item)}</p></li>'


def publication_records(data):
    """List published featured papers and other publications without duplicate data."""
    candidates = [item for item in data['research'] if item.get('authors') and item.get('year')]
    candidates.extend(data['publications'])
    unique = {}
    for item in candidates:
        key = ' '.join(item['title'].casefold().split())
        unique.setdefault(key, item)
    return sorted(unique.values(), key=lambda item: int(item.get('year', 0)), reverse=True)


def teaching(item):
    context = ' · '.join(esc(item[key]) for key in ('institution', 'dates') if item.get(key))
    meta = f'<p class="venue">{context}</p>' if context else ''
    return f'<li><h3>{esc(item["title"])}</h3>{meta}<p>{esc(item["description"])}</p></li>'


def validate(data):
    ids = set()
    for item in data['research'] + data['projects']:
        assert item['id'] not in ids, f'Duplicate id: {item["id"]}'
        ids.add(item['id'])
        assert item.get('figure') or item.get('youtube') or item.get('video'), item['id']
        if item.get('figure'):
            assert (ROOT / 'assets/media' / f'{item["id"]}.webp').is_file(), item['id']
        if item.get('video'):
            assert (ROOT / 'assets/media' / f'{item["video"]}.mp4').is_file(), item['id']
    for item in data['research'] + data['publications']:
        if item.get('paper'):
            assert urlparse(item['paper']).scheme == 'https', item['title']
    selected = {item['title'] for item in data['research']}
    assert not selected.intersection(item['title'] for item in data['publications'])


def build():
    data = json.loads((ROOT / '_data/homepage.json').read_text(encoding='utf-8'))
    validate(data)
    profile = {key: esc(value) for key, value in data['profile'].items()}
    profile.update(research='\n'.join(row(item) for item in data['research']),
                   projects='\n'.join(row(item) for item in data['projects']),
                   publications='\n'.join(publication(item) for item in publication_records(data)),
                   teaching='\n'.join(teaching(item) for item in data['teaching']),
                   service='\n'.join(f'<li>{esc(name)}</li>' for name in data['service']))
    template = Template((ROOT / 'scripts/homepage.template.html').read_text(encoding='utf-8'))
    document = '\n'.join(line.rstrip() for line in template.substitute(profile).splitlines()) + '\n'
    frontmatter = '---\nlayout: null\npermalink: /\ntitle: "Yiran Zhang | AI Agent Evaluation & Robotics"\nredirect_from:\n  - /about/\n  - /about.html\n---\n'
    return frontmatter + document, document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the committed HTML is out of date.')
    parser.add_argument('--preview', action='store_true', help='Also write a standalone preview under local/preview.')
    args = parser.parse_args()
    output, document = build()
    target = ROOT / '_pages/about.html'
    if args.check:
        if not target.is_file() or target.read_text(encoding='utf-8') != output:
            raise SystemExit('Homepage is stale. Run: python scripts/build_homepage.py')
        print('Homepage matches its content and template.')
    else:
        target.write_text(output, encoding='utf-8')
        print('Built _pages/about.html')
    if args.preview:
        preview = ROOT / 'local/preview'
        preview.mkdir(parents=True, exist_ok=True)
        (preview / 'index.html').write_text(document, encoding='utf-8')
        for name in ('media',):
            shutil.copytree(ROOT / 'assets' / name, preview / 'assets' / name, dirs_exist_ok=True)
        for name in ('css/homepage.css', 'js/homepage.js'):
            dest = preview / 'assets' / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / 'assets' / name, dest)
        (preview / 'images').mkdir(exist_ok=True)
        shutil.copy2(ROOT / 'images/favicon.svg', preview / 'images/favicon.svg')
        for route, anchor in [('projects', 'research'), ('robotics', 'projects'), ('publications', 'publications'), ('about', 'about')]:
            destination = preview / route
            destination.mkdir(exist_ok=True)
            (destination / 'index.html').write_text(
                f'<!doctype html><html lang="en"><title>Redirecting</title><meta http-equiv="refresh" content="0;url=/#{anchor}"><a href="/#{anchor}">Continue to Yiran Zhang’s homepage</a></html>', encoding='utf-8')
        print('Preview: python -m http.server 4000 --bind 127.0.0.1 --directory local/preview')


if __name__ == '__main__':
    main()
