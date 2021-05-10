from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('space/', views.space, name='space_list'),
    path('space/create/', views.SpaceCreate.as_view(), name='space_create'),
    path('space/<int:pk>/change/', views.space_detail, name='space_detail'),
    path('space/<int:pk>/task/create/', views.task_create, name='task_create'),
    path('space/<int:space_pk>/task/<int:task_pk>/change/', views.task_change, name='task_update'),
]
