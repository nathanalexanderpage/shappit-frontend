from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from pprint import pprint

API_URL = 'http://localhost:8000'
site_company = 'Shappit﹏'
test_user_permissions = 'employee'
user_permissions = test_user_permissions

def redirect_view(request):
    response = redirect('/')
    return response

# TOP
def index(request):
    print(request)
    if user_permissions == 'employee':
        customers_list = requests.get(f'{API_URL}/customers').json()
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
    shipment_detail_fields = requests.get(f'{API_URL}/new_shipment_info').json()
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

def new_shipment_submit(request):
    # print(request.body)
    decoded = request.body.decode('utf-8')
    # print(decoded)
    key_val_pair = decoded.split('&')
    # print(key_val_pair)
    send_data = {}
    for pair in key_val_pair:
        key_val_list = pair.split('=')
        # print(key_val_list)
        # print(key_val_list[0])
        key = key_val_list[0]
        # print(key_val_list[1])
        val = key_val_list[1]
        try:
            val = int(key_val_list[1])
        except:
            pass
        send_data.update({key:val})
    # print(send_data)
    shipment_post_result = requests.post(f'{API_URL}/shipment', data=send_data).json()
    print(shipment_post_result)
    reuse_fields = {}
    has_list = False
    for value in shipment_post_result.values():
        print(value)
        if type(value) is list:
            print('list')
            has_list = True
        else:
            print('not list')
    if has_list:
        response = redirect('/new',
        # can values be passed into redirects?
        passed_data={
            'alerts': [
                {
                    'format': 'red',
                    'tag': 'Operation failure',
                    'content': 'One or more fields were missing from initial form submit. Please re-check the form and try again.'
                }
            ]
        })
        return response
    else:
        shipment_id = shipment_post_result['id']
        response = redirect(f'/shipments/{shipment_id}')
        return response

def spec_shipment(request, shipment_id):
    shipment_details = requests.get(f'{API_URL}/shipment/{shipment_id}').json()
    print(shipment_details)
    if shipment_details:
        return render(
            request,
            'spec_shipment.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
                'pro': shipment_details
            }
        )
    return render(
        request,
        'index.html',
        {
            'site_company': site_company,
            'alerts': [
                {
                    'format': 'red',
                    'tag': shipment_details.status,
                    'content': 'One or more fields were missing from initial form submit. Please re-check the form and try again.'
                }
            ]
        }
    )
