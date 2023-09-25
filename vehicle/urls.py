from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r"su_vehicles", views.SuperUserVehicleViewSet)
router.register(r"user_vehicles", views.UserVehicleViewSet, basename="Vehicles")
