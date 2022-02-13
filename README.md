# Microcenter Inventory Checker
Microcenter Inventory checker checks the inventory of a given item as often as the user defines. If the state of the inventory changes, the script will send the user a notification using pushsafer. This notification can be sent to any device that supports pushsafer. The user will be asked if they want to save the data to a csv file. This file will contain a history of the data the script returns. The user also has the option to set the store location to get an accurate inventory at any given microcenter location. 

## config.txt
The config file contains all of the configuration settings that can be modified by the user. This file can be modified with any text editor. If the config is invalid the user will be prompted to modify the config. The config can also be modified by running config.py. Below is a list of the configuration options and what they do. 

* refresh time - The time (in seconds) between inventory checks. This value must be greater than 60 to prevent getting blacklisted from the website. Microcenter states on their  own website that they only refresh the inventory every ten minutes. So setting this value to anything under 600 seconds is pointless.
* savecsv - A yes or no option to save the data to the historicaldata.csv file. Useful for evaluating historically inventory changes
* sendnotification - A yes or no option to send the user a notification using pushsafer. If this is set to yes, valid pushsafer credentials must be input
* pushsaferkey - The pushsafer private key for the user. This is provided in the pushsafer dashboard.
* deviceid - The device you would like have the notification sent to. This is also provided on the pushsafer dashboard.
* microcenter - This is the entire link to the product you would like to check the inventory of. Just find the product, grab the url, and paste it here
* storenumber - The store number inventory will be checked at. For a current list, run config.py

## requirements.txt
Currently the project requires:

* requests

* beautifulsoup4

* python_pushsafer


## Installation
Clone:
```
git clone https://github.com/JosephSmarsh/Microcenter-Inventory-Checker.git
```
Install dependencies:
```
pip install -r requirements.txt
```

## Running Microcenter Inventory Checker
```
python3 main.py
```
The setup is handled within main.py. Running main.py will validate the config settings provided. If the configuration is invalid, the user will be prompted to correct the config and config.py will be started. config.py validates all the config values and provides a store list if a valid one hasnt been provided. 
