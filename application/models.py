from django.db import models
from django.contrib.auth.models import BaseUserManager, User


# Create your models here.

class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.is_active = True
        account.is_staff = True
        account.save()

        return account
    
    def create_normal_user(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = False
        account.is_active = True
        account.is_staff = False
        account.save()

        return account
    
