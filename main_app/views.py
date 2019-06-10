from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from pprint import pprint
import json

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

# SEARCH
def search(request):
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
    pprint(send_data)
    try:
        cust_no = send_data['cust-name']
    except:
        response = redirect(f'/')
        return response
    pprint(cust_no)
    if send_data['by'] == 'pro':
        ext = send_data['pro']
        response = redirect(f'/shipments/{ext}')
        return response
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
    elif send_data['by'] == 'shipper':
        print('shipper search')
        cust_details = requests.get(f'{API_URL}/customer/{cust_no}/shipper/shipments').json()
        # print(cust_details)
        pprint(cust_details)
        pprint(cust_details[0])
        data = json.loads(cust_details)
        pprint(data)
        pprint(data[0])

        if cust_details:
            # remove if time crunch
            # pprint(cust_details)
            return render(
                request,
                'ship_by_cust.html',
                {
                    'site_company': site_company,
                    'permissions_level': user_permissions,
                    'shipments': data,
                }
            )
    elif send_data['by'] == 'consignee':
        print('consignee search')
        cust_details = requests.get(f'{API_URL}/customer/{cust_no}/consignee/shipments').json()
        # print(cust_details)
        pprint(cust_details)
        pprint(cust_details[0])
        data = json.loads(cust_details)
        pprint(data)
        pprint(data[0])

        if cust_details:
            # remove if time crunch
            # pprint(cust_details)
            return render(
                request,
                'ship_by_cust.html',
                {
                    'site_company': site_company,
                    'permissions_level': user_permissions,
                    'shipments': data,
                }
            )
    elif send_data['by'] == 'billto':
        print('billto search')
        cust_details = requests.get(f'{API_URL}/customer/{cust_no}/billto/shipments').json()
        # print(cust_details)
        pprint(cust_details)
        pprint(cust_details[0])
        data = json.loads(cust_details)
        pprint(data)
        pprint(data[0])

        if cust_details:
            # remove if time crunch
            # pprint(cust_details)
            return render(
                request,
                'ship_by_cust.html',
                {
                    'site_company': site_company,
                    'permissions_level': user_permissions,
                    'shipments': data,
                }
            )
    response = redirect(f'/')
    return response

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
    try:
        shipment_id = int(shipment_id)
    except:
        response = redirect(f'/')
        return response
    if shipment_id < 1:
        response = redirect(f'/')
        return response
    try:
        shipment_details = requests.get(f'{API_URL}/shipment/{shipment_id}').json()
        detail_keys = requests.get(f'{API_URL}/new_shipment_info').json()
    except:
        return render(
            request,
            'spec_shipment.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
            }
        )
    print(shipment_details)
    print('detail_keys')
    pprint(detail_keys)
    print('detail_keys[cust_serializer]')
    pprint(detail_keys['cust_serializer'])
    loc_list = detail_keys['serv_cent_serializer']
    pro_origin = [loc for loc in loc_list if loc['id'] in [shipment_details['origin']]]
    pro_destination = [loc for loc in loc_list if loc['id'] in [shipment_details['destination']]]
    cust_list = detail_keys['cust_serializer']
    pro_shipper = [cust for cust in cust_list if cust['id'] in [shipment_details['shipper']]]
    pro_consignee = [cust for cust in cust_list if cust['id'] in [shipment_details['consignee']]]
    pro_billto = [cust for cust in cust_list if cust['id'] in [shipment_details['billto']]]
    if shipment_details:
        return render(
            request,
            'spec_shipment.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
                'pro': shipment_details,
                'keys': detail_keys,
                'pro_origin': pro_origin[0],
                'pro_destination': pro_destination[0],
                'pro_shipper': pro_shipper[0],
                'pro_consignee': pro_consignee[0],
                'pro_billto': pro_billto[0]
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
