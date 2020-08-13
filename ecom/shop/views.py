from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Contact, Orders, OrderUpdate

from math import ceil

import json

# Create your views here.

def index(request):

    allProds = []
    catprods = Product.objects.values('category','id')

    category_dict = {item['category'] for item in catprods}

    for category in category_dict:
        prod = Product.objects.filter(category=category)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

    
    params = {'allProds': allProds}
    return render(request,'shop/index.html', params)
    #return HttpResponse('Index Shop')

def about(request):
    return render(request,'shop/about.html')
    #return HttpResponse("We are at about page.")

def contact(request):
    thank = False

    # Fetching the Contact details from the form
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')

        # Adding data to the model
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

        # Provide message for successful submission
        thank = True
        
        
    return render(request,'shop/contact.html',{'thank':thank})
    # return HttpResponse("We are at contact page.")

def tracker(request):

    # Fetching the Order details from the form
    if request.method == "POST":
        # This time the values are fetched from formData variable in tracker.html's JS
        order_id = request.POST.get('order_id','')
        email = request.POST.get('email','')

        try:
            # Check whether order exists for the given id
            order = Orders.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                # If order exists, then convert updates in json and send
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                # If order doesn't exist
                return HttpResponse('{}')
        
        except Exception as e:
            return HttpResponse('{}')
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

        # Provide update once order is placed
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        # Provide final message for placed order
        thank = True
        oid = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank, 'id':oid})

    return render(request,'shop/checkout.html')
    # return HttpResponse("We are at checkout page.")
