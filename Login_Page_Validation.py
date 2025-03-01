import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver with the Service object pointing to chromedriver executable
service = Service('C:/WebDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Open the NoKodr platform login page
driver.get('https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/loginu')
# Set up WebDriverWait (1800 seconds timeout)
wait = WebDriverWait(driver, 1800)


# Validate input fields for mandatory requirements
def check_mandatory_fields():
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))  # Wait for the username field
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))  # Wait for the password field

    # Check that both fields are empty initially
    assert username_field.get_attribute('value') == ''
    assert password_field.get_attribute('value') == ''

    # Check form submission without filling fields
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, 'staticElement')))
    login_button.click()

    # Check for error messages
    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'This field is required' in error_message.text  # Validate error text


# Test for valid credentials
def test_valid_credentials():
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, 'staticElement')))

    username_field.clear()
    username_field.send_keys('validUsername')
    password_field.clear()
    password_field.send_keys('ValidPassword123!')
    login_button.click()

    # Validate redirection to dashboard
    time.sleep(2)
    assert driver.current_url == 'https://app-staging.nokodr.com/super/apps/user-profile/v1/index.html#/'


# Test for invalid credentials
def test_invalid_credentials():
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    # Test incorrect username
    username_field.clear()
    username_field.send_keys('invalidUsername')
    password_field.clear()
    password_field.send_keys('ValidPassword123!')
    login_button.click()

    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error_message.text

    # Test incorrect password
    username_field.clear()
    username_field.send_keys('validUsername')
    password_field.clear()
    password_field.send_keys('wrongPassword')
    login_button.click()

    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error_message.text


# Test for blank fields
def test_blank_fields():
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    # Test blank username
    username_field.clear()
    password_field.clear()
    password_field.send_keys('ValidPassword123!')
    login_button.click()

    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'This field is required' in error_message.text

    # Test blank password
    username_field.clear()
    username_field.send_keys('validUsername')
    password_field.clear()
    login_button.click()

    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'This field is required' in error_message.text


# Test for special characters
def test_special_characters():
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    username_field.clear()
    password_field.clear()
    username_field.send_keys('validUsername')
    password_field.send_keys('Pass@#$%^&*!')
    login_button.click()

    error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error_message.text


# Run all tests
try:
    check_mandatory_fields()
    test_valid_credentials()
    test_invalid_credentials()
    test_blank_fields()
    test_special_characters()

    # Hold the browser open until you manually close it by pressing "Enter"
    input("Press Enter to close the browser...")
finally:
    driver.quit()
