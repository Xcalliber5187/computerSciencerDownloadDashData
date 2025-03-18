#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Orginial code from: https://github.com/dclabby/EirgridDashboardAnalysis/blob/master/downloadDashboardData.py
"""
Created on Wed Feb  3 12:41:03 2021

@author: dclabby



"""

"""

Modified by me for the purposes of this project, added user input for data selection, added timeout to prevent rate limiting, added various comments for clarity>
Leveraging this exising code allowed me to quickly download the data I needed from the EirGrid Smart Grid Dashboard, without having to manually download each file.

"""

#This script downloads data from the EirGrid Smart Grid Dashboard, please note that some data is only available from 2014 onwards, and a blocksize of greater than 30 may cause errors.

import datetime
import time
import requests
import os





def download(tableName,tableID):
    #Start and end dates for the download
    #YYYY-MM-DD
    startTime = datetime.date(2014, 12, 1)
    endTime = datetime.date(2024, 12, 1)#datetime.date.today()

    #Block size in days (how many days worth of data to download to each file)
    blockSize = 30

    #Max number of loops to run (safety feature to prevent infinite loops)
    maxLoops = 1000

    blockStart = startTime
    blockEnd = blockStart + datetime.timedelta(blockSize-1)

    loopCounter = 0


    linkStr = "http://smartgriddashboard.eirgrid.com/DashboardService.svc/csv?area=<tableID>&region=ALL&datefrom=<blockStart>%2000:00&dateto=<blockEnd>%2023:59"
    os.makedirs(tableName, exist_ok=True)
    savePath = os.path.join(os.getcwd() + "/"+tableName+"/")



    while (blockEnd.toordinal() < endTime.toordinal() + blockSize) and (loopCounter < maxLoops): 
        if blockEnd.toordinal() > endTime.toordinal():
            url = linkStr.replace("<blockStart>", blockStart.strftime("%d-%b-%Y")).replace("<blockEnd>", endTime.strftime("%d-%b-%Y")).replace("<tableID>", tableID)
            filename = tableName + "_" + blockStart.strftime("%Y-%m-%d") + "_" + endTime.strftime("%Y-%m-%d") + ".csv"
        else:
            url = linkStr.replace("<blockStart>", blockStart.strftime("%d-%b-%Y")).replace("<blockEnd>", blockEnd.strftime("%d-%b-%Y")).replace("<tableID>", tableID)
            filename = tableName + "_" + blockStart.strftime("%Y-%m-%d") + "_" + blockEnd.strftime("%Y-%m-%d") + ".csv"
        print("...")
        print("Downloading " + filename)
        t1 = time.time()   
        r = requests.get(url, allow_redirects=True, verify=False)    
        open(savePath + filename, "wb").write(r.content)
        print("Download completed & file written in " + "{:.2f}".format(time.time() - t1) + "s")
        
        blockStart = blockEnd + datetime.timedelta(1)
        blockEnd = blockStart + datetime.timedelta(blockSize-1)

        #Added to prevent rate limiting, adjust as necessary
        time.sleep(1)


        loopCounter += 1




selection = input("Please select the data you would like to download: \n1. Wind Generation\n2. System Demand\n3. System Generation\n4. CO2 Intensity\n""5.CO2 Emissions\n6. All (Expect very long download times)\n: ")
if selection == "1":
    tableName = "WindGeneration"
    tableID = "windActual"
    download(tableName,tableID)
elif selection == "2":
    tableName = "SystemDemand"
    tableID = "demandActual"
    download(tableName,tableID)
elif selection == "3":
    tableName = "SystemGeneration"
    tableID = "generationActual"
    download(tableName,tableID)
elif selection == "4":
    tableName = "Co2Intensity"
    tableID = "co2intensity"
    download(tableName,tableID)
elif selection == "5":
    tableName = "Co2Emissions"
    tableID = "co2emission"
    download(tableName,tableID)
elif selection == "6":
    tableName = "WindGeneration"
    tableID = "windActual"
    download(tableName,tableID)
    tableName = "SystemDemand"
    tableID = "demandActual"
    download(tableName,tableID)
    tableName = "SystemGeneration"
    tableID = "generationActual"
    download(tableName,tableID)
    tableName = "Co2Intensity"
    tableID = "co2intensity"
    download(tableName,tableID)
    tableName = "Co2Emissions"
    tableID = "co2emission"
    download(tableName,tableID)
else:
    print("Invalid selection")
    exit()




