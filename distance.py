from selenium.webdriver.common.by import By
import time

from webdriver import WebDriver

class DistanceDriver(WebDriver):
  
  def getDistance(self, place1, place2):
    self.setLangEnglish()
    
    time.sleep(2)
    distanceButton = self.driver.find_element(By.XPATH, '//*[@id="hArJGc"]')
    distanceButton.click()
    time.sleep(2)
    drivingButton = self.driver.find_element(By.XPATH, '//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[2]/button')
    drivingButton.click()
    place1Box = self.driver.find_element(By.XPATH, '//*[@id="sb_ifc50"]/input')
    place1Box.send_keys(place1)
    place2Box = self.driver.find_element(By.XPATH, '//*[@id="sb_ifc51"]/input')
    place2Box.send_keys(place2)
    submitButton = self.driver.find_element(By.XPATH, '//*[@id="directions-searchbox-1"]/button[1]')
    submitButton.click()
    time.sleep(5)
    
    self.estimatedTime = self.driver.find_element(By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[1]').text
    self.estimatedDistance = self.driver.find_element(By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div').text
    print("Estimated time: " + self.estimatedTime)
    print("Estimated distance: " + self.estimatedDistance)
    return self.estimatedTime, self.estimatedDistance
		
place1 = 'inani beach'
place2 = 'kolatoli beach'
# place1 = 'dhaka'
# place2 = 'sylhet'
d = DistanceDriver()
d.getDistance(place1, place2)
d.exit()