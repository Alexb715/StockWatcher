from bs4 import BeautifulSoup
import requests
import random
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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
website = {r'https://www.newegg.ca/p/pl?N=100007708%20601469156%20601469154&PageSize=96', r'https://www.canadacomputers.com/en/search?s=rtx+5070+ti', r'https://www.memoryexpress.com/Category/VideoCards?FilterID=1c84b44a-7d8b-bfad-8f43-f0cbe5b89a34&Sort=Price&PageSize=120',
           r'https://www.canadacomputers.com/en/search?s=rtx+5080', r'https://www.vuugo.com/category/video-cards-563/?min-price=0&max-price=10700&ordering=newest&G PU=GeForce+RTX+5000+Series',r'https://www.canadacomputers.com/en/search?s=rtx+5070',
           r'https://www.bestbuy.ca/en-ca/collection/nvidia-founders-edition/412549?icmp=computing_nvidia_graphic_cards_ssc_category_icon_founders_edition',r'https://www.pc-canada.com/?query=rtx%205070%20ti&productType=Graphic%20Card',
           r'https://www.bestbuy.ca/en-ca/collection/nvidia-graphic-cards-rtx-50-series/bltbd7cf78bd1d558ef?sort=priceLowToHigh',r'https://www.pc-canada.com/?query=rtx%205070&productType=Graphic%20Card',r'https://www.vuugo.com/category/video-cards-563/?min-price=0&max-price=2202&ordering=newest&GPU=GeForce+RTX+4000+Series&GPU=GeForce+RTX+5000+Series'}
class web:

    def __init__(self):
        self.headerForRequests  = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}
        self.Instock = []
        self.webData = {}  
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
    def forMemory(self,data):
        for Instock in data.find_all('a', title="Buy this item."):
            parent = Instock.find_parent('div',class_='c-shca-icon-item')
            title = parent.find('div',class_='c-shca-icon-item__body-name').find('a').text
            url = parent.find('div',class_='c-shca-icon-item__body-name').find('a').get('href')
            url = "https://memoryexpress.com" + url
            price = parent.find('div',class_='c-shca-icon-item__summary-list').find('span').text
            price = re.sub(r'[^0-9.,]', '', price)
            url = url.replace('\n',' ').replace('\t',"")
            title = title.replace('\t',' ').strip()
            self.Instock.append((title,price,url))
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
    def forCP(self,data):
        for Instock in data.find_all('p',class_='mb-0 fs-sm text-center fw-bold text-green-500'):
            parent = Instock.find_parent('div',class_='col-6 col-lg-4 col-xl-3 col-xxxl-2')
            price = parent.find('p',class_='mb-0 mt-0.5rem text-red-500 fw-bolder fs-2xl text-center').text
            price = re.sub(r'[^0-9.,]', '', price)
            titlearea = parent.find('p',class_='GridDescription-Clamped mb-0 fs-xs')
            title = titlearea.text
            url = parent.find('a',class_="d-block mt-0.5rem fw-bold text-gray-800 text-red-500-hover text-decoration-none text-center transition duration-150 ease-in-out").get('href')
            url = 'https://www.pc-canada.com'+url
            title = title.replace('\n',' ').replace('\t',"")
            self.Instock.append((title,price,url))
    
    def forBB(self,data):
        for Instock in data.find_all('span',class_='container_1DAvI'):
            if Instock.text in ['Available to ship', 'Available for backorder']:
                parent = Instock.find_parent('a',class_='link_3hcyN inline-block h-full w-full focus-visible-outline-2')
                title = parent.find('h3',class_="productItemName_3IZ3c").text
                price = parent.find('div',class_='productPricingContainer_3gTS3').find('span').find('span').text
                price = re.sub(r'[^0-9.,]', '', price)
                url = 'https://bestbuy.ca'+ parent.get('href')
                self.Instock.append((title,price,url))
    def checkForStockedItems(self):
        for count, data in self.webData.items():
            if 'Canada Computers' in data.title.text:
                self.forCC(data)
                print("Running CanadaComputers Website\n")
                continue
            if 'Newegg' in data.title.text:     
                print("Running Newegg Website\n")   
                self.forNewegg(data)
                continue
            if 'Memory' in data.title.text:
                #error 403 need to bypass
                print('Running Memory Express\n')
                self.forMemory(data)
                continue
            if 'Vuugo' in data.title.text:
                print('Running Vugoo\n')
                self.forVugoo(data)
                continue
            if 'PC-Canada.com' in data.title.text:
                print("Running PC-Canada\n")
                self.forCP(data)
                continue
            if"Best Buy" in data.title.text:
                print("Running BestBuy\n")
                self.forBB(data)
            else:
                print("Unknown Website Please Edit and try again")
                print(data.title.string)
    def Run(self,previous):
        self.webData.clear()
        self.GetData()
        self.Instock.clear()
        self.checkForStockedItems()
        #if it didnt change dont send again
        amount = len(self.Instock)
        print(f"Found {amount} items")
        if(previous == self.Instock):
            self.Instock.clear()
            print("no new devices\n")
    def GetData(self):
        count = 0
        #passes thru all url in list above
        for url in website:
            if'bestbuy' not in url:
                response = requests.get(url,headers=self.headerForRequests)
                if response.status_code == 200:
                #make it in a soup format
                    soup = BeautifulSoup(response.content, 'html.parser')
                    soup.prettify()
                #adds it to a table
                    self.webData[count] = soup  # Store the parsed data by count
                    count += 1
                elif response.status_code == 403:
                #goes thru headless to mitigate cloudflare
                    self.webData[count] = self.goThruHeadless(url)
                    count+=1
                else:
                    print(f"Failed to fetch data from {url} response code {response.status_code}")
            elif 'bestbuy' in url:
                self.webData[count] = self.goThruHeadless(url)
                count+=1
            else:
                print('error')
    def goThruHeadless(self, url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if os.uname().machine == "x86_64":
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        else:
            driver = webdriver.Chrome(
            service=Service('/usr/lib/chromium-browser/chromedriver'),
            options=chrome_options)
        if os.uname().nodename == 'raspberrypi':
            driver.set_page_load_timeout(300)
            driver.set_script_timeout(300)
    # Use selenium-stealth to bypass detection
        
        print('running headless')
        if'bestbuy' not in url:
                #best buy breaks if stealth is on
            stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        try:  
            #here is usually where it fails 
            driver.get(url)
            #makes sure the website loads correctly
            time.sleep(5)
        # Extract content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            return soup
        except:
            print("ERROR" + str(driver.error_handler))

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
            self.fullMessage = ''
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
       self.fullMessage = "In Stock \n" + "\n".join([" ".join(item) for item in inStock])
    def splitMessage(self):
        print('Splitting Message\n')
    #found 1000 char to be not too long not to short
        max_length = 1000
        self.splitMessages = []
        #while its too long
        while len(self.fullMessage) > max_length:
        # Find the nearest space or punctuation before the max_length
            split_at = max_length
            for i in range(max_length, 0, -1):
                if self.fullMessage[i] in ' .,;!?':
                    split_at = i
                    break

        # Split the string at the found position
            part = self.fullMessage[:split_at].strip()
            self.splitMessages.append(part)

        # Remove the processed part from the long_string
            self.fullMessage = self.fullMessage[split_at:].strip()

    # Add the remaining part of the string
        if self.fullMessage:
            self.splitMessages.append(self.fullMessage)

    def sendEmail(self, inStock):
        #checks if anything is in stock
        if len(inStock) == 0:
            print("nothing in stock")
            return
        #creates the message
        self.createMessage(inStock)
        #prepares to send and advises as much
        print('Sending Message')
        self.splitMessage()
        for i in self.splitMessages:
            message = MIMEMultipart()
            message['to'] = self.toEmail 
            message['from'] = self.fromEmail
            message['subject'] = 'ALERT'
            msg = MIMEText(i)
            message.attach(msg)
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            try:
            #sends message
                send_message = self.service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
                print("message sent")
                time.sleep(5)
            except Exception as error:
                print(error)

def main():
    print(len(website))
    previous = []
    site = web()
    #get Current list that we dont want sent
    message =sendMessage()
    while True:
        site.Run(previous)
        previous = site.Instock
        message.sendEmail(site.Instock)
        time.sleep(60)
main()