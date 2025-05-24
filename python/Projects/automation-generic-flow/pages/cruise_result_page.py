 # Classes and methods for Cruise Result Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot

sec = 60

class CruiseResultPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, sec)

    
    def cruise_result(self, test_result):
        
        try:
            time.sleep(1)
            start_time = time.time()

            WebDriverWait(self.driver, sec).until(EC.title_contains('Cruise Result'))
            print(" This is Cruise Result Page ")

            # Find all articles with the class 'crCruiseListing'
            articles = WebDriverWait(self.driver, sec).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'crCruiseListing')))

            # Collect all 'zzSelectButton' buttons inside the found articles
            select_buttons = []
            for article in articles:
                buttons = article.find_elements(By.CLASS_NAME, 'zzSelectButton')
                select_buttons.extend(buttons)

            # Ensure there are buttons to interact with
            if not select_buttons:
                error_msg = "No select sailings buttons found in Cruise Result Page."
                print(error_msg)
                test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
                log_error(error_msg)
                return False, error_msg

            time.sleep(1)
            # Randomly select a button and click it
            random_button = random.choice(select_buttons)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_button)
            time.sleep(1)

            # Check if the randomly selected button is clickable and enabled, and if so, click it
            # if random_button.is_displayed() and random_button.is_enabled():
            try:
                WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(random_button))
                # driver.implicitly_wait(10)
                ActionChains(self.driver).move_to_element(random_button).click(random_button).perform()
            except Exception as e:
                error_msg = "Cruise Result Page, selected button is not interactable."
                print(f"Click failed with ActionChains, trying JavaScript click: {e}")
                self.driver.execute_script("arguments[0].click();", random_button)

            end_time = time.time()
            total_time = end_time - start_time - 3
            test_result['Cruise_Result_TimeTaken'] = total_time
            test_result['Cruise_Result'] = 'Pass'
            print("Cruise Result Page Testing:  Passed")
            log_info("Cruise Result Page Testing:  Passed")
            time.sleep(1)
            return True, ""
        except Exception as e:
            error_msg = f"An error occurred during CruiseResult: {e}"
            print(error_msg)
            test_result['Cruise_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            log_error(error_msg)
            screenshot_url = take_screenshot(self.driver, "Cruise_Result_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg