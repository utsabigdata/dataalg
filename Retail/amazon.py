import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


class Amazon_Selenium:
    def __init__(self, option=None, url="https://www.amazon.com/"):
        self.url = url
        self.option = option
        self.profile = FirefoxProfile()
        self.driver = None

    '''
    open_page
    Purpose:  Sets the useragent, opens a firefox browser, goes to retailers home page
    Inputs:   None
    Returns:  Sets the objects profile and driver

    '''
    def open_page(self):
        self.profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36")
        self.driver = webdriver.Firefox(firefox_profile = self.profile)
        time.sleep(5)
        self.driver.get(self.url)
        time.sleep(10)

    '''
    close_page
    Purpose:  Closes the firefox browser when data collection in done
    Inputs:   None
    Returns:  None

    '''

    def close_page(self):
        self.driver.implicitly_wait(30)
        self.driver.close()


    '''
    search_key_word
    Purpose:  Given a search term and option = Product Search, the function looks
              up the item, clicks through the pages and collects meta data
    Inputs:   search_term - product name that is to be searched
    Returns:  metadata ()

    '''
    def search_key_word(self, search_term):
        ### try to search for search_term
        try: 
            search_bar = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(10)
        ### TODO: Throw exception
        except: 
            print ("Unsuccesful: COULD NOT FIND ELEMENT")
            return

        ### Get total pages of results from search
        num_pages = self.driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[7]/div/div/div/ul/li[6]')
        num_pages = int(num_pages.text.strip())
        print ("\nTotal Pages: {}".format(num_pages))
        
        ###Click through the pages
        for i in range(num_pages):
            print ("Page {} of {}".format(i+1, num_pages))
            
            ### Check 2 Locations for the Next Button
            button_list = ['//*[@id="search"]/div[1]/div[2]/div/span[7]/div/div/div/ul/li[7]/a',
                            '/html/body/div[1]/div[2]/div[1]/div[2]/div/span[7]/div/div/div/ul/li[8]/a']

            for button in button_list:
                try:
                    next_button = self.driver.find_element_by_xpath(button)
                    next_button.click()
                    break
                except:
                    continue
                
            time.sleep(20)

    '''
    collect_data
    Purpose:  The main controller of the data collection for object. Depending on what option is
              selected, this function selects what other functions needs to be called
    Input:    url - if the user is looking to scrape a specific product page
              search_word - if the user is searching for a product
    Returns:  the metadata collected from the subprocess called
    '''
    def collect_data(self, url=None, search_word=None):
            if self.option == 'S': ### Product Search
                self.search_key_word(search_word)
            elif self.option == 'R':
                print()
            elif self.option == 'B':
                print()
            elif self.option == "U":
                print()
            else:
                print ("INCORRECT OPTION CHOICE")
            return


