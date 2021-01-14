import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = True

ALLOWED_HOSTS = ["dreamer.stickergramapp.com"]
sentry_sdk.init(
    dsn="https://d683d6882f5f4850b6dcbd174d192b7f@sentry.stickergramapp.com//2",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
