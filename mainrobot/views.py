from django.shortcuts import render
from django.http import HttpRequest , HttpResponse 
from django.template import loader
from .models import products

# Create your views here.


def load_product(request):
    products_ = products.objects.all() 
    template = loader.get_template('products.html')
    context = {'products' : products_}
    return HttpResponse(template.render(context , request))


def load_product_details(request , id):
    products_ = products.objects.get(id = int(id))
    template = loader.get_template('product_details.html')
    context = {'pro_detail' : products_}
    return HttpResponse(template.render(context , request))