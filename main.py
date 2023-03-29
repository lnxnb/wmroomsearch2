import bs4 as bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import re

#Create Dataframe
table = pd.DataFrame()

#Import HTML file
with open('html.html', 'r') as f:

    contents = f.read()

    soup = bs(contents, 'html.parser')

#Get outermost tag containing class information 
first = soup.findAll('div',{"class":'ui-widget ui-layout-center overflow-table ui-layout-pane ui-layout-pane-center'})
#Get list of titles
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':"courseTitle"})
    for child in titleSet:
        emptyset += child.find('a',{'class':'section-details-link'}).contents
    table['Class Title'] = emptyset

#Get list of subjects
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'subjectDescription'})
    for child in titleSet:
        emptyset += child.contents
    table['Subject'] = emptyset

#Get list of course numbers
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'courseNumber'})
    for child in titleSet:
        emptyset += child.contents
    table['Course Number'] = emptyset

#Get list of section numbers
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'sequenceNumber'})
    for child in titleSet:
        emptyset += child.contents
    table['Section Number'] = emptyset

#Get list of credit hours
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'creditHours'})
    for child in titleSet:
        emptyset += child.contents
    table['Credit Hours'] = emptyset

#Get list of CRNS
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'courseReferenceNumber'})
    for child in titleSet:
        emptyset += child.contents
    table['CRN'] = emptyset

#Get list of terms
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'term'})
    for child in titleSet:
        emptyset += child.contents
    table['Term'] = emptyset

#Get list of instructors
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'instructor'})
    for child in titleSet:
        names = child.findAll('a',{'class':'email'})
        if len(names) > 1:
            names = names[:-1]
        for child in names:
            emptyset += child.contents
    table['Instructor'] = emptyset

#Get list of meeting days and times
for child in first:
    emptydayset = []
    emptytimeset = []
    titleSet = child.findAll('td',{'data-property':'meetingTime'})
    for child in titleSet:
        emptydayset += [re.findall("Monday|Tuesday|Wednesday|Thursday|Friday",child['title'])]
        spans = child.findAll('span')
        for child in spans:
            if re.search("PM|AM",child.text):
                if re.search("[0-9]",child.text):
                    emptytimeset.append(child.text)
            elif re.search("-",child.text):
                emptytimeset.append("")
    table['Meeting Days'] = emptydayset
    table['Meeting Times'] = emptytimeset

#Get list of buildings and room numbers
for child in first:
    emptyhallset = []
    emptyroomset = []
    titleSet = child.findAll('td',{'data-property':'meetingTime'})
    for child in titleSet:
        spans = child.findAll('span')
        for child in spans:
            if re.search("Building",child.text):
                if child.text != "Building: ":
                    emptyhallset.append(child.text[11:])
            if re.search("Room" ,child.text):
                if child.text != "Room: ":
                    emptyroomset.append(child.text[6:])
    table['Hall'] = emptyhallset
    table['Room Number'] = emptyroomset


#Get list of campuses
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'campus'})
    for child in titleSet:
        emptyset += child.contents
    table['Campus'] = emptyset


#Get list of open seats
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'status'})
    for child in titleSet:
        openSet = child.findAll('span')
        for child in openSet:
            emptyset += child.contents
    table['Open Seats'] = emptyset

#Get list of total seats
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'status'})
    for child in titleSet:
        totSeatsList = []
        totSeatsStr = re.findall('of .. seats remain|of . seats remain', str(child))
        if len(totSeatsStr) > 1:
            totSeatsStr = totSeatsStr[0] 
        totSeatsNum = ''
        for c in str(totSeatsStr):
            if c.isdigit():
                totSeatsNum += c
        totSeatsList.append(totSeatsNum)
        emptyset += totSeatsList

    table['Total Seats'] = emptyset

#Get list of attributes
for child in first:
    emptyset = []
    titleSet = child.findAll('td',{'data-property':'attribute'})
    for child in titleSet:
        attributes = child.findAll('span')
        emptyset.append(attributes)
    table['Attributes'] = emptyset

print(table)


#with open('test.txt', 'w') as f:
#    f.write(str(first))