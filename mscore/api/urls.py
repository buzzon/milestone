from django.urls import path
from mscore.api import views
from mscore.api.views import api_root

urlpatterns = [
    path('', api_root, name='root-api'),
    path('space/', views.SpaceList.as_view(), name='space-list-api'),
    path('space/<int:pk>/change/', views.SpaceDetail.as_view(), name='space-detail-api'),
    path('task/', views.TaskList.as_view(), name='task_list_api'),
    path('task/period/', views.get_task_time_period, name='task_time_period_api'),
]
