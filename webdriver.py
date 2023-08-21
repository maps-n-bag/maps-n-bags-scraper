from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebDriver:

  def __init__(self):
    self.service = Service("chromedriver_win32\chromedriver.exe")
    self.options = Options()
    # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    # self.options.add_argument("--headless")
    self.options.add_argument("--disable-extensions")
    self.options.add_argument("--disable-gpu")
    self.driver = webdriver.Chrome(service=self.service, options=self.options)
    
  def goToMaps(self):
    self.driver.get("https://www.google.com/maps/place/Lal+Dighi+%28Pond%29%2F+%E0%A6%B2%E0%A6%BE%E0%A6%B2+%E0%A6%A6%E0%A6%BF%E0%A6%98%E0%A7%80/data=!4m7!3m6!1s0x30adc97e1ee2b41d:0x1b620a5b61d868fc!8m2!3d21.4440233!4d91.9748367!16s%2Fg%2F11rkcyp4wt!19sChIJHbTiHn7JrTAR_GjYYVsKYhs?authuser=0&hl=en&rclk=1")
  def goToMapsURL(self, url):
    self.driver.get(url)
    
  def setLangEnglish(self):
    self.goToMaps()

    try:
      time.sleep(2)
      menuButton = self.driver.find_element(By.XPATH, '//*[@id="omnibox-singlebox"]/div/div[1]/button')
      menuButton.click()
      time.sleep(2)
      languageButton = self.driver.find_element(By.XPATH, '//*[@id="settings"]/div/div[2]/ul/div[7]/li[1]/button')
      languageButton.click()
      time.sleep(2)
      englishButton = self.driver.find_element(By.XPATH, '//*[@id="languages"]/div/div[3]/div[1]/div[11]/span')
      englishButton.click()
      time.sleep(2)
      closeButton = self.driver.find_element(By.XPATH, '//*[@id="modal-dialog"]/div/div[2]/div/div[2]/button')
      closeButton.click()
      time.sleep(2)
    except:
      print("Error in setting language to English")
     
  def exit(self):
    self.driver.quit()