from dj_rql.filter_cls import AutoRQLFilterClass
from follows.models import Follow


class FollowFilterClass(AutoRQLFilterClass):
    MODEL = Follow

    # Defining filters for the Follow model
    FILTERS = [
        {
            "filter": "follower",
            "source": "follower__username",
        },  # Filters by the username of the follower
        {
            "filter": "following",
            "source": "following__username",
        },  # Filters by the username of the followed
        {
            "filter": "created_at",
            "source": "created_at",
        },  # Filters by the creation date of the follow
    ]
