from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('space/', views.space, name='space-list'),
    path('space/<int:pk>/change/', views.space_detail, name='space-detail'),
]
