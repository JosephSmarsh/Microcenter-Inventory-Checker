# STD library
from bs4 import BeautifulSoup
from datetime import datetime
import requests
# 3rd Party
from pushsafer import Client
# Local
from config import createconfigobj

# Create config object once
config = createconfigobj()

# Base link used for product name, and locations (Dont need to refresh link everytime called. Just once at import.
result = BeautifulSoup(requests.get(config.productlink).content, "html.parser")


# Check the inventory of Raspberry pis, return 'Sold out' or the number of raspberry pis in stock
def checkinventory():
    # Dynamic link used for inventory, needs to be refreshed everytime function is called
    inventory = BeautifulSoup(requests.get(config.productlink + '?storeid=' + config.storenumber).content, "html.parser")\
        .find("p", class_="inventory").text.strip()
    if "SOLD OUT" in inventory:
        return 'Sold Out'
    else:
        return inventory.split(" ")[0] + " in stock"


# Return Product name
def checkproductname():
    product = result.find(class_='summary').select('span')
    return product[1].text.replace(product[2].text, "")


# Check all current locations, return an array of locations with store #, state, and city
def checklocations():
    locations = result.findAll(class_='dropdown-item')
    # List of a list containing store #, State, and City
    storelist = []
    # Loop until second to last result - Last result is online shopping (Raspberry Pi not available to be shipped)
    for i in range(len(locations) - 1):
        # Format results and append to the list
        storelist.append(str(locations[i]).split('storeid=')[1]
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
