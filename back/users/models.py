from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from follows.models import Follow


class CustomUser(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)  # unique
    bio = models.TextField(_("Biography"), blank=True, null=True)
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to="profile_pics/", blank=True, null=True
    )

    USERNAME_FIELD = "email"  # Email as the primary identifier
    REQUIRED_FIELDS = ["username"]  # Remains mandatory

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
