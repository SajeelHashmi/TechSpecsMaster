import requests
from bs4 import BeautifulSoup
import  csv 
import json


def getModelsName(write:bool = False):
    page = 1
    data = []
    while 1:
        try:
            url  = f"https://mistore.pk/collections/band-and-smart-watches?page={page}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            # with open('testMiStore.html', 'w',encoding="utf-8") as file:
            #     file.write(soup.prettify())
            productList  = soup.select('.product-collection.products-grid > div')
            if len(productList) == 0:
                break
            # print(productList)
            for product in productList:
                obj = {}
                a = product.select('.product-title')[0]
                if a.text.strip() == "":
                    continue
                obj['link'] = a['href']
                obj['name'] = a.text.strip()
                data.append(obj)  
            page += 1
        except:
            break
    
    if write:
        with open('data/watchNameLink.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

if __name__ == "__main__":
    getModelsName(True)
    # getDetails()

