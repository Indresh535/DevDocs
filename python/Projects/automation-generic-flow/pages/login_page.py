# Classes and methods for Login Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.logger import log_info, log_error
from utils.helpers import take_screenshot

sec = 60
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login_page(self, url, test_result):
        username = 'joesmithtest@travtech.com'
        password = 'js12pwd'
        start_time = time.time()
        try:
            # Extract skin from URL if present
            skin_value = url.split('skin=')[-1]

            # If skin is 583 or 233, perform additional actions
            if skin_value in ['583', '233']:
                print(f"Skin {skin_value} detected. Performing additional operations.")
                log_info(f"Skin {skin_value} detected. Performing additional operations.")
                # Wait for the pxLoginInfo div and click the a tag inside it
                px_login_info = WebDriverWait(self.driver, sec).until(
                    EC.presence_of_element_located((By.ID, 'pxLoginInfo'))
                )
                if px_login_info:
                    print(f"pxLoginInfo found. Clicking anchor tag inside.")
                    anchor_tag = px_login_info.find_element(By.TAG_NAME, 'a')
                    anchor_tag.click()
                    time.sleep(2)
                    print("Anchor tag clicked.")

            login = WebDriverWait(self.driver, sec).until(EC.title_contains('Login or Register'))
            if login:
                print(" This is Login Page ")
                log_info(" This is Login Page ")
                # Locate the username and password fields and login button
                username_field = self.driver.find_element(By.ID, "loginEmail")
                password_field = self.driver.find_element(By.ID, "loginPassword")

                #buffer_load_time = calculate_page_buffer_load_time(driver, sec)
                #print("buffer_load_time Login", buffer_load_time)
                #test_result['Login_TimeTaken'] = buffer_load_time

                login_button = self.driver.find_element(By.CSS_SELECTOR, "button.zzContinueButton")

                # Enter the input field
                time.sleep(1)
                username_field.send_keys(username)
                time.sleep(1)
                password_field.send_keys(password)
                time.sleep(1)

                # Submit the form
                login_button.click()
                test_result['Login_Result'] = 'Pass'
                end_time = time.time()
                total_time = end_time - start_time
                print("Login, Page Testing:- Passed")
                log_info("Login, Page Testing:- Passed")
                return True, ""
        except Exception as e:
            error_msg = f"An error occurred during Login or Register: {e}"
            print(error_msg)
            test_result['Login_Result'] = 'Fail'
            test_result['Testing_Comments'] = f'Error_Message__:-{error_msg}'
            log_error(error_msg)
            screenshot_url = take_screenshot(self.driver, "Login_Fail")
            test_result['Error_Img'] = screenshot_url
            return False, error_msg