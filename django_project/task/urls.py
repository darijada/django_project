from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'cargo_type', views.CargoTypeViewSet)
router.register(r'task_status', views.TaskStatusViewSet)
router.register(r'task_type', views.TaskTypeViewSet)
router.register(r'task', views.TaskViewSet)