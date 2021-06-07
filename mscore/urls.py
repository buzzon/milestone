from django.urls import path

from . import views

app_name = 'mscore'
urlpatterns = [
    path('', views.index, name='index'),
    # path('space/create/', views.space_create, name='space_create'),
    path('space/create/', views.SpaceCreateView.as_view(), name='space_create'),
    path('space/<int:pk>/gantt/', views.space_gantt, name='space_gantt'),
    path('space/<int:space_pk>/task/<int:task_pk>/change/', views.task_change, name='task_update'),


    path('space/<int:pk>/constructor/', views.space_constructor, name='space_constructor'),
    path('space/<int:pk>/edit/', views.space_edit, name='space_edit'),
    path('space/<int:pk>/task/create/', views.task_create, name='task_create'),
    path('space/<int:space_pk>/task/<int:task_pk>/nested_create/', views.task_nested_create, name='task_create'),

]
