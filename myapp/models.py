from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra registration data that Django's built-in User doesn't have."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField()

    def __str__(self):
        return self.user.get_username()
