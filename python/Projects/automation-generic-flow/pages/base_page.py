from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def load_page(self, url):
        self.driver.get(url)

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "dwSelectCriteria"))
            )
            return True
        except:
            return False