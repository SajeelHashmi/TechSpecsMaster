import requests
from bs4 import BeautifulSoup
import  csv 
import json

def getModelsName(write:bool = False):
    url  = "https://danytech.com.pk/collections/wireless-earbuds"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    modelsDiv = soup.select('#main-collection-product-grid > div > div')
    print(len(modelsDiv))
    data=[]
    for model in modelsDiv:
        a = model.select('a.product-title')
        data.append({
            'link' : a[0]['href'],
            'name' : a[0].find('span').text.strip()
            })
    if write:
        with open('data/earbudsNameLink.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    models = []
    with open('data/earbudsNameLink.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    print( models[0])
    for model in models:
        obj = {}
        # print(model['model'])
        
        obj['name'] = model['name']
        url = model['link']+ "/specs/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        size = soup.select('div.product-size')
        sizeFeatures = soup.select('.large-accordion__inner.large-accordion__inner--short')
        for feature in sizeFeatures:
            obj[feature.find('div').text] = feature.find('p').text
        colors = soup.select('.spec-ul-color li')
        obj['colors'] = [color.text for color in colors]
        # all this is in one paragraph unable to write a perfect scrapper for this
        """ 
            Size:
            6.58 inches
            *With a rounded corners design on the display, the diagonal length of the screen is 6.58 inches when measured according to the standard rectangle (the actual viewable area is slightly smaller).

            Colour:
            16.7 million colours

            Type:
            OLED, up to 90 Hz frame refresh rate

            Resolution:
            2640 x 1200 Pixels
            *The resolution measured as a standard rectangle, with a rounded corners design, the effective pixels are slightly less.
        """
        data.append(obj)
    try:
        with open('data/earbudsDetails.csv', 'w',encoding="utf-8",newline="") as file:
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

