"""
Accesses the most streamed song from spotify charts, then prints it out per date
"""

import requests
from bs4 import BeautifulSoup

def goBackOneDay(date):
    """
    when given a date, returns the previous day
    yyyy-mm-dd is the form of date
    0123456789
    """
    
    monthList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    day = int(date[8:10])
    month = int(date[5:7])
    year = int(date[0:4])
    day -= 1
    if day == 0:
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        day = monthList[month-1]
        if month == 2 and year%4 == 0:
            #if a leap year
            day = 29

    return f"{year:04d}-{month:02d}-{day:02d}"
    
    
def findToppers():
    """
    Main method of program
    """
    
    date = "2020-07-14" #current date
    URL = "https://spotifycharts.com/regional/global/daily/"
    page = requests.get(URL+date)
    while page != "<Response [404]>":
        #get the number one
        topper = BeautifulSoup(page.content, "html.parser").find_all('tr')[1]
        #turns the raw HTML into a BeautifulSoup object, then finds a list of the songs
        #index 0 is the header, so index 1 is the most-streamed song
        streams = int(topper.find("td", class_="chart-table-streams").
                      text.strip().replace(",", ""))
        #In the HTML of the song, find the <td> that is marked with streams, get only the text instead of the HTML, remove whitespace, then remove commas
        print(f"{date} {streams}")
          
        #make sure the loop doesn't run forever
        date = goBackOneDay(date)
        page = requests.get(URL+date)
