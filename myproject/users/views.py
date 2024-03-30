#from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import User
from .serializers import userSerializer
from .services import shardServices, normalServices, cacheServices
from django.core.exceptions import BadRequest

NormalServices = normalServices()
ShardServices = shardServices()
CacheServices = cacheServices()

def users(request):
    return HttpResponse("Hello There!")

# Normal API
class normal(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                user = NormalServices.get_user(pk)
                if hasattr(user,'keys'):
                    return Response(user)
                serializer = userSerializer(user)
                return Response(serializer.data)
            else:
                users = NormalServices.get_all_users()
                if hasattr(users,'keys'):
                    return Response(users)
                serializer = userSerializer(users,many=True)
                return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error':'User Not Found'})
        
    def post(self, request):
        data = request.data
        try:
            if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
                return Response({'error':'User already exists'})
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
                user = NormalServices.create_user(data['username'], data['email'], data['fname'], data['lname'])
                return Response({'message': 'User created successfully', 'user_id': user.id})
        except:
            raise BadRequest('Invalid request.')
        
    def put(self, request, pk):
        msg = NormalServices.update_user(pk=pk, data=request.data)
        if hasattr(msg, 'keys'):
            return Response(msg)
        return Response({'message':'User Updated successfully', 'username':msg.username,'fname':msg.fname,'lname':msg.lname})
        
    def delete(self, request, pk):
        try:
            User.objects.get(id=pk)
            return Response(NormalServices.delete_user(pk))
        except User.DoesNotExist:
            return Response({'error':'User does not exist'})

# Caching API
class caching(APIView):
    def get(self, request, pk=None):
        if pk:
            data,flag = CacheServices.retrieve_data_from_cache(pk=pk)
            if hasattr(data,'keys'):
                    return Response(data)
            serialized = userSerializer(data)
            return Response([serialized.data,{'Found in cache':flag}])
        else:
            return Response(data="Invalid request - Add user id after 'caching/' ", status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        data = request.data
        try:
            if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
                return Response({'error':'User already exists'})
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
                user = CacheServices.store_data_in_cache(pk=0,data=data)
                return Response({'message': 'User created successfully', 'user_id': user.id})
        except:
            raise BadRequest('Invalid request.')
        
    def delete(self, request, pk):
        try:
            User.objects.get(id=pk)
            return Response(NormalServices.delete_user(pk))
        except User.DoesNotExist:
            return Response({'error':'User does not exist'})


# Sharding API
class sharding(APIView):
    class normal(APIView):
        def get(self, request, pk=None):
            try:
                if pk:
                    user = ShardServices.get_user(pk)
                    if hasattr(user,'keys'):
                        return Response(user)
                    serializer = userSerializer(user)
                    return Response(serializer.data)
                else:
                    users_a, users_b = ShardServices.get_all_users()
                    if hasattr(users_a,'keys'):
                        return Response(users)
                    serializer_a = userSerializer(users_a,many=True)
                    serializer_b = userSerializer(users_b,many=True)
                    data = []
                    if len(serializer_a.data) > 0:
                        for i in serializer_a.data:
                            data.append(i)
                    if len(serializer_b.data) > 0:
                        for i in serializer_b.data:
                            data.append(i)
                    return Response(data=data)
            except User.DoesNotExist:
                return Response({'error':'User Not Found'})
            
        def post(self, request):
            data = request.data
            try:
                if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
                    return Response({'error':'User already exists'})
                else:
                    raise User.DoesNotExist
            except User.DoesNotExist:
                    user = NormalServices.create_user(data['username'], data['email'], data['fname'], data['lname'])
                    return Response({'message': 'User created successfully', 'user_id': user.id})
            except:
                raise BadRequest('Invalid request.')
            
        def put(self, request, pk):
            user = shardServices.get_user(pk)
            if hasattr(user,'keys'):
                return Response(user)
            data = request.data
            user = shardServices.update_user(user, data)
            return Response({'message':'User Updated successfully', 'username':user.username,'fname':user.fname,'lname':user.lname})
            
        def delete(self, request, pk):
            try:
                if pk % 2 == 0:
                    user = User.objects.using('shard_a').get(id=pk)
                    user.delete()
                    NormalServices.delete_user(pk)
                else:
                    user = User.objects.using('shard_b').get(id=pk)
                    user.delete()
                    NormalServices.delete_user(pk)
                return Response({'message':'User Deleted'})
            except User.DoesNotExist:
                return Response({'error':'User does not exist'})
            
    class caching(APIView):
        def get(self, request, pk=None):
            if pk:
                data,flag = ShardServices.retrieve_data_from_cache(pk=pk)
                if hasattr(data,'keys'):
                        return Response(data)
                serialized = userSerializer(data)
                return Response([serialized.data,{'Found in cache':flag}])
            else:
                return Response(data="Invalid request - Add user id after 'caching/' ", status=status.HTTP_400_BAD_REQUEST)
            
        def post(self, request):
            data = request.data
            try:
                if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
                    return Response({'error':'User already exists'})
                else:
                    raise User.DoesNotExist
            except User.DoesNotExist:
                    user = CacheServices.store_data_in_cache(pk=0,data=data)
                    return Response({'message': 'User created successfully', 'user_id': user.id})
            except:
                raise BadRequest('Invalid request.')
            
        def delete(self, request, pk):
            try:
                User.objects.get(id=pk)
                return Response(NormalServices.delete_user(pk))
            except User.DoesNotExist:
                return Response({'error':'User does not exist'})
