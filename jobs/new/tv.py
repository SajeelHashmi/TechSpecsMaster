import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import *


def getTvLinks():
    page = 1
    url = f"https://priceoye.pk/led-tv/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')  
    try:
        lastPage = soup.select(".pagination > a")[-2].text
    except:
        lastPage = 0
    data = []
    linksEl = soup.select(".product-list .productBox")
    for link in linksEl:
        data.append({
        'link':link.find('a')['href'],
        'name':link.select(".p-title")[0].text.strip().lower()
            })
    page += 1
    for i in range(page, int(lastPage)+1):
        url = f"https://priceoye.pk/led-tv/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={i}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })
    return data
        

def getTvDetails(name ,link):
    try:
        obj = {}
        brand = link.split('/led-tv/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ').strip()
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
            image = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict = False)['image']
        except:
            return
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image,category = 'TV')

        """
    screenSize = models.CharField(max_length = 255)
    screenType = models.CharField(max_length = 255)
    resolution = models.CharField(max_length = 255)
    threeD = models.CharField(max_length = 255)
    HD = models.CharField(max_length = 255)
    fourK = models.CharField(max_length = 255)
    SmartTv = models.CharField(max_length = 255)
        """         
        screenSize = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        screenType = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
            

        resolution = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        threeD = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        HD = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        fourK = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text

        SmartTv = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        product.save()    
        TV.objects.create(product = product,screenSize = screenSize,screenType = screenType,resolution = resolution,threeD = threeD,HD = HD,fourK = fourK,SmartTv = SmartTv)
        
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()

    except Exception as e:
        print("exception",e)
        





if __name__ == "__main__":
    data = getTvLinks()
    print(data)
    # getDetails()

