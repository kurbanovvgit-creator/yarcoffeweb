# PythonAnywhere Deploy Guide

Replace `YOUR_USERNAME` and `REPO_URL` with your real values.

## 1. Push Project To GitHub

From your local machine:

```powershell
git remote add origin REPO_URL
git push -u origin main
```

## 2. Clone On PythonAnywhere

Open a PythonAnywhere Bash console:

```bash
cd ~
git clone REPO_URL yarcoffee
cd yarcoffee
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure Environment

In the same Bash console, generate a secret:

```bash
python - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
```

Use that value in the Web tab WSGI file or in a `.env` strategy if you add one later.

## 4. Prepare Django

```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY='PASTE_GENERATED_SECRET_HERE'
export DJANGO_ALLOWED_HOSTS='YOUR_USERNAME.pythonanywhere.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://YOUR_USERNAME.pythonanywhere.com'

python manage.py migrate
python manage.py seed_demo
python manage.py sync_translations
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 5. Configure PythonAnywhere Web App

In PythonAnywhere:

- Go to **Web**.
- Add a new web app.
- Choose **Manual configuration**.
- Choose **Python 3.12**.

Set paths:

- Source code: `/home/YOUR_USERNAME/yarcoffee`
- Working directory: `/home/YOUR_USERNAME/yarcoffee`
- Virtualenv: `/home/YOUR_USERNAME/yarcoffee/.venv`

## 6. WSGI File

Open the WSGI file from the PythonAnywhere Web tab.

Paste the contents of:

```text
deploy/pythonanywhere_wsgi.py
```

Then replace:

```python
USERNAME = "YOUR_USERNAME"
```

with your real PythonAnywhere username.

Also replace `DJANGO_SECRET_KEY` if you prefer setting it in WSGI:

```python
os.environ.setdefault("DJANGO_SECRET_KEY", "PASTE_GENERATED_SECRET_HERE")
```

## 7. Static And Media Files

In the **Static files** section:

```text
URL:       /static/
Directory: /home/YOUR_USERNAME/yarcoffee/staticfiles
```

Required for photos uploaded in admin (drinks, gallery, hero):

```text
URL:       /media/
Directory: /home/YOUR_USERNAME/yarcoffee/media
```

Create the folder if needed:

```bash
mkdir -p ~/yarcoffee/media
```

## 8. Reload

Press **Reload** in the PythonAnywhere Web tab.

Open:

```text
https://YOUR_USERNAME.pythonanywhere.com/
```

## Updating Later

```bash
cd ~/yarcoffee
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then press **Reload** in the Web tab.
