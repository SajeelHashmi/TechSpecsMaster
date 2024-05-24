
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import * 
from home.models import Wishlist,History
# from jobs.ByBrand.gfive.scrapper import scrape
from recommendation_utils.utils import getRecommendedStore 
from jobs.startDb import task
from django.contrib import messages




def addReview(request,id):
    if not request.user.is_authenticated:
        return redirect('product',id=id)    
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=id)
            generalReview = request.POST.get('generalReview')
            softwareReview = request.POST.get('softwareReview')
            buildReview = request.POST.get('buildReview')
            rating = request.POST.get('rating')

            print(generalReview,softwareReview,buildReview,rating)


            review = Review(user = request.user,product = product,generalReview = generalReview.strip(),softwareReview = softwareReview,buildReview = buildReview,rating = rating)
            review.save()
            return redirect('product',id=id)
        except Exception as e:
            print(e)
            return redirect('product',id=id)
    messages.success(request, "Review Added")
    return redirect('home')
def allProdNames(request, category=None):
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    names = [product.name for product in products]
    return JsonResponse(names, safe=False)


def getDetails(request,name):
    try:
        product= Product.objects.get(name=name)
    except:
        try:
            product= Product.objects.filter(name__contains=name)[0]
        except:
            print("No data found for this product.")
            return JsonResponse({'error':"No data found for this product."})
    # document.getElementById('product1_img').src = data.image;
    #         document.getElementById('product1_name').innerHTML = data.name;
    #         document.getElementById('product1_price').innerHTML = data.price;
    
    print(product)
    if product.category == 'BTspeaker':
        item = BTspeaker.objects.get(product=product)

    elif product.category == 'MobilePhone':
        item = MobilePhone.objects.get(product=product)
    
    elif product.category == 'TV':
        item = TV.objects.get(product=product)
    
    elif product.category == 'SmartWatch':
        item = SmartWatch.objects.get(product=product)
    
    elif product.category == 'Tablet':
        item = Tablet.objects.get(product=product)
    
    elif product.category == 'PowerBank':
        item = PowerBank.objects.get(product=product)
   
    elif product.category == 'Laptop':
        item = Laptop.objects.get(product=product)
    
    elif product.category == 'WirelessEarbuds':
        item = WirelessEarbuds.objects.get(product=product)
    
    specs = []

    for key, value in vars(item).items():
        if key != 'product_id' and key != 'id' and key != 'product' and key != '_state':

            specs.append({key: value})

    return JsonResponse({'image':product.image_url,
                        'name':product.name,
                        'price':product.price,
                        'specs':specs})
def compare(request):
    return render(request,'compare.html')






#get_recommendation(2)

def getMobilePhones(request,page = 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'MobilePhone')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]
    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'mobile'
    })




def getTablets(request,page = 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'Tablet')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]
    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)
    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'tablet'
    })
def startDb(request):
    return "abcd"
    task()

    # prod = Product.objects.all()
    # stores = []
    # for p in prod:
    #     s = Store.objects.filter(product = p,name='Official Store')
    #     if len(s)==0:
    #         store = Store.objects.create(product = p,name='Official Store',link = p.link,price = 0)
    #         store.save()
    #     stores+=s
    # print(len(stores))
    # print(len(prod))
    return


def getTvs(request,page = 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'TV')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]   
    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)
    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'tvs'
    })


def getPowerBanks(request,page = 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'PowerBank')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]

    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'powerbank'
    })

def getSmartWatches(request,page = 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'SmartWatch')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]

    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'smartwatch'
    })

def getLaptops(request,page= 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'Laptop')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]


    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'laptops'
    })


def getEarbuds(request,page= 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'WirelessEarbuds')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]
    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
       'currentUrl' : 'earbuds'
    })


def getSpeakers(request,page= 1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.filter(category = 'BTspeaker')
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]

    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)

    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages,
        
       'currentUrl' : 'speakers'
    })


def explore(request,page=1):
    brands = request.GET.get('brands')
    q = request.GET.get('q')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice:
        minPrice = int(minPrice.replace('K', '')) * 1000
    if maxPrice:
        maxPrice = int(maxPrice.replace('K', '')) * 1000

    products = Product.objects.all()
    if minPrice:
        products = products.filter(price__gte=minPrice)
    if maxPrice:
        products = products.filter(price__lte=maxPrice)
    if brands or q:
        if brands and q:
            brands = brands.split('_')
            print(brands)
            products = products.filter(name__icontains=q, brand__in=brands)
        elif brands:
            brands = brands.split('_')
            print(brands)
            products = products.filter(brand__in=brands)
        elif q:
            products = products.filter(name__icontains=q)

    productLen = len(products)
    products = products[(page-1)*12:((page-1)*12 ) + 12]
    wishlist =[]
    if request.user.is_authenticated:
        wishlist  = Wishlist.objects.filter(user = request.user)
        wishlist = [w.product for w in wishlist]
    prods = []
    for p in products:
        if p in wishlist:
            p.wishlisted = True
            print(p)
        prods.append(p)
    # print(products)
    totalPages  =int( productLen/12) 
    if productLen%12 !=0:
        totalPages+=1

    return render(request, 'explore.html',{
        'products':prods,
        'range':f"{(page-1)*12} - {((page-1)*12 ) + 12} of {productLen} products",
        'nextPageNumber': int(page)+1,
        'previousPageNumber' : int(page)-1,
        'pageNumber':page,
       'currentUrl' : 'explore',
       'totalPages':totalPages

    })


def productDetails(request,id):
    try:
        product = Product.objects.get(id=id)
        storesList = Store.objects.filter(product =product)
    except:
        return redirect ('home')
    stores = [] 
    lowestPrice = float('inf')
    try:
        stores = getRecommendedStore(storesList)
    except Exception as e:
        print(e)   
        stores = []
        for s in storesList:
            
            print(s.name)
    wishlisted = False
    try:
        wishlist = Wishlist.objects.get(user = request.user,product = product)
        wishlisted = True
    except:
        pass
    if request.user.is_authenticated:
        history = History(user = request.user,product = product)
        history.save()
    if product.category == 'BTspeaker':
        item = BTspeaker.objects.get(product=product)

    elif product.category == 'MobilePhone':
        item = MobilePhone.objects.get(product=product)
    
    elif product.category == 'TV':
        item = TV.objects.get(product=product)
    
    elif product.category == 'SmartWatch':
        item = SmartWatch.objects.get(product=product)
    
    elif product.category == 'Tablet':
        item = Tablet.objects.get(product=product)
    
    elif product.category == 'PowerBank':
        item = PowerBank.objects.get(product=product)
   
    elif product.category == 'Laptop':
        item = Laptop.objects.get(product=product)
    
    elif product.category == 'WirelessEarbuds':
        item = WirelessEarbuds.objects.get(product=product)
    reviews = Review.objects.filter(product = product)
    return render(request,'product-info.html',{
        'product':product,
        'item':item,
        'stores' :stores,
        'wishlisted':wishlisted,
        'reviews':reviews
        })

