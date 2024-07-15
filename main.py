from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get("https://onramp.dot.ca.gov/")

time.sleep(3)

driver.quit()
