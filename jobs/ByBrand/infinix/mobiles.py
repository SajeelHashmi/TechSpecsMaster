import requests
from bs4 import BeautifulSoup
import  csv 
import json


def getModelsName(write:bool = False):
    url  = "https://pk.infinixmobility.com/smartphones"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    modelsDiv = soup.select('.lib-Rec-sonDiv')
    data=[]
    for model in modelsDiv:
        data.append({
            'link' : model.find('a').href,
            'name' : model.select('p.lib-Rec-text.lib-mt12')[0].text
            })
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
    with open('mobileNameModel.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    print( models[0])
    for model in models:
        obj = {}
        # print(model['model'])
        
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

