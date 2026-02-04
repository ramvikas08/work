from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_job_fit, name='predict'),
    path('history/', views.prediction_history, name='history'),
]
