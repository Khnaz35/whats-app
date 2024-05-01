from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep 
from urllib.parse import quote
import csv
import logging
import os
from logging.handlers import RotatingFileHandler

# Setup logging with rotation
log_filename = 'whatsapp_messenger.log'
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Rotate log file when it reaches 10 MB, keep 5 old log files as backup
log_handler = RotatingFileHandler(log_filename, maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set to ERROR or WARNING to reduce log output
logger.addHandler(log_handler)

# Example usage
logger.info("This is an informational message")

# Setup options for Chrome Canary
options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
os.environ["WDM_LOG_LEVEL"] = "0"

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
logging.info('Web driver initialized, navigating to WhatsApp Web.')
driver.get('https://web.whatsapp.com')

# Load CSV file
with open('contacts.csv', mode='r', encoding='utf8') as file:
    csv_reader = csv.DictReader(file)
    contacts = list(csv_reader)
logging.info(f'Loaded {len(contacts)} contacts from CSV.')

input("After logging into WhatsApp Web and your chats are visible, press ENTER...")

# Message sending logic
delay = 30  # seconds to wait for elements to appear
for idx, contact in enumerate(contacts):
    personalized_message = contact['Message'].replace("{%S first name last name}", f"{contact['FirstName']} {contact['LastName']}")
    message = quote(personalized_message)
    phone_number = contact['Phone']
    
    logging.info(f'Starting to send message to {phone_number} ({idx+1}/{len(contacts)}).')
    try:
        url = f'https://web.whatsapp.com/send?phone={phone_number}&text={message}'
        sent = False
        for attempt in range(3):
            if not sent:
                driver.get(url)
                try:
                    click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')))
                    sleep(1)
                    click_btn.click()
                    sent = True
                    sleep(3)
                    logging.info(f'Message successfully sent to {phone_number}.')
                except Exception as e:
                    logging.error(f"Attempt {attempt+1}: Failed to send message to {phone_number}. Error: {str(e)}")
                    if attempt == 2:
                        logging.error(f"Final attempt failed. Message not sent to {phone_number}.")
    except Exception as e:
        logging.error(f'Error sending message to {phone_number}: {str(e)}')

driver.close()
logging.info('Web driver closed.')
