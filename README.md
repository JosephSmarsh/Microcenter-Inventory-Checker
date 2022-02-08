# Raspberry Pi Inventory Checker
Raspberry Pi Inventory Checker gathers current raspberry pi inventory from local and national stores and checks for changes in that inventory. If there is a change in the status of the inventory, Raspberry Pi Inventory Checker can send a notification using pushsafer. As well, piScraper has the ability to save the output of the script to a local CSV file. 

## config.ini
Config.ini contains three configuration settings: refreshtime, savecsv, and sendnotification. By default they are set to 300 seconds, y, and y. The script will check inventory every 5 minutes (300 sec), save to a local CSV file, and it will send a notification to a device using pushsafer. These values can all be changed, the refresh time must only be changed to an int > 60 sec to prevent constant refreshes.

## Constants.py
Currently not included in the project is the Constants.py file. This file is required to run the script properly. It containts three variabls: pushsaferkey, deviceid, and microcenter (soon to be an array of links). 
```python
pushsaferkey = ''
deviceid = ''
microcenter = ''
```
pushsaferkey: Acquired when you register for [pushsafer](https://www.pushsafer.com/ "Pushsafer Registration"). 

deviceid: Acquired when a device is registered to your pushsafer account

microcenter: The link to the microcenter page (To be made an array of national links and local stores)

## requirements.txt
Currently the project requires:

* requests

* beautifulsoup4

* python_pushsafer


## Installation
Clone:
```
git clone https://github.com/JosephSmarsh/Raspberry-Pi-Inventory-Checker.git
```
Install dependencies:
```
pip install -r requirements.txt
```
Navigate to the installation directory, add Constants.py with your credentials. 

Then run the script: 
```
python main.py
```
