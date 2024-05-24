
import requests
import  csv 
import json

def getModelsName(write:bool = False):
    modelsApi  = "https://searchapi.samsung.com/v6/front/b2c/product/finder/global?type=01020000&siteCode=pk&start=0&num=500000&sort=recommended&onlyFilterInfoYN=N&keySummaryYN=N&specHighlightYN=N&familyId="
    res = requests.get(modelsApi)
    jsonRes = json.loads(res.text)
    totalRecords = jsonRes['response']['resultData']['common']['totalRecord']
    print(totalRecords)
    productList = jsonRes['response']['resultData']['productList']
    data = []
    for product in productList:
        data.append({
        "model" : product['modelList'][0]['modelCode'],
        "name" : product['modelList'][0]['displayName'],
        })
    
    # print(data)
    if write:
        with open('tabletNameModel.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    models = []
    with open('tabletNameModel.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append(row)
    data = []
    print( models[0])
    i = 1
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
        print(i)
        i += 1
        data.append(obj)
    print(data[0].keys()    )
    try:
        with open('tabletDetails.csv', 'w',encoding="utf-8",newline="") as file:
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

    

