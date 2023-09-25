from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r"task_status", views.TaskStatusViewSet)
router.register(r"task_type", views.TaskTypeViewSet)
router.register(
    r"transportation_tasks",
    views.TransportationTasksViewSet,
    basename="Transportation Tasks",
)
router.register(
    r"transportation_task",
    views.SingleTransportationTaskViewSet,
    basename="Transportation Task",
)
router.register(r"storage_tasks", views.StorageTasksViewSet, basename="Storage Tasks")
router.register(
    r"storage_task", views.SingleStorageTaskViewSet, basename="Storage Task"
)
router.register(
    r"shipping_tasks", views.ShippingTasksViewSet, basename="Shipping Tasks"
)
router.register(
    r"shipping_task", views.SingleShippingTaskViewSet, basename="Shipping Task"
)
