from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Contact, Orders

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

    # Fetching the Checkout details from the form
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')

        # Adding data to the model
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()

        thank = True
        oid = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank, 'id':oid})

    return render(request,'shop/checkout.html')
    # return HttpResponse("We are at checkout page.")
