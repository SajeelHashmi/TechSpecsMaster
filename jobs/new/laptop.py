import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import *

def getLaptopLinks():
    page = 1
    url = f"https://priceoye.pk/laptops/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
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
        url = f"https://priceoye.pk/laptops/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={i}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })
    
    return data

def getLaptopDetails(name,link):

    try:
        brand = link.split('/laptops/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ').strip()
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
            image = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict = False)['image']
        except:
            return
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image,category = 'Laptop')

        """
    battery = models.CharField(max_length=255)
    blueTooth = models.CharField(max_length=255)
    wifi = models.CharField(max_length=255)
    usb = models.CharField(max_length=255)
    fingerPrint = models.CharField(max_length=255)"""


            # specs
        weight = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        os = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        generation = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        screen = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        resolution = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text

        internalMemory = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        ram = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        graphicsCard = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text

        processorType = soup.select('table.p-spec-table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        processorSpeed = soup.select('table.p-spec-table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text

        battery = soup.select('table.p-spec-table:nth-child(5) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text

        bluetooth = soup.select('table.p-spec-table:nth-child(6) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        wifi = soup.select('table.p-spec-table:nth-child(6) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        fingerPrint = soup.select('table.p-spec-table:nth-child(6) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text
        product.save()

        l = Laptop.objects.create(product = product,weight = weight,os = os,generation = generation,screen = screen,resolution = resolution,internalMemory = internalMemory,ram = ram,graphicsCard = graphicsCard,processor = processorType,processorSpeed = processorSpeed,battery = battery,blueTooth = bluetooth,wifi = wifi,fingerPrint = fingerPrint)
        l.save()
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()

    except Exception as e:
            print(e)
    




if __name__ == "__main__":
    data = getLaptopLinks()

    