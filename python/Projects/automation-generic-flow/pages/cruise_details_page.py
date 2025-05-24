# Classes and methods for Cruise Details Page
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.navigations import WebNavaigation
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot
import random
import time

sec = 60
class CruiseDetailsPage:
    def __init__(self, driver):
        self.driver = driver

    
    def cruise_details(self, test_result, guestOptions=False):
        try:
            start_time = time.time()
            #logger.info(start_time)
            CruiseDetailsPage = WebDriverWait(self.driver, sec).until(EC.title_contains('Cruise Details'))
            if CruiseDetailsPage:
                print(" This is Cruise Details Page ")
                log_info(" This is Cruise Details Page ")

                WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.ID, "cdPaxBox")))

                #buffer_load_time = calculate_page_buffer_load_time(driver, sec)
                #print("buffer_load_time Cruise Details ", buffer_load_time)
                #test_result['Cruise_Details_TimeTaken'] = buffer_load_time

                self.driver.implicitly_wait(10)

                paxType_div = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.paxType")))
                select_element = Select(paxType_div.find_element(By.TAG_NAME, "select"))
                select_element.select_by_visible_text("2")

                # Wait for the section with id "cdItinInfo" to be present
                h2_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "section#cdItinInfo h2")))
                # Extract the text inside the h2 element
                h2_text = h2_element.text
                # The text includes all content, so split it by line
                lines = h2_text.split('\n')
                # Extract individual parts
                days = lines[0] if len(lines) > 0 else ""
                destination = lines[1] if len(lines) > 1 else ""
                ship_name = lines[2] if len(lines) > 2 else ""
                extracted_text = f"{days}, {destination}, {ship_name}"

                print("extracted_text ", extracted_text)
                test_result['Test_Cases'] = extracted_text + "-"
                time.sleep(1)
                time.sleep(1)

                try:
                    cdResidency_div = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cdResidency")))
                    select_element = cdResidency_div.find_element(By.TAG_NAME, "select")
                    # If found, interact with it using Select
                    select_element = Select(select_element)
                    select_element.select_by_visible_text("Alaska (AK)")

                    time.sleep(1)
                    if guestOptions:
                       # AdditionalGuestOption(driver)
                       pass
                except Exception as e:
                    # The class 'cdPaxQual' does not exist, continue with other code
                    print("Class 'cdPaxQual' does not exist. Continuing with other actions.")
                    #logger.info("Class 'cdPaxQual' does not exist. Continuing with other actions.")
                    # Continue with your remaining code here

                # Wait for the 'cdSailingRates' element to be present
                rating_tab = WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.ID, 'cdSailingRates')))

                # Within 'rating_tab', wait for the 'row selected' element to be present
                default_sailing = WebDriverWait(rating_tab, sec).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'row.selected')))
                selected_sailing = WebDriverWait(default_sailing, sec).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sailDate')))
                # Find the 'zzSelectButton' button inside the 'default_sailing' element
                sailing_date = WebDriverWait(selected_sailing, sec).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'label')))
                test_result['Test_Cases'] += sailing_date.text

                select_buttons = default_sailing.find_elements(By.CSS_SELECTOR, 'button.zzSelectButton')
                if not select_buttons:
                    error_msg = "No select salings buttons found in Cruise Details."
                    print(error_msg)
                    log_error(error_msg)
                    test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
                    return False, error_msg

                # Click the select button
                button = select_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)

                if button.is_displayed() and button.is_enabled():
                    ActionChains(self.driver).move_to_element(button).click(button).perform()
                    # return True,"",
                else:
                    error_msg = "Cruise Details, Selected button is not interactable."
                    print(error_msg)
                    log_error(error_msg)
                    return False, error_msg

            test_result['Cruise_Details_Result'] = 'Pass'
            end_time = time.time()
            total_time = end_time - start_time
            print("Cruise Details Page Testing:  Passed")
            log_info("Cruise Details Page Testing: Passed")
            time.sleep(1)
            return True, ""
        except Exception as e:
            error_msg = f"An error occurred during Cruise Details: {e}"
            print(error_msg)
            test_result['Cruise_Details_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{e}'
            log_error(error_msg)
            screenshot_url = take_screenshot(self.driver, "Cruise_Details_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg
