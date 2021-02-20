from django.urls import path
from mscore.api import views

urlpatterns = [
    path('spaces/', views.space_list),
    path('spaces/<int:pk>/', views.space_detail),
]
