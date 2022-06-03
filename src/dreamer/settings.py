import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIRS = (os.path.join(BASE_DIR, "fixtures"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "n=4_&rx%3c(0x=z@)wct45g72_-oo02jt!-&!i1#_ypjt&_q+z"
)

SERVER_ENVIRONMENT = os.environ.get("SERVER_ENVIRONMENT", "LOCAL")
IS_PRODUCTION = SERVER_ENVIRONMENT == "PRODUCTION"
IS_LOCAL = SERVER_ENVIRONMENT == "LOCAL"

DEBUG = os.environ.get("DJANGO_DEBUG", str(IS_LOCAL)).lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "colorfield",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_better_admin_arrayfield",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "djoser",
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",
    "user",
    "configuration",
    "utils",
    "post",
    "notification",
    "fcm_django",
    "versatileimagefield",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dreamer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "dreamer.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/backend_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "backend_static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AUTHENTICATION_BACKENDS = (
    "rest_framework_social_oauth2.backends.DjangoOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework_social_oauth2.authentication.SocialAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "utils.paginator.DreamerPaginator",
    "PAGE_SIZE": 30,
    "EXCEPTION_HANDLER": "utils.rest_validation.dreamer_exception_handler",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_THROTTLE_RATES": {
        "file_upload_throttle": "100/day",
    },
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",  # <--- enable this one
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

FCM_DJANGO_SETTINGS = {
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "Dreamer",
    # Your firebase API KEY
    "FCM_SERVER_KEY": os.environ.get("FCM_SERVER_KEY", ""),
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}

DJOSER = {
    "SERIALIZERS": {"current_user": "user.serializers.UserSelfSerializer"},
    "HIDE_USERS": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
}

OAUTH2_PROVIDER = {
    # "SCOPES": {
    #     "read": "Read scope",
    #     "write": "Write scope",
    # },
    # "CLIENT_ID_GENERATOR_CLASS": "oauth2_provider.generators.ClientIdGenerator",
    # "CLIENT_ID_GENERATOR_CLASS": "oauth2_provider.generators.ClientIdGenerator",
    # "ACCESS_TOKEN_EXPIRE_SECONDS": 1,
}

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY", "")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET", "")
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email"}
CACHE_DEFAULT_TIME_OUT = 3600
CACHE_ENABLED = True

AUTH_USER_MODEL = "user.User"

if os.environ.get("IN_DOCKER"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DREAMER_DB_NAME"],
            "USER": os.environ["DREAMER_DB_USER"],
            "PASSWORD": os.environ["DREAMER_DB_PASS"],
            "PORT": os.environ["DB_PORT"],
            "HOST": os.environ["DB_SERVICE"],
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f'redis://{os.environ["REDIS_SERVICE"]}:{os.environ["REDIS_PORT"]}/',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
    CELERY_BROKER = "amqp://rabbitmq:5672"

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "dreamer",
            "USER": "dreamer",
            "PASSWORD": "dreamer",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
    CELERY_BROKER = "redis://localhost:6379"

f = os.path.join(BASE_DIR, "dreamer", "local_settings.py")
if os.path.exists(f):
    exec(open(f, "rb").read())
