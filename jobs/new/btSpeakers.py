import requests
from bs4 import BeautifulSoup
import  csv 
import json
from products.models import * 


def getBTspeakersLink():
    page = 1
    url = f"https://priceoye.pk/bluetooth-speakers/pricelist?brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
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
        url = f"https://priceoye.pk/bluetooth-speakers/brands=samsung_realme_huawei_tecno_oppo_nokia_infinix_oneplus_apple_dell_hp_lenovo_asus_ronin_audionic_mi_dany_itel_vivo_zero_airox_soundpeats_gfive_helofaster&page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        linksEl = soup.select(".product-list .productBox")

        for link in linksEl:
            data.append({
            'link':link.find('a')['href'],
            'name':link.select(".p-title")[0].text.strip().lower()
                })
        
    return data

def getBtSpeakersDetails(name,link):    
    try:
        obj = {}
        brand = link.split('/bluetooth-speakers/')[1].split('/')[0]
        name = link.split('/')[-1].replace('-', ' ')
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')

        price = soup.select('.price-size-lg')[0].text.strip().replace('Rs','').replace(',','').strip()
        image_url = json.loads(soup.select('script[type="application/ld+json"]')[2].text,strict=False)['image']

        
        product  = Product.objects.create(name = name,brand = brand,price = price,image_url = image_url,category = 'BTspeaker')
        # specs
        model = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')[0].text
        waterProof = soup.select('table.p-spec-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')[0].text
        batteryType = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        chargeTime = soup.select('table.p-spec-table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        BTVersion = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')[0].text
        BTRange = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')[0].text
        usbCompatability = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)')[0].text
        micTech = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')[0].text
        sdCard = soup.select('table.p-spec-table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)')[0].text

        speaker = BTspeaker.objects.create(product = product,model = model,waterProof = waterProof,batteryType = batteryType,chargeTime = chargeTime,BTVersion = BTVersion,BTRange = BTRange,usbCompatability = usbCompatability,micTech = micTech,sdCard = sdCard)
        Store.objects.create(product = product,name = 'priceoye',link = link,price = price).save()
        product.save()
        speaker.save()
    except Exception as e:
        print(e)
    return







if __name__ == "__main__":
    links =     getBTspeakersLink()
    print(links)
    
