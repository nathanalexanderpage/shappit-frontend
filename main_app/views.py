from django.shortcuts import render
from django.http import HttpResponse
import requests

site_company = 'Shappit'
test_user_permissions = 'customer'
user_permissions = test_user_permissions

def index(request):
    if user_permissions == 'employee':
        customers_list = requests.get('http://localhost:8000/customers/').json()
        return render(
            request,
            'index.html',
            {
                'site_company': site_company,
                'permissions_level': user_permissions,
                'customers_list': customers_list,
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
    return render(request, 'index.html', {'site_company': site_company})

def search(request):
    resp2 = requests.get('http://localhost:8000/customers/').json()
    if resp2:
        return render(request, 'index.html', {'site_company': site_company, 'cats': cats, 'resp2': resp2})
    return render(request, 'index.html', {'site_company': site_company, 'cats': cats})


class Cat:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

cats = [
    Cat('Lolo', 'tabby', 'foul little demon', 3),
    Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
    Cat('Raven', 'black tripod', '3 legged cat', 4)
]
