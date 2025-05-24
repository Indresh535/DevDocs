# Classes and methods for Category Availability
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log_info, log_error
from utils.navigations import WebNavaigation
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import logging
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot

sec = 60
class CategoryAvailabilityPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(self.driver, sec)  # Initialize self.wait with WebDriverWait

    def category_availability(self, test_result):
        try:
            start_time = time.time()
            CatFare = self.wait.until(
                lambda driver: EC.title_contains('Category/Fare Availability')(driver) or 
                               EC.title_contains('Category Availability')(driver)
            )

            if CatFare:
                print(" This is Category/Fare Availability Page ")
                time.sleep(2)
                # copy session id
                sessionid = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.refNum")))
                test_result['Session_ID'] = sessionid.text + "-"
                print("sessionid : ", sessionid.text)
                log_info(f"sessionid :  {sessionid.text}", )

                # copy cruiseline
                zzBookingCruiseline = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'zzBookingCruiseline')))
                cruiseline = zzBookingCruiseline.find_element(By.TAG_NAME, 'div').text
                test_result['Cruise_Line'] = cruiseline
                log_info(f"cruiseline :  {cruiseline}")
                print("cruiseline: ", cruiseline)

                # copy ship Name
                zzBookingShip = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'zzBookingShip')))
                shipName = zzBookingShip.find_element(By.TAG_NAME, 'div').text
                test_result['Ship'] = shipName
                print("shipName: ", shipName)
                log_info(f"shipName :  {shipName}", )

                # copy sailing date
                zzBookingDepart = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'zzBookingDepart')))
                salingdate = zzBookingDepart.find_element(By.TAG_NAME, 'div').text
                date_obj = datetime.strptime(salingdate, '%a, %b %d, %Y')
                print("date_obj: ", date_obj)
                test_result['Sailing_Date'] = date_obj
                print("salingdate: ", salingdate)
                log_info(f"salingdate :  {salingdate}")
                log_info(f"date_obj :  {date_obj}")

                # select the category Availibility
                cdResidency_div = WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.CLASS_NAME, "tab")))
                # driver.implicitly_wait(10)
                select_buttons = WebDriverWait(cdResidency_div, sec).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.zzSelectButton")))
                # Randomly select a button and click it
                time.sleep(1)
                random_button = random.choice(select_buttons)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_button)
                time.sleep(1)
                # if random_button.is_displayed() and random_button.is_enabled():
                try:
                    WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(random_button))
                    # self.driver.implicitly_wait(10)
                    ActionChains(self.driver).move_to_element(random_button).click(random_button).perform()
                    # return True, ""
                except Exception as e:
                    error_msg = "Category Availibility, selected button is not interactable."
                    print(f"Click failed with ActionChains, trying JavaScript click: {e}")
                    self.driver.execute_script("arguments[0].click();", select_buttons)
                    # return False, error_msg

            end_time = time.time()
            total_time = end_time - start_time
            test_result['Category_Avail_TimeTaken'] = total_time - 4
            print("Category/Fare Availability", total_time)
            test_result['Category_Avail_Result'] = 'Pass'
            print("Category/Fare Availability, Page Testing:-  Passed")
            log_info("Category/Fare Availability, Page Testing:-  Passed")
            return True, ""
        except Exception as e:
            error_msg = f"An error occurred during Category/Fare Availability: {e}"
            test_result['Category_Avail_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            print(error_msg)
            log_error(error_msg)
            screenshot_url = take_screenshot(self.driver, "Category_Availability_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg
