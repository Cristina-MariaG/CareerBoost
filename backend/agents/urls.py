from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('agents/linkedin/', views.linkedin_generate),
    path('agents/cv/', views.cv_generate),
]
