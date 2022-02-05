import requests
from bs4 import BeautifulSoup
from datetime import datetime
import Constants
from pushsafer import Client
from configparser import ConfigParser


def checkinventory():
    result = BeautifulSoup(requests.get(Constants.microcenter).content, "html.parser")\
        .find("p", class_="inventory").text.strip()
    if result == "SOLD OUT at Denver Store":
        return 'Sold Out'
    else:
        return int(result)


def sendnotification(message, title):
    client = Client(Constants.pushsaferkey)
    device = Constants.deviceid

    client.send_message(message, title, device)


def gettime():
    return datetime.now().strftime("%H:%M:%S | %m/%d/%Y")


def savedata(data, i):
    with open('historicaldata.csv', 'a') as f:
        f.write("\n" + str(i) + ", " + data.replace(" | ", ", "))
        f.close()

def setupscript():
    config = ConfigParser()
    config.read('config.ini')

    ttr = config.getint('main', 'refreshtime')
    savecsv = config.get('main', 'savecsv')
    notification = config.get('main', 'sendnotification')

    if savecsv == "y":
        with open("historicaldata.csv", "w") as f:
            f.write("ID, INVENTORY, TIME, DATE")
            f.close()

    return ttr, savecsv, notification

""" - Use for no config file setup 
def setupscript():
    while True:
        ttr = int(input("Enter website refresh time (sec): "))
        if ttr < 60:
            print("Enter valid refresh time (>60 sec)")
            continue
        else:
            while True:
                savedata = input("Save data to historicaldata.csv (Y/N): ").lower()
                if savedata == "n":
                    break
                elif savedata == "y":
                    with open("historicaldata.csv", "w") as f:
                        f.write("ID, INVENTORY, TIME, DATE")
                        f.close()
                    break
                else:
                    print("Enter a valid response")
                    continue
            return ttr, savedata
"""
