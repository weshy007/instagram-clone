from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PIL import Image

from posts.models import Post


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_picture", null=True, default="static/default.png")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    favourite = models.ManyToManyField(Post, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} - Profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Signals connections
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
