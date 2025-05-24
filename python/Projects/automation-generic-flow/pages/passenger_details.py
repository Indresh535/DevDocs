# Classes and methods for Passenger Details Page
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot


sec = 60
class PassengerDetailsPage:
    def __init__(self, driver):
        self.driver = driver

    def passenger_details(self, test_result):
        try:
            start_time = time.time()
            # Wait for the page to load and check for the presence of a title tag with text "Passenger Details"
            Passenger_Details_Page = WebDriverWait(self.driver, sec).until(EC.title_contains('Passenger Details'))

            if Passenger_Details_Page:
                print("This is Passenger Details Page ")
                log_info("This is Passenger Details Page ")

                # Clear the values of textboxes with id="pastPaxNumber1" and id="pastPaxNumber2"
                pastPaxNumber1 = self.driver.find_element(By.ID, "pastPaxNumber1")
                pastPaxNumber2 = self.driver.find_element(By.ID, "pastPaxNumber2")


                #buffer_load_time = calculate_page_buffer_load_time(driver, sec)
                #print("buffer_load_time Passenger Details", buffer_load_time)
                #test_result['Passenger_Details_TimeTaken'] = buffer_load_time

                pastPaxNumber1.clear()
                pastPaxNumber2.clear()

                try:
                    # Attempt to locate and interact with the dining dropdown
                    diningDropdown = Select(self.driver.find_element(By.ID, "dining"))
                    dining_options = [option for option in diningDropdown.options if "Dining Time" not in option.text]
                    if dining_options:
                        selected_dining = random.choice(dining_options)
                        diningDropdown.select_by_visible_text(selected_dining.text)
                        print(f"Selected dining option: {selected_dining.text}")
                        log_error(f"Selected dining option: {selected_dining.text}")
                        # Attempt to locate and interact with the tableSize dropdown
                        dining_table_elements = self.driver.find_elements(By.ID, "tableSize")
                        if dining_table_elements:
                            diningtable = Select(dining_table_elements[0])
                            # Get all options and filter out the option with text "Table Size"
                            filtered_options = [option for option in diningtable.options if option.text != "Table Size"]
                            random_option = random.choice(filtered_options)
                            diningtable.select_by_visible_text(random_option.text)
                except NoSuchElementException:
                    print("Dining dropdown not found, proceeding to continue.")
                    #log_info("Dining dropdown not found, proceeding to continue.")

                # Locate and click the continue button
                pxs_ContinueButton = WebDriverWait(self.driver, sec).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.zzContinueButton")))
                pxs_ContinueButton.click()
                test_result['Passenger_Details_Result'] = 'Pass'
                end_time = time.time()
                total_time = end_time - start_time
                print("Passenger Details Page Testing:-  Passed")
                #log_info("Passenger Details Page Testing:-  Passed")
                return True, ""
            else:
                error_msg = "Error in Passenger Details Page loading."
                print(error_msg)
                test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
                log_error(error_msg)
                return False, error_msg
        except Exception as e:
            error_msg = f"An error occurred during Passenger Details: {e}"
            print(error_msg)
            test_result['Passenger_Details_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            log_error(error_msg)
            screenshot_url = take_screenshot(self.driver, "Passenger_Details_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg