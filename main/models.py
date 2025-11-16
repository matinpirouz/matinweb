from django.db import models

class page(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    page_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    