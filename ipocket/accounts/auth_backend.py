from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model 
from accounts.models import MyUser


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self,request,mobile_number):
        
        User = get_user_model()
        
        try:
            user = User.objects.filter(mobile_number=mobile_number)
            return user

        except User.DoesNotExist:
            return None 

