from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class WebDriver:

  def __init__(self):
    self.service = Service("chromedriver_win32\chromedriver.exe")
    self.options = Options()
    # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    self.options.add_argument("--headless")
    self.driver = webdriver.Chrome(service=self.service, options=self.options)
    
    self.driver.get("https://www.google.com/maps/")
    
  def exit(self):
    self.driver.quit()