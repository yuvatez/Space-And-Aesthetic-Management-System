from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator

def store(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     products = Product.objects.all()
     context = {'products':products, 'cartItems':cartItems}
     return render(request, 'store/store.html', context)


def cart(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     data = cartData(request)
     
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('Product:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
     else:
          customer, order = guestOrder(request, data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == order.get_cart_total:
          order.complete = True
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(
          customer=customer,
          order=order,
          address=data['shipping']['address'],
          city=data['shipping']['city'],
          state=data['shipping']['state'],
          zipcode=data['shipping']['zipcode'],
          )

     return JsonResponse('Payment submitted..', safe=False)

def contact(request):
     if request.method == 'POST':
          form = ContactForm(request.POST)
          if form.is_valid():
               subject = "Website Inquiry" 
               body = {
               'name': form.cleaned_data['name'], 
               'phone_number': form.cleaned_data['phone_number'], 
               'email': form.cleaned_data['email_address'],
               'height': form.cleaned_data['height'], 
               'width': form.cleaned_data['width'], 
               'depth': form.cleaned_data['depth'], 
               'material': form.cleaned_data['material'], 
               'color': form.cleaned_data['color'], 
               'message':form.cleaned_data['message'], 
               }
               message = "\n".join(body.values())

               try:
                    send_mail(subject, message, 'yuvatez745@gmail.com', ['yuvatez745@gmail.com']) 
               except BadHeaderError:
                    return HttpResponse('Invalid header found.')
      
     form = ContactForm()
     return render(request, "store/contact.html", {'form':form})

def productView(request):
     productId = data['productId']
     product = Product.objects.filter(id = productId)
     print(product)
     return render(request, "store/prodView.html", {'Product:', product[0]})

def search(request):
    if request.GET.get('myform'): # write your form name here      
        product =  request.GET.get('myform')      
        try:
            status = Product.objects.filter(id=productId)
            return render(request,"store/search.html",{"products":status})
        except:
            return render(request,"store/search.html",{'products':status})
    else:
        return render(request, 'store/search.html', {'products':status})
 
def pagination(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'main.html', {'products': products})