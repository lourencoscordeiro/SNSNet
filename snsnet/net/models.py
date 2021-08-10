from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
import datetime


class Health_Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField(unique=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    type = models.CharField(max_length=20)


class Health_Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    phone = models.IntegerField(unique=True)
    gender = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    work = models.ForeignKey(
        Health_Institution, on_delete=models.CASCADE, null=True, related_name='work')
    type = models.CharField(max_length=20)

    following_prof = models.ManyToManyField(
        'Health_Professional', related_name='%(class)s_following')
    following_inst = models.ManyToManyField(
        'Health_Institution', related_name='%(class)s_following')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/', blank=True)
    likes = models.IntegerField(default=0)
    inst_likers = models.ManyToManyField(
        'Health_Institution', related_name='%(class)s_workers')
    prof_likers = models.ManyToManyField(
        'Health_Professional', related_name='%(class)s_workers')
    time = models.DateTimeField('Data de publicação')

    def is_recent(self):
        return self.time >= timezone.now() - datetime.timedelta(days=2)
