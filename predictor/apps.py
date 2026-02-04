from django.apps import AppConfig
import os
from django.db.utils import OperationalError, ProgrammingError

class PredictorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "predictor"

    def ready(self):
        try:
            from django.contrib.auth import get_user_model

            username = os.environ.get("DJANGO_ADMIN_USERNAME")
            password = os.environ.get("DJANGO_ADMIN_PASSWORD")
            email = os.environ.get("DJANGO_ADMIN_EMAIL", "")

            if not username or not password:
                return

            User = get_user_model()

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    password=password,
                    email=email
                )
                print("✅ Default admin user created")

        except (OperationalError, ProgrammingError):
            # 🔥 Database not ready yet (migrations still running)
            print("⚠️ Database not ready — skipping admin creation")
