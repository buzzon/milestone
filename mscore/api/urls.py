from django.urls import path
from mscore.api import views

urlpatterns = [
    path('space/', views.SpaceList.as_view(), name='space-list-api'),
    path('space/<int:pk>/change/', views.SpaceDetail.as_view(), name='space-detail-api'),
]
