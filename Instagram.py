import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os


try:
        username = input("Enter a username: ")

        options = Options()
        options.add_argument('--headless')
        
        url = "https://www.instagram.com/" + username
        driver = webdriver.Firefox()#options=options
        driver.get(url)
        html_content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html_content, "html.parser")

        SCROLL_PAUSE_TIME = 2

        last_height = driver.execute_script("return document.body.scrollHeight")

        image_list = []

        while True:
                

                html_content = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html_content, "html.parser")
                img_html = soup.find_all("img",{"class":"FFVAD"})

                img_list = [x['src'] for x in img_html]

                for i in img_html:
                        url = str(i['src'])
                        if (url not in image_list):
                                image_list.append(url)

                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                #21:12
                if new_height == last_height:

                        time.sleep(15)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        new_height = driver.execute_script("return document.body.scrollHeight")

                        if new_height == last_height:
                                break
                last_height = new_height

        
        if not os.path.exists('Images\\' + username):
                os.mkdir('Images\\' + username)

        print(len(image_list))

        for i,z in zip(image_list,range(1,len(image_list) + 1)):

                response = requests.get(i)
                with open("Path Here" + username + "\\Image_" + str(z) + ".png",'wb') as f:
                                f.write(response.content)

except Exception as e:
        print(e)

finally:
        driver.close()
        driver.quit()
