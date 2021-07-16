from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = CloudinaryField('images')
    bio = models.TextField(max_length=500, blank=True)
    contact = models.CharField(max_length=30, blank=True)  
    # email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    image = CloudinaryField('images')
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    url = models.URLField(blank=True)
    description = models.TextField(max_length=300, blank=True)  
    date = models.DateTimeField(auto_now_add=True)
     # rating = models.ManyToManyField(User, related_name='votes', blank=True)
