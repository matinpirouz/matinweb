import os
import sys
import django
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matinweb.settings")
django.setup()
from main.models import Province, City

province_url = 'http://prayer.aviny.com/api/province'
city_url = 'http://prayer.aviny.com/api/city'

provinces = requests.get(province_url)
cities = requests.get(city_url)

if provinces.status_code == 200 and cities.status_code == 200:
    for this_province in provinces.json():
        Province.objects.update_or_create(
            code = this_province['Code'],
            country_code = this_province['Country_Code'],
            center_city_code = this_province['Center_City_Code'],
            l_name = this_province['LName'],
            name = this_province['Name'],
        )
    for this_city in cities.json():
        if this_city['Country_Code'] == 1:
            prov = Province.objects.get(code=this_city['Province_Code'])
            City.objects.update_or_create(
                code = this_city['Code'],
                country_code = this_city['Country_Code'],
                l_name = this_city['LName'],
                name = this_city['Name'],
                province = prov,
            )
        else:
            continue
