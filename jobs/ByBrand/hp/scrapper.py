


import requests
from bs4 import BeautifulSoup
import  csv 
import json

# pricce and other details all included in name 
# other stores donot carry this product
def getModelsName(write:bool = False):


    page = 1
    url = f"https://hpshop.pk/shop/page/{page}/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')  
    try:
        lastPage = soup.select("ul.page-numbers a")[-2].text
    except:
        lastPage = 0
    productList  = soup.select('.product-grid-item')
    print(len(productList))
    # print(productList)
    data = []
    for product in productList:
        obj = {}
        obj['link'] = product.find('a')['href']
        obj['name'] = product.select('h3 > a:nth-child(1)')[0].text.strip()
        data.append(obj)  
    page+=1
    for i in range(page, int(lastPage)+1):
        url = f"https://hpshop.pk/shop/page/{page}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')  
        productList  = soup.select('.product-grid-item')
        print(len(productList))
        # print(productList)
        for product in productList:
            obj = {}
            obj['link'] = product.find('a')['href']
            obj['name'] = product.select('h3 > a:nth-child(1)')[0].text.strip()
            data.append(obj) 

    if write:
        with open('data/nameLink.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

if __name__ == "__main__":
    getModelsName(True)
    # getDetails()

