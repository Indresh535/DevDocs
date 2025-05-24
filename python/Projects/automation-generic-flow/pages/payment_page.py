# Classes and methods for Payment Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot

sec = 60
class PaymentPage:
    def __init__(self, driver):
        self.driver = driver

    def payment_page(self, test_result):
        start_time = time.time()
        try:
            # Wait for the page to load and check for the presence of an <h1> tag with text "Insurance / Payment"
            Payment_Page = WebDriverWait(self.driver, sec).until(EC.title_contains('Insurance and Payment'))

            if Payment_Page:
                print(" Insurance / Payment Page loaded successfully. ")
                WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.ID, "pmPaymentInfo")))
                #buffer_load_time = calculate_page_buffer_load_time(driver, sec)
                #print("buffer_load_time Payment Details", buffer_load_time)
                #test_result['Payment_Page_TimeTaken'] = buffer_load_time


                sessionid = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.refNum")))
                test_result['Session_ID'] += sessionid.text
                end_time = time.time()
                total_time = end_time - start_time
                test_result['Payment_Page_Result'] = 'Pass'
                test_result['Testing_Comments'] = f'All Pass, No Errors'
                screenshot_url = take_screenshot(self.driver, "All_Test_Cases_Passed")
                test_result['Error_Img'] = screenshot_url
                print("Insurance / Payment, Page Testing:-  Passed")
                log_info("Insurance / Payment, Page Testing:-  Passed")
                return True, ""
        except Exception as e:
            error_msg = f"An error occurred while handling Error in Insurance / Payment Page: {e}"
            print(f"An error occurred while handling Error in Insurance / Payment Page: {e}")
            test_result['Payment_Page_Result'] = 'Fail'
            screenshot_url = take_screenshot(self.driver, "Payment_Page_Fail")
            log_error(error_msg)
            test_result['Error_Img'] = screenshot_url
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            return False, error_msg