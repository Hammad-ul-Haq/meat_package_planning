from django.urls import path
from . import views

urlpatterns = [
    path("",views.capacity,name='input_data'),
    path("capacity/",views.capacity,name='capacity'),
    path("prodMeat/",views.prodMeat,name='prodMeat'),
    path("sequence/",views.sequence,name='sequence'),
    path("requirement/",views.requirement,name='requirement'),
    path("meat/", views.meat, name='meat'),
    path("meat_hourly/", views.meat_hourly, name='meat_hourly'),
]