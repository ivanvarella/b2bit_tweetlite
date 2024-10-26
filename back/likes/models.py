from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from tweets.models import Tweet


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="liked_tweets",  # Reference to the tweets that the user liked
        verbose_name=_("User"),
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name="likes",  # Reference to the likes associated with a tweet
        verbose_name=_("Tweet"),
    )
    created_at = models.DateTimeField(_("Creation Date"), auto_now_add=True)

    # Class method to count the likes of a specific tweet
    @classmethod
    def get_likes_count(cls, tweet_id):
        return cls.objects.filter(tweet__id=tweet_id).count()

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = (
            "user",
            "tweet",
        )  # Ensures that a user cannot like the same tweet more than once.

    def __str__(self):
        return f"{self.user.username} liked tweet {self.tweet.id}"
