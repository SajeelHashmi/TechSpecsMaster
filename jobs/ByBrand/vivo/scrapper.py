import requests
from bs4 import BeautifulSoup


def getData():
    url = f"https://www.vivo.com/pk"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    ul = soup.select(".shop-items-main > li")
    for li in ul:

        titleEl = li.select('.product-box-title')[0]
        title = titleEl.text.strip().lower()
        link = "https://zerolifestyle.co" + titleEl.find('a')['href']
        price = li.select('.pbprice h5')[0].text
        price = price.replace('Rs.','').replace(',','').strip()
        price = ''.join(filter(lambda x: x.isdigit() or x == '.', price))
        data.append({
            'name': title,
            'price': price,
            'url': link
        })
    return data


if __name__ == '__main__':
    data = getData()
    print(data)