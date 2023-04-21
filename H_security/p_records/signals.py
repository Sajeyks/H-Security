from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import HealthRecord

User = get_user_model()

@receiver(post_save, sender=User)
def create_record(sender, instance, created, **kwargs):
    if created:
        try:
            HealthRecord.objects.create(owner=instance)
        except Exception:
            print(Exception)
        
@receiver(post_save, sender=User)
def save_record(sender, instance, **kwargs):
    instance.healthrecord.save()