import requests
from bs4 import BeautifulSoup


def scrape(name):
    print(name)
    name = name.replace(' ', '+')
    url = f"https://gfivepakistan.com/search?type=product&q={name}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    prod = soup.select(".col-md-4")

    try:
        prod = prod[0]
        try:
            price = prod.select(".sold-out > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > span:nth-child(2)")[0].text
        except:
            price = prod.select(".sold-out > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > span:nth-child(1)")[0].text
        price = price.replace('Rs','').replace(',','').replace('.00','').replace('.','').strip()
        title = prod.select('.sold-out > div:nth-child(1) > div:nth-child(2) > a:nth-child(2)')[0]
        print(title.text)
        url ="https://gfivepakistan.com/" +  title['href']

        print(price, url)
        return (price, url)
    except:
        return (None, url)
    

if __name__ == '__main__':
    scrape('gfive g550 power')