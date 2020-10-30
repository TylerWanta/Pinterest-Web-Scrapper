import scrapy
from WebScraper.items import ImageItem

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import datetime

import logging

import sys

# spider used to scrape pinterest images
class pSpider(scrapy.Spider):

    # name of spider used for 'scrapy crawl -name' command
    name = "pSpider"

    # initilizer
    def __init__(self):

        # set so less stuff gets printed to console
        LOGGER.setLevel(logging.WARNING)

        chrome_options = Options()
        # chrome_options.add_argument('--no-proxy-server')
        # #chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--proxy-server='direct://'")
        # chrome_options.add_argument("--proxy-bypass-list=*")
        
        # webdriver
        self.driver = webdriver.Chrome(executable_path='C:\\Users\\WantaTyler\\OneDrive - University of Wisconsin-Stout\\Documents\\Ruby\\chromedriver', chrome_options=chrome_options)

        # set some timeouts 
        self.driver.set_script_timeout(300)
        self.wait = WebDriverWait(self.driver, timeout=10, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))

        # array used to store urls of images
        self.urls = []

        # keep track if we have logged in yet
        self.logedIn = False

        self.count = 0


    # urls to scrape - 10 each. Trying to get as many as possible as ill probs have to go 
    # through and delete the ones that arn't actually outfits that get scraped
    start_urls = [
        # men outfits 
        "https://www.pinterest.com/dalepartridge/mens-fashion/", # overall fashionable outfits
        "https://www.pinterest.com/search/pins/?q=Mens%20fashion%20summer&rs=srs&b_id=BEI4Pf9qFGCMAAAAAAAAAABp_AIYPwYDBSx0xvRnIG4ShAlrc1e2gYgXm-gZ7Au9JKNJ50csiLLzjMcZOOYvg1Y&source_id=3Y97iOlW", # summer outfits
        "https://www.pinterest.com/search/pins/?q=Mens%20winter%20fashion&rs=srs&b_id=BARCtg8Fa5CAAAAAAAAAAADsCgKgrMdhpcajZ87EA5_rc9a7c8FJeGQybLV61mxB-wu57tLSllgoCvvgSOrZaq4&source_id=3Y97iOlW", # winter outfits
        "https://www.pinterest.com/search/pins/?q=men%20business%20casual%20outfit&rs=typed&term_meta[]=men%7Ctyped&term_meta[]=business%7Ctyped&term_meta[]=casual%7Ctyped&term_meta[]=outfit%7Ctyped", #Business Casual
        "https://www.pinterest.com/search/pins/?q=best%20men%20outfits&rs=typed&term_meta[]=best%7Ctyped&term_meta[]=men%7Ctyped&term_meta[]=outfits%7Ctyped", # another general one
        "https://www.pinterest.com/search/pins/?q=formal%20men%20outfits&rs=typed&term_meta[]=formal%7Ctyped&term_meta[]=men%7Ctyped&term_meta[]=outfits%7Ctyped", # formal outfits
        "https://www.pinterest.com/search/pins/?q=fahionable%20mens%20outfits&rs=typed&term_meta[]=fahionable%7Ctyped&term_meta[]=mens%7Ctyped&term_meta[]=outfits%7Ctyped", # more fashionable
        "https://www.pinterest.com/search/pins/?q=beach%20men%20outfit&rs=typed&term_meta[]=beach%7Ctyped&term_meta[]=men%7Ctyped&term_meta[]=outfit%7Ctyped", # more summer outfits
        "https://www.pinterest.com/search/pins/?q=preppy%20men%20outfit&rs=typed&term_meta[]=preppy%7Ctyped&term_meta[]=men%7Ctyped&term_meta[]=outfit%7Ctyped", # preppy outfits
        "https://www.pinterest.com/search/pins/?q=sports%20men%20outfit&rs=typed&term_meta[]=sports%7Ctyped&term_meta[]=men%7Ctyped&term_meta[]=outfit%7Ctyped", # sport outfits

        # women outfits
        "https://www.pinterest.com/esbedesignslynn/cute-outfits/", # overall fashionable outfits
        "https://www.pinterest.com/search/pins/?q=Summer%20outfits%20women&rs=srs&b_id=BPgJ3WbyA5hkAAAAAAAAAABrDXTowd4XyQfUI7b4BaMjed6IK_FQWpVJqarU_MJzaJFzPh5VgoF7b3XuzeLBYyE&source_id=D1LIcFeD", #summer outfits
        "https://www.pinterest.com/search/pins/?q=winter%20outfits%20women&rs=typed&term_meta[]=winter%7Ctyped&term_meta[]=outfits%7Ctyped&term_meta[]=women%7Ctyped", # winter outfits 
        "https://www.pinterest.com/search/pins/?q=business%20casual%20outfits%20women&rs=typed&term_meta[]=business%7Ctyped&term_meta[]=casual%7Ctyped&term_meta[]=outfits%7Ctyped&term_meta[]=women%7Ctyped", # business casual
        "https://www.pinterest.com/search/pins/?q=best%20women%20outfits&rs=typed&term_meta[]=best%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # another general one
        "https://www.pinterest.com/search/pins/?q=formal%20women%20outfits&rs=typed&term_meta[]=formal%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # formal outfits
        "https://www.pinterest.com/search/pins/?q=fashionable%20women%20outfits&rs=typed&term_meta[]=fashionable%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # more fashionable
        "https://www.pinterest.com/search/pins/?q=beach%20women%20outfits&rs=typed&term_meta[]=beach%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # more summer outfits
        "https://www.pinterest.com/search/pins/?q=preppy%20women%20outfits&rs=typed&term_meta[]=preppy%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # preppy outfits
        "https://www.pinterest.com/search/pins/?q=sports%20women%20outfits&rs=typed&term_meta[]=sports%7Ctyped&term_meta[]=women%7Ctyped&term_meta[]=outfits%7Ctyped", # sports
    ]
    
    # method used to log in 
    def login(self):

        self.driver.get('https://www.pinterest.com/')

        # find login button
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//button/div[text()="Log in"]')))

        # find and click log in button
        self.driver.find_element(By.XPATH, '//button/div[text()="Log in"]').click()

        # wait for iframe to appear and switch to it
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe')))

        # wait for span to click on
        # this is really fragile and will probs need to be changed in the furture
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_8jan"]')))

        # get the span and click on it
        ele = self.driver.find_element(By.XPATH, '//span[@class="_8jan"]')
        self.driver.execute_script("arguments[0].click()", ele)

        # wait and switch to new instance of chrome that appears - facebook login page
        self.wait.until(lambda driver: len(driver.window_handles) == 2)
        self.driver.switch_to_window(self.driver.window_handles[1])

        # wait till email field is available
        self.wait.until(EC.presence_of_element_located((By.ID, "email")))

        # get and update fields
        userName = self.driver.find_element_by_id('email')
        passWord = self.driver.find_element_by_id('pass')

        # username and password for Pinterest
        userName.send_keys('')
        passWord.send_keys('')

        # login 
        self.driver.find_element_by_name('login').click()

        # switch back to first instance
        self.wait.until(lambda driver: len(driver.window_handles) == 1)
        self.driver.switch_to_window(self.driver.window_handles[0])

        self.logedIn = True

        return True

    # method called for each url 
    def parse(self, response):    
        self.count += 1

        # if we havn't logged in, we need to so we can get more images
        if not self.logedIn:
            # since im using the sketchiest way possible to locate the login button
            # somtimes it doesn't work but refreshing everntually works
            while True:
                try:
                    self.login()
                    break
                except:
                    self.driver.refresh()

        # as to not overload pinterest with requests
        print('Waiting...')
        time.sleep(10)
        print('Ready To Go!')

        # load the page
        self.driver.get(response.url)

        # wait for page to load
        while True:
            try: 
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//body')))
                break
            except:
                self.driver.refresh()

        # current height of the page. 
        current_height = self.driver.execute_script("return document.body.scrollHeight;")

        # used to store current urls
        current_urls = []

        # keep going while we can keep scrolling or are below 500 images
        while True:

            # used so I can handle StaleElementReferenceExceptions
            # Dom changes while scraping and any element changed will throw excpetion
            # ok to just ignore it and keep going since I just want the img url
            try:
                # get all current image urls
                image_urls = map(lambda x: x.get_attribute('src'), self.driver.find_elements_by_tag_name('img'))

                # check to see if it has already been scraped on this site
                current_urls.extend(list(set(image_urls) - set(current_urls)))

                # check to see if it has been scraped on another site
                current_urls = list(set(current_urls) - set(self.urls))

            except StaleElementReferenceException:
                print('\n Error occured \n')
                pass

            # stop at 500 
            if(len(current_urls) > 500):
                print(f'Total Number of images so far is {len(current_urls)} from {response.url}')
                break

            print(f'Length of current is {len(current_urls)} fron {response.url}')

            #Scroll to the bottom and get the new height. Break out if we are unable to get a new height i.e Webdriver Wait TimeoutException
            try:
                self.wait.until(lambda driver: self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight); console.log(document.body.scrollHeight); return document.body.scrollHeight;")  > current_height)
                current_height = self.driver.execute_script("return document.body.scrollHeight;")
            except:
                break
        
        # add new urls to array
        self.urls.extend(current_urls)
        print(f'Running image total is {len(self.urls)} at url # {self.count}')

        if self.count == 20:
            print('Ready to donwload')
            yield ImageItem(image_urls=self.urls)

    def closed(self, reason):
        self.driver.quit()
        
        if len(self.urls) > 10000:
            print(f'SUCCESS!!!!! We got {len(self.urls)} images')
        else:
            print(f'Ehhhhh, we only got {len(self.urls)} images')
