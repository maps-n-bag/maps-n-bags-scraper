from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

from webdriver import WebDriver

class all_place(WebDriver):
    def __init__(self):
        super().__init__()
        self.goToMaps()
    def get_all_Tourist_places(self,place):
        # self.setLangEnglish()
        time.sleep(2)
        searchBox = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        searchBox.clear()
        searchBox.send_keys('Tourists attraction in '+place +Keys.ENTER)
        # submitButton = self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
        # submitButton.click()
        # time.sleep(20)
        time.sleep(20)
        # try:
        #     while True:
        #         try:
        #             places = self.driver.find_element(By.CLASS_NAME, 'hfpxzc')
        #         except:
        #             break
        #         self.driver.execute_script("arguments[0].scrollIntoView();", places)
        # # Scroll to the bottom of the page
        # while True:
        #     # Scroll down using Keys
        #     self.driver.find_element(By.CLASS_NAME, "hfpxzc").send_keys(Keys.PAGE_DOWN)

        #     # Check if you have reached the bottom of the page
        #     # You can customize this condition based on your use case
        #     if self.driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
        #         break
        # while True:
        #     # Scroll down using Keys
        #     self.driver.find_element(By.CLASS_NAME, "hfpxzc").send_keys(Keys.PAGE_DOWN)

        #     # Check if you have reached the bottom of the page
        #     # You can customize this condition based on your use case
        #     if self.driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
        #         break
        set_of_places = set()
        bool = True
        while bool:
            time.sleep(5)
            lenth = len(set_of_places)
            places=self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            for place in places:
                if place.get_attribute('aria-label') in set_of_places:
                    continue
                self.driver.execute_script("arguments[0].scrollIntoView();", place)
                set_of_places.add(place.get_attribute('aria-label'))
            if lenth == len(set_of_places):
                bool = False
        time.sleep(5)
        all_places = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        for place in all_places:
            print(place.get_attribute('aria-label'))
            print(place.get_attribute('href'))
        return all_places
place = 'Coxs Bazar'
d = all_place()
d.get_all_Tourist_places(place)
d.exit()