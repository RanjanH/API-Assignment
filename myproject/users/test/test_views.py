import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..serializers import userSerializer


# initialize the APIClient app
client = Client()