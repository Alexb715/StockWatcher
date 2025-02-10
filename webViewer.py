from bs4 import BeautifulSoup
import requests
import re
#           newegg
#website = {"https://www.newegg.ca/p/pl?N=100007708%20601469156", "https://www.canadacomputers.com/en/search?s=rtx+5080", "https://www.canadacomputers.com/en/search?s=rtx+5080"}\
    #for testing putposes
website = {"https://www.canadacomputers.com/en/search?s=rtx+4060"}


class web:
    def __init__(self):
        self.Instock = []
        self.webData = {}  # This will store the parsed web data by index (or URL)
        count = 0
        #passes thru all url in list above
        for url in website:
            response = requests.get(url)
            if response.status_code == 200:
                #make it in a soup format
                soup = BeautifulSoup(response.content, 'html.parser')
                soup.prettify()
                #adds it to a table
                self.webData[count] = soup  # Store the parsed data by count
                count += 1
            else:
                print(f"Failed to fetch data from {url}")
        #for newegg websites
    def forNewegg(self,data):
        #for finds all btn which say add to cart which are the ones in stock
        for inStock in data.find_all(class_="btn btn-primary btn-mini"):
            #finds the top parent to get usuful information
            parent=inStock.find_parent('div', class_="item-cell")
            #finds the price which is hidden in a list
            price = parent.find('li', class_='price-current').find('strong').text
            #gets the clickable url immediatly
            url = parent.find('a').get('href')
            #also gets the title
            title = parent.find('a',class_='item-title').text
            #adds it to a list
            self.Instock.append((title,price,url)) 
    def forCC(self,data):
        #gets the availble tage of all items
        for inStock in data.find_all(class_="available-tag"):
            #if its available for online delivery
            if inStock.get('data-stock_availability_online') == '1':
                #get the parent of the item
                parent = inStock.find_parent('div',class_="js-product product col-sm-6 col-xl-3")
                #find the url
                url = parent.find('a',class_='thumbnail product-thumbnail').get('href')
                #find the title
                title = parent.find('h2',class_='h3 product-title mb-1').find('a').text
                #find the price and chang the format
                price = parent.find('span', {'aria-label': 'Price'}).text
                price = re.sub(r'[^0-9.,]', '', price)
                #add it to the list
                self.Instock.append((title,price,url))
            else:
                continue
    def checkForStockedItems(self):
        for count, data in self.webData.items():
            if 'Newegg' in data.title.string:        
                self.forNewegg(data)
                
            if 'Canada Computers & Electronics' in data.title.string:
                self.forCC(data)
            else:
                print("Unknown Website")