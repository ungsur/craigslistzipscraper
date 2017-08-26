#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:25:38 2017

@author: rungsunan
"""
baseurl = 'https://newyork.craigslist.org'
searchurl = baseurl + '/search/zip'

import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

req =  urllib.request.Request(url,None,headers)
resp =  urllib.request.urlopen(req)
data = resp.read()


soup = BeautifulSoup(data, "lxml")
txt = (soup.prettify())
'''
links =  soup.find_all("a")
for link in links:
    print("<a href='%s'>%s</a>" %(link.get('href'), link.text))
'''

def get_pages(soupobj):
    pagelinks = soupobj.find_all("li",{"class":"result-row"})
    return pagelinks
def get_page_links(soupobj):
    itemdict = {}
    g_data = soupobj.find_all("li",{"class":"result-row"})
    for item in g_data:
        linkinfo = item.contents[3].find_all("a", {"class":"result-title hdrlnk"})[0]
        itemdict[baseurl + linkinfo.get('href')] = linkinfo.text
    return itemdict

firstdict = get_page_links(soup)
client = MongoClient('localhost', 27017)
db = client.craigslist