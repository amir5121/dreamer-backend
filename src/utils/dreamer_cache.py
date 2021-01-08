from django.conf import settings
from django.core.cache import cache


def get_cache_or_set(key, lazy_value, timeout=settings.CACHE_DEFAULT_TIME_OUT):
    value = cache.get(key)
    if value is not None and settings.CACHE_ENABLED:
        return value
    value = lazy_value()
    cache.set(key, value, timeout)
    return value
