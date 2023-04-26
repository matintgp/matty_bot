import requests
import sys
import json


def wheather():
    response = requests.request("GET",
                            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Iran%20Tehran?unitGroup=metric&include=days%2Ccurrent%2Chours&key=DSBAM534RZZMWS6DQZPM3PHYM&contentType=json")
    if response.status_code != 200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit()

    # Parse the results as JSON
    jsonData = response.json()
    daysdata = jsonData["days"]
    #  ** daysdata is a list **
    hoursdata= (daysdata[1])["hours"] #now housrsdata is dict

    global newdata

    newdata=f'''Tomorrow is {(daysdata[1])["icon"]}
    {(daysdata[1])["datetime"]},{(hoursdata[1])["datetime"]}
    {jsonData["timezone"]}
    minimum temperature: {(daysdata[1])['tempmin']}C
    maximum temperature: {(daysdata[1])['tempmax']}C
    Today's average temperature: {(daysdata[1])['temp']}C    
    Current temperature: {(hoursdata[1])["temp"]}C
    description: {(daysdata[1])["description"]}
    HAVE GOOD DAY :)
    '''
    return newdata


wheather()

