from products.models import *
import requests
from bs4 import BeautifulSoup
import csv
import threading

from .new.btSpeakers import getBTspeakersLink,getBtSpeakersDetails
from .new.tablets import getTabletLinks, getTabletDetails
from .new.mobiles import getMobileLinks, getMobileDetails
from .new.tv import getTvLinks, getTvDetails

from .new.smartWatches import getSmartWatchLinks, getSmartWatchDetails
from .new.powerBanks import getPowerBankLinks, getPowerBankDetails
from .new.laptop import getLaptopLinks, getLaptopDetails
from .new.wirelessEarbuds import getWirelessEarbudsLinks, getWirelessEarbudsDetails


def check_similarity(name, product_text):
    name_words = name.lower().split()
    product_words = product_text.lower().split()

    threshold = int(0.90 * len(name_words))

    common_words_count = sum(word in product_words for word in name_words)

    return common_words_count >= threshold


def scrapeOfficialStore(p):
    pass

def scrapePaklap(p):
    s = None
    try:
        s = store.objects.get(product = p, name='paklap')
    except:
        pass
    if s is not None:
        return

    baseUrl = "https://www.paklap.pk/catalogsearch/result/?cat=0&q="

    name = p.name.strip()
    nameLink = name.replace(' ','+').strip()    
    response = requests.get(baseUrl+nameLink)
    soup = BeautifulSoup(response.text, "html.parser")
    product  = soup.select('li.product:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(1) > a:nth-child(1)')
    price = soup.select('li.product:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1) > span.price-wrapper > span:nth-child(1)')
    if product and price:
        product = product[0]
        price = price[0]
    else:
        return
    if name.lower() in  product.text.lower():
        link = product['href']
        price = price.text.replace('Rs','').replace(',','').replace('.00','').replace('.','').strip()
    else:
        return
    store = Store.objects.create(product = p,name='paklap', link=link, price=price)
    store.save()

    return


def scrapeMegaStore(product):
    s = None
    try:
        s = store.objects.get(product = product, name='Mega Store')
    except:
        pass
    if s is not None:
        return
    try:
        links = {
                'Tablet' : "https://www.mega.pk/search/multimediatablets-SEARCHTERM/",
                'BTspeaker' : "https://www.mega.pk/search/speakers-SEARCHTERM/",
                'TV' : "https://www.mega.pk/search/ledtv-SEARCHTERM/",
                'MobilePhone' : "https://www.mega.pk/search/mobiles-SEARCHTERM/",
                'Laptop' : "https://www.mega.pk/search/laptop-SEARCHTERM/",
                'PowerBank' : "https://www.mega.pk/search/powerbank-SEARCHTERM/",
                'SmartWatch' : "https://www.mega.pk/search/watches-SEARCHTERM/",
                'WirelessEarbuds' : "https://www.mega.pk/search/bluetoothhandfree-SEARCHTERM/",
                }
        baseLink = links[product.category]
        name = product.name
        nameLink = name.replace(' ','+').strip()    
        response = requests.get(baseLink.replace('SEARCHTERM',nameLink))
        soup = BeautifulSoup(response.text, "html.parser")
        empty = soup.select('.resulter > b:nth-child(2)')[0].text


        if empty == '0':
            return
        firstRes  = soup.select('li.col-xs-6:nth-child(1)')
        if firstRes:
            priceEl = firstRes[0].select("div.cat_price")[0].text
            nameEl = firstRes[0].select('h3 > a')
            price = ''.join(char for char in priceEl if char.isdigit())
            if price == '':
                return
            name = nameEl[0].text
            link = nameEl[0]['href']
        else:
            return

            # need to normalize name and product.text somehow to compare
        if product.name.lower() in name.lower():

            store = Store.objects.create(product=product, name='Mega Store', link=link, price=price)
            store.save()
            
        else:
            return
    except Exception as e:
        print(e)
    return

def scrapeRhizmall(product):
    s = None
    try:
        s = store.objects.get(product = product, name='Rhizmall')
    except:
        pass
    if s is not None:
        
        return

    links = {
"WirelessEarbuds" : 'https://rhizmall.pk/?s=SEARCHTERM&post_type=product&product_cat=best-wireless-earbuds',
"PowerBank" : "https://rhizmall.pk/?s=SEARCHTERM&post_type=product&product_cat=powerbank-price-in-pakistan",
"SmartWatch" : "https://rhizmall.pk/?s=SEARCHTERM&post_type=product&product_cat=best-smart-watches",
"BTspeaker" : "https://rhizmall.pk/?s=SEARCHTERM&post_type=product&product_cat=speakers",

}
    try:
        baselink = links[product.category]
    except:
        print('category not available on rhizmall')
        return
    try:
        name = product.name.strip()
        nameLink = name.replace(' ','+').strip()    
        response = requests.get(baselink.replace('SEARCHTERM',nameLink))
        soup = BeautifulSoup(response.text, "html.parser")
        empty = soup.select('.woocommerce-no-products-found')
        if empty:
            
            return
        firstRes = soup.select('div.product-grid-item:nth-child(1)')
        if firstRes:
            name = firstRes[0].select('h3.wd-entities-title')[0].text

            if product.name.lower() in name.lower():
                link = firstRes[0].select('a')[0].get('href')
                priceEl = firstRes[0].select('span.price')[0].text
                price = ''.join(char for char in priceEl if char.isdigit())

                if link and price:
                    store = Store.objects.create(product=product, name='Rhizmall', link=link, price=price)
                    store.save()
                    return
                else:
                    return
                    
            else:
                return

    except Exception as e:
        print('Error' ,e)

        return



def scrapeMtechStore(product):
    s = None
    try:
        s = store.objects.get(product = product, name='MtechStore')
    except:
        pass
    if s is not None:
        
        return
    baseUrl = "https://www.mtechstore.com/search?q=SEARCHTERM&submit=search-results"
   
    try:
        name = product.name.strip()
        nameLink = name.replace(' ','+')
        url = baseUrl.replace('SEARCHTERM',nameLink)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        productList = soup.select('#products-list')
        if not productList:
        
            return
        firstRes = soup.select('li.item:nth-child(1)')
        if firstRes:
            firstRes = firstRes[0]
            name = firstRes.select('h2.product-name > a')[0].text.strip()
            link = firstRes.select('h2.product-name > a')[0]['href']
            priceEl = firstRes.select('span.price')[0].text.strip()
            price = ''.join(char for char in priceEl if char.isdigit())
            if price == '':
                return
            price = int(price)
            if product.name.lower() in name.lower():

                store = Store.objects.create(product=product, name='MtechStore', link=link, price=price)
                store.save()
                return
        else:
            return
    except Exception as e:
        print(e)
    return


def scrapeDablew(product : Product):
    s = None
    try:
        s = store.objects.get(product = product, name='Dablew')
    except:
        pass
    if s is not None:
        
        return
    links = {

        'SmartWatch': "https://dablew.pk/?product_cat=smart-watch-and-band/&s=SEARCHTERM&post_type=product",
        'WirelessEarbuds': "https://dablew.pk/?product_cat=earphones/&s=SEARCHTERM&post_type=product",
        'BTspeaker': "https://dablew.pk/?product_cat=wireless-speakers/&s=SEARCHTERM&post_type=product",
        'PowerBank':"https://dablew.pk/?product_cat=best-power-banks-in-pakistan/&s=SEARCHTERM&post_type=product",
    }
    try:
        baseUrl = links[product.category]
    except:
        print('category not available on dablew')
        return
    try:
        name = product.name.strip()
        nameLink = name.replace(' ','+')
        url = baseUrl.replace('SEARCHTERM',nameLink)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        empty = soup.select("message-container.container.medium-text-center")
        if empty:
            return
        firstRes = soup.select('div.product-small:nth-child(1)')
        if firstRes:
            firstRes = firstRes[0]
            nameEl = firstRes.select('div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > p:nth-child(2) > a:nth-child(1)')
            priceEl = firstRes.select('div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2) > ins:nth-child(2) > span:nth-child(1) > bdi:nth-child(1)')
            if not priceEl:
                priceEl = firstRes.select('div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1) > bdi:nth-child(1)')
            if not nameEl or not priceEl:
                return
            name = nameEl[0].text.strip()
            link = nameEl[0]['href']
            priceEl = priceEl[0].text.strip()
            price = ''.join(char for char in priceEl if char.isdigit())
            if price == '':
                return
            price = int(price)
            if product.name.lower() in name.lower():
                store = Store.objects.create(product=product, name='Dablew', link=link, price=price)
                store.save()
                return
            else:
                return
                
        else:
            return
    except Exception as e:
        print(e)
    return


def scrapeMyShop(product : Product):
    s = None
    try:
        s = store.objects.get(product = product, name='MyShop')
    except:
        pass
    if s is not None:
        
        return
    baseUrl = "https://myshop.pk/catalogsearch/result/?q=SEARCHTERM"

    try:
        name = product.name.strip()
        nameLink = name.replace(' ','+')
        url = baseUrl.replace('SEARCHTERM',nameLink)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        empty = soup.select('.message.notice')
        if empty:
            return
        firstRes = soup.select('li.product:nth-child(1)')
        if firstRes:
            firstRes = firstRes[0]
            name = firstRes.select('.product.details.product-item-details a')[0].text.strip()
            link = firstRes.select('.product.details.product-item-details a')[0]['href']
            priceEl = firstRes.select('.price-box.price-final_price span.price')[0].text.strip().split('.')[0]
            price = ''.join(char for char in priceEl if char.isdigit())
            if price == '':
                return
            price = int(price)
            if product.name.lower() in name.lower():
                
                store = Store.objects.create(product=product, name='MyShop', link=link, price=price)
                store.save()
                return
            else:
                return
        else:
            return
    except Exception as e:
        print(e)
    return


def task():
    btSpeakers = getBTspeakersLink()
    allBtSpeakers =[ p.name for p in Product.objects.filter(category = 'BTspeaker')]
    newBtSpeakers = [speaker for speaker in btSpeakers if speaker['name'] not in allBtSpeakers]
    for speaker in newBtSpeakers:
        getBtSpeakersDetails(speaker['name'], speaker['link'])
    tablets = getTabletLinks()
    allTablets =[ p.name for p in Product.objects.filter(category = 'Tablet')]
    newTablets = [t for t in tablets if t['name'] not in allTablets]
    for t in newTablets:
        getTabletDetails(t['name'], t['link'])

    mb = getMobileLinks()
    allMb =[ p.name for p in Product.objects.filter(category = 'MobilePhone')]
    newMb = [m for m in mb if m['name'] not in allMb]
    for m in newMb:
        getMobileDetails(m['name'], m['link'])

    tvs = getTvLinks()
    allTv =[ p.name for p in Product.objects.filter(category = 'TV')]
    newTv = [t for t in tvs if t['name'] not in allTv]
    for t in newTv:
        getTvDetails(t['name'], t['link'])

    smartWatch = getSmartWatchLinks()
    allSmartWatch =[ p.name for p in Product.objects.filter(category = 'SmartWatch')]
    newSmartWatch = [s for s in smartWatch if s['name'] not in allSmartWatch]
    for t in newSmartWatch:
        getSmartWatchDetails(t['name'], t['link'])



    pb = getPowerBankLinks()
    allPb =[ p.name for p in Product.objects.filter(category = 'PowerBank')]
    newPb = [p for p in pb if p['name'] not in allPb]
    for t in newPb:
        getPowerBankDetails(t['name'], t['link'])




    laptops = getLaptopLinks()
    allLaptop =[ p.name for p in Product.objects.filter(category = 'Laptop')]
    newLaptop = [t for t in laptops if t['name'] not in allLaptop]
    for t in newLaptop:
        getLaptopDetails(t['name'], t['link'])




    wirelessEarbuds = getWirelessEarbudsLinks()
    allWirelessEarbuds =[ p.name for p in Product.objects.filter(category = 'WirelessEarbuds')]
    newWirelessEarbuds = [t for t in wirelessEarbuds if t['name'] not in allWirelessEarbuds]
    for t in newWirelessEarbuds:
        getWirelessEarbudsDetails(t['name'], t['link'])
    task2()

    i = len(Product.objects.all())
    for product in Product.objects.all():
        t = threading.Thread(target=scrapeDablew, args=(product,))
        t2 = threading.Thread(target=scrapeMtechStore, args=(product,))
        t3 = threading.Thread(target=scrapeMyShop, args=(product,))
        t4 = threading.Thread(target=scrapeRhizmall, args=(product,))
        t5 = threading.Thread(target=scrapeMegaStore, args=(product,))
        t6 = threading.Thread(target=scrapePaklap, args=(product,))
        t7 = threading.Thread(target=scrapeOfficialStore, args=(product,))
        t.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        i -= 1
        s = Store.objects.filter(product = product,name = 'Official Store')
        if len(s) == 0:
            store = Store.objects.create(product = product,name = 'Official Store',link = product.link,price = 0)
            store.save()



def task2():
    links = {
    'nokia':{
        'link':'https://advancetelecom.com.pk/?s=',
        'pl':True
    },
   'audionic': {
    'link':"https://audionic.co/search?type=product&q=SEARCHTERM",
    'pl':True
   },
   
       
   'samsung':{
        'link':"https://www.samsung.com/pk/search/?searchvalue=SEARCHTERM",
        'pl':True
   },
   'huawei':{
       'link':"https://consumer.huawei.com/pk/search/?keyword=SEARCHTERM",
       'pl':True
   },
   
   'apple':{
       'link':"https://www.apple.com/us/search/SEARCHTERM",
       'pl':True
   },
   
   'infinix':{
       'link':"",
       'pl':True
   },
   'dany':{
       'link':"https://danytech.com.pk/search?type=product&q=SEARCHTERM",
       'pl':True
   },
   
   'tecno':{
       'link':'https://www.tecno-mobile.com/pak/search?q=SEARCHTERM',
       'pl':False
   },
   'oppo':{
       'link':"https://www.oppo.com/pk/search/?params=SEARCHTERM#SEARCHTERM",
       'pl':False
   },
   'asus':{
       'link':"https://asusstore.pk/?s=SEARCHTERM",
       'pl':True
   },
   'realme':{
       'link':'https://www.mi.com/pk/search/SEARCHTERM?tab=product',
       'pl':False
   },
    'xiaomi':{
       'link':'https://www.mi.com/pk/search/SEARCHTERM?tab=product',
       'pl':False
   },
    'mi':{
       'link':'https://www.mi.com/pk/search/SEARCHTERM?tab=product',
       'pl':False
   },
    'oneplus':{
        'link':'https://www.oneplus.com/pk',
        'pl':False
   },
   'hp':{
        'link':'https://hpshop.pk/?s=SEARCHTERM&post_type=product',
        'pl':True
   },
    'infinix':{
       'link':'https://pk.infinixmobility.com/search?searchVal=SEARCHTERM',
       'pl':False
   },
    'dell':{
       'link':'https://www.dell.com/en-pk',
       'pl':False
   },
    'lenovo':{
       'link':'https://www.lenovo.com/pk/en/search?text=SEARCHTERM',
       'pl':False
   },
    'ronin':{
       'link':'https://ronin.pk/search?q=SEARCHTERM',
       'pl':True
   },
    'itel':{
       'link':'https://itelpakistan.com/?s=SEARCHTERM',
       'pl':True
   },
    'vivo':{
       'link':'https://www.vivo.com/pk/searchData/search?sk=SEARCHTERM',
       'pl':False
   },
    'zero':{
       'link':'https://zerolifestyle.co/search?q=SEARCHTERM',
       'pl':True
   },
    'airox':{
       'link':'https://airox.pk',
       'pl':False
   },
    'soundpeats':{
       'link':'https://soundpeats.pk/search?q=SEARCHTERM',
       'pl':True
   },
    'gfive':{
       'link':'https://gfivepakistan.com/search?type=product&q=SEARCHTERM',
       'pl':True
   },
    'hellofaster':{
       'link':'https://pk.hellofaster.com/search?q=SEARCHTERM',
       'pl':True
   },
}

    for product in Product.objects.filter(link = ''):
        try:
            name = product.name.strip()
            brand = product.brand
            link = links[brand.lower()]
            if link['pl']:
                name = name.replace(' ','+')
            l = link['link'].replace('SEARCHTERM',name)
            product.link = l
            product.save()
            
        except Exception as e:
            print(e)
            continue
            

