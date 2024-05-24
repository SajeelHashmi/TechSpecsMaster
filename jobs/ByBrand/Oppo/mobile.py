import requests
from bs4 import BeautifulSoup
import  csv 
import json

#     Oneplus	https://www.oneplus.com/pk (all phones and audio mentioned on the footer)
def getModelsName(write:bool = False):
    url  = "https://www.oppo.com/pk/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    footer  = soup.select('nav.nav > dl:nth-child(1)')[0]
    mobileList = footer.select('dd')
    data = []
    for mobile in mobileList:
        obj = {}
        obj['link'] = mobile.find('a')['href']
        obj['name'] = mobile.text.strip()
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
    print( models[0])

    for model in models:
        obj = {}
        obj['name'] = model['name']
        detailsApi =  model['link'] +'/specs'
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

