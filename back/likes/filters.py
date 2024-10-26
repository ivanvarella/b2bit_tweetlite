from dj_rql.filter_cls import AutoRQLFilterClass
from likes.models import Like


class LikeFilterClass(AutoRQLFilterClass):
    MODEL = Like

    # Defining filters for the Like model
    FILTERS = [
        {
            "filter": "user",
            "source": "user__username",
        },  # Filters by the username of the user who liked the tweet
        {
            "filter": "tweet",
            "source": "tweet__id",
        },  # Filters by the ID of the tweet that was liked
        {
            "filter": "created_at",
            "source": "created_at",
        },  # Filters by the creation date of the like
    ]
