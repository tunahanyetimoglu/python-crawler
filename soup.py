"""
    1 - Web sitesine baÄŸlan
    2 - Kaynak kodunu al ve bs modÃ¼lÃ¼nÃ¼ aktar
    3 - Bs modÃ¼lÃ¼ ile html kodlarÄ±nÄ± parÃ§ala
    import os   
    os.mkdir(path + "\\" + movieTable[i].find("a",attrs={"class":"film"}).text)
"""

import requests
import urllib.request
import os
from bs4 import BeautifulSoup

def _jpg(url,path,name):
    full_path = path + name + '.jpg'
    urllib.request.urlretrieve(url,full_path)

headers_param = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
path = "E:\CALISMALAR\DATASET"

url = "https://boxofficeturkiye.com/yillik/?yilop=tum&yil=2018&sayfa=2"
r = requests.get(url,headers=headers_param)
soup = BeautifulSoup(r.content,"lxml")

movieTable = soup.find("table",attrs={"class":"ustcizgi"}).find("table",attrs={"class":"navkutu"}).select("table:nth-of-type(4) > tr")
movieCount = len(movieTable)

for i in range(1,movieCount):
    movieUrl = "https://boxofficeturkiye.com" + movieTable[i].find("a",attrs={"class":"film"}).get("href")
    
    pageRequest = requests.get(movieUrl,headers=headers_param)
    pageSource = BeautifulSoup(pageRequest.content,"lxml")
    movieName = movieTable[i].find("a",attrs={"class":"film"}).text
    
    if '?' or ':' in movieName:
        movieName = movieName.replace("?","")
        movieName = movieName.replace(":","")
        
    moviePath = path + "\\" + str(i+100) 
    trailerPath = moviePath + "\Trailer"  
    picturePath = moviePath + "\Picture"
    
    os.mkdir(moviePath)
    os.mkdir(trailerPath)
    os.mkdir(picturePath)
    print(movieName)
    f = open( moviePath+"\{}".format(movieName) + ".txt","a+")
    ### FRAGMAN ISLEMLERI
    movieTrailer = movieUrl + "?filmop=fragman"
    pageTrailerRequest = requests.get(movieTrailer,headers=headers_param)
    pageTrailerSource = BeautifulSoup(pageTrailerRequest.content,"lxml")
    
    trailerTable = pageTrailerSource.findAll("a",attrs={"class":"trailer-link-play-icon"})
    trailerCount = len(trailerTable)
    for i in (0,trailerCount-1):
        trailerLink = pageTrailerSource.findAll("a",attrs={"class":"trailer-link-play-icon"})[i].get("href")
        cmd = "youtube-dl -o {}\%(title)s.%(ext)s {}".format(trailerPath,trailerLink)
        os.system(cmd)
        print("Success")
        
### AFIS ISLEMLERI  
    moviePhotoUrl = movieUrl + "?filmop=resim"
    pagePhotoRequest = requests.get(moviePhotoUrl,headers=headers_param)
    pagePhotoSource = BeautifulSoup(pagePhotoRequest.content,"lxml")
    
    photoTable = pagePhotoSource.find("table",attrs={"class":"navkutu"}).findAll("a",attrs={"class":"poster"})
    for i in range(0,len(photoTable)):
        photoUrl = "https://boxofficeturkiye.com" + photoTable[i].get("href")
        _jpg(photoUrl,picturePath,"\picture{}".format(str(i + 1)))
        
### Izleyici Kısıtlamaları
    movieViewerRestrictions = pageSource.find("table",attrs={"class":"ustcizgi"}).find("div",attrs={"class":"rate-icons"}).select("i")
   
    for i in range(0,len(movieViewerRestrictions)):
        f.write(movieViewerRestrictions[i].get("title") + "\n")
        
    f.close()
