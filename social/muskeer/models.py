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
    profileImage = models.ImageField(null=True, blank=True, upload_to= "images/")
    
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

#create model for status
class Meep(models.Model):
    user = models.ForeignKey(
        User, related_name = 'meeps', on_delete = models.DO_NOTHING
    )
    body = models.CharField(max_length = 200)
    createdAt = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return(
            f"{self.user} "
            f"({self.createdAt: %Y-%m-%d}): "
            f"{self.body}..."
        )
    