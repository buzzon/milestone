from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('space/', views.space, name='space-list'),
    path('space/<int:pk>/change/', views.space_detail, name='space-detail'),
]

urlpatterns += [
    path('space/create/', views.SpaceCreate.as_view(), name='space_create'),
    # path(r'^space/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    # path(r'^space/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]