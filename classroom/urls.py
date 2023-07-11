from django.urls import path

from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.index, name='index'),
]