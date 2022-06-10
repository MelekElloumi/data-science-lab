import requests,time,shutil

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from mongodb_access import send_to_mongo

class Connector:
    """
    This Connector class contains a scraper scenario in the connect() method. It logins to facebook
    and send the data to mongodb_access.py.
    """
    def __init__(self):
        self.driver=None

    #The connector go through all of these functions one by one
    def connect(self):
        self.create_driver()
        self.getCredentials()
        self.facebook_login()
        self.access_photos()
        self.save_data()
        self.end()

    #This creates the chrome driver
    def create_driver(self):
        options=self.initialize_chrome_options()
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver.exe')
        self.driver.maximize_window()

    #This initialises chrome driver starting options
    def initialize_chrome_options(self):
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("--disable-extensions")
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        return option

    #Get the email,password and subject from facebook_credentials.txt
    def getCredentials(self):
        with open('facebook_credentials.txt') as file:
            self.email = file.readline().split('"')[1]
            self.password = file.readline().split('"')[1]
            self.subject = file.readline().split('"')[1]

    #opens facebook.com and logins with the credentials
    def facebook_login(self):
        self.driver.get('https://www.facebook.com/')
        self.driver.find_element(by=By.NAME, value='email').send_keys(self.email)
        self.driver.find_element(by=By.NAME, value='pass').send_keys(self.password)
        self.driver.find_element(by=By.NAME, value='login').click()
        WebDriverWait(self.driver, 20).until(
            EC.title_is("Facebook")
        )

    #Make a search with the given subject and access all photos
    def access_photos(self):
        query=self.subject.replace(" ","%20")
        self.driver.get(f'https://www.facebook.com/search/photos?q={query}')
        self.driver.find_elements(by=By.XPATH, value="//a[@aria-label='See all']")[-1].click()
        time.sleep(1)
        self.image_posts_elements = self.driver.find_elements(by=By.XPATH,
                        value="//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/div/a")

    #This function iterates over every photo, and saves the image, the description and the comments if they exisits.
    #Then it sends the data to mongodb
    def save_data(self):
        for i,img_post_element in enumerate(self.image_posts_elements):
            #enter a photo
            img_post_element.click()
            time.sleep(1)

            #get image
            image_element = self.driver.find_element(by=By.XPATH, value="//div/div/div/img")
            image_url = image_element.get_attribute("src")
            self.save_image(image_url)

            #get description
            try:
                description_element = self.driver.find_element(by=By.XPATH,
                         value="//div/div[1]/div/div[4]/div/div/div[1]/div/div[3]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/span").text
            except NoSuchElementException:
                description_element=""

            #get comments
            comments_elements = self.driver.find_elements(by=By.XPATH,
                        value="//div/div[1]/div/div[4]/div/div/div[1]/div/div[3]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[4]/ul/li")
            comments_data=[]
            for comment_element in comments_elements:
                comment = comment_element.find_element(by=By.XPATH, value="//div/div/div/span/div/div[@dir='auto']")
                comments_data.append({f"comment":comment.text})

            #send to mongodb
            data={
                "description": description_element,
                "image_url": image_url,
                "comments":comments_data
            }
            print(data)
            send_to_mongo(data)

            #return to all photos page
            self.driver.back()
            time.sleep(1)

    #Save the image locally in the 'images' folder
    def save_image(self,image_url):
        r = requests.get(image_url, stream=True)
        filename = image_url.split("/")[-1]
        filename = filename.split("?")[0]
        filename = "images/"+filename
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    #Closing the driver
    def end(self):
        self.driver.close()


if __name__ == '__main__':
    connector=Connector()
    connector.connect()

