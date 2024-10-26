from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from tweets.models import Tweet
import os


# Manage the updated_at field
# - When creating a new, will be None
# - When updating, will get the current date and time
@receiver(pre_save, sender=Tweet)
def set_updated_at(sender, instance, **kwargs):
    if instance.pk is None:  # Checks if the tweet is being created
        instance.updated_at = None  # Sets to None when creating
    else:
        instance.updated_at = (
            timezone.now()
        )  # Updates to the current date and time when modifying


# Delete tweet image when tweet is deleted
@receiver(pre_delete, sender=Tweet)
def delete_tweet_image(sender, instance, **kwargs):
    """Delete the tweet's image when the tweet is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            try:
                os.remove(instance.image.path)
            except (OSError, FileNotFoundError) as e:
                print(f"Error deleting tweet image: {e}")
