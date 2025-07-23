from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='analytics'),
    path('api/stats/', views.dashboard_stats_api, name='stats_api'),
    path('api/connections/', views.live_connections_api, name='connections_api'),
]