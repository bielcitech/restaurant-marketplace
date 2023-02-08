from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('Le profile a été crée avec succès')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('Le profile a été mis à jour avec succès')
        except:
            UserProfile.objects.create(user=instance)
            print("Le profile n'existait pas, mais je l'ai créé avec succès")

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(f"L'utilisateur {instance.username} est entrain d'être créé")