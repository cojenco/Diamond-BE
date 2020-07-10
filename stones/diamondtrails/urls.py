from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.apiOverview, name='api-overview'),
    path('trail/<str:external_id>/', views.trailDetail, name='trail-detail'),
    path('all-trails/', views.allTrails, name='all-trails'),
]