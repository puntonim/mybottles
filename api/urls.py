from django.urls import path, re_path

from . import views


urlpatterns = [
    path('health/', views.health, name='health'),
    path('unhealth/', views.unhealth, name='unhealth'),

    re_path(r'^bottles/$', views.BottlesListView.as_view(), name='bottles-list'),
]
