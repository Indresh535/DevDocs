# Workflow test cases covering the entire flow
from datetime import datetime
import pytest
from utils.driver import get_driver
from utils.timer import Timer
from utils.logger import log_info, log_error
from pages.base_page import BasePage
from pages.cruise_search_page import CruiseSearchPage
from pages.cruise_result_page import CruiseResultPage
from pages.cruise_details_page import CruiseDetailsPage
from pages.category_availability import CategoryAvailabilityPage
from pages.cabin_page import CabinPage
from pages.login_page import LoginPage
from pages.passenger_details import PassengerDetailsPage
from pages.payment_page import PaymentPage
from utils.helpers import generate_test_results


test_results = []

url = "https://cs.cruisebase.com/cs/?skin=1"
des = "All Destinations"
ports = "All Ports"
cruiseline = "All Cruise Lines"
ships = "All Ships"
mon = "Nov 2024"
leng = "All Lengths"

test_result = {
        'SL_No': len(test_results) + 1,
        'Module': 'CBE',
        'Skin': url.split('skin=')[-1] if 'skin=' in url else 'Default',
        'Cruise_Line': cruiseline,
        'Ship': ships,
        'Sailing_Date': '',
        'Remarks': '',
        'Session_ID': '',
        'Test_Cases': f"{des}, {ports}, {cruiseline}, {ships}, {mon}, {leng}",
        'Testing_Comments': '',
        'Load_CS_Result': '',
        'Load_CS_TimeTaken': '',
        'Cruise_Search_Result': '',
        'Cruise_Search_TimeTaken': '',
        'Cruise_Result': '',
        'Cruise_Result_TimeTaken': '',
        'Cruise_Details_Result': '',
        'Cruise_Details_TimeTaken': '',
        'Category_Avail_Result': '',
        'Category_Avail_TimeTaken': '',
        'Cabin_Selection_Result': '',
        'Cabin_Selection_TimeTaken': '',
        'Login_Result': '',
        'Login_TimeTaken': '',
        'Passenger_Details_Result': '',
        'Passenger_Details_TimeTaken': '',
        'Payment_Page_Result': '',
        'Payment_Page_TimeTaken': '',
        'Final_Results': '',
        'Final_Results_TimeTaken': '',
        'Tested_On': datetime.now(),
        'Error_Img': ''
    }

class TestCBECruiseFlow:
    @pytest.fixture(scope="class")
    def setup(self):        
        self.driver = get_driver()
        yield self.driver
        self.driver.quit()

    def test_workflow(self, setup):
        driver = setup
        timer = Timer()
        landing_page = BasePage(driver)
        timer.start()
        landing_page.load_page(url)
        time_taken = timer.stop()
        log_info(f"Landing Page load time: {time_taken:.2f} seconds")

        assert landing_page.is_loaded(), "Landing Page did not load successfully"

        cruise_search_page = CruiseSearchPage(driver)
        cruise_search_page.cruise_search(des, ports, cruiseline, ships, mon, leng, test_result)
        # Repeat similar process for each page, such as CruiseResultPage, etc.
        cruise_result_page = CruiseResultPage(driver)
        timer.start()
        cruise_result_page.cruise_result(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Cruise Result Page load time: {time_taken:.2f} seconds")
        # Repeat similar process for each page, such asCruiseDetailsPage, etc.
        cruise_details_page = CruiseDetailsPage(driver)
        timer.start()
        cruise_details_page.cruise_details(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Cruise Details Page load time: {time_taken:.2f} seconds")
        # test cases for other pages CategoryAvailabilityPage.
        category_availability_page = CategoryAvailabilityPage(driver)
        timer.start()
        category_availability_page.category_availability(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Category Availability Page load time: {time_taken:.2f} seconds")
        # CabinSelectionPage.
        cabin_page = CabinPage(driver)
        timer.start()
        cabin_page.cabin_selection(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Cabin Selection Page load time: {time_taken:.2f} seconds")
        # LoginPage.
        login_page = LoginPage(driver)
        timer.start()
        login_page.login_page(url, test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Login Page load time: {time_taken:.2f} seconds")
        # PassengerDetailsPage.
        passenger_details_page = PassengerDetailsPage(driver)
        timer.start()
        passenger_details_page.passenger_details(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Passenger Details Page load time: {time_taken:.2f} seconds")
        # PaymentPage.
        payment_page = PaymentPage(driver)
        timer.start()
        payment_page.payment_page(test_result) # define actions within each page class
        time_taken = timer.stop()
        log_info(f"Payment Page load time: {time_taken:.2f} seconds")
        test_results.append(test_result)
        generate_test_results(test_results)
        # pytest tests/test_cbe_workflow.py --capture=no  