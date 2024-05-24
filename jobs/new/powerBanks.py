import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import *

def getPowerBankLinks():
    page = 1
    url = f"https://priceoye.pk/power-banks/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
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
        url = f"https://priceoye.pk/power-banks/brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })

    return data

def getPowerBankDetails(name,link):

    try:
        brand = link.split('/power-banks/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ').strip()
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
            image = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict = False)['image']
        except:
            return
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image,category = 'PowerBank')
        """
    model = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
    bateryCapacity = models.CharField(max_length=255)
    batteryType = models.CharField(max_length=255)
    inputPort = models.CharField(max_length=255)
    outputPort = models.CharField(max_length=255)
        """


        model = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        display = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        batteryCapacity = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        batteryType = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text

        inputPort = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        outputPort = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text

        product.save()
        powerbank =PowerBank.objects.create(product = product,model = model,display = display,bateryCapacity = batteryCapacity,batteryType = batteryType,inputPort = inputPort,outputPort = outputPort)
        powerbank.save()
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()
   



    except Exception as e:
            print(e)
            


if __name__ == "__main__":
    data = getPowerBankLinks()
    print(data)

    
