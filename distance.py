from selenium.webdriver.common.by import By
import time

from webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from db_connection.db_connection import db_connection
conn=db_connection()
cur=conn.cursor()

class DistanceDriver(WebDriver):
  
  def getDistance(self):
    self.goToMaps()
    # self.setLangEnglish()
    
    time.sleep(10)
    cross_button = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[2]/button')
    cross_button.click()
    time.sleep(2)
    cross_button.click()
    time.sleep(2)
    drivingButton = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button/img')
    drivingButton.click()
    query="""
    SELECT first_place_id, second_place_id FROM public.distance WHERE distance = 0 """
    cur.execute(query)
    rows=cur.fetchall()
    i=0
    for row in rows:
      if i>= 30:
        break
      i+=1
      query="""
      SELECT latitude,longitude FROM public.place WHERE id=%s """

      cur.execute(query,(row[0],))
      langs=cur.fetchall()
      lat1=langs[0][0]
      long1=langs[0][1]
      print(langs)
      query="""
      SELECT latitude,longitude FROM public.place WHERE id=%s """
      cur.execute(query,(row[1],))
      langs=cur.fetchall()
      lat2=langs[0][0]
      long2=langs[0][1]
      placeBox = self.driver.find_elements(By.CLASS_NAME, 'tactile-searchbox-input')
      placeBox[0].clear()
      placeBox[0].send_keys(str(lat1)+","+str(long1))
      placeBox[1].clear()
      placeBox[1].send_keys(str(lat2)+","+str(long2)+Keys.ENTER)
      time.sleep(10)
      
      self.estimatedTime = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[1]').text
      self.estimatedDistance = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[2]/div').text
      print("Estimated time: " + self.estimatedTime)
      print("Estimated distance: " + self.estimatedDistance)
      if(self.estimatedDistance.split(' ')[1]=='km'):
        distance=float(self.estimatedDistance.split(' ')[0])
      else:
        distance=float(self.estimatedDistance.split(' ')[0])/1000
      if(self.estimatedTime.split(' ')[1]=='min'):
        est_time=float(self.estimatedTime.split(' ')[0])
      else:
        est_time=float(self.estimatedTime.split(' ')[0])*60+float(self.estimatedTime.split(' ')[2])
      query="""
      UPDATE public.distance SET distance=%s, est_time=%s WHERE first_place_id=%s AND second_place_id=%s """
      cur.execute(query,(distance,est_time,row[0],row[1]))
      conn.commit()

    return self.estimatedTime, self.estimatedDistance
		
place1 = 'inani beach'
place2 = 'kolatoli beach'
# place1 = 'dhaka'
# place2 = 'sylhet'
d = DistanceDriver()
d.getDistance()
d.exit()