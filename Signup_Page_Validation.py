import time  # For time.sleep() if you want to use it
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set up Chrome WebDriver path (adjust to your location)
service = Service("C:/WebDriver/chromedriver.exe")  # Ensure this path is correct for your system
driver = webdriver.Chrome(service=service)


# Define helper functions
def validate_mandatory_fields():
    """Function to check mandatory fields on the signup page."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")  # Adjust this URL if needed

        # Wait for the signup button to be present
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup_button_id"))  # Replace with the actual button ID
        )
        print("Signup button found")

        # Check for mandatory fields
        name_field = driver.find_element(By.ID, "name")  # Adjust with actual name field ID
        email_field = driver.find_element(By.ID, "email")  # Adjust with actual email field ID
        password_field = driver.find_element(By.ID, "password")  # Adjust with actual password field ID
        confirm_password_field = driver.find_element(By.ID, "confirm_password")  # Adjust with actual confirm password field ID

        # Print found fields for debugging
        print("Name field, Email field, Password field, Confirm Password field found")

        # Enter valid data into the fields
        name_field.send_keys("Test User")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("ValidPassword123")
        confirm_password_field.send_keys("ValidPassword123")

        # Submit the form
        signup_button.click()
        print("Form submitted")

        # Increase the wait time to allow for server-side processing
        time.sleep(5)  # Adding a small delay for testing purposes

        # Wait for success message (check the correct XPath or use class name if needed)
        success_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Account created successfully!')]"))
        )
        print("Signup successful:", success_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
        print(driver.page_source)  # Print page source to debug what content is actually on the page
    finally:
        # Wait for user input before closing the browser
        input("Press Enter to close the browser...")
        driver.quit()


def test_invalid_email_format():
    """Function to test invalid email format validation."""
    try:
        driver.get("https://app-staging.nokodr.com/signup")

        # Locate fields
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        password_field = driver.find_element(By.ID, "password")
        confirm_password_field = driver.find_element(By.ID, "confirm_password")
        signup_button = driver.find_element(By.ID, "signup_button_id")  # Replace with actual ID

        # Enter invalid email format
        email_field.send_keys("invalid-email-format")
        password_field.send_keys("ValidPassword123")
        confirm_password_field.send_keys("ValidPassword123")
        signup_button.click()

        # Wait for error message
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid email format')]"))
        )
        print("Invalid email format detected:", error_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        # Wait for user input before closing the browser
        input("Press Enter to close the browser...")
        driver.quit()


def test_password_mismatch():
    """Function to test password mismatch validation."""
    try:
        driver.get("https://app-staging.nokodr.com/signup")

        # Locate fields
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        confirm_password_field = driver.find_element(By.ID, "confirm_password")
        signup_button = driver.find_element(By.ID, "signup_button_id")  # Replace with actual ID

        # Enter mismatching passwords
        password_field.send_keys("ValidPassword123")
        confirm_password_field.send_keys("DifferentPassword456")
        signup_button.click()

        # Wait for error message
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Passwords do not match')]"))
        )
        print("Password mismatch detected:", error_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        # Wait for user input before closing the browser
        input("Press Enter to close the browser...")
        driver.quit()


# Running the tests
validate_mandatory_fields()  # Test with valid data
test_invalid_email_format()  # Test invalid email format
test_password_mismatch()  # Test password mismatch
