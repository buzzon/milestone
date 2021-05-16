from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('space/', views.space, name='space_list'),
    path('space/create/', views.space_create, name='space_create'),
    path('space/<int:pk>/change/', views.space_detail, name='space_detail'),
    path('space/<int:pk>/edit/', views.space_edit, name='space_edit'),
    path('space/<int:pk>/task/create/', views.task_create, name='task_create'),
    path('space/<int:space_pk>/task/<int:task_pk>/change/', views.task_change, name='task_update'),
    path('user/change/', views.user_change, name='user_change'),
]
