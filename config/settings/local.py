from .base import *

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATICFILES_DIRS = [
    BASE_DIR / 'static/',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        }
    }
}

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"]

