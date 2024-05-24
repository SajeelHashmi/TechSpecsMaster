from django.shortcuts import render, redirect
from products.models import * 
from .models import Wishlist,Message
from django.http import JsonResponse
from recommendation_utils.utils import get_recommendation 
from .emailAlerts import sendMessage
from django.contrib import messages

sender="techspecsmaster@gmail.com"
# Create your views here.
def home(request):
    recomedataions = []
    wishlist = []
    if request.user.is_authenticated:
        r = get_recommendation(request.user.id)
        print(len(r))
        recomedataions= []
        for id in r: 
            try:
                recomedataions.append(Product.objects.get(id = id)) 
            except:
                continue
        wishlist = [w.product for w in Wishlist.objects.filter(user = request.user)]
        products = Product.objects.all()[0:6]

        p = []
        
        for product in products:
            product.wishlisted = False
            if product in wishlist:
                product.wishlisted = True

            p.append(product)
        print(p)
    else:
        p = Product.objects.all()[0:6]

    return render(request, 'index.html',
                  {
                      "products":p,
                      "recomendations":recomedataions,
                      'wishlist':wishlist
                   })
def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')

def getInTouch(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")  # Use a different variable name for the message text
        messages.success(request, 'Your Message has been saved. Thank you.')

        # Create the Message model instance
        message_instance = Message(name=name, email=email, subject=subject, message=message_text)
        message_instance.save()

        try:
            print("sending message")
            # Acknowledgment message to the sender
            acknowledgment_message = f"Thank you, {name}, for contacting us. We have received your message. We will get back to you soon. \n\nMessage Details are:\n    Name: {name}\n    Email: {email}\n    Subject: {subject}\n    Message: {message_text}"
            sendMessage(email, acknowledgment_message)

            # Notification message to the admin
            admin_notification = f"New message received:\n    Name: {name}\n    Email: {email}\n    Subject: {subject}\n    Message: {message_text}"
            sendMessage(sender, admin_notification)  # Ensure 'sender' is defined somewhere as the admin's email
        except Exception as e:
            print("exception", e)

    return redirect("contact")


"""
    Check if user is authenticated if yes show them a list of recommended products and their wishlisted products
    We will have to create an additional wishlist model 
"""
def dashboard(request):
    if request.user.is_authenticated:
        products = Product.objects.all()[0:6]
        wishlist = Wishlist.objects.filter(user = request.user)
        # print(wishlist)
        r = get_recommendation(request.user.id)
        recomendations= [ ]
        for id in r:
            try:
                recomendations.append(Product.objects.get(id = id))
            except:
                continue
        p = []
        w = [w.product for w in wishlist]
        for product in products:
            product.wishlisted = False
            if product in w:
                product.wishlisted = True

            p.append(product)
    
        
            
        return render(request, 'dashboard.html',
                      {
                          "products":p,
                          'wishlist':wishlist,
                          'recomendations':recomendations
                       }
                      )
    else:
        return redirect("home:home")
        
def addToWishlist(request,id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id = id)
        except:        
            messages.warning(request, 'Product not found')
            return JsonResponse({"error":"Product not found"})
        wishlist = Wishlist(user = request.user,product = product)
        wishlist.save()
        print('wishlist')
        messages.success(request, "Product added to wishlist")

        return JsonResponse({"success":"Product added to wishlist"})
    else:
        messages.warning(request, "Log in to add to wishlist")

        return JsonResponse({"error":"User not authenticated"})
    

def removeFromWishlist(request,id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id = id)
        except:
            messages.warning(request, "Product Not Found")
            return JsonResponse({"error":"Product not found"})
        wishlist = Wishlist.objects.filter(user = request.user,product = product).delete()

        messages.success(request, "Product Removed from wishlist")
        return JsonResponse({"success":"Product Removed From Wihslist"})
    else:
        messages.warning(request, "Log in to add remove from wishlist")
        return JsonResponse({"error":"Not authenticated"})
    