from django.urls import path, re_path

from . import views


urlpatterns = [
    path('health/', views.health, name='health'),
    path('unhealth/', views.unhealth, name='unhealth'),

    re_path(r'^bottles/$', views.BottleListView.as_view(), name='bottle-list'),
    re_path(r'^bottles/(?P<uuid>[\w\\-]+)/$', views.BottleDetailView.as_view(), name='bottle-detail'),
    re_path(r'^producers/(?P<uuid>[\w\\-]+)/$', views.ProducerDetailView.as_view(), name='producer-detail'),
    re_path(r'^locations/(?P<uuid>[\w\\-]+)/$', views.LocationDetailView.as_view(), name='location-detail'),

]
