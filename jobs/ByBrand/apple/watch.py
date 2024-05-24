import requests
from bs4 import BeautifulSoup
import  csv 
import json

# api to get all products name availiable but for specs we will have to use bs4 Api bookmarked
# not as usefull
iphone = "https://www.apple.com/iphone/"
ipad = "https://www.apple.com/ipad/"
watch =   "https://www.apple.com/watch/"
aripods = "https://www.apple.com/aripods/"
mac =    "https://www.apple.com/mac/"

def getModelsName(write:bool = False):
    # get all models of iphones
    response = requests.get(watch)
    soup = BeautifulSoup(response.text, "html.parser")
    compareTbl = soup.select(".compare-table")[0]
    models = compareTbl.select(".device")
    links = compareTbl.select(".device-cta")
    
    data = []
    
    for model,link in zip(models,links):
        print(model,link)
        obj = {}
        obj['name'] = model.select("h3 ")[0].text.strip().split("\n")[0]
        obj['link'] = link.find_all("a")[1]['href']
        data.append(obj)
    if write:
        with open('data/watchLinks.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data



def getDetails():
    models = []
    with open('data/iphoneLinks.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    print( models[0])
    baseUrl = 'https://www.apple.com'
    data = []
    for model in models:
        try:
            link = baseUrl + model['link'] +'specs/'
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(e)
            continue
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
