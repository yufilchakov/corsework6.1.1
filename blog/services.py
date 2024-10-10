from django.core.cache import cache
from config.settings import CACHE_ENABLED
from blog.models import Blog


def get_blog_from_cache():
    """Получает данные блога из кэша, если кэш пуст, то поучает данные из базы данных."""
    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = 'blog_list'
    blog = cache.get(key)
    if blog is not None:
        return blog
    blog = Blog.objects.all()
    cache.set(key, blog)
    return blog
