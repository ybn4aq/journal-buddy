from django.db import models
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class UserProfile(models.Model):
    #one to one - each profile has one user, each user has one profile
    #on delete cascade - when a userProfile is deleted, so is the user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #user.profile
    hobbies = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def create_or_update_user_profile(user, **kwargs):
        #if profile doesn't exist, create one. otherwise, update it.
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=kwargs)
        #if profile already exists, update the info.
        if not created:
            for key, value in kwargs.items():
                setattr(profile, key, value)
            profile.save()

class Journal(models.Model):
    date = models.DateField
    content = models.CharField(max_length=500)
    rate = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    media = models.ImageField()

    def __str__(self):
        return "Date: " + self.date + "\nContent: " + self.content + "\nRate: " + self.rate