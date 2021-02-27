from django.urls import path
from mscore.api import views
from mscore.api.views import api_root

urlpatterns = [
    path('', api_root, name='root-api'),
    path('space/', views.SpaceList.as_view(), name='space-list-api'),
    path('space/<int:pk>/change/', views.SpaceDetail.as_view(), name='space-detail-api'),
]
