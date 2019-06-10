from django.urls import path
from . import views
from .views import redirect_view

urlpatterns = [
	path('', views.index, name='index'),
	path('search', views.search, name='search'),
	path('new', views.new_shipment, name='new_shipment'),
	path('new_shipment_submit', views.new_shipment_submit, name='new_shipment_submit'),
	path('redirect', redirect_view),
	path('shipments/<str:shipment_id>', views.spec_shipment, name='spec_shipment'),
	path('customers/<int:cust_id>/<str:cust_role>/shipments/<str:shipment_id>', views.spec_shipment, name='spec_shipment'),
]
