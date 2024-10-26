from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_users",  # References who is being followed
        verbose_name=_("Follower"),
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",  # References who is following
        verbose_name=_("Following"),
    )
    created_at = models.DateTimeField(_("Creation Date"), auto_now_add=True)

    # Dynamically calculates the follower and following counts
    @classmethod
    def get_followers_count(cls, user_id):
        return cls.objects.filter(
            following__id=user_id
        ).count()  # Count how many are following this user

    @classmethod
    def get_following_count(cls, user_id):
        return cls.objects.filter(
            follower__id=user_id
        ).count()  # Count how many users this one is following

    class Meta:
        verbose_name = _("Follow")
        verbose_name_plural = _("Follows")
        unique_together = (
            "follower",
            "following",
        )  # Ensures that a user cannot follow the same user more than once.

    def __str__(self):
        return f"{self.follower.username} is following {self.following.username}"
