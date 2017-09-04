#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:25:38 2017

@author: rungsunan
"""

from urllib import request
from bs4 import BeautifulSoup
import pathlib
from random import randint
from time import sleep
#from pymongo import MongoClient


#The url we want to scrape. We seperate the base url becuase there are sub urls
baseurl = 'https://newyork.craigslist.org'
starturl = baseurl + '/search/zip'

#set useragent and headers to fool website into thinking we're a person
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent} 



#Converts a webpage to a soup element
def url_to_soup(url):
    req =  request.Request(url,None,headers)
    resp = request.urlopen(req)
    data = resp.read()
    soup = BeautifulSoup(data, "lxml")
    return soup

#Gets the posting links from a soup object and returns a dictionary with the
#link as the key and the title of the posting as the value
def get_page_links(soupobj):
    itemdict = {}
    g_data = soupobj.find_all("li",{"class":"result-row"})
    for item in g_data:
        linkinfo = item.contents[3].find_all("a", {"class":"result-title hdrlnk"})[0]
        itemdict[baseurl + linkinfo.get('href')] = linkinfo.text
    return itemdict

#takes the next link on a soup object and 
#returns all the sublinks until the last as a list
def get_soup_links(soup):
    templinks = []    
    while (soup):
        try :
            soup.find('link',{"rel":"next"})["href"]
            templinks.append(soup.find('link',{"rel":"next"})["href"])
            newurl = soup.find('link',{"rel":"next"})["href"]
            soup = url_to_soup(newurl)  
        except :
            soup = 0
            exit
    return templinks

#Creates an images directory, and grabs the first image with the title
#as the filename
def get_link_img(link,filename):
    soup = url_to_soup(link)
    pathlib.Path('/Volumes/data/craigslist/images').mkdir(parents=True, exist_ok=True) 
    try:
        imagefilelink =(soup.findAll('img')[0].attrs)['src']
        print (imagefilelink.split('/')[-1]+ "," + filename)
        request.urlretrieve(imagefilelink, '/Volumes/data/craigslist/images/' + filename + ".jpg")
    except:
        print("error")
        exit
    return soup

#scrapelist holds the urls to grab the posting links
scrapelist = [starturl]

startsoup = url_to_soup(starturl)

#All_links holds the links of the craigslist postings
all_links = {}
all_links.update(get_page_links(startsoup))

scrapelist.extend(get_soup_links(startsoup))

for link in scrapelist:
    all_links.update(get_page_links(url_to_soup(link)))

for k,v in all_links.items():
    sleep(randint(10,100))
    get_link_img(k,v)

'''   
client = MongoClient('localhost', 27017)
db = client.craigslist
'''