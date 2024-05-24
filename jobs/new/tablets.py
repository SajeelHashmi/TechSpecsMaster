import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import * 


def getTabletLinks():
    page = 1
    url = f"https://priceoye.pk/tablets/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
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
        url = f"https://priceoye.pk/tablets/brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")
        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })

    return data
        
    # with open('test.html', 'w',encoding="utf-8") as file:
    #     file.write(links[0].prettify())

def getTabletDetails(name,link):
    try:
        obj = {}
        brand = link.split('/tablets/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ')
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')


        obj = {}
        brand = link.split('/tablets/')[1].split('/')[0]
        link = link
        name = link.split('/')[-1].replace('-', ' ')


        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
    
        price = soup.select('span.summary-price')[0].text.strip().replace('Rs','').replace(',','').strip()
        image_url = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict = False)['image']
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image_url,category = 'Tablet')
            
            # specs
        releaseDate = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        simSupport = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        dimensions = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        weight = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text
        os = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')[0].text

        screenSize = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        resolution = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        screenType = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text

        internalMemory  = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        ram  = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        cardSlot  = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text

        processor = soup.select('table.p-spec-table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        gpu = soup.select('table.p-spec-table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text

        battery = soup.select('table.p-spec-table:nth-child(5) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text

        frontCamera = soup.select('table.p-spec-table:nth-child(6) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        backCamera = soup.select('table.p-spec-table:nth-child(6) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')[0].text
        

        bluetooth = soup.select('table.p-spec-table:nth-child(7) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        wifi = soup.select('table.p-spec-table:nth-child(7) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')[0].text
        
        product.save()
        tab = Tablet.objects.create(product = product,realeseDate = releaseDate,simSupport = simSupport,dimensions = dimensions,weight = weight,os = os,screenSize = screenSize,resolution = resolution,screenType = screenType,internalMemory = internalMemory,ram = ram,cardSlot = cardSlot,processor = processor,gpu = gpu,battery = battery,frontCamera = frontCamera,backCamera = backCamera,bluetooth = bluetooth,wifi = wifi)
        tab.save()
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()
           
            
   



    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    data = getTabletLinks()


    
