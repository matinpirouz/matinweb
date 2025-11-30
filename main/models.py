from django.db import models

class page(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    page_url = models.CharField(max_length=50)
    internal_link = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    