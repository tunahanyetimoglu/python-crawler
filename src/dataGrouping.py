# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 18:06:44 2019

@author: tuhanan
"""

import os
from path import Path

source = "../DATASET\\"
dest = "../DATASET_YAS"


if not os.path.exists(source):
    os.mkdir(source)
    
if not os.path.exists(dest):
    os.mkdir(dest)
    
a = "Genel İzleyici Kitlesi."
b = "7 yaş ve üzeri izleyici kitlesi içindir."
c = "7 yaş altı izleyici kitlesi aile eşliğinde izleyebilir."
d = "13 yaş altı izleyici kitlesi aile eşliğinde izleyebilir."
e = "13 yaş ve üzeri izleyici kitlesi içindir."
f = "15 yaş ve üzeri izleyici kitlesi içindir."
g = "15 yaş altı izleyici kitlesi aile eşliğinde izleyebilir."
h = "18 yaş ve üzeri izleyici kitlesi içindir."

thisList = [a, b, c, d, e, f, g, h]

files = []

def transfer(sr,dc):
    print ("\n\Files copying form  %s to %s  !!\n" % (sr, dc))
    fileCount = 0
    for i in Path(sr).walk(): #browse files in the directory
        if i.isfile() and i.endswith("mp4"): #If there is an mp4 file extension
 
            fileCount += 1 # Increase the number of files
            print("Copying.. %s" % i)
            i.copy(Path(dc)) #copy the file with the mp4 extension in the current index to the destination
 
 
    if (fileCount == 0):
        print("Current directory not found  .mp4 file ! ")
    else:
        print("\n%s files copied successfully" % fileCount)
 
for r, d, f in os.walk(source):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

fileCount = 0
for f in files:
    file = open(f,"r")
    count = 0
    textList = (file.read()).split("\n")
    for i in range(0,len(textList)):
        if textList[i] in thisList:
            count += 1
    if count > 1:
        fileCount += 1
        text = open("../garbage.txt","a+")
        text.write("{}".format(f.split("\\")[1]) + "\t" + textList[0] + " , " + textList[1] + "\n")
    elif count == 1:
        if(textList[0] == thisList[1]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\7 Yas")
        elif(textList[0] == thisList[2]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\7 Yas ve Aile")
        elif(textList[0] == thisList[3]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\13 Yas ve Aile")
        elif(textList[0] == thisList[4]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\13 Yas")
        elif(textList[0] == thisList[5]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\15 Yas")
        elif(textList[0] == thisList[6]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\15 Yas ve Aile")
        elif(textList[0] == thisList[7]):
            transfer(source + (f.split("\\"))[1] ,dest + "\\18 Yas")
    file.close()
text.write("\nNumber of files containing 2 groups")
text.close()
   
