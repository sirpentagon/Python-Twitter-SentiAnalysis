# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 11:36:44 2017

@author: Arijit
"""
import sys
import json
from os import getcwd
from bs4 import BeautifulSoup
from selenium import webdriver

class IMDB():
    
    def __init__(self,path=getcwd()+'\phantomjs.exe',url="http://m.imdb.com/feature/bornondate",limit=10):
        self.path = path
        self.url = url
        self.limit =  limit
        self.__connect()
        self.__scrapeWebContent()
    
    def __connect(self):
        try:       
            driver = webdriver.PhantomJS(self.path.__str__())
            driver.get(self.url)
            readHTML = driver.page_source
            self.readHTML = readHTML
        except Exception as exp:
            exp.args
            sys.exit()
        finally:
            driver.close()
            driver.quit()
            
    def __scrapeWebContent(self):
        soup = BeautifulSoup(self.readHTML, 'lxml')
        self.celeb_name = []
        self.celeb_img = []
        self.celeb_profession = []
        self.celeb_best_work = []
        
        #Get Image
        img = soup.find_all('a', class_='poster ', limit=self.limit)
        for cel_img in img:
            self.celeb_img.append(cel_img.find('img')['src'])
            
        #Get Name    
        name = soup.find_all('span', class_='title', limit=self.limit)
        for info in name:
            self.celeb_name.append(info.text)
            
        #Get Profession & Work
        tmp = soup.find_all('div', class_='detail', limit=self.limit)
        for i in tmp:
            a,b = i.text.split(',',1)
            self.celeb_profession.append(a)
            self.celeb_best_work.append((b.replace("\"",'')).strip())

    def __printData(self):
        print "Celeb Name : \n------------------"
        for name in self.celeb_name:
            print name            
        print "\nCeleb Image : \n------------------"
        for img in self.celeb_img:
            print img        
        print "\nCeleb Prof : \n------------------"
        for prof in self.celeb_profession:
            print prof            
        print "\nCeleb Best Work : \n------------------"
        for best_work in self.celeb_best_work:
            print best_work
        
    def getdata(self):
        json_obj = json.dumps([{'name': n, 'profession':p, 'bestwork':b, 'image':i} \
                                     for n,p,b,i in zip(self.celeb_name,self.celeb_profession, \
                                                        self.celeb_best_work,self.celeb_img)])
        jsondata = json.loads(json_obj)
        return jsondata

if __name__ == "__main__":
    path = getcwd()+'\phantomjs.exe'
    url = "http://m.imdb.com/feature/bornondate"
    limit_data = 10
    IMDBobj = IMDB()
    print IMDBobj.getdata()