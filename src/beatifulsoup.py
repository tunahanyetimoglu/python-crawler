# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 21:02:35 2019

@author: tuhanan

"""

import requests
import urllib.request
import os
from bs4 import BeautifulSoup


headersParam = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
url = "https://boxofficeturkiye.com/yillik/?yilop=tum&yil=2018&sayfa=6"
address = "https://boxofficeturkiye.com/"
path = "../DATASET"

if not os.path.exists(path):
    os.mkdir(path)

def _jpg(url,path,name):
    full_path = path + name + '.jpg'
    urllib.request.urlretrieve(url,full_path)

r = requests.get(url,headers=headersParam)
soup = BeautifulSoup(r.content,"lxml")

movieTable = soup.find("table",attrs={"class":"ustcizgi"}).find("table",attrs={"class":"navkutu"}).select("table:nth-of-type(4) > tr")
movieCount = len(movieTable)

for i in range(80,movieCount):
    movieUrl = address + movieTable[i].find("a",attrs={"class":"film"}).get("href")
    
    pageRequest = requests.get(movieUrl,headers=headersParam)
    pageSource = BeautifulSoup(pageRequest.content,"lxml")
    movieName = movieTable[i].find("a",attrs={"class":"film"}).text
    
    if '?' or ':' or '/' in movieName:
        movieName = movieName.replace("?","")
        movieName = movieName.replace(":"," ")       
        movieName = movieName.replace("/"," ")
        
    moviePath = path + "\\" + str(i+500) 
    trailerPath = moviePath + "\Trailer"  
    picturePath = moviePath + "\Picture"
    
    os.mkdir(moviePath)
    os.mkdir(trailerPath)
    os.mkdir(picturePath)
    print(movieName)
    f = open( moviePath+"\{}".format(movieName) + ".txt","a+")
    
### TRAILER PROCESS
    movieTrailer = movieUrl + "?filmop=fragman"
    pageTrailerRequest = requests.get(movieTrailer,headers=headersParam)
    pageTrailerSource = BeautifulSoup(pageTrailerRequest.content,"lxml")
    
    trailerTable = pageTrailerSource.findAll("a",attrs={"class":"trailer-link-play-icon"})
    trailerCount = len(trailerTable)
    
    if trailerCount == 0:
        trailerCount = 1
    elif trailerCount == 1:
        trailerCount = 2
    
    for i in range(0,trailerCount-1):
        trailerLink = pageTrailerSource.findAll("a",attrs={"class":"trailer-link-play-icon"})[i].get("href")
        cmd = "youtube-dl -o {}\%(title)s.%(ext)s {}".format(trailerPath,trailerLink)
        os.system(cmd)
        print("Success")
        
### BANNER PROCESS  
    moviePhotoUrl = movieUrl + "?filmop=resim"
    pagePhotoRequest = requests.get(moviePhotoUrl,headers=headersParam)
    pagePhotoSource = BeautifulSoup(pagePhotoRequest.content,"lxml")
    
    photoTable = pagePhotoSource.find("table",attrs={"class":"navkutu"}).findAll("a",attrs={"class":"poster"})
    for i in range(0,len(photoTable)):
        photoUrl = address + photoTable[i].get("href")
        _jpg(photoUrl,picturePath,"\picture{}".format(str(i + 1)))
        
### VIEWER RESTRICTIONS
    movieViewerRestrictions = pageSource.find("table",attrs={"class":"ustcizgi"}).find("div",attrs={"class":"rate-icons"}).select("i")
    if movieViewerRestrictions == 0:
        movieViewerRestrictions = 1
    elif movieViewerRestrictions == 1:
        movieViewerRestrictions = 2
    for i in range(0,len(movieViewerRestrictions)):
        f.write(movieViewerRestrictions[i].get("title") + "\n")
        
    f.close()