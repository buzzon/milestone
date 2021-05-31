from django.urls import path, include

from user_manager import views

app_name = 'user_manager'
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('update/', views.user_update, name='user_update'),
]
