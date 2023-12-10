from django.urls import include, path
from rest_framework.routers import DefaultRouter

from task.views import TaskViewSet, SubTaskViewSet

task_router = DefaultRouter()
sub_task_router = DefaultRouter()

task_router.register("task", TaskViewSet, basename="task")
sub_task_router.register("sub-task", SubTaskViewSet, basename="sub-task")
urlpatterns = [
    path('', include(task_router.urls)),
    path('', include(sub_task_router.urls)),
]