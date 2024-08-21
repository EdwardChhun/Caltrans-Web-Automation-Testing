import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the page
driver.get("https://caltrans.brightidea.com/TransformationalOperationsPilots")

# Load modified cookies
with open("cookies_modified.pkl", "rb") as file:
    cookies = pickle.load(file)

# Add cookies to the session
for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh to apply cookies
driver.refresh()

# Keep browser open
input("Press Enter to close the browser...")

driver.quit()