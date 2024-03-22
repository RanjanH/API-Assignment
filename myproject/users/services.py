from .models import User

def create_user(uname, email, password, fname, lname):
    return User.objects.create(username=uname, email=email, password=password,fname=fname,lname=lname)

def update_user(pk, data):
    user = User.objects.get(id=pk)
    if data['username']:
        user.username = data['username']
    if data['email']:
        user.email = data['email']
    if data['password']:
        user.password = data['password']
    if data['fname']:
        user.fname = data['fname']
    if data['lname']:
        user.lname = data['lname']
    user.save()
    return user

def delete_user(user_id):
    User.objects.filter(id=user_id).delete()

def get_user(user_id):
    return User.objects.get(id=user_id)

def get_all_users():
    return User.objects.all()
