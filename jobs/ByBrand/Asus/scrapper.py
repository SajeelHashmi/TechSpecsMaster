import requests
from bs4 import BeautifulSoup
import  csv 
import json

# pricce and other details all included in name 
# other stores donot carry this product
def getModelsName(write:bool = False):
    url  = "https://asusstore.pk/index.php/shop/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    productList  = soup.select('.texture-woo-product-list')
    print(len(productList))
    # print(productList)
    data = []
    for product in productList:
        obj = {}
        obj['link'] = product.find('a')['href']
        obj['name'] = product.select('.woocommerce-loop-product__title')[0].text.strip()
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

