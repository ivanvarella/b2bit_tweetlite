from django.contrib import admin
from tweets.models import Tweet
from django.utils.translation import gettext_lazy as _


class TweetAdmin(admin.ModelAdmin):
    model = Tweet

    # Display the desired fields in the tweet list
    list_display = (
        "author",
        "content",
        "created_at",
        "updated_at",
        "image",  # Adiciona o campo de imagem à lista de tweets
    )

    # Allow search by tweet content and author
    search_fields = ("content", "author__username")

    # Filters for the admin panel
    list_filter = ("created_at", "author")

    # Define which fields will be displayed in the Tweet detail form
    fieldsets = (
        (
            None,
            {"fields": ("author", "content", "image")},
        ),  # Adiciona 'image' aos campos do formulário
        (
            _("Important dates"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),  # 'updated_at' is kept editable
            },
        ),
    )

    # Fields for sorting objects in the admin
    ordering = ("-created_at",)

    # Limit the display of tweets in the list
    list_per_page = 20  # Number of tweets per page

    # Mark 'created_at' and 'updated_at' as read-only
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # Override the `get_readonly_fields` method to prevent editing of the `author` field after creation
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If the object already exists, prevent changing the `author` field
            return self.readonly_fields + ("author",)
        return self.readonly_fields


# Register the Tweet model in the admin
admin.site.register(Tweet, TweetAdmin)
