"""Optimize supplied media. Requires Pillow and imageio-ffmpeg; originals are untouched."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageOps
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Resource/Figures'
DEST = ROOT / 'assets/media'
DEST.mkdir(parents=True, exist_ok=True)
data = json.loads((ROOT / '_data/homepage.json').read_text(encoding='utf-8'))

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--portrait-only', action='store_true')
args = parser.parse_args()
portrait_source = ROOT / data['profile'].get('portrait_source', 'images/profile.png')
with Image.open(portrait_source) as image:
    image = ImageOps.exif_transpose(image).convert('RGB')
    image.thumbnail((560, 560))
    image.save(DEST / 'profile.webp', quality=88, method=6)
if args.portrait_only:
    print('Updated portrait from', portrait_source.name)
    raise SystemExit(0)

for item in data['research']:
    if 'figure' not in item:
        continue
    source = SOURCE / f"{item['figure']}.jpg"
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert('RGB')
        large = image.copy()
        large.thumbnail((2800, 2200))
        large.save(DEST / f"{item['id']}-full.jpg", quality=90, optimize=True, progressive=True)
        image.thumbnail((1100, 850))
        image.save(DEST / f"{item['id']}.webp", quality=88, method=6)

for item in data['projects']:
    if 'video' not in item:
        continue
    source = SOURCE / item['source']
    with Image.open(source) as image:
        image.seek(min(20, image.n_frames - 1))
        image.convert('RGB').save(DEST / f"{item['video']}.webp", quality=90, method=6)
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(source), '-an', '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-movflags', '+faststart',
        str(DEST / f"{item['video']}.mp4"),
    ], check=True)
    print(item['video'], 'converted')

print('Media total:', round(sum(p.stat().st_size for p in DEST.iterdir()) / 1024 / 1024, 2), 'MiB')
