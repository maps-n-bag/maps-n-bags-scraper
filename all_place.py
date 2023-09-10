from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

from webdriver import WebDriver
from search import SearchDriver
import csv
MAX_PLACE=10
from db_connection.db_connection import db_connection
# from search import SearchDriver
conn=db_connection()
cur=conn.cursor()

class all_place(WebDriver):
    def __init__(self):
        super().__init__()
        self.goToMaps()
    def get_all_Tourist_places(self,place):
        # self.setLangEnglish()
        time.sleep(2)
        searchBox = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        searchBox.clear()
        searchBox.send_keys('Restaurant in  '+place  +Keys.ENTER)
        # submitButton = self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
        # submitButton.click()
        # time.sleep(20)
        time.sleep(20)
        #         break
        set_of_places = set()
        bool = True
        
        i=0
        target_places=[]
        while bool:
            time.sleep(5)
            lenth = len(set_of_places)
            places=self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            ratings = self.driver.find_elements(By.CLASS_NAME, 'ZkP5Je')
            for place in places:
                if place.get_attribute('aria-label') in set_of_places:
                    continue
                if(i>=len(ratings)):
                    continue
                rating = ratings[i]
                i+=1
                rating_text=rating.get_attribute('aria-label')
                rating_with_comma=rating_text.split(' ')[2]
                rating_number=int(rating_with_comma.replace(',',''))
                print(rating_number)
                if(rating_number>=10):
                    target_places.append(place)
                if(len(target_places)>=MAX_PLACE):
                    bool=False
                    break
                self.driver.execute_script("arguments[0].scrollIntoView();", place)
                set_of_places.add(place.get_attribute('aria-label'))
            if lenth == len(set_of_places):
                bool = False
        time.sleep(5)
        # all_places = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        
        # f=open('places.csv','w',encoding='utf-8')
        # writer=csv.writer(f)
        # writer.writerow(['Name','Link'])
        i=0
        print(len(target_places))
        list_link={'name':[],'link':[]}
        for place in target_places:
            if i==MAX_PLACE:
                break
            # writer.writerow([place.get_attribute('aria-label'),place.get_attribute('href')])
            # click on the place
            self.driver.execute_script("arguments[0].scrollIntoView();", place)
            list_link['link'].append(place.get_attribute('href'))
            list_link['name'].append(place.get_attribute('aria-label'))
        for i in range(len(list_link['name'])):
            d=SearchDriver(self.driver)
            d.location_data['name']=list_link['name'][i]
            self.driver.get(list_link['link'][i])
            time.sleep(5)
            d.get_basic_info()
            d.get_reviews()
            d.get_location()
            query="""
                INSERT INTO public.place(title, description, latitude, longitude, rating, address, contact, website, region_id,type,rating_count) VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,4,'restaurant',%s)
            """
            try:
                cur.execute(query,(d.location_data['name'],d.location_data['description'],d.location_data['lat'],d.location_data['long'],d.location_data['rating'],d.location_data['address'],d.location_data['contact'],d.location_data['website'],d.location_data['reviews_count'].replace(',','')))
            except:
                continue
            conn.commit()
            if d.location_data['images']!=None:
                place_id=None
                while place_id==None:
                    cur.execute("SELECT last_value FROM public.place_id_seq")
                    place_id=cur.fetchone()[0]
                print(place_id)
                query="""INSERT INTO public.place_image(place_id, link) VALUES (%s,%s)"""
                cur.execute(query,(place_id,d.location_data['images']))
                conn.commit()
            for review in d.location_data['reviews']:
                query="""
                    INSERT INTO public.review(username, comment, place_id) VALUES 
                    (%s,%s,%s)
                """
                cur.execute(query,(review['name'],review['comment'][:255],place_id))
                conn.commit()
                review_id=None
                while review_id==None:
                    cur.execute("SELECT last_value FROM public.review_id_seq")
                    review_id=cur.fetchone()[0]
                for image in review['images']:
                    query="""
                        INSERT INTO public.review_image(review_id, link) VALUES 
                        (%s,%s)
                    """
                    cur.execute(query,(review_id,image))
                    conn.commit()
            print(d.location_data)
        
place = 'Rangamati'
d = all_place()
d.get_all_Tourist_places(place)
cur.close()
conn.close()
d.exit()