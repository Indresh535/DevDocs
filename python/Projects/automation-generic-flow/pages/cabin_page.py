# Classes and methods for Cabin Page
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log_info, log_error
from selenium.webdriver.common.action_chains import ActionChains
from utils.helpers import take_screenshot

sec = 60

class CabinPage:
    def __init__(self, driver):
        self.driver = driver

    def cabin_selection(self, test_result):
        try:
            start_time = time.time()
            Cabin = WebDriverWait(self.driver, sec).until(EC.title_contains('Cabin Selection'))
            if Cabin:
                print("This is Cabin Page ")
                log_info("This is Cabin Page ")

                #buffer_load_time = calculate_page_buffer_load_time(driver, sec)
                #print("buffer_load_time Cabin_Selection", buffer_load_time)
                #test_result['Cabin_Selection_TimeTaken'] = buffer_load_time

                time.sleep(2)
                sessionid = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.refNum")))
                test_result['Session_ID'] += sessionid.text + "-"
                csMainSection = WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.ID, "csMainSection")))
                csCabinNumbers = WebDriverWait(csMainSection, sec).until(
                    EC.presence_of_element_located((By.ID, "csCabinNumbers")))
                self.driver.implicitly_wait(10)
                select_buttons = WebDriverWait(csCabinNumbers, sec).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.zzSelectButton")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", select_buttons)
                time.sleep(1)

                # if select_buttons.is_displayed() and select_buttons.is_enabled():
                try:
                    WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(select_buttons))
                    ActionChains(self.driver).move_to_element(select_buttons).click(select_buttons).perform()
                except Exception as e:
                    error_msg = "Cabin_Selection, Randomly selected button is not interactable."
                    print(f"Click failed with ActionChains, trying JavaScript click: {e}")
                    self.driver.execute_script("arguments[0].click();", select_buttons)
                    log_error(error_msg)
                    # return False, error_msg

                test_result['Cabin_Selection_Result'] = 'Pass'
                end_time = time.time()
                total_time = end_time - start_time
                print("Cabin_Selection, Page Testing:- Passed")
                log_info("Cabin_Selection, Page Testing:- Passed")
                return True, ""
        except Exception as e:
            error_msg = f"An error occurred during Cabin_Selection: {e}"
            print(error_msg)
            test_result['Cabin_Selection_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            log_error("Cabin_Selection, button is not interactable. Error: %s" % str(e))
            screenshot_url = take_screenshot(self.driver, "Cabin_Selection_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg
