from django.db import models

class EquationImage(models.Model):
    image = models.ImageField(upload_to='equations/')
    uploaded_at = models.DateTimeField(auto_now_add=True)