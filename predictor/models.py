from django.db import models 
from django.contrib.auth.models import User 
 
class Prediction(models.Model): 
    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True 
    ) 
     
    # Input fields 
    cgpa = models.FloatField(help_text="CGPA (5.0 to 10.0)") 
    skills_score = models.IntegerField(help_text="Skills rating (1-10)") 
    projects = models.IntegerField(help_text="Number of projects") 
    internship = models.IntegerField(help_text="0=No, 1=Yes") 
    certifications = models.IntegerField(help_text="Number of certs") 
     
    # Output field 
    predicted_score = models.FloatField(help_text="Predicted score") 
     
    # Metadata 
    created_at = models.DateTimeField(auto_now_add=True) 
     
    def __str__(self): 
        return f"Prediction {self.id} - Score: {self.predicted_score:.2f}" 
     
    class Meta: 
        ordering = ['-created_at']