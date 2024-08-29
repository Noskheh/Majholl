from django.shortcuts import render
from django.http import HttpRequest , HttpResponse 
from django.template import loader
from .models import products

# Create your views here.


def load_product(request):
    products_ = products.objects.all() 
    template = loader.get_template('products.html')
    products_list = []
    for i in products_:
        i.data_limit = int(i.data_limit)
        i.pro_cost = format(i.pro_cost , ',')
        products_list.append(i)
    context = {'products' : products_list}
    return HttpResponse(template.render(context , request))



def load_product_details(request , id):
    products_ = products.objects.get(id = int(id))
    template = loader.get_template('product_details.html')
    products_.data_limit = int(products_.data_limit)
    products_.pro_cost = format(products_.pro_cost , ',')
    context = {'pro_detail' : products_}
    return HttpResponse(template.render(context , request))