import requests
from bs4 import BeautifulSoup
import  csv 
import json


iphone = "https://www.apple.com/iphone/"
ipad = "https://www.apple.com/ipad/"
watch =   "https://www.apple.com/watch/"
aripods = "https://www.apple.com/aripods/"
mac =    "https://www.apple.com/mac/"

"""
    Scrapping Capacity only yet that to for only one model on page but no errors or exceptions
    next scrape all other infor mation for one model first then add functionality for second model on page
"""


def getModelsName(write:bool = False):
    response = requests.get(iphone)
    soup = BeautifulSoup(response.text, "html.parser")
    compareTbl = soup.select(".compare-table")[0]
    models = compareTbl.select(".device")
    data = []
    for model in models:
        obj = {}
        obj['name'] = model.select("h3 .visuallyhidden")[0].text.strip()
        obj['link'] = model.find("a")['href']
        data.append(obj)
    if write:
        with open('data/iphoneLinks.csv', 'w',encoding="utf-8",newline="") as file:
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
    baseUrl = 'https://www.apple.com'
    data = []
    for model in models:
        obj = {}
        link = baseUrl + model['link'] +'specs/'
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        capacitySec = soup.select(".techspecs-section.section-capacity")[0]
        obj['capacity'] = [li.text.strip() for li in capacitySec.select("div.techspecs-row > div:nth-child(2) li ")]
    try:
        with open('mobileDetails.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames,extrasaction="ignore")
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    getDetails()
