"""
One-shot downloader of all third-party assets required by the site.

It pulls:
  * Tailwind CSS (precompiled, used as a supporting utility layer alongside our
    custom site.css)
  * Inter (sans) and Cormorant Garamond (display) web fonts
  * A curated set of premium Unsplash photographs for the demo content

Everything ends up inside the project so the site runs fully offline afterwards.
Photos are stored under static/images/ so templates can serve them as static assets.

Usage:
    python manage.py setup_assets
    python manage.py setup_assets --skip-images   # only CSS / fonts
    python manage.py setup_assets --force         # re-download everything
"""

from __future__ import annotations

import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


STATIC_CSS_URLS = {
    "css/tailwind.css": "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
}

STATIC_FONT_URLS = {
    "fonts/inter-400.woff2": "https://rsms.me/inter/font-files/Inter-Regular.woff2?v=3.19",
    "fonts/inter-500.woff2": "https://rsms.me/inter/font-files/Inter-Medium.woff2?v=3.19",
    "fonts/inter-600.woff2": "https://rsms.me/inter/font-files/Inter-SemiBold.woff2?v=3.19",
    "fonts/inter-700.woff2": "https://rsms.me/inter/font-files/Inter-Bold.woff2?v=3.19",
    "fonts/cormorant-400.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/cormorant-garamond@latest/latin-400-normal.woff2",
    "fonts/cormorant-500.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/cormorant-garamond@latest/latin-500-normal.woff2",
    "fonts/cormorant-600.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/cormorant-garamond@latest/latin-600-normal.woff2",
}

MEDIA_IMAGE_URLS = {
    "hero/hero-main.jpg":
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1800&q=80",
    "story/story-1.jpg":
        "https://images.unsplash.com/photo-1453614512568-c4024d13c247?auto=format&fit=crop&w=1400&q=80",
    "story/story-2.jpg":
        "https://images.unsplash.com/photo-1521017432531-fbd92d768814?auto=format&fit=crop&w=1400&q=80",
    "story/story-3.jpg":
        "https://images.unsplash.com/photo-1442975631115-c4f7b05b8a2c?auto=format&fit=crop&w=1400&q=80",
    "drinks/iced-latte.jpg":
        "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=1200&q=80",
    "drinks/cappuccino.jpg":
        "https://images.unsplash.com/photo-1561882468-9110e03e0f78?auto=format&fit=crop&w=1200&q=80",
    "drinks/raffaello.jpg":
        "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=1200&q=80",
    "drinks/matcha.jpg":
        "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=1200&q=80",
    "drinks/espresso.jpg":
        "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?auto=format&fit=crop&w=1200&q=80",
    "drinks/cold-brew.jpg":
        "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1200&q=80",
    "drinks/flat-white.jpg":
        "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?auto=format&fit=crop&w=1200&q=80",
    "drinks/mocha.jpg":
        "https://images.unsplash.com/photo-1494314671902-399b18174975?auto=format&fit=crop&w=1200&q=80",
    "drinks/croissant.jpg":
        "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=1200&q=80",
    "drinks/cheesecake.jpg":
        "https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=1200&q=80",
    "drinks/lemonade.jpg":
        "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=1200&q=80",
    "drinks/milkshake.jpg":
        "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=1200&q=80",
    "drinks/beans.jpg":
        "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?auto=format&fit=crop&w=1200&q=80",
    "gallery/g-1.jpg":
        "https://images.unsplash.com/photo-1453614512568-c4024d13c247?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-2.jpg":
        "https://images.unsplash.com/photo-1442975631115-c4f7b05b8a2c?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-3.jpg":
        "https://images.unsplash.com/photo-1521017432531-fbd92d768814?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-4.jpg":
        "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-5.jpg":
        "https://images.unsplash.com/photo-1521017432531-fbd92d768814?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-6.jpg":
        "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-7.jpg":
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-8.jpg":
        "https://images.unsplash.com/photo-1572441713132-c542fc4fe282?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-9.jpg":
        "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-10.jpg":
        "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-11.jpg":
        "https://images.unsplash.com/photo-1493857671505-72967e2e2760?auto=format&fit=crop&w=1400&q=80",
    "gallery/g-12.jpg":
        "https://images.unsplash.com/photo-1497636577773-f1231844b336?auto=format&fit=crop&w=1400&q=80",
    "interior/i-1.jpg":
        "https://images.unsplash.com/photo-1453614512568-c4024d13c247?auto=format&fit=crop&w=1400&q=80",
    "interior/i-2.jpg":
        "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=1400&q=80",
    "interior/i-3.jpg":
        "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1400&q=80",
    "team/t-1.jpg":
        "https://images.unsplash.com/photo-1564564321837-a57b7070ac4f?auto=format&fit=crop&w=900&q=80",
    "team/t-2.jpg":
        "https://images.unsplash.com/photo-1583195764036-6dc248ac07d9?auto=format&fit=crop&w=900&q=80",
    "team/t-3.jpg":
        "https://images.unsplash.com/photo-1521119989659-a83eee488004?auto=format&fit=crop&w=900&q=80",
    "team/t-4.jpg":
        "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=900&q=80",
}


class Command(BaseCommand):
    help = "Download Tailwind CSS, fonts and curated Unsplash images for offline use."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing files")
        parser.add_argument("--skip-images", action="store_true", help="Do not download static images")
        parser.add_argument("--skip-css", action="store_true", help="Do not download Tailwind/fonts")
        parser.add_argument("--timeout", type=int, default=20)

    def handle(self, *args, **opts):
        if requests is None:
            self.stderr.write("The `requests` library is required. Install it via: pip install requests")
            sys.exit(1)

        self.force = opts["force"]
        self.timeout = opts["timeout"]

        if not opts["skip_css"]:
            self.stdout.write(self.style.MIGRATE_HEADING("-> Downloading CSS & fonts"))
            self._download_map(STATIC_CSS_URLS, base=Path(settings.STATICFILES_DIRS[0]))
            self._download_map(STATIC_FONT_URLS, base=Path(settings.STATICFILES_DIRS[0]))
            self._write_font_face_css()

        if not opts["skip_images"]:
            self.stdout.write(self.style.MIGRATE_HEADING("-> Downloading static images"))
            self._download_map(
                MEDIA_IMAGE_URLS,
                base=Path(settings.STATICFILES_DIRS[0]) / "images",
            )

        self.stdout.write(self.style.SUCCESS("[OK] Setup complete."))
        self.stdout.write(
            "  You can now run: python manage.py seed_demo (to populate sample content)"
        )

    def _download_map(self, mapping, base):
        for rel_path, url in mapping.items():
            dest = base / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and not self.force:
                self.stdout.write(f"  -- skip  {rel_path}")
                continue
            try:
                r = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={"User-Agent": "Yarcoffee/1.0 (offline-fetch)"},
                )
                r.raise_for_status()
                dest.write_bytes(r.content)
                self.stdout.write(self.style.SUCCESS(f"  [OK] {rel_path} ({len(r.content)//1024} KB)"))
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"  [!]  {rel_path} -- {exc}"))

    def _write_font_face_css(self):
        """Generate static/css/fonts.css that registers locally-saved web fonts."""
        css = """/* Auto-generated by setup_assets -- links locally saved web fonts. */
@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("../fonts/inter-400.woff2") format("woff2");
}
@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url("../fonts/inter-500.woff2") format("woff2");
}
@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url("../fonts/inter-600.woff2") format("woff2");
}
@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url("../fonts/inter-700.woff2") format("woff2");
}
@font-face {
  font-family: "Cormorant Garamond";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("../fonts/cormorant-400.woff2") format("woff2");
}
@font-face {
  font-family: "Cormorant Garamond";
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url("../fonts/cormorant-500.woff2") format("woff2");
}
@font-face {
  font-family: "Cormorant Garamond";
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url("../fonts/cormorant-600.woff2") format("woff2");
}
"""
        out = Path(settings.STATICFILES_DIRS[0]) / "css" / "fonts.css"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(css, encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"  [OK] css/fonts.css written ({len(css)} bytes)"))
