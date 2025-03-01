import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set up Chrome WebDriver path (adjust to your location)
service = Service("C:/WebDriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)


# Define helper functions
def navigate_to_forgot_password_page():
    """Navigates to the forgot password page."""
    driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/loginu")
    try:
        # Wait for forgot password link to be clickable and click on it
        forgot_password_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot Password?"))
        )
        forgot_password_link.click()
        print("Navigated to Forgot Password page")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed to navigate to Forgot Password page: {e}")


def validate_email_field():
    """Check for mandatory email field and validate email format."""
    try:
        # Ensure email field exists
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_17406477278348063")))
        print("Email field found")

        # Check if the field is required
        if email_field.get_attribute('required'):
            print("Email field is mandatory")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed to locate email field: {e}")


def test_valid_input():
    """Test forgot password functionality with valid email."""
    try:
        email_field = driver.find_element(By.ID, "id_17406477278348063")
        submit_button = driver.find_element(By.ID, "staticElement")

        # Provide a registered email
        email_field.clear()
        email_field.send_keys("registered@example.com")
        submit_button.click()

        # Wait for success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Reset link sent to your email')]"))
        )
        print("Success message received:", success_message.text)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed during valid input test: {e}")


def test_invalid_inputs():
    """Test forgot password functionality with invalid inputs."""
    try:
        email_field = driver.find_element(By.ID, "id_17406477278348063")
        submit_button = driver.find_element(By.ID, "staticElement")

        # Test with non-registered email
        email_field.clear()
        email_field.send_keys("nonregistered@example.com")
        submit_button.click()

        # Wait for error message
        non_registered_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email not found')]"))
        )
        print("Non-registered email message received:", non_registered_message.text)

        # Test with invalid email format
        email_field.clear()
        email_field.send_keys("invalid-email-format")
        submit_button.click()

        invalid_email_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid email format')]"))
        )
        print("Invalid email format message received:", invalid_email_message.text)

        # Test with blank email field
        email_field.clear()
        submit_button.click()

        blank_email_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email is required')]"))
        )
        print("Blank email field message received:", blank_email_message.text)

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed during invalid input tests: {e}")


# Running the tests
navigate_to_forgot_password_page()
validate_email_field()
test_valid_input()
test_invalid_inputs()

# Close the browser after tests
input("Press Enter to close the browser...")
driver.quit()
