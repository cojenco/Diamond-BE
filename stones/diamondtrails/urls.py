from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.apiOverview, name='api-overview'),
    path('trail/<str:external_id>/', views.trailDetail, name='trail-detail'),
    path('all-trails/<str:state_name>', views.allTrails, name='all-trails'),
    path('trail/<str:external_id>/live-update', views.liveUpdate, name='live-update'),
    path('trail/<str:external_id>/subscribe', views.subscribe, name='subscribe'),
    # path('all-trails/', views.allTrails, name='all-trails'),
]