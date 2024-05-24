
# use this api for samsung products
import requests
from bs4 import BeautifulSoup
import  csv 
import json

def getPhones(write:bool = False):
    modelsApi  = "https://searchapi.samsung.com/v6/front/b2c/product/finder/global?type=01010000&siteCode=pk&start=0&num=500000&sort=recommended&onlyFilterInfoYN=N&keySummaryYN=N&specHighlightYN=N&familyId="
    res = requests.get(modelsApi)
    jsonRes = json.loads(res.text)
    totalRecords = jsonRes['response']['resultData']['common']['totalRecord']
    productList = jsonRes['response']['resultData']['productList']
    data = []
    for product in productList:
        data.append({
        "name" : product['modelList'][0]['displayName'].lower(),
        'price': product['modelList'][0]['afterTaxPrice'],
        'url': 'https://www.samsung.com' + product['modelList'][0]['pdpUrl'],
        })
    if write:
        with open('mobileNameModel.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails(models: list = []):
    print( models[0])
    for model in models:
        obj = {}        
        obj['name'] = model['name']
        detailsApi = f"https://searchapi.samsung.com/v6/front/b2c/product/spec/detail?siteCode=pk&modelList={model['model'].strip()}&specAnnotationYN=N"
        res = requests.get(detailsApi)
        jsonRes = json.loads(res.text)
        # ususally 14 specs per mobile
        specList = jsonRes['response']['resultData']['modelList'][0]['spec']['specItems']
        for spec in specList:
            # print(spec)
            try:
                for attr in spec['attrs']:
                    # print(attr)
                    obj[attr['attrName']] = attr['attrValue']
            except TypeError:
                # meaning attr is none
                # this means that the specs doesnot have any more details to show so we take the spec value
                obj[spec['attrName']] = spec['attrValue']
        data.append(obj)
    print(data[0].keys()    )
    try:
        with open('mobileDetails.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames,extrasaction="ignore")
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(e)
    # print(models)



if __name__ == "__main__":
    getModelsName(True)
    getDetails()

