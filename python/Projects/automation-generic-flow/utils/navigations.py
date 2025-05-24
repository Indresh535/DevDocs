import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

class WebNavaigation:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=60):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def wait_for_title(self, title, timeout=60):
        WebDriverWait(self.driver, timeout).until(EC.title_contains(title))
        
    def wait_visibility_of_element(self, by, value, timeout=60):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((by, value)))

    def select_dropdown(self, selectId, selectOption):
        try:
            # Wait for the dropdown to be present
            dw_destination_div = self.wait.until(EC.presence_of_element_located((By.ID, selectId)))
            select_element = dw_destination_div.find_element(By.TAG_NAME, "select")
            select = Select(select_element)

            # Get all options in the dropdown
            all_options = select.options

            # Check if the specified option is not disabled
            for option in all_options:
                if option.text == selectOption:
                    if not option.get_attribute('disabled'):
                        select.select_by_visible_text(selectOption)
                        # logger.info(f"Selected destination: {selectOption}")
                        return
                    else:
                        # logger.error(f"Destination {selectOption} is disabled.")
                        print(f"Destination {selectOption} is disabled.")

            # If the specified option is disabled, select a random enabled option
            enabled_options = [option for option in all_options if not option.get_attribute('disabled')]
            if enabled_options:
                random_choice = random.choice(enabled_options)
                select.select_by_visible_text(random_choice.text)
                #logger.info(f"Selected random enabled destination: {random_choice.text}")
            else:
                #logger.error("No enabled destinations available to select.")
                print("No enabled destinations available to select.")
        except Exception as e:
            # logger.error(f"An error occurred while selecting destination: {e}")
            return False, str(e)