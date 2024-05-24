import requests
from bs4 import BeautifulSoup
import  csv 
import json


"""
    Bring links to follow one format either pages/phoneName/specs or product/phoneName
    pages have more specs
    products is for shoppers and offers only basic info
    going with products because not all phones have pages
    """


def getModelsName(write:bool = False):
    page = 1
    data = []
    while 1:
        try:
            url  = f"https://mistore.pk/collections/smartphones?page={page}"
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
                obj['link'] = a['href'] if  'products' in a['href'] else a['href'].replace('pages', 'products').replace('-overview', '')
                obj['name'] = a.text.strip() 
                data.append(obj)  
            page += 1
        except:
            break
    
    if write:
        with open('data/mobileNameLink.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    with open('data/mobileNameLink.csv', 'r',encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = []
        baseUrl = 'https://mistore.pk'
        for row in reader:
            obj = {}
            url = baseUrl +  row['link']
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            # .short-description > ul:nth-child(3)
            
            keyFeatureListLi = soup.select('.short-description.checkshort > ul li')
            if len(keyFeatureListLi)== 0:
                continue
            i = 0
            while i < len(keyFeatureListLi):
                try:
                    print('keyFeatureListLi')
                    print(i)
                    obj[keyFeatureListLi[i].find('strong').text.strip()] = keyFeatureListLi[i].text.strip().replace(keyFeatureListLi[i].find('strong').text.strip(), '')
                    try:
                        if keyFeatureListLi[i+1].find('strong') is None:
                            obj[keyFeatureListLi[i].find('strong').text.strip()] +=  keyFeatureListLi[i+1].text.strip()
                            i+=1
                            print('i', i)
                    except IndexError:
                        pass
                except:
                    i+=1
                    continue
                i+=1

            data.append(obj)
            # with open('testMiStore.html', 'w',encoding="utf-8") as file:
            #     file.write(soup.prettify())
            # try:
            #     obj = {}
            #     obj['name'] = row['name']
            #     obj['link'] = url
            #     obj['price'] = soup.select('.product-price')[0].text
            #     obj['image'] = soup.select('.product-image')[0]['src']
            #     obj['description'] = soup.select('.product-description')[0].text
            #     obj['specification'] = soup.select('.product-description')[1].text
            #     data.append(obj)
            # except:
            #     print(url)
            #     continue
    # with open('data/mobileDetails.json', 'w',encoding="utf-8") as file:
    #     json.dump(data, file, indent=4)
    # return data
    try:
        with open('data/mobileDetails.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames,extrasaction="ignore")
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(e)


"""svm 
test train split
random forest 
rvc curve"""
if __name__ == "__main__":
    # getModelsName(True)
    getDetails()

