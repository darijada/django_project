from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'cargo_type', views.CargoTypeViewSet)
router.register(r'task_status', views.TaskStatusViewSet)
router.register(r'task_type', views.TaskTypeViewSet)
router.register(r'transportation_task', views.TransportationTaskViewSet)
router.register(r'storage_task', views.StorageTaskViewSet)
router.register(r'shipping_task', views.ShippingTaskViewSet)
router.register(r'market_tasks', views.MarketTasksViewSet, basename='market_tasks')
