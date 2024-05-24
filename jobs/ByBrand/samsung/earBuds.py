
# use this api for samsung products
import requests
import  csv 
import json
# Get modelCode using this api 
# change sort = recommended to sort = newest to get the latest products
# https://searchapi.samsung.com/v6/front/b2c/product/finder/global?type=01010000&siteCode=pk&start=25&num=12&sort=recommended&onlyFilterInfoYN=N&keySummaryYN=Y&specHighlightYN=Y&familyId=
#  eg modelCode SM-S928BZTQMEA
typeCode = "01040000"


# insert modelCode in this api to get the details of the mobile
# keep spec anotation to N to reduce size of the response
# https://searchapi.samsung.com/v6/front/b2c/product/spec/detail?siteCode=pk&modelList=SM-S928BZTQMEA&specAnnotationYN=Y
# https://searchapi.samsung.com/v6/front/b2c/product/spec/detail?siteCode=pk&modelList=SM-S928BZTQMEA&specAnnotationYN=Y

def getModelsName(write:bool = False):
    modelsApi  = f"https://searchapi.samsung.com/v6/front/b2c/product/finder/global?type=01040000&siteCode=pk&start=0&num=500000&sort=recommended&onlyFilterInfoYN=N&keySummaryYN=N&specHighlightYN=N&familyId="
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
        with open('earphoneNameModel.csv', 'w',encoding="utf-8",newline="") as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    return data

def getDetails():
    models = []
    with open('earphoneNameModel.csv', 'r', encoding="utf-8") as file:
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
        with open('earphoneDetails.csv', 'w',encoding="utf-8",newline="") as file:
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

