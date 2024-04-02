from .models import User
from django.core.cache import cache
from time import sleep

# Normal API Services

class normalServices:
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return {'error':'User does not exist'}

    def get_all_users(self):
        users = User.objects.all()
        if len(users) > 0:
            return users
        else:
            return {'message':'No users registered till now'}

    def create_user(self, uname, email, fname, lname, url=None):
        user = User.objects.create(username=uname, email=email, fname=fname, lname=lname)
        user.save()
        return user

    def update_user(self, pk, data):
        user = self.get_user(pk)
        if hasattr(user,'keys'):
            return user
        if data['username']:
            user.username = data['username']
        if data['email']:
            user.email = data['email']
        if data['fname']:
            user.fname = data['fname']
        if data['lname']:
            user.lname = data['lname']
        user.save()
        return user

    def delete_user(self, user_id):
        User.objects.filter(id=user_id).delete()
        return {'message':'User Deleted'}

NormalServices = normalServices()

# Cache services

class cacheServices:
    def store_data_in_cache(self, pk, data):
        if pk:
            cache.set(pk, data, timeout=300)
        else:
            user = NormalServices.create_user(data['username'], data['email'], data['fname'], data['lname'])
            cache.set(user.id, data, timeout=300)
            return user

    def retrieve_data_from_cache(self, pk):
        data = cache.get(pk)
        if data is not None:
            # Data exists in cache
            return data,True
        else:
            # Data doesn't exist in cache or has expired
            data = NormalServices.get_user(pk)
            if hasattr(data,'keys'):
                return data
            self.store_data_in_cache(pk,data)
            return data,False
            
    def update_user_cache(self, pk, data):
        self.delete_user_cache(pk)
        NormalServices.update_user(pk, data)
        user = self.retrieve_data_from_cache(pk)
        return user
            
    def delete_user_cache(self, pk):
        if cache.get(pk) is not None:
            cache.delete(pk)
            return {'message':'Deleted user data from cache'}
        else:
            return {'message':'User data does is not stored in cache'}
        

# Sharding services

class shardServices:
    def get_user(self, pk):
        try:
            if pk % 2 == 0:
                user = User.objects.using('shard_a').get(id=pk)
            else:
                user = User.objects.using('shard_b').get(id=pk)
            return user
        except User.DoesNotExist:
            return {'error':'User Not Found'}

    def get_all_users(self):
        users_a = User.objects.using('shard_a').all()
        users_b = User.objects.using('shard_b').all()
        if len(users_a) > 0 or len(users_b) > 0:
            return users_a, users_b
        else:
            return {'message':'No users registered till now'},{}
    
    def update_user(self, user, data):
        if data['username']:
            user.username = data['username']
        if data['email']:
            user.email = data['email']
        if data['fname']:
            user.fname = data['fname']
        if data['lname']:
            user.lname = data['lname']
        user.save()
        return user
    
    def store_data_in_cache(self, pk, data):
        if pk:
            cache.set('shard'+str(pk), data, timeout=300)
        else:
            user = NormalServices.create_user(data['username'], data['email'], data['fname'], data['lname'])
            cache.set(user.id, data, timeout=300)
            return user

    def retrieve_data_from_cache(self, pk):
        data = cache.get('shard' + str(pk))
        if data is not None:
            # Data exists in cache
            return data,True
        else:
            # Data doesn't exist in cache or has expired
            try:
                data = self.get_user(pk)
                self.store_data_in_cache(pk,data)
                return data,False
            except User.DoesNotExist:
                return {'error':'User Does Not Exist'}
            
    def delete_user_cache(self, pk):
        if cache.get('shard' + str(pk)) is not None:
            cache.delete('shard' + str(pk))
            return {'message':'Deleted user data from cache'}
        else:
            return {'message':'User data does is not stored in cache'}
        
    def update_user_cache(self, pk, data):
        print(self.update_user(self.get_user(pk), data))
        self.delete_user_cache(pk)
        user,flag = self.retrieve_data_from_cache(pk)
        print(flag)
        return user