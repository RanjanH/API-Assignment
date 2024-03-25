from .models import User

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return {'error':'User does not exist'}

def get_all_users():
    users = User.objects.all()
    if len(users) > 0:
        return users
    else:
        return {'message':'No users registered till now'}

def create_user(uname, email, fname, lname, url=None):
    return User.objects.create(username=uname, email=email, fname=fname,lname=lname)

def update_user(pk, data):
    user = User.objects.get(id=pk)
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

def delete_user(user_id):
    User.objects.filter(id=user_id).delete()
    return {'message':'User Deleted'}
