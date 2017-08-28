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

req =  urllib.request.Request(starturl,None,headers)
resp =  urllib.request.urlopen(req)
data = resp.read()
soup = BeautifulSoup(data, "lxml")
txt = (soup.prettify())

def get_page_links(soupobj):
    itemdict = {}
    g_data = soupobj.find_all("li",{"class":"result-row"})
    for item in g_data:
        linkinfo = item.contents[3].find_all("a", {"class":"result-title hdrlnk"})[0]
        itemdict[baseurl + linkinfo.get('href')] = linkinfo.text
    return itemdict

all_links = {}
def get_soup_links(soup):
    templinks = []    
    while (soup):
        try :
            soup.find('link',{"rel":"next"})["href"]
            templinks.append(soup.find('link',{"rel":"next"})["href"])
            newurl = soup.find('link',{"rel":"next"})["href"]
            newreq =  urllib.request.Request(newurl,None,headers)
            newresp =  urllib.request.urlopen(newreq)
            newdata = newresp.read()
            soup = BeautifulSoup(newdata, "lxml")
        except :
            soup = 0
            exit
    return templinks
scrapelist.extend(get_soup_links(soup)) 

for linkurl in scrapelist:
    req =  urllib.request.Request(linkurl,None,headers)
    resp =  urllib.request.urlopen(req)
    data = resp.read()
    soup = BeautifulSoup(data, "lxml")
    all_links.update(get_page_links(soup))
'''
client = MongoClient('localhost', 27017)
db = client.craigslist
'''