from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sync', views.sync, name='sync'),
    path('detail/<int:pokemon_id>', views.detail, name='detail'),
    path('sync_api/<int:pokemon_id>', views.sync_api, name='sync_api'),
    path('detail_api/<int:pokemon_id>', views.detail_api, name='detail_api'),
]