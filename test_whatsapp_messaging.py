import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote

@pytest.fixture(scope="module")
def driver():
    # Set options for Chrome WebDriver
    options = Options()
    options.headless = True  # Headless mode for CI environments
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get('https://web.whatsapp.com')
    yield driver
    driver.quit()

def test_login_page_loaded(driver):
    # Ensure that the WhatsApp web login page loads correctly
    assert "WhatsApp" in driver.title

def test_send_message_to_contact(driver):
    # Test sending a message to a contact and verify it's sent
    phone_number = "+1234567890"
    message = "Hello, this is a test message!"
    encoded_message = quote(message)
    url = f'https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}'
    driver.get(url)
    
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]'))
        )
        send_button.click()
        assert "sent" in driver.page_source  # Confirm message appears as sent in the page
    except Exception as e:
        pytest.fail(f"Failed to send message: {str(e)}")

def test_message_send_failure(driver):
    # Verify that error handling works when message sending fails
    phone_number = "+1234567890"
    message = "This will not send."
    encoded_message = quote(message)
    url = f'https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}'
    driver.get(url)
    
    try:
        # Attempt to click a non-existent button to simulate a failure
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="non-existent-button"]'))
        ).click()
    except Exception:
        # Check for error message display
        assert "error" in driver.page_source, "Error message should be displayed"
