# STD library
from bs4 import BeautifulSoup
from datetime import datetime
import requests
# 3rd Party
from pushsafer import Client
# Local
from setup import createconfigobj

# Create config object once
config = createconfigobj()
# Check the inventory of Raspberry pis, return 'Sold out' or the number of raspberry pis in stock
def checkinventory():
    result = BeautifulSoup(requests.get(config.productlink).content, "html.parser")\
        .find("p", class_="inventory").text.strip()
    if "SOLD OUT" in result:
        return 'Sold Out'
    else:
        return result.split(" ")[0] + " in stock"


# Return Product name
def checkproductname():
    result = BeautifulSoup(requests.get(config.productlink).content, "html.parser")\
        .find(class_='summary').select('span')
    return result[1].text.replace(result[2].text, "")


# Check all current locations, return an array of locations with store #, state, and city
def checklocations():
    result = BeautifulSoup(requests.get(config.productlink).content, "html.parser")\
        .findAll(class_='dropdown-item')
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


# Send notification using pushsafer.
# Message - Message to send.
# Title - Tile of message
def sendnotification(message, title):
    client = Client(config.pushsaferkey)
    device = config.deviceid

    client.send_message(message, title, device)


# Return formatted time: H:M:S | M/D/Y
def gettime():
    return datetime.now().strftime("%H:%M:%S | %m/%d/%Y")


# Save data to historicaldata.csv.
# data - Data to write to csv.
# i - counter used for id#
def savedata(data, i):
    with open('historicaldata.csv', 'a') as f:
        f.write("\n" + str(i) + ", " + data.replace(" | ", ", "))
        f.close()


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
