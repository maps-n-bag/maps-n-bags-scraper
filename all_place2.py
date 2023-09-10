from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

from webdriver import WebDriver
from search import SearchDriver
import csv
MAX_PLACE=0
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
        searchBox.send_keys('Things to do in  '+place +' Riview count high' +Keys.ENTER)
        # submitButton = self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
        # submitButton.click()
        # time.sleep(20)
        time.sleep(20)
        #         break
        set_of_places = set()
        bool = True
        
        list_link={'name':[],'link':[]}
        list_link['name'].append('Shuvolong Choto Waterfalls')
        list_link['link'].append('https://www.google.com/maps/place/Shuvolong+Choto+Waterfalls+(%E0%A6%B6%E0%A7%81%E0%A6%AD%E0%A6%B2%E0%A6%82+%E0%A7%A8)/@22.7067639,92.2373573,17z/data=!3m1!4b1!4m6!3m5!1s0x3752b1c8b84866b9:0x542cba893f6eba45!8m2!3d22.7067639!4d92.2373573!16s%2Fg%2F11qmnk4t8_?authuser=0&hl=en&entry=ttu')
        list_link['name'].append('Polwel Park')
        list_link['link'].append('https://www.google.com/maps/place/Polwel+Park/@22.6411599,92.1999049,17z/data=!3m1!4b1!4m6!3m5!1s0x3752b58c9bcbfe81:0x13a4de90953f35cb!8m2!3d22.6411599!4d92.1999049!16s%2Fg%2F11j3v84jjb?authuser=0&hl=en&entry=ttu')
        list_link['name'].append('Rangamati Hanging Bridge')
        list_link['link'].append('https://www.google.com/maps/place/Rangamati+Hanging+Bridge/@22.627617,92.187376,17z/data=!3m1!4b1!4m6!3m5!1s0x3752b573327f055f:0xea1f8fb8d4e8dbac!8m2!3d22.6276121!4d92.1899509!16s%2Fg%2F11q4dgdfb3?authuser=0&hl=en&entry=ttu')
        list_link['name'].append('Kaptai National Park')
        list_link['link'].append('https://www.google.com/maps/place/Kaptai+National+Park/@22.4989571,92.1776684,17z/data=!3m1!4b1!4m6!3m5!1s0x30ad4984c4ec0c4b:0xd4a579c55f6c6ce4!8m2!3d22.4989571!4d92.1776684!16s%2Fg%2F11clszfkwt?authuser=0&hl=en&entry=ttu')

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
                (%s,%s,%s,%s,%s,%s,%s,%s,4,'spot',%s)
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