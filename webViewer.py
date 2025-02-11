from bs4 import BeautifulSoup
import requests
import re
import time
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import textwrap
website = {"https://www.newegg.ca/p/pl?N=100007708%20601432392%20601408875%20601432394%20601408874&d=rtx+5060&isdeptsrh=1","https://www.newegg.ca/p/pl?N=100007708%20601469156",
        "https://www.canadacomputers.com/en/search?s=rtx+5080","https://www.canadacomputers.com/en/search?s=rtx+5090",'https://www.canadacomputers.com/en/search?s=rtx+5070+ti',"https://www.canadacomputers.com/en/search?s=rtx+5070" , "https://www.newegg.ca/p/pl?d=rtx+5070","https://www.newegg.ca/p/pl?d=rtx+5070+ti"
       }
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
                print(f"Failed to fetch data from {url} response code {response.status_code}")
        #for newegg websites
    def forNewegg(self,data):
        #for finds all btn which say add to cart which are the ones in stock
        for inStock in data.find_all(class_="btn btn-primary btn-mini"):
            #finds the top parent to get usuful information
            parent=inStock.find_parent('div', class_="item-cell")
            #finds the price which is hidden in a list
            price = parent.find('li', class_='price-current').find('strong').text
            price = re.sub(r'[^0-9.,]', '', price)
            #gets the clickable url immediatly
            url = parent.find('a').get('href')
            #also gets the title
            title = parent.find('a',class_='item-title').text
            #adds it to a list
            print("Found Device " + title + '\n')
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
                print("Found Device " + title + '\n')
                self.Instock.append((title,price,url))
            else:
                continue
    def forMemory(self,data):
        for Instock in data.find_all('a', title="Buy this item."):
            print('found Something')
    def forVugoo(self,data):
        for Instock in data.find_all('div', class_='in-stock'):
            #find the parent with the right class
            parent = Instock.find_parent('div', class_='product-wrap mb-2')
            #get the price info
            price = parent.find(class_='new-price').text
            price = re.sub(r'[^0-9.,]', '', price)
            #get the title
            title = parent.find('h3').find('a').get('title')
            urltmp = parent.find('h3').find('a').get('href')
            #get and add the complete url
            url = 'https://www.vuugo.com'+urltmp
            self.Instock.append((title,price,url))
            print(title,price,url)
    def forCP(self,data):
        for Instock in data.find_all('p',class_='mb-0 fs-sm text-center fw-bold text-green-500'):
            parent = Instock.find_parent('div',class_='col-6 col-lg-4 col-xl-3 col-xxxl-2')
            price = parent.find('p',class_='mb-0 mt-0.5rem text-red-500 fw-bolder fs-2xl text-center').text
            price = re.sub(r'[^0-9.,]', '', price)
            title = parent.find('p',class_='GridDescription-Clamped mb-0 fs-xs').text
            print(title)
    def checkForStockedItems(self):
        for count, data in self.webData.items():
            if 'Canada Computers' in data.title.string:
                self.forCC(data)
                print("Running CanadaComputers Website\n")
                continue
            if 'Newegg' in data.title.string:     
                print("Running Newegg Website\n")   
                self.forNewegg(data)
                continue
            if 'Memory' in data.title.string:
                #error 403 need to bypass
                print('Running Memory Express\n')
                self.forMemory(data)
                continue
            if 'Vuugo' in data.title.string:
                print('Running Vugoo\n')
                self.forVugoo(data)
                continue
            if'PC-Canada.com' in data.title.string:
                print("Running PC-Canada\n")
                self.forCP(data)
                #error 403 need to bypass
                continue
            else:
                print("null")
    def Run(self,previous):
        self.Instock.clear()
        self.checkForStockedItems()
        #if it didnt change dont send again
        amount = len(self.Instock)
        print(f"Found {amount} items")
        if(previous == self.Instock):
            self.Instock.clear()
            print("no new devices\n")
class sendMessage:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        # If modifying the SCOPES, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.credentials_file = credentials_file  # Path to the credentials file
        self.token_file = token_file  # Path to the token file (stores the OAuth2 credentials)
        self.creds = None  # Variable to store credentials
        #self.service = None  # Variable to store the Google gmail service object
        
        try:
            #try to open file and take contents
            emailFile = open("email.txt")
            self.toEmail = emailFile.readline()
            self.fromEmail = emailFile.readline()
            self.message = ''
        except:
            print("Couldn't find file")
            #run googles credentials and service requirements
        self.load_credentials()
        self.build_service()
    def load_credentials(self):
        """Load the user's credentials from the token file or authenticate the user."""
        if os.path.exists(self.token_file):
            # Load the existing credentials from token.json if it exists
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials exist, we need to authenticate the user
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired credentials using the refresh token
                self.creds.refresh(Request())
            else:
                # Authenticate the user if no valid credentials exist
                self.authenticate_user()
            # Save the credentials for future use
            self.save_credentials()
    def authenticate_user(self):
        """Handle the OAuth2 authentication process."""
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
        self.creds = flow.run_local_server(port=0)  # Launch the OAuth flow in a local server
    def save_credentials(self):
        """Save the credentials to the token file to reuse in the future."""
        with open(self.token_file, "w") as token:
            token.write(self.creds.to_json())  # Write the credentials to token.json
    def build_service(self):
        """Build the Google Calendar service object."""
        if self.creds is None:
            raise ValueError("Credentials not loaded. Call load_credentials first.")
        
        # Use the loaded credentials to build the Calendar API service object
        self.service = build("gmail", "v1", credentials=self.creds)
    def createMessage(self, inStock):
        
        #creates the message by adding everything together
       self.message = "In Stock \n" + "\n".join([" ".join(item) for item in inStock])
    def sendEmail(self, inStock):
        #checks if anything is in stock
        if len(inStock) == 0:
            print("nothing in stock")
            return
        #creates the message
        self.createMessage(inStock)
        #prepares to send and advises as much
        print('Sending Message')
        message = MIMEMultipart()
        message['to'] = self.toEmail 
        message['from'] = self.fromEmail
        message['subject'] = 'ALERT'
        msg = MIMEText(self.message)
        message.attach(msg)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        create_message = {"raw": raw_message}
        try:
            #sends message
            send_message = self.service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
            print("message sent")
        except Exception as error:
            print(error)




def main():
    previous = []
    
    send = sendMessage()
    while True:
        inStockData = web()
        inStockData.Run(previous)
        previous = inStockData.Instock
        print(inStockData.Instock)
        send.sendEmail(inStockData.Instock)
        time.sleep(60)

        
main()
