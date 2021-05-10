from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('space/', views.space, name='space-list'),
    path('space/create/', views.SpaceCreate.as_view(), name='space-create'),
    path('space/<int:pk>/change/', views.space_detail, name='space-detail'),
    path('space/<int:pk>/add_task/', views.task_create, name='space_task_create'),
]
