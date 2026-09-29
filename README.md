# Portable Impero

Website for **portableimpero.com**: cordless, portable essentials, based in Doha, Qatar.

## How it works
- `data/products.json`: all product info (name, category, description, specs).
- `public/products/original/`: product photos without the logo.
- `scripts/brand-photos.py`: adds the Portable Impero logo to every photo.
- `scripts/build-site.py`: builds the website pages into `public/`.
- Vercel serves the `public/` folder (see `vercel.json`).

## Updating the site
```
python3 scripts/brand-photos.py
python3 scripts/build-site.py
```
Then commit and push. Vercel redeploys automatically.

To turn on the WhatsApp enquiry buttons, set `WHATSAPP` at the top of `scripts/build-site.py`.
