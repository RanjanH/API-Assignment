import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..serializers import userSerializer

# initialize the APIClient app
client = Client()

class normalTest(TestCase):
    def setUp(self):
        User.objects.create(username='testing1',email='testing1@gmail.com',fname='test1',lname='really')
        User.objects.create(username='testing2',email='testing2@gmail.com',fname='test2',lname='really')
        User.objects.create(username='testing3',email='testing3@gmail.com',fname='test3',lname='really')
        User.objects.create(username='testing4',email='testing4@gmail.com',fname='test4',lname='really')

    def test_get_all_users(self):
        response = client.get(reverse('normal'))
        users = User.objects.all()
        serializer = userSerializer(users,many=True)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user(self):
        for i in range(1,5):
            user = User.objects.get(username='testing'+str(i))
            response = client.get(reverse('normal')+str(user.id))
            serializer = userSerializer(user)
            self.assertEqual(serializer.data,response.data)
            self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_post_user_pass(self):
        payload = {'username':'testing5','email':'testing5@gmail.com','password':'testing','fname':'test5','lname':'really'}
        response = client.post(reverse('normal'), data = json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_fail(self):
        payload = {'username':'testing1','email':'testing5@gmail.com','password':'testing','fname':'test5','lname':'really'}
        response = client.post(reverse('normal'), data = json.dumps(payload), content_type='application/json')
        data = {'error':'User already exists'}
        self.assertEqual(data, response.data)

    def test_put_user_pass(self):
        user = User.objects.get(username='testing1')
        payload = {'username':'testing10','email':None,'password':None,'fname':None,'lname':None}
        response = client.put(reverse('normal')+str(user.id), data = json.dumps(payload), content_type='application/json')
        user = User.objects.get(id=user.id)
        data = {'message':'User Updated successfully', 'username':user.username,'fname':user.fname,'lname':user.lname}
        self.assertEqual(data, response.data)

class cachingTest(TestCase):
    def setUp(self):
        User.objects.create(username='testing1',email='testing1@gmail.com',fname='test1',lname='really')
        User.objects.create(username='testing2',email='testing2@gmail.com',fname='test2',lname='really')
        User.objects.create(username='testing3',email='testing3@gmail.com',fname='test3',lname='really')
        User.objects.create(username='testing4',email='testing4@gmail.com',fname='test4',lname='really')

    def test_get_one_user(self):
        for i in range(1,5):
            user = User.objects.get(username='testing'+str(i))
            response = client.get(reverse('caching')+str(user.id))
            serializer = userSerializer(user)
            self.assertEqual(serializer.data, response.data[0])
            self.assertEqual(response.status_code, status.HTTP_200_OK)