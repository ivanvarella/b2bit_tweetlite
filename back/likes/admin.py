from django.contrib import admin
from likes.models import Like
from django.utils.translation import gettext_lazy as _


class LikeAdmin(admin.ModelAdmin):
    model = Like

    # Display the desired fields in the likes list
    list_display = (
        "user",  # User who liked
        "tweet",  # Tweet that received the like
        "created_at",  # Creation date of the like
    )

    # Allow searching by usernames of users who liked
    search_fields = (
        "user__username",
        "tweet__content",
    )  # Assuming there is a content field in the Tweet model

    # Filter by the creation date of the like
    list_filter = ("created_at",)

    # Define which fields will be displayed in the Like detail form
    fieldsets = (
        (None, {"fields": ("tweet",)}),  # The user field is not editable
        (
            _("Important dates"),
            {
                "fields": ("created_at",),
                "classes": ("collapse",),  # Collapse the section if necessary
            },
        ),
    )

    # Fields for sorting the objects in the admin
    ordering = ("created_at",)

    # Make the user and tweet fields read-only
    def get_readonly_fields(self, request, obj=None):
        # Here, we also make 'created_at' read-only
        readonly_fields = ["user", "tweet", "created_at"]
        return readonly_fields


# Register the Like model in the admin
admin.site.register(Like, LikeAdmin)
