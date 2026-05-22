import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")
django.setup()

from django.contrib.auth.models import User

for i in range(1, 201):
    username = f"k6user{i}"

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password="password123")

print("200 test users created.")
