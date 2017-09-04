#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:25:38 2017

@author: rungsunan
"""
baseurl = 'https://newyork.craigslist.org'
starturl = baseurl + '/search/zip'
import pathlib
import urllib
from bs4 import BeautifulSoup
#from pymongo import MongoClient


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent} 

scrapelist = [starturl]

def url_to_soup(url):
    req =  urllib.request.Request(url,None,headers)
    resp =  urllib.request.urlopen(req)
    data = resp.read()
    soup = BeautifulSoup(data, "lxml")
    return soup

startsoup = url_to_soup(starturl)

def get_page_links(soupobj):
    itemdict = {}
    g_data = soupobj.find_all("li",{"class":"result-row"})
    for item in g_data:
        linkinfo = item.contents[3].find_all("a", {"class":"result-title hdrlnk"})[0]
        itemdict[baseurl + linkinfo.get('href')] = linkinfo.text
    return itemdict

all_links = {}
all_links.update(get_page_links(startsoup))

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

scrapelist.extend(get_soup_links(startsoup))

for link in scrapelist:
    all_links.update(get_page_links(url_to_soup(link)))


def get_link_img(link,filename):
    soup = url_to_soup(link)
    pathlib.Path('images').mkdir(parents=True, exist_ok=True) 
    try:
        imagefilelink =(soup.findAll('img')[0].attrs)['src']
        print (imagefilelink.split('/')[-1])
        urllib.request.urlretrieve(imagefilelink, 'images/' + filename + ".jpg")
    except:
        exit
    return soup
for k,v in all_links.items():
    testsoup = get_link_img(k,v)


'''   
soupify = get_link_img(list(all_links.keys())[0])
txt = (soupify.prettify())
linksoup = get_link_img(list(all_links.keys())[0])

client = MongoClient('localhost', 27017)
db = client.craigslist
'''