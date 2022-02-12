# STD library, used to loop for given time
import time
# Local imports
import inventorycheck
from inventorycheck import (checkinventory, sendnotification, gettime, savedata)
from config import createconfigobj


def main():
    try:
        # Create config object
        config = createconfigobj()
        # Print Valid Config at start of script if config is valid
        validconfig = config.isvalidconfig() is True
        if validconfig:
            print('Valid Config')
            print('Checking inventory for: ' + inventorycheck.checkproductname())
        if config.savecsv == 'y':
            config.setcsv()
        # Counter used for ID# in historicaldata.csv
        counter = 1
        # While config settings are valid
        while validconfig:

            # Initial State used to check inventory on startup for comparison checking for change
            initialstate = checkinventory()

            # If config SAVE == y, save to file as well as console output
            if config.savecsv == 'y':
                # Check inventory ONCE at start of while loop
                currentstate = checkinventory()
                output = currentstate + " | " + gettime()
                print(output)
                savedata(output, counter)
                counter += 1

                # If there is a change in state and notifications are on, send notification, update initial state
                if config.sendnotification == "y" and currentstate != initialstate:
                    sendnotification(currentstate, "Inventory Change!")
                    # Set initial state to the new current state
                    initialstate = currentstate

                # Sleep while loop for refresh time defined in CONFIG.ini

            # if config SAVE == 'n', only output to console
            if config.savecsv == 'n':
                currentstate = checkinventory()
                output = currentstate + " | " + gettime()
                print(output)
                counter += 1

                # If there is a change in state and notifications are on, send notification, update initial state
                if config.sendnotification == "y" and currentstate != initialstate:
                    sendnotification(currentstate, "Inventory Change!")
                    # Set initial state to the new current state
                    initialstate = currentstate

            # Sleep while loop for refresh time defined in CONFIG.ini
            time.sleep(int(config.refreshtime))

        # If config is invalid, ask to launch config.py to fix config
        else:
            print('Invalid Configuration')
            if input('Edit config now? (y/n): ').lower() == 'y':
                print('Launching config.py...')
                time.sleep(2)
                exec(open('config.py').read())

    finally:
        pass


if __name__ == "__main__":
    main()
