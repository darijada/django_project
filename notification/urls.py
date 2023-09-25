from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(
    r"seen_user_notifications",
    views.SeenUserNotificationsViewSet,
    basename="Users seen notifications",
)
router.register(
    r"all_user_notifications",
    views.AllUserNotificationsViewSet,
    basename="All users notification",
)
