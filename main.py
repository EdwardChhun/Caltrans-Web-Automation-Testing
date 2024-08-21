from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
import time
import re

def load_projects(file_path):
    projects = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        content = file.read()
        # Split the content into rows, considering that some fields might contain newlines
        rows = re.split(r'\n(?=D\d+|HQ)', content)
        
        # Create a CSV reader from the modified content
        csv_reader = csv.reader(rows)
        
        # Get the header
        headers = next(csv_reader)
        
        for row in csv_reader:
            if len(row) == len(headers):
                project = {headers[i]: row[i].strip() for i in range(len(headers))}
                projects.append(project)
            else:
                print(f"Skipping malformed row: {row}")
    
    print(f"Loaded {len(projects)} projects from the CSV file.")
    return projects

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def scroll_to_element(driver, element, offset=100):
    # Get the height of the viewport
    viewport_height = driver.execute_script("return window.innerHeight")
    
    # Calculate the y position to scroll to (element's top position - half of viewport height + offset)
    scroll_y = driver.execute_script(f"""
        var rect = arguments[0].getBoundingClientRect();
        return rect.top + window.pageYOffset - (window.innerHeight / 2) + {offset};
    """, element)
    
    # Scroll to the calculated position
    driver.execute_script(f"window.scrollTo(0, {scroll_y});")
    
    time.sleep(1)

def wait_for_element(driver, by, value, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        scroll_to_element(driver, element, offset=100)
        return element
    except TimeoutException:
        print(f"Element not found: {value}")
        return None

def safe_click(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)

def safe_send_keys(driver, element, text):
    try:
        element.clear()
        element.send_keys(text)
        element.send_keys(Keys.ENTER)
    except:
        driver.execute_script(f"arguments[0].value = '{text}';", element)

def click_left_side(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, 5, element.size['height'] // 2)
    actions.click()
    actions.perform()

def submit_project(driver, project):
    driver.get("https://caltrans.brightidea.com/TransformationalOperationsPilots/submit")
    time.sleep(2)

    # Input project title
    title_input = wait_for_element(driver, By.XPATH, "//input[@class='form-control']")
    if title_input:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='form-control']")))
        safe_click(driver, title_input)
        safe_send_keys(driver, title_input, project['Project Title'])
    
    time.sleep(1)
    # Select District
    district_number = project['District'].replace('D', '')
    if district_number == 'HQ':
        district_number = '13'
    district_xpath = f"//div[contains(@class, 'question-section-8756515C-ABE8-11ED-BCB3-0AB688EFA52D')]//div[@class='checkbox'][{district_number}]/label"
    district_label = wait_for_element(driver, By.XPATH, district_xpath)
    if district_label:
        click_left_side(driver, district_label)
        time.sleep(.25)
        checkbox = district_label.find_element(By.XPATH, "./preceding-sibling::input[@type='checkbox']")
        if not checkbox.is_selected():
            print(f"Checkbox for district {project['District']} was not selected. Retrying...")
            click_left_side(driver, district_label)
            time.sleep(.25)
    
    time.sleep(.25)
    # Input Division/Office
    division_input = wait_for_element(driver, By.XPATH, "//div[contains(@class, 'question-section-87654F20-ABE8-11ED-BCB3-0AB688EFA52D')]/input[@class='iii form-control']")
    if division_input:
        safe_click(driver, division_input)
        safe_send_keys(driver, division_input, "Traffic Operations")
    
    time.sleep(.25)
    # Input Project Description
    description_input = wait_for_element(driver, By.XPATH, "//div[@class='redactor-styles redactor-in redactor-in-0']")
    if description_input:
        safe_click(driver, description_input)
        safe_send_keys(driver, description_input, project['Project Description (Brief)'])

    
    time.sleep(.25)
    # Select Project Status
    status_map = {'Active': '1', 'Proposed': '2', 'Complete': '3'}
    status_value = project['Status'].strip()
    status_number = status_map.get(status_value, '1')
    print(f"Project status: {status_value}, Status number: {status_number}")

    status_xpath = f"//div[@class='set-section question-section-BC593FE4-ABE9-11ED-BCB3-0AB688EFA52D']/div[@class='radio'][{status_number}]/label"
    status_label = wait_for_element(driver, By.XPATH, status_xpath)

    if status_label:
        click_left_side(driver, status_label)
        time.sleep(.25)
        
        # Check if the radio button is selected
        radio_input = status_label.find_element(By.XPATH, "./preceding-sibling::input[@type='radio']")
        if not radio_input.is_selected():
            print(f"Radio button for status {status_value} was not selected. Retrying...")
            click_left_side(driver, status_label)
            time.sleep(1)
            
        # Double-check if it's selected after retry
        if radio_input.is_selected():
            print(f"Successfully selected status: {status_value}")
        else:
            print(f"Failed to select status: {status_value}")
    
    time.sleep(.25)
    # Select Project Category
    category_select_element = wait_for_element(driver, By.XPATH, "//div[@id='idea-form-category']/div[@class='form-group']/select[@class='form-control']")
    if category_select_element:
        category_select = Select(category_select_element)
        try:
            category_select.select_by_visible_text(project['Project Category'])
        except NoSuchElementException:
            category_select.select_by_visible_text('Other')
    
    # Select Project Lead Engineer
    time.sleep(.25)
    # Input Project Lead
    project_lead_input = wait_for_element(driver, By.XPATH, "//div[@class='set-section question-section-CB8A3D3B-ABEB-11ED-BCB3-0AB688EFA52D']/input[@class='iii form-control']")
    if project_lead_input:
        safe_click(driver, project_lead_input)
        project_lead = project.get('Project point-of-contact', 'N/A')  # Use 'N/A' if no project lead is specified
        safe_send_keys(driver, project_lead_input, project_lead)        
        
    time.sleep(.25)
    # Submit the form
    submit_button = wait_for_element(driver, By.XPATH, "//button[@class='btn btn-primary f-submit-idea-btn']")
    if submit_button:
        safe_click(driver, submit_button)
        
    
    # Wait for submission to complete
    time.sleep(10)
    

def main():
    projects = load_projects('list.csv')
    driver = setup_driver()
    
    driver.get("https://caltrans.brightidea.com/TransformationalOperationsPilots/submit")
    
    # Allow time for manual login
    print("Please log in manually. You have 30 seconds.")
    time.sleep(30)
    
    for project in projects:
        try:
            submit_project(driver, project)
            print(f"Submitted project: {project['Project Title']}")
        except Exception as e:
            print(f"Failed to submit project {project['Project Title']}: {str(e)}")
    
    driver.quit()

if __name__ == "__main__":
    main()