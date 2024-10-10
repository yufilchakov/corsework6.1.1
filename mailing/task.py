from django.core.cache import cache
from config.settings import CACHE_ENABLED
from mailing.models import Mailing


def get_index_from_cache():
    """Получает данные главной страницы из кэша, если кэш пуст, то поучает данные из базы данных."""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'index'
    mailing = cache.get(key)
    if mailing is not None:
        return mailing
    mailing = Mailing.objects.select_related(
        'index').all()
    cache.set(key, mailing, 3600)
    return mailing
