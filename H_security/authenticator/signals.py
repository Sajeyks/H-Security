from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    

@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        
        email = instance.email
        if email.endswith('@hospital.staff.go.ke'):
            group, created = Group.objects.get_or_create(name='Hospital Staff Group')
            instance.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='Non-Staff Group')
            instance.groups.add(group)