# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='avatar')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='user', related_name='profile')
    git = models.URLField(max_length=100, blank=True, null=True, verbose_name='link')
    bio = models.TextField(max_length=2000, null=True, blank=True, verbose_name='bio')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
