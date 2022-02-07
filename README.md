# piScraper
piScraper gathers current raspberry pi inventory from local and national stores and checks for changes in that inventory. If there is a change in the status of the inventory, piScraper can send a notification using pushsafer. As well, piScraper has the ability to save the output of the script to a local CSV file. 

## Config.ini
Config.ini contains three configuration settings: refreshtime, savecsv, and sendnotification. By defaul they are set to 300 seconds, y, and y. The script will check inventory every 5 minutes (300 sec), save to a local CSV file, and it will send a notification to a device using pushsafer. These values can all be changed, the refresh time must only be changed to an int > 60 sec to prevent constant refreshes.

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
