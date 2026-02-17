from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

User = get_user_model()
email = '7bhilal.chitou7@gmail.com'
password = 'Bh7777777'
username = 'admin_7bhilal'
name = 'Super Admin'

if not User.objects.filter(email=email).exists():
    try:
        User.objects.create_superuser(username=username, email=email, password=password, name=name)
        print("Superuser created successfully.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
else:
    print("Superuser already exists.")
