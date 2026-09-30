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
    "Home & Majlis",
    "Car",
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
<meta property="og:image" content="https://portableimpero.com/brand/og-image.jpg">
<link rel="icon" href="{base}brand/logo.png">
{FONTS}
<link rel="stylesheet" href="{base}styles.css">
<script>document.documentElement.classList.add("js")</script>
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
<script>
(function () {{
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {{ els.forEach(function (e) {{ e.classList.add('is-in'); }}); return; }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (en) {{
      if (en.isIntersecting) {{ en.target.classList.add('is-in'); io.unobserve(en.target); }}
    }});
  }}, {{ threshold: 0.12, rootMargin: '0px 0px -40px 0px' }});
  els.forEach(function (e) {{ io.observe(e); }});
}})();
</script>
</body>
</html>
"""


def card(p):
    return f"""<a class="card reveal" href="products/{p['id']}" data-cat="{slug(p['category'])}">
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
    hero_words = " ".join(
        f'<span class="w" aria-hidden="true" style="--i:{i}">{escape(w)}</span>' for i, w in enumerate(TAGLINE.split())
    )
    ribbon = "".join(
        f'<figure class="ribbon-item"><img src="products/original/{os.path.basename(p["image"])}" alt="" loading="lazy">'
        f'<figcaption>{escape(p["name"].removeprefix("PI "))}</figcaption></figure>'
        for p in products
    )
    home = f"""
<section class="hero hero-cinema">
  <div class="cinema-bg" aria-hidden="true"></div>
  <div class="cinema-frame">
    <div class="cinema-move">
      <img class="cinema-img" src="brand/hero-desert.jpg" width="1214" height="1295"
        alt="PI cordless products on a desert rock at sunset beside a camping tent. Portable. Cordless. Limitless.">
      <span class="cinema-sun" aria-hidden="true"></span>
      <span class="cinema-lantern" aria-hidden="true"></span>
    </div>
    <span class="cinema-sheen" aria-hidden="true"></span>
    <canvas class="cinema-sand" aria-hidden="true"></canvas>
  </div>
  <h1 class="sr-only">Portable. Cordless. Limitless.</h1>
  <p class="hero-sub">Cordless, rechargeable essentials for home, work, the car and the desert camp &mdash; curated in Qatar.</p>
  <a class="btn btn-lg hero-cta" href="#shop">Explore the collection</a>
  <a class="scroll-cue" href="#shop" aria-label="Scroll to the collection"><span></span></a>
</section>

<section class="ribbon" aria-hidden="true">
  <div class="ribbon-track">{ribbon}{ribbon}</div>
</section>

<section class="values" aria-label="Why Portable Impero">
  <div class="reveal"><h2>Cordless</h2><p>Battery-powered, so they work wherever you are.</p></div>
  <div class="reveal"><h2>Curated</h2><p>Every piece chosen for everyday use in Qatar.</p></div>
  <div class="reveal"><h2>6-month warranty</h2><p>Every PI product is covered for six months.</p></div>
  <div class="reveal"><h2>Local</h2><p>Based in Doha, delivering across Qatar.</p></div>
</section>

<section id="shop" class="shop">
  <h2 class="section-title reveal">The collection</h2>
  <div class="chips" role="toolbar" aria-label="Filter by category">{chips}</div>
  <div class="grid">
{''.join(card(p) for p in products)}
  </div>
</section>

<section id="about" class="about">
  <span class="eyebrow reveal">Our story</span>
  <h2 class="section-title reveal">Your world, unplugged.</h2>
  <div class="story reveal">
    <p>Life in Qatar never stays in one place. The morning starts at home, moves to the office, carries on in the car,
    and on the best days ends under the stars at a desert camp or by the sea. Yet so many of the things that make those
    moments comfortable are still tied to a socket.</p>
    <p>Portable Impero was born in Doha to change that. We search for well-made, cordless and rechargeable essentials:
    a lunch box that warms your meal on the road, a fan that cools the camp, a blender that fits in your bag. Then we
    bring them together in one place, chosen for the way people here really live.</p>
    <p><em>Impero</em> means &ldquo;empire&rdquo;. To us, it is the simple idea that your comfort should go wherever
    you go &mdash; that every place you spend your day can feel like your own.</p>
  </div>
  <p class="signature reveal">Power that travels with you.</p>
  <img class="story-mark" src="brand/logo.png" alt="" width="40" height="69">
  {enquire_button(large=True)}
</section>

<script>
(function () {{
  var c = document.querySelector('.cinema-sand');
  if (!c || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var ctx = c.getContext('2d'), ps = [], W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
  function size() {{
    W = c.clientWidth; H = c.clientHeight; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }}
  function spawn(init) {{
    return {{ x: init ? Math.random() * W : -10, y: H * (0.45 + Math.random() * 0.55),
      r: 0.4 + Math.random() * 1.4, v: 0.25 + Math.random() * 0.9, a: 0.15 + Math.random() * 0.5,
      w: Math.random() * Math.PI * 2 }};
  }}
  size(); window.addEventListener('resize', size);
  for (var i = 0; i < 70; i++) ps.push(spawn(true));
  (function tick() {{
    ctx.clearRect(0, 0, W, H);
    ps.forEach(function (p, i) {{
      p.x += p.v; p.w += 0.02; p.y += Math.sin(p.w) * 0.15;
      if (p.x > W + 10) ps[i] = spawn(false);
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283);
      ctx.fillStyle = 'rgba(255, 214, 160,' + p.a + ')'; ctx.fill();
    }});
    requestAnimationFrame(tick);
  }})();
}})();
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
