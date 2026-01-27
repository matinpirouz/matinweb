from django.contrib import admin
from .models import Page, Province, City

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'l_name')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_province_name', 'code')
    search_fields = ('name', 'l_name')
    list_filter = ('province',)

    def get_province_name(self, obj):
        return obj.province.name
    get_province_name.short_description = 'استان'

admin.site.register(Page)
