from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50,  blank=True, null=True)
    birth_day = models.DateTimeField( blank=True, null=True)
    mobile = models.IntegerField( blank=True, null=True)

    def __str__(self):
        return self.user.username

def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=CustomUser)