from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_photos',blank=True)

    def __str__(self):
        return self.user.username

class CFSchedules(models.Model):
    cid = models.CharField(max_length=10,primary_key=True)
    cname = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)