import requests
from bs4 import BeautifulSoup
import  csv 
import json

#     Oneplus	https://www.oneplus.com/pk (all phones and audio mentioned on the footer)
def getModelsName(write:bool = False):
    url  = "https://www.oneplus.com/pk"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    footer  = soup.select('.footer-nav > dl')[:2]
    mobilesDl = footer[0]
    audioDl = footer[1]
    mobileList = mobilesDl.select('dd:nth-child(2) > ul:nth-child(1) > li')
    audioList = audioDl.select('dd:nth-child(2) > ul:nth-child(1) > li')
    data = []
    for mobile in mobileList:
        obj = {}
        obj['type'] = "mobile"
        obj['link'] = mobile.find('a')['href']
        obj['name'] = mobile.text.strip()
        data.append(obj)  
    for audio in audioList:
        obj = {}
        obj['type'] = "audio"
        obj['link'] = audio.find('a')['href']
        obj['name'] = audio.text.strip()
        data.append(obj)
        
            # jsonRes = json.loads(res.text)
    # totalRecords = jsonRes['response']['resultData']['common']['totalRecord']
    # print(totalRecords)
    # productList = jsonRes['response']['resultData']['productList']
    # data = []
    # for product in productList:
    #     data.append({
    #     "model" : product['modelList'][0]['modelCode'],
    #     "name" : product['modelList'][0]['displayName'],
    #     })
    
    # # print(data)
    if write:
        with open('data/completeData.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    url = 'https://www.oneplus.com'
    models = []
    with open('data/completeData.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    print( models[0])
    mobileData = []
    audioData = []  
    for model in models:

        obj = {}
        obj['name'] = model['name']
        detailsApi = url + model['link'] +'/specs'
    # specs in a form of paragraph not tabular

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
    # getDetails()

