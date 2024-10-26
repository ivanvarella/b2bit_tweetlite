from dj_rql.filter_cls import AutoRQLFilterClass
from tweets.models import Tweet


class TweetFilterClass(AutoRQLFilterClass):
    MODEL = Tweet

    # Defining filters for the Tweet model
    FILTERS = [
        {
            "filter": "author",
            "source": "author__username",
        },  # Filters by the author's username
        {
            "filter": "author_id",
            "source": "author_id__id",
        },  # Filters by author`s ID
        {
            "filter": "created_at",
            "source": "created_at",
        },  # Filters by the creation date of the tweet
    ]
