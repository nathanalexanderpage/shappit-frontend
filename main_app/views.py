from django.shortcuts import render
from django.http import HttpResponse

site_company = 'Shappit'

def index(request):
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
