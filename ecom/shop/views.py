from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Contact

from math import ceil

# Create your views here.

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))

    allProds = []
    catprods = Product.objects.values('category','id')

    category_dict = {item['category'] for item in catprods}

    for category in category_dict:
        prod = Product.objects.filter(category=category)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

    #params = {'num_of_slides' : nSlides, 'range' : range(1,nSlides) ,'product' : products}
    # allProds = [[products, range(1,nSlides), nSlides],
    #             [products, range(1,nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request,'shop/index.html', params)
    #return HttpResponse('Index Shop')

def about(request):
    return render(request,'shop/about.html')
    #return HttpResponse("We are at about page.")

def contact(request):

    # Fetching the Contact details from the form
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')

        # Adding data to the model
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        
        
    return render(request,'shop/contact.html')
    # return HttpResponse("We are at contact page.")

def tracker(request):
    return render(request,'shop/tracker.html')
    # return HttpResponse("We are at tracker page.")

def search(request):
    return render(request,'shop/search.html')
    # return HttpResponse("We are at search page.")

def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    
    return render(request,'shop/prodview.html',{'product':product[0]})
    # return HttpResponse("We are at productview page.")

def checkout(request):
    return render(request,'shop/checkout.html')
    # return HttpResponse("We are at checkout page.")
