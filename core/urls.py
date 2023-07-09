from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('quote/', views.quote, name='quote'),
    path('history/', views.history, name='history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]