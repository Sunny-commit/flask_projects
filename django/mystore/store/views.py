from django.shortcuts import render
from django.http import HttpResponse
from .product import Product
def home(request):
    products=Product.objects.all()
    return render(request,'index.html',{'product':products})
    
# Create your views here.
