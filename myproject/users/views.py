#from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import User
from .serializers import userSerializer
from .services import create_user, update_user, delete_user, get_user, get_all_users

def users(request):
    return HttpResponse("Hello There!")

class normal(APIView):

    def get(self, request, pk=None):
        try:
            if pk:
                user = User.objects.get(pk=pk)
                serializer = userSerializer(user)
                return Response(serializer.data)
            else:
                users = User.objects.all()
                serializer = userSerializer(users,many=True)
                return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error':'User Not Found'})
        
    def post(self, request):
        data = request.data
        try:
            user = create_user(data['username'], data['email'], data['password'], data['fname'], data['lname'])
            return Response({'message': 'User created successfully', 'user_id': user.id})
        except Exception as e:
            return Response({"error":str(e)})
        
    def put(self, request, pk):
        data = request.body
        user = update_user(data)
        return Response({'message':'User Updated successfully', 'username':user.username,'fname':user.fname,'lname':user.lname})

class caching(APIView):

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
