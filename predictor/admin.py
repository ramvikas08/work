from django.contrib import admin 
from .models import Prediction 
 
@admin.register(Prediction) 
class PredictionAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'cgpa', 'predicted_score', 'created_at'] 
    list_filter = ['created_at', 'internship'] 
    search_fields = ['user__username'] 
    readonly_fields = ['created_at'] 
    ordering = ['-created_at'] 