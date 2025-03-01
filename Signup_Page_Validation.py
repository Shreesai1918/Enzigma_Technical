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
def validate_mandatory_fields():
    """Function to check mandatory fields on the signup page."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")

        # Wait for the signup button to be present
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up')]"))
        )
        print("Signup button found")

        # Check for mandatory fields
        name_field = driver.find_element(By.ID, "id_1740589192196393")
        email_field = driver.find_element(By.ID, "id_17405890626872154")
        password_field = driver.find_element(By.ID, "id_17405891922005504")
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")
        print("Name, Email, Password, and Confirm Password fields found")

        # Check for blank fields
        signup_button.click()
        time.sleep(2)  # Wait for error messages
        blank_field_error = driver.find_element(By.XPATH, "//div[contains(text(), 'This field is required')]")
        if blank_field_error:
            print("Blank fields detected:", blank_field_error.text)

        # Enter valid data into the fields
        name_field.send_keys("Test User")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("ValidPassword123!")
        confirm_password_field.send_keys("ValidPassword123!")

        # Submit the form
        signup_button.click()
        print("Form submitted with valid data")

        # Increase wait time to allow for server-side processing
        time.sleep(5)

        # Wait for success message
        success_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Account created successfully!')]"))
        )
        print("Signup successful:", success_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
        print(driver.page_source)
    finally:
        input("Press Enter to close the browser...")
        driver.quit()

def test_invalid_email_format():
    """Function to test invalid email format validation."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")

        # Locate fields
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_17405890626872154")))
        password_field = driver.find_element(By.ID, "id_17405891922005504")
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")
        signup_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign up')]")

        # Enter invalid email format
        email_field.send_keys("invalid-email-format")
        password_field.send_keys("ValidPassword123!")
        confirm_password_field.send_keys("ValidPassword123!")
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
        input("Press Enter to close the browser...")
        driver.quit()

def test_password_mismatch():
    """Function to test password mismatch validation."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")

        # Locate fields
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_17405891922005504")))
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")
        signup_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign up')]")

        # Enter mismatching passwords
        password_field.send_keys("ValidPassword123!")
        confirm_password_field.send_keys("DifferentPassword456!")
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
        input("Press Enter to close the browser...")
        driver.quit()

def test_special_characters_and_long_inputs():
    """Function to test edge cases such as special characters and long inputs."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")

        # Locate fields
        name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_1740589192196393")))
        email_field = driver.find_element(By.ID, "id_17405890626872154")
        password_field = driver.find_element(By.ID, "id_17405891922005504")
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")
        signup_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign up')]")

        # Test special characters and long inputs
        name_field.send_keys("!@#$%^&*()_+{}|:\"<>?")
        email_field.send_keys("testuser_with_a_very_very_very_very_long_email@example.com")
        password_field.send_keys("ValidPassword123!")
        confirm_password_field.send_keys("ValidPassword123!")
        signup_button.click()

        # Wait for error or success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Account created successfully!')]"))
        )
        print("Special characters and long inputs handled successfully:", success_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        input("Press Enter to close the browser...")
        driver.quit()

def test_password_format():
    """Function to test password format validation."""
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")

        # Locate fields
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_17405891922005504")))
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")
        signup_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign up')]")

        # Test weak password
        password_field.send_keys("weakpass")
        confirm_password_field.send_keys("weakpass")
        signup_button.click()

        # Wait for error message related to weak password
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Password must be at least 8 characters long and contain a combination of uppercase letters, lowercase letters, numbers, and special characters')]"))
        )
        print("Weak password detected:", error_message.text)

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        input("Press Enter to close the browser...")
        driver.quit()

# Running the tests
validate_mandatory_fields()
test_invalid_email_format()
test_password_mismatch()
test_special_characters_and_long_inputs()
test_password_format()
