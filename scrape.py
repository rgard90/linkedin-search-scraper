
#Import all your libraries

#Selenium and BeautifulSoup let us access the web and navigate a webpage
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


#Time lets us sleep allowing webpages to load better and not bog down LinkedIns site with too many automated requests
import time


#The following libraries are what we use to save the data and export it as a csv for easy consumption in a program like Excel
import pandas as pd
from itertools import zip_longest
import itertools
import operator
import csv


#Set your webdriver. Chromedriver opens up a chrome web browser. Geckodriver opens up a firefox browser and runs the program there.
#Be sure to install either driver you want to use and have it installed in the correct location as written below.
#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe')
driver = webdriver.Firefox(executable_path='C:\Windows\geckodriver.exe')


#Opens up a browser and pulls up the linkedin login page.
driver.get("https://www.linkedin.com/login")
assert "LinkedIn" in driver.title


#Be sure to put your linkedin username and password in the following fields or else you wont be able to search.
userid = str("PUT YOUR USERNAME IN HERE")
password = str("PUT YOUR PASSWORD IN HERE")


#Finds the username and password areas of the page and logs in for you.
driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(password)
time.sleep(2)
driver.find_element_by_xpath("""//*[@class="btn__primary--large from__button--floating"]""").click()


#A small buffer to ensure page loads properly.
time.sleep(5)


#Initialize the lists we will fill out in our search. You can see the things we will be collecting are name, title and location of each person. 
#The company name is actually baked into the title though so we got that too. We can parse that out later.
name_list = []
title_list = []
loc_list = []


#Loop through the number of pages that your search returned. Be sure to change this number to the correct number of pages in your search results.
#Also be sure to switch out the url in the top of this for loop. Craft your advanced search on your linkedin page then copy that URL over here to save the results.
#In this example I am searching for all ex-Google employees living in SLC.
for i in range(NUMBER OF SEARCH RESULT PAGES):
    driver.get("https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A716%22%5D&facetPastCompany=%5B%221441%22%5D&origin=FACETED_SEARCH"+"&page="+str(i+1))
    time.sleep(9)
    #The scroll here is important because if you dont scroll linkedin doesnt load the entire webpage and you wont be able to save all results off each page.
    driver.execute_script("window.scrollBy(0,500)");
    time.sleep(5)


    #Finds all names, titles, and locations of people on the page and saves them.
    name = driver.find_elements_by_xpath("""//*[@class="name actor-name"]""")
    title = driver.find_elements_by_xpath("""//*[@class="subline-level-1 t-14 t-black t-normal search-result__truncate"]""")
    location = driver.find_elements_by_xpath("""//*[@class="subline-level-2 t-12 t-black--light t-normal search-result__truncate"]""")
    
    for x in name:
        name_list.append(x.text.replace('\n', ' ').replace('\r', ''))

    for x in title:
        title_list.append(x.text.replace('\n', ' ').replace('\r', ''))
        
    for x in location:
        loc_list.append(x.text.replace('\n', ' ').replace('\r', ''))


    #This just prints to the console how many results are saved on each page as a way to check for errors as the scan runs.
    #Sometimes the scan will miss a name or title (about 1/1000) so it makes it easy to go back and fix manually.
    print('')
    print(len(name_list))
    print(len(title_list))
    print(len(loc_list))
    
    print('')
    print("Done with page " + str(i+1))
    print('')
    print("--------------------------------------");
   
   
#Zips together the three lists of data we created above. Matches the first/second/third of each list with the first/second/third of the other lists.
ziplist = list(itertools.zip_longest(name_list,title_list,loc_list))


#Turns that zipped list into a Pandas df
ziplist_df = pd.DataFrame(ziplist)


#Prints first 10 rows of df for basic error checking
print(ziplist_df.head(10))


#Saves df as csv in your current working directory.
ziplist_df.to_csv('list.csv', index = False)

