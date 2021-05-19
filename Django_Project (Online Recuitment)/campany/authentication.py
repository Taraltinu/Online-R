from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import MyUser

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        MyUser = get_user_model()
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None