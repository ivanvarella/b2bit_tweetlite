from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Display the desired fields in the user list
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "first_name", "last_name", "bio")
    list_filter = ("is_staff", "is_active")

    # Define which fields will be displayed in the user detail form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal Information"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "bio",
                    "profile_picture",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Define which fields will be available when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "bio",
                    "profile_picture",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    # Fields for ordering objects in the admin
    ordering = ("username",)


# Register CustomUser in the admin
admin.site.register(CustomUser, CustomUserAdmin)
