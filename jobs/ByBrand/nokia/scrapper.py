import requests
from bs4 import BeautifulSoup



def getPrice(name):
    name = name.replace(' ', '+')
    url = f"https://advancetelecom.com.pk/?s={name}&post_type=product"
    
    print(url)
    
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    prod = soup.select(".product-item")
    try:
        prod = prod[0]
        
        price = soup.select(".woocommerce-Price-amount > bdi:nth-child(1)")[0].text
        try:
            url  =  soup.select('.thumb-link')[0]['href']
        except:
            pass
    except:
        print('not found')
        return (None,url)
    price = price.replace('Rs','').replace(',','').replace('.00','').replace('.','').strip()
    
    return (price, url)