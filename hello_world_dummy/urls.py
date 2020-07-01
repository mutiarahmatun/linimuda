from django.contrib import admin
from django.urls import path, include
from hello_world_dummy import views

from .views import hello

app_name = 'hello_world_dummy'

urlpatterns = [
    path('', hello, name="hello")
]