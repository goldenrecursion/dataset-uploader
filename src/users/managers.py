from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

#Custom user model manager->
class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, godel_jwt, **extra_fields):
        if not username:
            raise ValueError(_('Users must have a username'))
        user = self.model(username=username, godel_jwt=godel_jwt**extra_fields)
        user.set_password(password)
        user.save()
        return user