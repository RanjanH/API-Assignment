#from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import User
from .serializers import userSerializer
from .services import create_user, update_user, delete_user, get_user, get_all_users
from django.core.exceptions import BadRequest
from .cacheServices import store_data_in_cache,retrieve_data_from_cache

def users(request):
    return HttpResponse("Hello There!")

class normal(APIView):

    def get(self, request, pk=None):
        try:
            if pk:
                user = get_user(pk)
                if 'error' in user.keys():
                    return Response(user)
                serializer = userSerializer(user)
                return Response(serializer.data)
            else:
                users = get_all_users()
                if 'message' in users.keys():
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
                user = create_user(data['username'], data['email'], data['password'], data['fname'], data['lname'])
                return Response({'message': 'User created successfully', 'user_id': user.id})
        except:
            raise BadRequest('Invalid request.')
        
    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            data = request.body
            user = update_user(pk, json.loads(data))
            return Response({'message':'User Updated successfully', 'username':user.username,'fname':user.fname,'lname':user.lname})
        except User.DoesNotExist:
            return Response({'error':'User Not Found'})

class caching(APIView):

    def get(self, request, pk=None):
        if pk:
            data = retrieve_data_from_cache(pk)
            serialized = userSerializer(data)
            return Response(serialized.data)
        else:
            return Response(data="Invalid request - Add user id after 'caching/' ", status=status.HTTP_400_BAD_REQUEST)
class sharding(APIView):

    def get(self, request, pk):
        try:
            users = User.objects.get(pk=pk)
            return Response({'username':users.username,'fname':users.fname,'lname':users.lname})
        except User.DoesNotExist:
            return Response({'error':'User Not Found'})
        
    def post(self,request):
        data = request.data
        user = create_user(data['username'], data['email'], data['password'], data['fname'], data['lname'])
        return Response({'message': 'User created successfully', 'user_id': user.id})
