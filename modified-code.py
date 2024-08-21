from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://caltrans.brightidea.com/TransformationalOperationsPilots")

print(driver.title)
print(driver.current_url)

actions = ActionChains(driver)

wait = WebDriverWait(driver, 100)  # Increased wait time to n seconds

# element = wait.until(EC.presence_of_element_located((By.ID, "{7328D0AF-DF5C-11EB-B011-0A2E49781BB2}_rich_text_widget")))

# # Find the specific paragraph within the div
# paragraph = element.find_element(By.XPATH, "./p[2]")

# # Scroll the element into view
# driver.execute_script("arguments[0].scrollIntoView(true);", paragraph)

# time.sleep(1)

# actions.move_to_element(paragraph).perform()

# # Now you can interact with the paragraph
# text = paragraph.text
# print(text)

# time.sleep(3)

# driver.quit()