import requests
from bs4 import BeautifulSoup



def getPrice(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    grid = soup.select(".products-grid")
    try:
        grid = grid[0]
        try:
            price = soup.select(".special-price")[0].text
        except:
            price = soup.select(".old-price")[0].text
    except:
        print('not found')
        return 

    price = price.replace('Rs','').replace(',','').replace('.00','').replace('.','').strip()
    
    return price