from django.db.models.signals import pre_delete
from django.dispatch import receiver
from users.models import CustomUser
import os


@receiver(pre_delete, sender=CustomUser)
def delete_user_image(sender, instance, **kwargs):
    """Delete the user's profile picture when the user is deleted."""
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            try:
                os.remove(instance.profile_picture.path)
            except (OSError, FileNotFoundError) as e:
                print(f"Error deleting user image: {e}")
