"""PythonAnywhere WSGI entrypoint for Yarcoffee.

Copy this file's contents into the WSGI configuration file in the
PythonAnywhere Web tab, then replace YOUR_USERNAME with your PythonAnywhere
username.
"""

import os
import sys

USERNAME = "YOUR_USERNAME"
PROJECT_PATH = f"/home/{USERNAME}/yarcoffee"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yarcoffee_site.settings")
os.environ.setdefault("DJANGO_DEBUG", "0")
os.environ.setdefault(
    "DJANGO_ALLOWED_HOSTS",
    f"{USERNAME}.pythonanywhere.com",
)
os.environ.setdefault(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    f"https://{USERNAME}.pythonanywhere.com",
)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
