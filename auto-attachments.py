import os
import shutil
import subprocess
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
import logging
import random
from logging.handlers import RotatingFileHandler
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re
from urllib.parse import quote

# Load configuration from environment.yml
with open("environment.yml", "r") as file:
    config = yaml.safe_load(file)

# Setup logging with rotation
log_level = getattr(logging, config['logging']['level'].upper(), logging.INFO)
log_formatter = logging.Formatter(config['logging']['format'])
log_handler = RotatingFileHandler(config['log_file'], maxBytes=config['max_log_size'], backupCount=config['log_backup_count'])
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(log_level)
logger.addHandler(log_handler)

def get_chrome_canary_version():
    try:
        result = subprocess.run([config['chrome_binary_location'], '--version'], capture_output=True, text=True)
        version = re.search(r'Google Chrome (\d+\.\d+\.\d+\.\d+)', result.stdout)
        if version:
            version = version.group(1)
            logger.info(f'Chrome Canary version: {version}')
            return version
        else:
            logger.error(f"Failed to parse Chrome Canary version: {result.stdout}")
            return None
    except Exception as e:
        logger.error(f"Failed to get Chrome Canary version: {e}")
        return None

def get_compatible_chromedriver_version(chrome_version):
    try:
        major_version = chrome_version.split('.')[0]
        url = 'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json'
        response = requests.get(url)
        if response.status_code == 200:
            versions_info = response.json()
            logger.info(f"API Response: {versions_info}")  # Log the entire response payload for debugging
            if major_version in versions_info["milestones"]:
                chromedriver_info = versions_info["milestones"][major_version]["downloads"]["chromedriver"]
                for entry in chromedriver_info:
                    if entry['platform'] == 'mac-x64':
                        chromedriver_url = entry['url']
                        chromedriver_version = re.search(r'(\d+\.\d+\.\d+\.\d+)', chromedriver_url).group(1)
                        logger.info(f'Compatible ChromeDriver version: {chromedriver_version}')
                        return chromedriver_version
            logger.error(f"No ChromeDriver version found for major version {major_version}")
            return None
        else:
            logger.error(f"Failed to fetch version information from {url}")
            return None
    except Exception as e:
        logger.error(f"Error fetching ChromeDriver version: {e}")
        return None

def initialize_driver():
    chrome_version = get_chrome_canary_version()
    if not chrome_version:
        raise Exception("Unable to get Chrome Canary version")

    chromedriver_version = get_compatible_chromedriver_version(chrome_version)
    if not chromedriver_version:
        raise Exception("Unable to find compatible ChromeDriver version")

    # Ensure to clear any cache that might cause conflicts
    cache_dir = os.path.expanduser("~/.wdm/drivers/chromedriver")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        logger.info('WebDriver Manager cache cleared.')

    # Automatically download the correct ChromeDriver version for Chrome Canary
    service = Service(ChromeDriverManager(driver_version=chromedriver_version).install())

    options = Options()
    options.binary_location = config['chrome_binary_location']
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument(f"--user-data-dir={config['user_data_dir']}")
    os.environ["WDM_LOG_LEVEL"] = "0"

    driver = webdriver.Chrome(service=service, options=options)
    logger.info('Web driver initialized, navigating to WhatsApp Web.')
    driver.get('https://web.whatsapp.com')
    return driver

def load_contacts(file_path):
    with open(file_path, mode='r', encoding='utf8') as file:
        csv_reader = csv.DictReader(file)
        contacts = list(csv_reader)
    logger.info(f'Loaded {len(contacts)} contacts from CSV.')
    return contacts

def send_message(driver, contact, delay, retry_attempts):
    personalized_message = contact['Message'].replace("{%S first name last name}", f"{contact['FirstName']} {contact['LastName']}")
    message = quote(personalized_message)
    phone_number = contact['Phone']
    attachment_path = contact.get('AttachmentPath', '').strip()
    
    logger.info(f'Starting to send message to {phone_number}.')
    url = f'https://web.whatsapp.com/send?phone={phone_number}&text={message}'
    for attempt in range(retry_attempts):
        try:
            driver.get(url)
            sleep(random.uniform(config['min_sleep_time'], config['max_sleep_time']))  # Random delay before interacting

            # If there is an attachment, handle it
            if attachment_path:
                # Click the attach button
                attach_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
                attach_btn.click()
                sleep(random.uniform(config['min_sleep_time'], config['max_sleep_time']))  # Random delay after opening the attachment dialog

                # Select "Photos & videos" option and upload the file
                file_input = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
                )
                file_input.send_keys(attachment_path)
                sleep(random.uniform(config['min_sleep_time'], config['max_sleep_time']))  # Random delay after uploading the file

            # Ensure the send button is clickable and send the message
            send_button = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]'))
            )
            sleep(random.uniform(config['min_sleep_time'], config['max_sleep_time']))  # Random delay before clicking the button
            send_button.click()
            sleep(random.uniform(config['min_sleep_time'], config['max_sleep_time']))  # Random delay after sending the message
            logger.info(f'Message successfully sent to {phone_number}.')
            return True
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: Failed to send message to {phone_number}. Error: {str(e)}")
            sleep(2 ** attempt)  # Exponential backoff
    logger.error(f"Final attempt failed. Message not sent to {phone_number}.")
    return False

def main():
    driver = None
    try:
        driver = initialize_driver()
        contacts = load_contacts(config['contacts_file'])
        input("After logging into WhatsApp Web and your chats are visible, press ENTER...")
        for contact in contacts:
            send_message(driver, contact, config['delay'], config['retry_attempts'])
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
    finally:
        if driver:
            driver.close()
            logger.info('Web driver closed.')

if __name__ == "__main__":
    main()
