from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    name = models.CharField(max_length=255,unique=True)
    brand = models.CharField(max_length=255)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083)
    category = models.CharField(max_length=50,default='')
    link = models.CharField(max_length = 2083 ,default = '')



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generalReview = models.CharField(max_length=255)
    softwareReview = models.CharField(max_length=255)
    buildReview = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)




class TV(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    screenSize = models.CharField(max_length = 255)
    screenType = models.CharField(max_length = 255)
    resolution = models.CharField(max_length = 255)
    threeD = models.CharField(max_length = 255)
    HD = models.CharField(max_length = 255)
    fourK = models.CharField(max_length = 255)
    SmartTv = models.CharField(max_length = 255)



class MobilePhone(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    releaseDate = models.CharField(max_length=255)
    simSupport = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    screenSize = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    screenType = models.CharField(max_length=255)
    internalMemory = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    cardSlot = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)
    frontCamera = models.CharField(max_length=255)
    backCamera = models.CharField(max_length=255)
    bluetooth = models.CharField(max_length=255)    
    wifi = models.CharField(max_length=255)
    threeG = models.CharField(max_length=255)
    fourG = models.CharField(max_length=255)
    fiveG = models.CharField(max_length=255)
    radio = models.CharField(max_length=255)



class PowerBank(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
    bateryCapacity = models.CharField(max_length=255)
    batteryType = models.CharField(max_length=255)
    inputPort = models.CharField(max_length=255)
    outputPort = models.CharField(max_length=255)

class SmartWatch(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    strapMaterial = models.CharField(max_length=255)
    waterResistance = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    speaker = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    screenSize = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    screenType = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    rom = models.CharField(max_length=255)
    wifi = models.CharField(max_length=255)
    batteryCapacity = models.CharField(max_length=255)
    batteryLife = models.CharField(max_length=255)


class Tablet(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    realeseDate = models.CharField(max_length=255)
    simSupport = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    screenSize = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    screenType = models.CharField(max_length=255)
    internalMemory = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    cardSlot = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)
    frontCamera = models.CharField(max_length=255)
    backCamera = models.CharField(max_length=255)
    bluetooth = models.CharField(max_length=255)    
    wifi = models.CharField(max_length=255)


class BTspeaker(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    waterProof = models.CharField(max_length=255)
    batteryType = models.CharField(max_length=255)
    chargeTime = models.CharField(max_length=255)
    BTVersion = models.CharField(max_length=255)
    BTRange = models.CharField(max_length=255)
    usbCompatability = models.CharField(max_length=255)
    micTech = models.CharField(max_length=255)
    sdCard = models.CharField(max_length=255)

class Laptop(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    weight = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    generation = models.CharField(max_length=255)
    screen = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    internalMemory = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    graphicsCard = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    processorSpeed = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)
    blueTooth = models.CharField(max_length=255)
    wifi = models.CharField(max_length=255)
    usb = models.CharField(max_length=255)
    fingerPrint = models.CharField(max_length=255)


class WirelessEarbuds(models.Model):
    model = models.CharField(max_length = 255)
    waterProof = models.CharField(max_length = 255)
    wearingType = models.CharField(max_length = 255)
    volumeControl = models.CharField(max_length = 255)
    chargingTime = models.CharField(max_length = 255)
    playTime = models.CharField(max_length = 255)
    batteryCapBud = models.CharField(max_length = 255)
    batteryCapCase = models.CharField(max_length = 255)
    BTVersion = models.CharField(max_length = 255)
    BTRange = models.CharField(max_length = 255)
    microphone = models.CharField(max_length = 255)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

class Store(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255,unique=True)
    price = models.FloatField()



links = {
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



