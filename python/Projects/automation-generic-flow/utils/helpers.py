import csv
import os
import time
from datetime import datetime
from openpyxl import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from utils.s3_config import s3_upload_file
from utils.logger import log_info, log_error

script_dir = os.path.dirname(os.path.abspath(__file__))

def parse_numeric(value):
    if value is None or value == '':
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        log_error(f"Invalid numeric value: {value}. Setting to None.")
        return None

def parse_datetime(date_str):
    if isinstance(date_str, datetime):
        return date_str
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        log_error(f"Error parsing datetime: '{date_str}'")
        return datetime.now()
    

def read_test_cases_from_csv(file_path):
    test_cases = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                test_cases.append(row)
    return test_cases


def generate_test_results(test_results):    
    from utils.db_config import create_sqlalchemy_session, write_to_database
    # Get today's date and current time
    folder_name = "CBE_Test_Results_"
    # today_date = os.path.abspath(folder_name + datetime.now().strftime('%Y-%m-%d'))
    # today_date = os.path.join(script_dir, folder_name + datetime.now().strftime('%Y-%m-%d'))
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H-%M-%S')

    # Define the path to the Test_Reports/CBE/ directory
    report_dir = os.path.join(script_dir, "Test_Reports", "CBE")

    # Create the directory if it doesn't exist
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Create a folder with today's date in the script directory
    today_folder_path = os.path.join(report_dir, folder_name + today_date)

    # Create a folder with today's date
    if not os.path.exists(today_folder_path):
        os.makedirs(today_folder_path)

    # Define the file name with the current time
    file_name = f"Tests_Case_{current_time}.xlsx"
    file_path = os.path.join(today_folder_path, file_name)

    header = [
        'SL_No',
        'Module',
        'Skin',
        'Cruise_Line',
        'Ship', 'Sailing_Date',
        'Remarks', 'Session_ID',
        'Test_Cases', 'Testing_Comments',
        'Load_CS_Result', 'Load_CS_TimeTaken',
        'Cruise_Search_Result', 'Cruise_Search_TimeTaken',
        'Cruise_Result', 'Cruise_Result_TimeTaken',
        'Cruise_Details_Result', 'Cruise_Details_TimeTaken',
        'Category_Avail_Result', 'Category_Avail_TimeTaken',
        'Cabin_Selection_Result', 'Cabin_Selection_TimeTaken',
        'Login_Result', 'Login_TimeTaken',
        'Passenger_Details_Result', 'Passenger_Details_TimeTaken',
        'Payment_Page_Result', 'Payment_Page_TimeTaken',
        'Final_Results', 'Final_Results_TimeTaken',
        'Tested_On','Error_Img'
    ]

    # Create an Excel workbook and worksheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "CBE_Test_Results"

    # Write the header to the first row
    sheet.append(header)

    # Write the test results to the worksheet
    for result in test_results:
        row = [result.get(column, '') for column in header]
        sheet.append(row)

    # Save the workbook to the file path
    workbook.save(file_path)

    print("Test results xlsx generated successfully. ")
    log_info("Test results xlsx generated successfully. ")
    # Database operations
    session = create_sqlalchemy_session()
    if session:
        for result in test_results:
            write_to_database(session, result)
        session.close()

    # Upload the file to AWS S3
    bucket_name = "genericflow"
    s3_folder_path = f'Automation_Generic_flow/Test_Reports/CBE/CBE_Test_Results_{today_date}/'
    object_path = s3_folder_path + file_name
    s3_upload_file(file_path, bucket_name, object_path)
    print("Test results processing completed.")
    #logger.info("Test results processing completed.")


def take_screenshot(driver, test_case_name):
    screenshot_dir = os.path.join(script_dir, "reports", "Error_Screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{test_case_name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
    driver.save_screenshot(screenshot_path)
    log_info(f"Screenshot saved: {screenshot_path}")
    return screenshot_path


def calculate_page_buffer_load_time(driver, timeout=60):
    """
    Waits for the web page to fully load and calculates the buffer load time.

    :param driver: Selenium WebDriver instance
    :param timeout: Maximum time to wait for the page to load (default: 10 seconds)
    :return: Buffer load time in seconds
    """

    pageTitle = driver.title
    try:
        # Wait until document.readyState is 'complete'
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')

        # Capture performance timing after the page load completes
        timing = driver.execute_script("return window.performance.timing")

        # Calculate the time when all resources finished loading (loadEventEnd)
        buffer_load_time = (timing['loadEventEnd'] - timing['navigationStart']) / 1000.0  # Convert to seconds

        # Log the performance timing and buffer load time (Optional logging)
        #logger.info(f"Timing: {timing}")
        log_info(f"{pageTitle} Load Page Buffer Load Time: {buffer_load_time} seconds")

        return buffer_load_time

    except Exception as e:
        log_error(f"Error calculating page load time: {e}")
        return None