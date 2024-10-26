from dj_rql.filter_cls import AutoRQLFilterClass
from users.models import CustomUser


class CustomUserFilterClass(AutoRQLFilterClass):
    MODEL = CustomUser

    FILTERS = [{"filter": "user", "source": "username"}]
