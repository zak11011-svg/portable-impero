# Adds the Portable Impero logo badge to every product photo.
# Originals live in public/products/original/; run: python3 scripts_brand.py
import glob, os
from PIL import Image, ImageDraw
POS = {"cordless-heated-lunch-box": ("right", 0.40)}  # (side, vertical fraction)
logo = Image.open("public/brand/logo.png")
for orig in sorted(glob.glob("public/products/original/*.jpg")):
    name = os.path.splitext(os.path.basename(orig))[0]
    im = Image.open(orig).convert("RGBA"); W, H = im.size
    lh = int(H * 0.11); lw = int(logo.width * lh / logo.height)
    L = logo.resize((lw, lh), Image.LANCZOS)
    pad = int(lh * 0.22); m = int(W * 0.035); bw, bh = lw + 2 * pad, lh + 2 * pad
    side, fy = POS.get(name, ("left", None))
    x = m if side == "left" else W - m - bw
    y = m if fy is None else int(H * fy)
    badge = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(badge)
    d.rounded_rectangle((x, y, x + bw, y + bh), radius=pad, fill=(248, 243, 236, 225))
    badge.alpha_composite(L, (x + pad, y + pad)); im.alpha_composite(badge)
    im.convert("RGB").save(f"public/products/{name}.jpg", quality=92)
