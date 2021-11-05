from django.db import models
from django.contrib.auth.models import AbstractUser
from leadership.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.dispatch import receiver
from django.db.models.signals import post_save
from leadership.models import RedeemableItem,Wallet

# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=CASCADE,null=True,related_name='userprofile')
    image = models.ImageField(upload_to='profile_image', blank=True)
    gender = models.CharField(default='', blank=True, max_length=20)
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role==3:
            Student.objects.create(user=instance)
            Wallet.objects.create(owner=instance, choinBalance=20)

    else:
        pass





class Redeem(models.Model):
    student=models.ForeignKey(Student,on_delete=CASCADE,null=True)
    date_of_purchase=models.DateField(null=True)


class RewardedItem(models.Model):
    reward=models.ForeignKey(RedeemableItem,on_delete=SET_NULL, null=True,blank=False)
    order=models.ForeignKey(Redeem,on_delete=SET_NULL ,null=True,blank=False)
    quantity=models.PositiveSmallIntegerField(null=True,blank=False)

    def calculate_total(self):
        total_price=self.reward.item_value*self.quantity
        return total_price

