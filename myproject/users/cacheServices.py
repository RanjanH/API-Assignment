from django.core.cache import cache
from .services import get_user
from .models import User

def store_data_in_cache(pk,data):
    cache_data = {}
    for i in data.keys():
        cache_data[i] = data[i]
    cache.set(pk, data, timeout=None)  # Set the data in cache with no timeout

def retrieve_data_from_cache(pk):
    data = cache.get(pk)
    if data is not None:
        # Data exists in cache
        return data
    else:
        # Data doesn't exist in cache or has expired
        try:
            print('-'*10,'\n','here\n','-'*10)
            data = get_user(pk)
            print('-'*10,'\n','here 22\n','-'*10)
            return data
        except User.DoesNotExist:
            return {'error':'User Does Not Exist'}
        