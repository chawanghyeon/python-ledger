DEBUG = False

ALLOWED_HOSTS = ["0.0.0.0"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "payhere",
        "USER": "payhere",
        "PASSWORD": "payhere",
        "HOST": "db",
        "PORT": "3306",
    }
}
