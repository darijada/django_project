from django.contrib import admin
from django.urls import path, include

from base.urls import router as base_router
from notification.urls import router as notification_router
from service.urls import router as service_router
from storage.urls import router as storage_router
from task.urls import router as task_router
from user.urls import router as user_router
from vehicle.urls import router as vehicle_router

urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("base/", include(base_router.urls)),
    path("service/", include(service_router.urls)),
    path("storage/", include(storage_router.urls)),
    path("notification/", include(notification_router.urls)),
    path("task/", include(task_router.urls)),
    path("user/", include(user_router.urls)),
    path("vehicle/", include(vehicle_router.urls)),
    path("admin/", admin.site.urls),
]
