#!/usr/bin/env python
# coding: utf-8

# In[2]:


# !pip install requests
# !pip install html5lib
# !pip install bs4

import pandas as pd 
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


def Scrape(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)
    driver.maximize_window()
    time.sleep(7)

    try:

        views = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
        uploaded_date = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text
        likes = driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a').text
        dislike = driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        views = 0
        uploaded_date = 0
        likes = 0
        dislike = 0
        comment_section = 0
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)     
    
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    
    time.sleep(7)
         
    try:
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')[0].text
    except:
        comment_elems = ""
#     try:
#             # Extract the elements storing the usernames and comments.
#         username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
#         comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
#     except exceptions.NoSuchElementException:
#         error = "Error: Double check selector OR "
#         error += "element may not yet be on the screen at the time of the find operation"
#         print(error)
#     print("> Views " + views + "\n")
#     print("> Uploaded Date " + uploaded_date + "\n")
#     print("> Likes " + likes + "\n")
#     print("> Dislike " + dislike + "\n")

#     print("> USERNAMES & COMMENTS:")
#     print(username_elems[0].text)
#     print(comment_elems[0].text)
    
    Views_list.append(views)
    Date_list.append(uploaded_date)
    Likes_list.append(likes)
    Dislike_list.append(dislike)
    Comment_list.append(comment_elems)

    driver.close()

Views_list = []
Date_list = []
Likes_list = []
Dislike_list = []
Comment_list = []

data = pd.read_csv("Youtube Links.csv")
data.head()
for i in range(len(data)):
    link = data.at[i,'Youtube Link']
    try:
        Scrape(link)
    except:
        print("Link does not work")
    
links_list = data.values.tolist()


# In[7]:


df = pd.DataFrame(list(zip(links_list,Views_list, Date_list,Comment_list,Likes_list,Dislike_list)), columns =['Video Link','Video Views', 'Uploaded Date','Comments','Likes','Dislikes']) 
df.to_csv (r'export_dataframe.csv', index = False, header=True) 


# In[6]:


#print(Views_list)
print(len(Views_list))
# print(Date_list)
# print(Likes_list)
# print(Dislike_list)
# print(Comment_list)

