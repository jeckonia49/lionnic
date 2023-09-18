from .__debug import *




# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get("DATABASE_NAME"),
#         'USER': os.environ.get("DATABASE_USER"),
#         'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}