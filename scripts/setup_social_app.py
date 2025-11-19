import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import django
from django.conf import settings

django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def read_secret(secret_name: str) -> str:
    """Read secret from files or env, similar to config.secrets.read_secret"""
    # 1. Try local secrets/ folder
    local_secret_path = project_root / "secrets" / f"{secret_name.lower()}.txt"
    if local_secret_path.exists():
        try:
            return local_secret_path.read_text().strip()
        except Exception as e:
            print(f"Error reading {local_secret_path}: {e}")

    # 2. Try env var
    if secret_name in os.environ:
        return os.environ[secret_name]

    raise ValueError(f"Secret {secret_name} not found")

def setup_social_app():
    try:
        # Get credentials from secrets or env
        client_id = read_secret("GOOGLE_CLIENT_ID")
        secret = read_secret("GOOGLE_CLIENT_SECRET")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Configuring Google SocialApp with Client ID: {client_id[:10]}...")

    # Get current site
    site = Site.objects.get_current()
    print(f"Current Site: {site.domain} ({site.name})")

    # Update site domain if it's example.com
    if site.domain == "example.com":
        site.domain = "localhost:8000"
        site.name = "10Code Intranet (Local)"
        site.save()
        print(f"Updated Site to: {site.domain}")

    # Create or update SocialApp
    app, created = SocialApp.objects.update_or_create(
        provider="google",
        defaults={
            "name": "Google",
            "client_id": client_id,
            "secret": secret,
        }
    )
    
    app.sites.add(site)
    
    if created:
        print("Created new Google SocialApp.")
    else:
        print("Updated existing Google SocialApp.")

if __name__ == "__main__":
    setup_social_app()
