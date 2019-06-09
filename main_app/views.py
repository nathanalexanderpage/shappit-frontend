from django.shortcuts import render
from django.http import HttpResponse
import requests
from pprint import pprint

site_company = 'Shappit'
test_user_permissions = 'employee'
user_permissions = test_user_permissions

# TOP
def index(request):
    print(request)
    if user_permissions == 'employee':
        customers_list = requests.get('http://localhost:8000/customers').json()
        alpha_cust_list = sorted(customers_list, key=lambda item: item['name'])
        return render(
            request,
            'index.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
                'customers_list': alpha_cust_list,
            }
        )
    elif user_permissions == 'customer':
        return render(
            request,
            'index.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
            }
        )
    return render(
        request,
        'index.html',
        {'site_company': site_company}
    )

# NEW SHIPMENT
def new_shipment(request):
    shipment_detail_fields = requests.get('http://localhost:8000/new_shipment_info').json()
    if shipment_detail_fields:
        return render(
            request,
            'new_shipment.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
                'shipment_detail_fields': shipment_detail_fields
            }
        )
    return render(
        request,
        'index.html',
        {
            'site_company': site_company,
        }
    )
