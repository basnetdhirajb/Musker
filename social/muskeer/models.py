from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save #after saving something, we want to do something
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) #Associating one user to one profile
    #A profile can follow many other profiles
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    
    modifiedDate = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.user.username
     

#create profile when a new user signs up
@receiver(post_save, sender= User)   
def createProfile(sender,instance,created,**kwargs):
        if created:
            userProfile = Profile(user = instance)
            userProfile.save()
            #Have the user follow himself
            userProfile.follows.set([instance.profile.id])
            userProfile.save()

#post_save.connect(createProfile, sender=User)