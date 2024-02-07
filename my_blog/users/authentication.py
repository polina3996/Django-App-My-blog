from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    # changing the base method used for USERNAME
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Getting a current user on his email"""
        user_model = get_user_model()
        try:
            # getting a User using base parameter 'username' as Email
            user = user_model.objects.get(email=username)
            # checking if the password is correct
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            # no users for this email or many users for this email
            return None

    def get_user(self, user_id):
        """Getting a current user on his id"""
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            # user not found
            return None
