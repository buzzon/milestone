from django.urls import path
from mscore.api import views

urlpatterns = [
    path('spaces/', views.SpaceList.as_view(), name='spaces-list'),
    path('spaces/<int:pk>/', views.SpaceDetail.as_view(), name='spaces-detail'),
]
