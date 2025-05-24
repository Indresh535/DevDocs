# Classes and methods for cruise search Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log_info, log_error
from utils.navigations import WebNavaigation
from utils.helpers import take_screenshot
import time


class CruiseSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)    
    

    def cruise_search(self, des, ports, cruiseline, ships, mon, leng, test_result):
        sel = WebNavaigation(self.driver)
        try:
            # ********* Select Destinations ***************
            time.sleep(1)  # Consider using a wait instead of sleep
            start_time = time.time()
            sel.select_dropdown('dwDestination', des)

            # Wait for loading to finish
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # ********* Select Ports ***************
            sel.select_dropdown('dwPort', ports)
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # ********* Select Cruise Line ***************
            sel.select_dropdown('dwCruiseline', cruiseline)
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # ********* Select Ships ***************
            sel.select_dropdown('dwShip', ships)
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # ********* Select Month ***************
            sel.select_dropdown('dwDate', mon)
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # ********* Select Length ***************
            sel.select_dropdown('dwDays', leng)
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "zzAjaxMask")))

            # Click Search button
            time.sleep(1)
            search_button = self.driver.find_element(By.ID, "dwGoButton")
            search_button.click()
            end_time = time.time()
            total_time = end_time - start_time
            test_result['Cruise_Search_Result'] = 'Pass'
            test_result['Cruise_Search_TimeTaken'] = total_time - 1

            log_info("Cruise Search Page Testing: Passed")
            print("Cruise Search Page Testing: Passed")
            return True, ""
        except Exception as e:
            error_msg = f"An error occurred during CruiseSearch: {e}"
            log_error(error_msg)
            test_result['Cruise_Search_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            # Assuming take_screenshot is a function you have defined elsewhere
            screenshot_url = take_screenshot(self.driver, "Cruise_Search_Dropdown_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg
