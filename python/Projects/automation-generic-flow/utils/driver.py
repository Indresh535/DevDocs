# WebDriver setup and teardown functions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    #chrome_options.add_argument('--headless')  # Add this line to enable headless mode
    # chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (useful for headless mode)
    # chrome_options.add_argument('--no-sandbox') # Bypass OS security model (useful for running as root)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
