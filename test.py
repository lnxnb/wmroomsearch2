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

#Get open seats
    emptyset = []
    titleSet = rowChild.findAll('td',{'data-property':'status'})
    for openSeatChild in titleSet:
        openSeat = openSeatChild.findAll('span')
        for spanChild in openSeat:
            emptyset += spanChild.contents
    print(emptyset)