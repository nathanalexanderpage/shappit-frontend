from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('search', views.index, name='index'),
	path('new', views.new_shipment, name='new_shipment'),
]
