import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.headless = True  # Use headless mode for testing
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

    # Setup WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get('https://web.whatsapp.com')
    yield driver
    driver.quit()

def test_login_page_loaded(driver):
    assert "WhatsApp" in driver.title

def test_send_message_to_contact(driver):
    # Assume you have a way to bypass login for testing or use a session that is already logged in
    phone_number = "+1234567890"
    message = "Hello, this is a test message!"
    encoded_message = quote(message)
    url = f'https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}'
    driver.get(url)
    
    # Simulate clicking the send button
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]'))
        ).click()
        assert "sent" in driver.page_source
    except Exception as e:
        pytest.fail(f"Failed to send message: {str(e)}")

def test_message_send_failure(driver):
    # Setup a scenario where sending will fail
    phone_number = "+1234567890"
    message = "This will not send."
    encoded_message = quote(message)
    url = f'https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}'
    driver.get(url)
    
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="non-existent-button"]'))
        ).click()
    except Exception:
        assert "error" in driver.page_source, "Error message should be displayed"

