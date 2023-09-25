from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r"su_storages", views.SuperUserStorageViewSet)
router.register(r"user_storages", views.UserStorageViewSet, basename="Storages")
