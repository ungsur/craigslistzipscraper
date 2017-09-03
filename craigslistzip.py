#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:25:38 2017

@author: rungsunan
"""
baseurl = 'https://newyork.craigslist.org'
starturl = baseurl + '/search/zip'

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
            print(soup.find('link',{"rel":"next"})["href"])
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
'''
for linkurl in scrapelist:
    print(linkurl)
    soup = url_to_soup(linkurl)
    all_links.update(get_page_links(soup))
   
def link_to_soup(link):
    req = urllib.request.Request(link,None,headers)
    resp = urllib.request.urlopen(req)
    data = resp.read()
    soup = BeautifulSoup(data, "lxml")
    return soup

def get_link_img(link):
    print(link)
    soup = link_to_soup(link)
    return soup
   
soupify = get_link_img(list(all_links.keys())[0])
txt = (soupify.prettify())
linksoup = get_link_img(list(all_links.keys())[0])

client = MongoClient('localhost', 27017)
db = client.craigslist
'''