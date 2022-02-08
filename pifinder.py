import requests
from bs4 import BeautifulSoup
from datetime import datetime
import Constants
from pushsafer import Client
from configparser import ConfigParser


def checkinventory():
    result = BeautifulSoup(requests.get(Constants.microcenter).content, "html.parser")\
        .find("p", class_="inventory").text.strip()
    if "SOLD OUT" in result:
        return 'Sold Out'
    else:
        return int(result)


def checklocations():
    # Get page content, parse it, and find the dropdown menu
    content = requests.get('https://www.microcenter.com/product/621439/raspberry-pi-4-model-b---2gb-ddr4?').content
    soup = BeautifulSoup(content, "html.parser")
    result = soup.findAll(class_='dropdown-item')
    # List of a list containing store #, State, and City
    storelist = []
    # Loop until second to last result - Last result is online shopping (Raspberry Pi not available to be shipped)
    for i in range(len(result) - 1):
        # Format results and append to the list
        storelist.append(str(result[i]).split('storeid=')[1]
                         .replace(' ', '')
                         .replace('">', ", ")
                         .replace("-", ", ")
                         .replace("</a>", ""))
    return storelist


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
""" - Use for Config Class with config file 
class Config:
    def __init__(self, refresh, save, notification):
        self.refresh = refresh
        self.save = save
        self.notification = notification

    def setupenv(self):
        config = ConfigParser()
        config.read('config.ini')

        self.refresh = config.getint('main', 'refreshtime')
        self.save = config.get('main', 'savecsv')
        self.notification = config.get('main', 'sendnotification')

        if self.save == "y":
            with open("historicaldata.csv", "w") as f:
                f.write("ID, INVENTORY, TIME, DATE")
                f.close()
"""
