import requests
from bs4 import BeautifulSoup


def scrape(name):
    print(name)
    name = name.replace(' ', '+')   
    url = f"https://www.soundpeats.pk/search?type=product&q={name}"
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    prod = soup.select(".product-card")
    try:
        prod = prod[0]
        print(prod)
        price = prod.select("price-list.justify-center > sale-price:nth-child(1)")[0].text
        print(price)
        price = price.replace('Rs.','').replace(',','').strip()
        price = ''.join(filter(lambda x: x.isdigit() or x == '.', price))

        title = prod.select('.product-card__title > a:nth-child(1)')[0]
        print(title.text)

        url = title['href']
        print(url)

        return (price, url)
    except:
        return (None, url)
    

if __name__ == '__main__':
    scrape('halo')