# Stock Watcher - Web Scraping and Email Notification System

This project is a Python-based web scraping tool designed to monitor stock availability for specific products (e.g., GPUs) across multiple e-commerce websites. When products are in stock, the system sends email notifications to a specified recipient using the Gmail API.
## Features

- **Web Scraping**: Monitors stock availability on multiple websites, including:
    - Newegg
    - Canada Computers
    - Memory Express
    - Vuugo
    - PC-Canada
    - Best Buy Canada

- **Headless Browsing**: Uses Selenium with a headless Chrome browser to bypass anti-scraping measures (e.g., Cloudflare).

- **Email Notifications**: Sends email alerts via Gmail API when products are in stock.

- **Cross-Platform**: Works on both x86_64 and ARM64 architectures.

- **Customizable**: Easily add or remove websites to monitor.

## Requirements

- Python 3.10 or higher

- Libraries:

    - beautifulsoup4

    - requests

    - selenium

    - webdriver_manager

    - selenium-stealth

    - google-auth

    - google-api-python-client

    - google-auth-oauthlib

    - google-auth-httplib2

- Chrome or Chromium browser installed.

- Gmail API credentials (credentials.json).

## Installation

**Clone the Repository**:
```bash
git clone https://github.com/yourusername/StockWatcher.git
cd StockWatcher 
```
**Set Up a Virtual Environment** :
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
**Install Dependencies** :
```bash
    pip install -r requirements.txt
```
**Set Up Gmail API** :
- Go to the Google Cloud Console.

- Create a new project and enable the Gmail API.

- Download the credentials.json file and place it in the project directory.

**Set Up Email Recipient**:

- Create a file named email.txt in the project directory.

- Add the recipient's email address on the first line and the sender's email address on the second line:
```
recipient@example.com
sender@example.com
```
:bulb: **Tip:** For SMS Check for your SMS Gateway Address usually `number@carrieraddress`

**Install ChromeDriver**:

- For x86_64 systems, the script will automatically install ChromeDriver using webdriver_manager.

- For ARM64 systems, manually install Chromium and its corresponding chromedriver:
    ```bash
        sudo apt-get install chromium-browser chromium-chromedriver
    ```
## Usage
**Run the Script** :
```bash
    python webViewer.py
```
**How It Works**:

The script periodically checks the specified websites for stock availability.

If products are in stock, it sends an email notification with the product details (title, price, and URL).

The script runs indefinitely, checking for stock every 60 seconds.

Customize Websites:

To add or remove websites, modify the website set in the script:
```python
        website = {
            r'https://www.newegg.ca/p/pl?N=100007708%20601469156%20601469154&PageSize=96',
            r'https://www.canadacomputers.com/en/search?s=rtx+5070+ti',
            # Add more URLs here
        }
```
:warning: **Warning:** For better bot detection avoidence try not to put two of the same website back to back if they use detection
## File Structure
```
StockWatcher/
├── webViewer.py            # Main script
├── credentials.json        # Gmail API credentials
├── token.json              # OAuth2 token (generated after first run)
├── email.txt               # Email addresses for notifications
├── requirements.txt        # Python dependencies
└── README.md               # This file
```
## **Troubleshooting**

#### **Error: `OSError: [Errno 8] Exec format error`**
This error occurs when the system cannot execute the `chromedriver` binary due to incompatibility with your system architecture (common on ARM64 devices).

#### **Causes**
1. Incorrect `chromedriver` version for your CPU architecture.
2. Corrupted or incompatible `chromedriver` binary.
3. Missing dependencies for ARM64 systems.

#### **Solutions**
1. **For ARM64 Systems**:
   ```bash
   # Install Chromium and ARM64-compatible chromedriver
   sudo apt-get install chromium-browser chromium-chromedriver

   # Verify installation
   which chromium-browser  # Should return /usr/bin/chromium-browser
   which chromedriver      # Should return /usr/bin/chromedriver
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    Selenium for browser automation.

    Beautiful Soup for HTML parsing.

    Google Gmail API for email notifications.

Contact

For questions or feedback, please contact Your Name.

Enjoy monitoring your favorite products! 🚀