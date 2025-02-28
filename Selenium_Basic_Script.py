from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to your ChromeDriver executable
service = Service("C:\WebDriver\chromedriver.exe")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Open the URL
driver.get("https://app-staging.nokodr.com/")

# Optionally, print the title of the page
print(driver.title)

# Close the browser
driver.quit()
