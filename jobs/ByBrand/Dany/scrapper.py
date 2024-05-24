import requests
from bs4 import BeautifulSoup
import  csv 


def scrape(name):
    name = name.replace(" ", "+")
    url = f"https://danytech.com.pk/search?type=product&q={name}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    prod = soup.select('div.grid-item:nth-child(1)')
    try:
        prod = prod[0]
        name = prod.select('.product-title')[0].text.strip()
        a = soup.select('div.grid-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(2)')
        link = a[0]['href']
        link = "https://danytech.com.pk"+ link
        print(link)
        price = soup.select("div.grid-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)")[0].text
        price = price.replace("Rs.", "").replace(",", "").strip()
        print(price)
        return (price,link)

    except:
        print("No product found")
    pass
if __name__ =="__main__":
    scrape('a')