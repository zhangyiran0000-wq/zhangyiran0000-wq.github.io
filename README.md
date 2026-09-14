# Yiran Zhang's personal website

A single-page research and robotics portfolio, inspired by the clear image-and-text
organization of [Jon Barron's homepage](https://jonbarron.info/). The page uses original
HTML/CSS, a small dependency-free script, and the repository's existing GitHub Pages setup.

## Edit content

1. Edit `_data/homepage.json`: profile, selected research, robotics projects, other publications,
   teaching experience, and reviewer service.
   The Publications section combines published featured papers with the other publications,
   sorts them by year, and highlights Yiran Zhang in every author list. Keep each paper in
   one data list only; the builder handles its appearance in both the research showcase and
   bibliography. Under-review work remains in the showcase until publication details exist.
2. Run `python scripts/build_homepage.py` to update `_pages/about.html`.
3. Run `python scripts/build_homepage.py --check` before committing.

Only concise, approved descriptions belong in the public data file. Full raw abstracts,
working notes, and source materials are kept under `Resource/`, which is ignored by Git
and excluded from Jekyll output. The CV PDF is not copied or linked on the site.

## Preview without Ruby

```powershell
python scripts/build_homepage.py --preview
python -m http.server 4000 --bind 127.0.0.1 --directory local/preview
```

Open <http://127.0.0.1:4000>. This serves the same standalone HTML, stylesheet, script,
and media as the homepage, with preview equivalents of the old-page redirects. It does
not run the Jekyll plugin pipeline. With Ruby and Bundler installed, a full site build is:

```sh
bundle install
bundle exec jekyll build
```

The generated homepage is committed as an HTML page with `layout: null` and `permalink: /`.
Jekyll strips its front matter and emits it as `index.html`; Python is not required on
GitHub Pages. The existing redirect plugin sends `/projects/`, `/robotics/`, and
`/publications/` to their corresponding homepage sections. `/about/` and `/about.html`
remain aliases of the homepage. Do not recreate a second page at `/publications/`.

## Media and appearance

- Layout: `scripts/homepage.template.html`
- Styles: `assets/css/homepage.css`
- Image zoom, Figure/Demo tabs, and theme controls: `assets/js/homepage.js`
- Optimized public figures, posters, and videos: `assets/media/`

`python scripts/prepare_media.py` regenerates media from the original files under
`Resource/Figures/`. This optional step requires `Pillow` and `imageio-ffmpeg` and leaves
the original files untouched. Future projects can instead supply already optimized files
directly in `assets/media/` and reference them from the public data.

Set `profile.portrait_source` to a local source image and run
`python scripts/prepare_media.py --portrait-only` to update just the profile photo.

Figures use lightweight WebP previews with larger JPEGs loaded only on enlargement.
Animated GIF sources are encoded as MP4 with native playback controls. YouTube embeds
are created only after a visitor chooses Play; a direct video link remains available.
The homepage does not load the legacy jQuery/Plotly bundle. Those theme assets are retained
for compatibility with other existing layouts.

## Verification

The initial redesign was checked in headless Chrome at 320, 390, 768, 1024, and 1440 px:
no horizontal overflow or JavaScript errors, working figure enlargement/escape handling,
keyboard-accessible media tabs, local video playback, persistent dark mode, and readable
content without JavaScript. YouTube embed activation was tested with a network stub;
third-party playback remains dependent on YouTube availability and embedding permissions.
