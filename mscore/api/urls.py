from django.urls import path
from mscore.api import views
from mscore.api.views import api_root

app_name = 'mscore_api'
urlpatterns = [
    path('', api_root, name='root'),
    path('space/', views.SpaceList.as_view(), name='space_list'),
    path('space/<int:pk>/change/', views.SpaceDetail.as_view(), name='space_detail'),
    # path('task/', views.TaskList.as_view(), name='task_list'),


    path('task/change/', views.task_change, name='task_change'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/delete/', views.task_delete, name='task_delete'),
    path('task/period/', views.get_task_time_period, name='task_time_period_api'),
]
