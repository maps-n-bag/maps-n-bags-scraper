from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from webdriver import WebDriver

class SearchDriver(WebDriver):

	location_data = {}

	def __init__(self):
		super().__init__()

		self.location_data["rating"] = "NA"
		self.location_data["reviews_count"] = "NA"
		self.location_data["address"] = "NA"
		self.location_data["contact"] = "NA"
		self.location_data["website"] = "NA"
		# self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
		# self.location_data["Reviews"] = []
		# self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

		
	def search_location(self, location):
		self.location_data["name"] = location
    
		searchBox = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
		searchBox.send_keys(location)
		submitButton = self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
		submitButton.click()

	def get_basic_info(self):
		try:
			WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')))
		except:
			print("Error in getting basic info for", self.location_data["name"])
			return

		try:
			avg_rating = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')			
			self.location_data["rating"] = avg_rating.text
		except:
			print("Error in getting rating for", self.location_data["name"])

		try:
			total_reviews = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span')
			self.location_data["reviews_count"] = total_reviews.text[1:-1]
		except:
			print("Error in getting reviews count for", self.location_data["name"])

		try:
			address = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div/div[2]/div[1]')
			self.location_data["address"] = address.text
		except:
			print("Error in getting address for", self.location_data["name"])

		try:
			phone_number = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[6]/button/div/div[2]/div[1]')
			self.location_data["contact"] = phone_number.text
		except:
			print("Error in getting phone number for", self.location_data["name"])

		try:
			website = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[5]/a/div/div[2]/div[1]')
			self.location_data["website"] = website.text
		except:
			print("Error in getting website for", self.location_data["name"])
   
		# time.sleep(20)


	def scrape(self, location):
		# self.setLangEnglish()
		self.goToMaps()
		self.search_location(location)
		self.get_basic_info()

		print(self.location_data)

location = 'Bangabandhu Military Museum'
# location = 'Headless Technologies Limited'
d = SearchDriver()
d.scrape(location)
d.exit()