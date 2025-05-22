from django.urls import path
from .views import generate_schedule_template

urlpatterns = [
    path('generate-schedule/', generate_schedule_template, name='generate_schedule'),
]