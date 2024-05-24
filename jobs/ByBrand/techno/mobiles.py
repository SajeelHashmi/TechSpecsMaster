
# MIght need to skip techno or use selenium for this
import requests
from bs4 import BeautifulSoup
import  csv 
import json


def getModelsName(write:bool = False):
    url  = "https://shop.tecno-mobile.com/pak/rest/V1/category/filters?categoryId=171"
    res = requests.get(url)
    jsonData = json.loads(res.text)
    # print(jsonData)
    data = []
    for product in jsonData['productData']:
        obj = {
             'link' : product['overview_url']+ '#spec',
            'name' : product['product_name']
        }
        data.append(obj)

    if write:
        with open('data/mobileNameLink.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    models = []
    with open('data/mobileNameLink.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    # print( models[0])
    for model in models:
        try:
            obj = {}
            
            obj['name'] = model['name']
            

            detailsApi = model['link'] 
            print(detailsApi)
            res = requests.get(detailsApi)
            soup = BeautifulSoup(res.text, 'html.parser')
            with open('mobileDetails.html','w',encoding="utf-8") as file:
                file.write(soup.prettify())
            features = soup.select('.product-spec')# this is colors wheel
            for feature in features:
                obj[feature.select('.section-title')[0].text] = feature.select('.spec')[0].text
        except Exception as e:
            print(e)
    try:
        with open('data/mobileDetails.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames,extrasaction="ignore")
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(e)
    # print(models)



if __name__ == "__main__":
    # getModelsName(True)
    getDetails()

