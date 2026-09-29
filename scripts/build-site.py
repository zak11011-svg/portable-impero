"""Builds the Portable Impero website into public/ from data/products.json.

Run:  python3 scripts/build-site.py
Vercel serves the public/ folder as-is, so re-run this and push after editing products.
"""
import json
import os
from html import escape
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")

# ---- Site settings -------------------------------------------------------
SITE_NAME = "Portable Impero"
TAGLINE = "Power that travels with you."
# WhatsApp number in international format, digits only (e.g. "97455555555").
# Leave empty to show "Launching soon" instead of the enquiry button.
WHATSAPP = ""
YEAR = 2026
# --------------------------------------------------------------------------

CATEGORY_ORDER = [
    "Kitchen & On the Go",
    "Home & Cooling",
    "Outdoor & Camping",
    "Work & Tech",
    "Baby & Family",
    "Beauty & Care",
]

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500&display=swap\">"
)


def slug(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--", "-").replace("--", "-")


def enquire_button(product_name=None, large=False):
    cls = "btn btn-lg" if large else "btn"
    if not WHATSAPP:
        return f'<span class="{cls} btn-muted">Launching soon in Qatar</span>'
    text = f"Hello Portable Impero, I'm interested in the {product_name}." if product_name else "Hello Portable Impero!"
    return (
        f'<a class="{cls}" href="https://wa.me/{WHATSAPP}?text={quote(text)}" '
        f'target="_blank" rel="noopener">Enquire on WhatsApp</a>'
    )


def page(title, description, body, depth=0):
    base = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<link rel="icon" href="{base}brand/logo.png">
{FONTS}
<link rel="stylesheet" href="{base}styles.css">
</head>
<body>
<header class="site-header">
  <a class="brand" href="{base or './'}" aria-label="{SITE_NAME} home">
    <img src="{base}brand/logo.png" alt="" width="28" height="48">
    <span>Portable Impero</span>
  </a>
  <nav><a href="{base}#shop">Shop</a><a href="{base}#about">About</a></nav>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <img src="{base}brand/logo.png" alt="" width="22" height="38">
  <p>&copy; {YEAR} Portable Impero &middot; Doha, Qatar</p>
</footer>
</body>
</html>
"""


def card(p):
    return f"""<a class="card" href="products/{p['id']}" data-cat="{slug(p['category'])}">
  <div class="card-img"><img src="products/{os.path.basename(p['image'])}" alt="{escape(p['name'])}" loading="lazy"></div>
  <div class="card-body">
    <span class="eyebrow">{escape(p['category'])}</span>
    <h3>{escape(p['name'])}</h3>
  </div>
</a>"""


def build():
    products = [p for p in json.load(open(os.path.join(ROOT, "data", "products.json"))) if p.get("image")]
    cats = [c for c in CATEGORY_ORDER if any(p["category"] == c for p in products)]
    cats += sorted({p["category"] for p in products} - set(cats))
    products.sort(key=lambda p: cats.index(p["category"]))

    chips = '<button class="chip is-on" data-filter="all" type="button">All</button>' + "".join(
        f'<button class="chip" data-filter="{slug(c)}" type="button">{escape(c)}</button>' for c in cats
    )
    home = f"""
<section class="hero">
  <img class="hero-logo" src="brand/logo.png" alt="Portable Impero crest" width="120" height="206">
  <h1>{TAGLINE}</h1>
  <p>Cordless, rechargeable essentials for home, work, the car and the desert camp &mdash; curated in Qatar.</p>
  <a class="btn btn-lg" href="#shop">Explore the collection</a>
</section>

<section class="values" aria-label="Why Portable Impero">
  <div><h2>Cordless</h2><p>Battery-powered, so they work wherever you are.</p></div>
  <div><h2>Curated</h2><p>Every piece chosen for everyday use in Qatar.</p></div>
  <div><h2>Local</h2><p>Based in Doha, delivering across Qatar.</p></div>
</section>

<section id="shop" class="shop">
  <h2 class="section-title">The collection</h2>
  <div class="chips" role="toolbar" aria-label="Filter by category">{chips}</div>
  <div class="grid">
{''.join(card(p) for p in products)}
  </div>
</section>

<section id="about" class="about">
  <h2 class="section-title">About us</h2>
  <p>Portable Impero is based in Doha. We bring together smart,
  portable and cordless products that make everyday life easier &mdash; at home, at the office, on the road and outdoors.</p>
  {enquire_button(large=True)}
</section>

<script>
document.querySelectorAll('.chip').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var f = b.dataset.filter;
    document.querySelectorAll('.chip').forEach(function (c) {{ c.classList.toggle('is-on', c === b); }});
    document.querySelectorAll('.card').forEach(function (c) {{
      c.hidden = !(f === 'all' || c.dataset.cat === f);
    }});
  }});
}});
</script>
"""
    with open(os.path.join(PUBLIC, "index.html"), "w") as fh:
        fh.write(page(f"{SITE_NAME} | Cordless essentials in Qatar",
                      "Cordless, rechargeable essentials for home, work, car and camping. Based in Doha, Qatar.",
                      home))

    for p in products:
        specs = "".join(f"<tr><th>{escape(k)}</th><td>{escape(v)}</td></tr>" for k, v in p["specs"].items())
        others = [o for o in products if o["category"] == p["category"] and o["id"] != p["id"]][:3]
        related = ""
        if others:
            related = ('<section class="related"><h2 class="section-title">You may also like</h2><div class="grid">'
                       + "".join(card(o).replace('href="products/', 'href="').replace('src="products/', 'src="')
                                 for o in others) + "</div></section>")
        body = f"""
<nav class="crumbs"><a href="../#shop">Collection</a> <span aria-hidden="true">/</span> {escape(p['category'])}</nav>
<article class="product">
  <div class="product-img"><img src="{os.path.basename(p['image'])}" alt="{escape(p['name'])}"></div>
  <div class="product-info">
    <span class="eyebrow">{escape(p['category'])}</span>
    <h1>{escape(p['name'])}</h1>
    <p class="lead">{escape(p['description'])}</p>
    {enquire_button(p['name'], large=True)}
    <h2>Specifications</h2>
    <table class="specs">{specs}</table>
  </div>
</article>
{related}
"""
        with open(os.path.join(PUBLIC, "products", f"{p['id']}.html"), "w") as fh:
            fh.write(page(f"{p['name']} | {SITE_NAME}", p["description"], body, depth=1))
    print(f"Built home page and {len(products)} product pages.")


if __name__ == "__main__":
    build()
