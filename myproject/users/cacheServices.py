from django.core.cache import cache
from .services import get_user
from .models import User

def store_data_in_cache(pk,data):
    cache_data = {}
    for i in data.keys():
        cache_data[i] = data[i]
    cache.set(pk, data, timeout=300)

def retrieve_data_from_cache(pk):
    data = cache.get(pk)
    if data is not None:
        # Data exists in cache
        return data
    else:
        # Data doesn't exist in cache or has expired
        try:
            data = get_user(pk)
            return data
        except User.DoesNotExist:
            return {'error':'User Does Not Exist'}
        