from django.contrib import admin
from follows.models import Follow
from django.utils.translation import gettext_lazy as _


class FollowAdmin(admin.ModelAdmin):
    model = Follow

    # Display the desired fields in the followers list
    list_display = (
        "follower",
        "following",
        "created_at",
    )

    # Allow searching by the usernames of followers and followed users
    search_fields = ("follower__username", "following__username")

    # Filter by the creation date of the relationship
    list_filter = ("created_at",)

    # Define which fields will be displayed in the details form of the Follow
    fieldsets = (
        (None, {"fields": ("following",)}),  # The follower field is not editable
        (
            _("Important Dates"),
            {
                "fields": ("created_at",),
                "classes": ("collapse",),  # Collapse the section if necessary
            },
        ),
    )

    # Fields for sorting objects in the admin
    ordering = ("created_at",)

    # Make the follower and following fields read-only
    def get_readonly_fields(self, request, obj=None):
        # Here, we also make 'created_at' read-only
        readonly_fields = ["follower", "following", "created_at"]
        return readonly_fields


# Register the Follow model in the admin
admin.site.register(Follow, FollowAdmin)
