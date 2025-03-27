
from django.contrib import admin
from django.urls import path

from .views import *



urlpatterns = [
    path('', gantt_chart_index, name = 'gantt_chart_index'),
    path("get_data", fetchJsonData, name="fetchJsonData"),

]


