import requests
from bs4 import BeautifulSoup
import  csv 


def scrape(name):
    name = name.replace(" ", "+")

    url = f"https://ronin.pk/search?q={name}&options%5Bprefix%5D=last"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    prod = soup.select('li.product:nth-child(1)')
    
    try:
        prod = prod[0]
        a = soup.select('li.product:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
        link = a[0]['href']
        name = soup.select("li.product:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)")
        name = name[0].get_text(strip=True).lower().strip()
        print(name)
        remove = '-' + name.split('-')[-1]
        print(remove)
        name = name.replace(remove, "")
        print(name)

        link = "https://ronin.pk"+ link
        print(link)
        price = soup.select("li.product:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > dl:nth-child(1) > div:nth-child(2) > dd:nth-child(1) > span:nth-child(1)")[0].text
        price = price.replace("Rs.", "").replace(",", "").strip()
        print(price)
        return (price,link,name)

    except:
        print("No product found")
        return (None,None,None)
    
if __name__ =="__main__":
    scrape('a')