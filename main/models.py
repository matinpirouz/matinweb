from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    page_url = models.CharField(max_length=50)
    internal_link = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    
class Province(models.Model):
    code = models.BigIntegerField(unique=True)
    country_code = models.BigIntegerField()
    center_city_code = models.BigIntegerField()
    l_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
class City(models.Model):
    code = models.BigIntegerField(unique=True)
    country_code = models.BigIntegerField()
    l_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='citys')
    
    def __str__(self):
        return self.name