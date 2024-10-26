from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Tweet(models.Model):
    content = models.TextField(_("Tweet Content"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tweets",  # Suggested alternative
        verbose_name=_("Author"),
    )
    created_at = models.DateTimeField(_("Creation Date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update Date"), null=True)
    image = models.ImageField(
        _("Tweet Image"), upload_to="tweet_images/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}..."  # Displays the author and the first 30 characters of the content

    class Meta:
        verbose_name = _("Tweet")
        verbose_name_plural = _("Tweets")
        ordering = ["-created_at"]  # Sorts tweets from newest to oldest
