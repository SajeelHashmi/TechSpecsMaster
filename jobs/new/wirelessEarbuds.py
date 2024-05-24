import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import *

def getWirelessEarbudsLinks():
    page = 1
    url = f"https://priceoye.pk/wireless-earbuds/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
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
    
    for i in range(page, int(lastPage)+1):
        url = f"https://priceoye.pk/wireless-earbuds/brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
            })
    return data

def getWirelessEarbudsDetails(name,link):

    try:
        brand = link.split('/wireless-earbuds/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ').strip()
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
            image = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict = False)['image']
        except:
            return
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image,category = 'WirelessEarbuds')


        """
    chargingTime = models.CharField(max_length = 255)
    playTime = models.CharField(max_length = 255)
    batteryCapBud = models.CharField(max_length = 255)
    batteryCapCase = models.CharField(max_length = 255)
    BTVersion = models.CharField(max_length = 255)
    BTRange = models.CharField(max_length = 255)
    microphone = models.CharField(max_length = 255)
        
        """
            # specs
        model = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        waterProof = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        wearingType = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        volumeControl = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        chargingTime = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        playTime = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        batteryCapBud = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        batteryCapCase = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        BTVersion = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        BTRange = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        microphone = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text

        product.save()
        w = WirelessEarbuds.objects.create(model = model,waterProof = waterProof,wearingType = wearingType,volumeControl = volumeControl,chargingTime = chargingTime,playTime = playTime,batteryCapBud = batteryCapBud,batteryCapCase = batteryCapCase,BTVersion = BTVersion,BTRange = BTRange,microphone = microphone,product = product)
        w.save()
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()
    except Exception as e:
            print(e)


if __name__ == "__main__":
    data = getWirelessEarbudsLinks()
    print(data)

    
