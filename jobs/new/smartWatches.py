import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import *

def getSmartWatchLinks():
    page = 1
    url = f"https://priceoye.pk/smart-watches/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')  
    try:
        lastPage = soup.select(".pagination > a")[-2].text
    except:
        lastPage = 0
    linksEl = soup.select(".product-list .productBox")
    data = []
    for link in linksEl:
        data.append({
        'link':link.find('a')['href'],
        'name':link.select(".p-title")[0].text.strip().lower()
            })
    page += 1
    for i in range(page, int(lastPage)+1):
        url = f"https://priceoye.pk/smart-watches/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={i}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })

    return data


def getSmartWatchDetails(name,link):
    
    try:
        brand = link.split('/smart-watches/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ')
        
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
        image = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict=False)['image']

        product = Product.objects.create(name = name,brand = brand,price = price,image_url = image,category = 'SmartWatch')


        """

    screenSize = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    screenType = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    rom = models.CharField(max_length=255)
    wifi = models.CharField(max_length=255)
    batteryCapacity = models.CharField(max_length=255)
    batteryLife = models.CharField(max_length=255)"""
            # specs
        strapMaterial = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        waterResistance = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text
        os = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)')[0].text
        speaker = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(7) > td:nth-child(2)')[0].text
        mode = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(8) > td:nth-child(2)')[0].text

        screenSize = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        resulotion = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        screenType = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        ram = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        rom = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        wifi = soup.select('table.p-spec-table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text

        batteryCapacity = soup.select('table.p-spec-table:nth-child(5) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        batteryLife = soup.select('table.p-spec-table:nth-child(5) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
   
        product.save
        smartWatch = SmartWatch.objects.create(product = product,strapMaterial = strapMaterial,waterResistance = waterResistance,os = os,speaker = speaker,mode = mode,screenSize = screenSize,resolution = resulotion,screenType = screenType,ram = ram,rom = rom,wifi = wifi,batteryCapacity = batteryCapacity,batteryLife = batteryLife)
        smartWatch.save()
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()


    except Exception as e:
            print(e)




if __name__ == "__main__":
    data =getSmartWatchLinks()
    print(data)

    