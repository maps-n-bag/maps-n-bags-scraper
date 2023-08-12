from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from db_connection.db_connection import db_connection

from webdriver import WebDriver
from plus_code_conv import getLatLongFromShortPlusCode

class SearchDriver(WebDriver):

	location_data = {}

	def __init__(self):
		super().__init__()

		self.location_data["rating"] = "NA"
		self.location_data["reviews_count"] = "NA"
		self.location_data["address"] = "NA"
		self.location_data["contact"] = "NA"
		self.location_data["website"] = "NA"
		self.location_data["reviews"] = []
		self.location_data["images"] ="NA"
		self.location_data["description"] = "NA"
		
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
			image=self.driver.find_element(By.XPATH,'/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/img')
			self.location_data["images"]=image.get_attribute('src')
		except:
			print("Error in getting image for", self.location_data["name"])
		try: 
			description=self.driver.find_element(By.CLASS_NAME,'DkEal')
			self.location_data["description"]=description.text
		except:
			print("Error in getting description for", self.location_data["name"])
		try:
			website = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[5]/a/div/div[2]/div[1]')
			self.location_data["website"] = website.text
		except:
			print("Error in getting website for", self.location_data["name"])
   
	def get_location(self):
		try:
			xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[7]/button/div/div[2]/div[1]'
			# WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
			plusCode = self.driver.find_element(By.XPATH, xpath)
			# print(plusCode.text)
			lat, long = getLatLongFromShortPlusCode(plusCode.text)
			self.location_data["lat"] = lat
			self.location_data["long"] = long
		except:
			print("Error in getting plus code for", self.location_data["name"])
			return

	def get_reviews(self):
		xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]'
		reviewButton = self.driver.find_element(By.XPATH, xpath)
		reviewButton.click()
		time.sleep(5)
  
		compiled_reviews = []
		set_of_reviews = set()
		MAX_REVIEWS = 20
		while True:
			length = len(set_of_reviews)
			reviews = self.driver.find_elements(By.CLASS_NAME, 'jftiEf')
			for review in reviews:
				# scroll into view
				self.driver.execute_script("arguments[0].scrollIntoView();", review)
				time.sleep(1)
    
				# get the reviewer name
				try:
					reviewer_name = review.find_element(By.CLASS_NAME, 'd4r55').text
				except:
					continue
				# print(reviewer_name)
    
				# first click on the more button if any
				try:
					more_button = review.find_element(By.CLASS_NAME, 'w8nwRe')
					more_button.click()
				except:
					pass
 
 				# get the review text
				try:
					review_text = review.find_element(By.CLASS_NAME, 'wiI7pd').text
				except:
					continue
				# print(review_text)
    
				# get the images
				# first click the more images button if any
				try:
					more_images_button = review.find_element(By.CLASS_NAME, 'Tap5If')
					more_images_button.click()
				except:
					pass
				
				try:
					images_list = list()
					images = review.find_elements(By.CLASS_NAME, 'Tya61d')
					for image in images:
						style_att = image.get_attribute('style')
						image_url = style_att.split('url("')[1].split('");')[0]
						# print(image_url)
						images_list.append(image_url)
				except:
					pass
    
				compiled_review = {'name': reviewer_name, 'comment': review_text, 'images': images_list}
				compiled_reviews.append(compiled_review)
				set_of_reviews.add(reviewer_name) # to avoid duplicates

			if len(reviews) >= MAX_REVIEWS or length == len(set_of_reviews):
				break
			
		# print("Total reviews:", len(compiled_reviews))
		# print(compiled_reviews)
		self.location_data["reviews"] = compiled_reviews
  
	def get_tags(self):
		pass

	def scrape(self, location):
		self.setLangEnglish()
		self.goToMaps()
		self.search_location(location)
		self.get_basic_info()
		self.get_location()
		self.get_reviews()
		self.get_tags()
		# time.sleep(50)

		print(self.location_data)
# location = "Lal Dighi (Pond)/ লাল দিঘী"
# d = SearchDriver()
# d.scrape(location)
# d.exit()