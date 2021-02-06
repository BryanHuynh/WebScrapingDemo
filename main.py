from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def main():
    print("start..")
    noNewLine = re.compile('\n')
    source = requests.get("https://www.memoryexpress.com/Category/VideoCards?Search=rtx+3070").text
    soup = BeautifulSoup(source, 'lxml')
    products = soup.find_all('div', {"class":"c-shca-icon-item"})
    productNames = []
    productPrices = []
    productStocks = []

    for product in products: 
        productName = product.find('div', {"class":"c-shca-icon-item__body-details"}).find('a').text
        productName = re.sub('\n+(\s*)', '' , productName)
        productNames.append(productName)
        productPrice = product.find('div', {'class': 'c-shca-icon-item__summary-list'}).text
        productPrice = re.sub('\n+(\s*)', '' , productPrice)
        productPrice = re.sub('[\\r+\\r]', '' , productPrice)
        productPrices.append(productPrice)
        productStock = ''
        try:
            productStock = product.find('div', {'class': 'c-shca-icon-item__body-inventory'}).text
            productStock = re.sub('\n+(\s*)', '' , productStock)
        except:
            productStock = "AVAILABLE"
        productStocks.append(productStock)
        
    productTable = {'Product': productNames,
            'Price': productPrices,
            'Stock': productStocks,
            }

    df = pd.DataFrame(productTable, columns = ['Product', 'Price', 'Stock'])

    print (df)

if __name__ == "__main__":
    main()