import bs4 as bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import re

progress = 0
#Create Dataframe
mainTable = pd.DataFrame(columns=['Course Title','Subject','Course Number','Section Number','Credit Hours','CRN','Term','Instructor(s)','Meeting Days','Meeting Times','Hall','Room Number','Campus','Open Seats','Total Seats','Attributes'])

#Import HTML file
with open('html.html', 'r') as f:

    contents = f.read()

    soup = bs(contents, 'html.parser')

#Get list of rows containing class information
row = soup.findAll('tr')

#Loop through rows
for rowChild in row:
    print(progress)
    newRow = pd.DataFrame(columns=['Course Title','Subject','Course Number','Section Number','Credit Hours','CRN','Term','Instructor(s)','Meeting Days','Meeting Times','Hall','Room Number','Campus','Open Seats','Total Seats','Attributes'])
    
    #Get title
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':"courseTitle"})
    for titleChild in titleSet:
        emptyset += titleChild.find('a',{'class':'section-details-link'}).contents
    newRow['Course Title'] = emptyset
    
    #Get subject
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'subjectDescription'})
    for subjectChild in titleSet:
        emptyset += subjectChild.contents
    newRow['Subject'] = emptyset

    #Get CRN
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'courseNumber'})
    for courseNumberChild in titleSet:
        emptyset += courseNumberChild.contents
    newRow['Course Number'] = emptyset

    #Get section number
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'sequenceNumber'})
    for sectionChild in titleSet:
        emptyset += sectionChild.contents
    newRow['Section Number'] = emptyset

    #Get credit hours
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'creditHours'})
    for creditChild in titleSet:
        emptyset += creditChild.contents
    newRow['Credit Hours'] = emptyset

    #Get CRN
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'courseReferenceNumber'})
    for CRNChild in titleSet:
        emptyset += CRNChild.contents
    newRow['CRN'] = emptyset

    #Get term
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'term'})
    for termChild in titleSet:
        emptyset += termChild.contents
    newRow['Term'] = emptyset

    #Get instructors
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'instructor'})
    for instructorChild in titleSet:
        subset = []
        names = instructorChild.findAll('a',{'class':'email'})
        if len(names) > 1:
            for nameChild in names:
                subset.append(nameChild.contents)
                if len(subset) == len(names):
                    emptyset.append(subset)
        elif len(names) == 0 :
            emptyset.append('None')
        else:
            for nameChild in names:
                emptyset.append(nameChild.contents)
    newRow['Instructor(s)'] = emptyset

    #Get list of meeting days and times
    emptydayset = []
    emptytimeset = []
    titleSet = rowChild.findAll('td',{'data-property':'meetingTime'})
    for timeChild in titleSet:
        tempset = []
        if len([*re.findall("SMTWTFS",timeChild['title'])]) > 1:
            dayList = timeChild['title'].split('SMTWTFS')
            for i in dayList:
                dayList2 = (i.split("2023"))
                for i in dayList2:
                    if re.match("Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday",i):
                        tempset.append(re.findall("Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday",i))
            emptydayset.append(tempset)
        else:
            emptydayset.append(re.findall("Monday|Tuesday|Wednesday|Thursday|Friday",timeChild['title']))
        
        timeSpans = timeChild['title']
        if len([*re.findall("PM|AM",timeSpans)]) > 2:
            emptytimeset.append(re.findall("[0-9][0-9]:[0-9][0-9]  .. - [0-9][0-9]:[0-9][0-9]  ..",timeSpans))
        else:
            emptytimeset.append(re.findall("[0-9][0-9]:[0-9][0-9]  .. - [0-9][0-9]:[0-9][0-9]  ..",timeSpans))
                
    newRow['Meeting Days'] = emptydayset
    newRow['Meeting Times'] = emptytimeset

    #Get building and room number
    emptyhallset = []
    emptyroomset = []
    titleSet = rowChild.findAll('td',{'data-property':'meetingTime'})
    for buildingChild in titleSet:
        building = re.findall(r'Building:\s+(.*?)\s+Room:', buildingChild['title'])
        emptyhallset.append(building)
        
        room = re.findall(r'Room:\s+(.*?)\s+Start Date:', buildingChild['title'])
        emptyroomset.append(room)
        
    newRow['Hall'] = emptyhallset
    newRow['Room Number'] = emptyroomset

    #Get campus
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'campus'})
    for campusChild in titleSet:
        emptyset += campusChild.contents
    newRow['Campus'] = emptyset

    #Get open seats
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'status'})
    for openSeatChild in titleSet:
        openSeat = openSeatChild.findAll('span')
        for spanChild in openSeat:
            emptyset += spanChild.contents
    newRow['Open Seats'] = emptyset

    #Get total seats
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'status'})
    for totalSeatChild in titleSet:
        totSeatsList = []
        totSeatsStr = re.findall('of .. seats remain|of . seats remain', str(totalSeatChild))
        if len(totSeatsStr) > 1:
            totSeatsStr = totSeatsStr[0] 
        totSeatsNum = ''
        for c in str(totSeatsStr):
            if c.isdigit():
                totSeatsNum += c
        totSeatsList.append(totSeatsNum)
        emptyset += totSeatsList

    newRow['Total Seats'] = emptyset

    #Get attributes
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'attribute'})
    for attributeChild in titleSet:
        attributes = attributeChild.findAll('span')
        emptyset.append(attributes)
    newRow['Attributes'] = emptyset
    mainTable = pd.concat([mainTable,newRow])
    progress += 1

mainTable.to_csv('full.csv')