from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    def __str__(self):
        return self.username

'''class UserShard1(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class UserShard2(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    def __str__(self):
        return self.username
'''