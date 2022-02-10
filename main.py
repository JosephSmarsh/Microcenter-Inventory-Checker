from inventorycheck import checkinventory
from inventorycheck import sendnotification
from inventorycheck import gettime
from inventorycheck import savedata
from setup import createconfigobj
import time


def main():
    config = createconfigobj()
    try:
        while config.isvalidconfig() is True:
            refresh = config.refreshtime
            save = config.savecsv
            notification = config.sendnotification

            # Initial State used to check inventory on startup for comparison checking for change
            initialstate = checkinventory()
            # Counter used for ID# in historicaldata.csv
            counter = 1

            # If config SAVE == y, save to file as well as console output
            if save == 'y':
                # Check inventory ONCE at start of while loop
                currentstate = checkinventory()
                output = currentstate + " | " + gettime()
                print(output)
                savedata(output, counter)
                counter += 1

                # If there is a change in state and notifications are on, send notification, update initial state
                if notification == "y" and currentstate != initialstate:
                    sendnotification(currentstate, "Inventory Change!")
                    # Set initial state to the new current state
                    initialstate = currentstate

                # Sleep while loop for refresh time defined in CONFIG.ini

            # if config SAVE == 'n', only output to console
            if save == 'n':
                currentstate = checkinventory()
                output = currentstate + " | " + gettime()
                print(output)
                counter += 1

                # If there is a change in state and notifications are on, send notification, update initial state
                if notification == "y" and currentstate != initialstate:
                    sendnotification(currentstate, "Inventory Change!")
                    # Set initial state to the new current state
                    initialstate = currentstate

            # Sleep while loop for refresh time defined in CONFIG.ini
            time.sleep(int(refresh))

        # If config is invalid, print:
        else:
            print('Invalid Configuration')
            print('Edit config or run setup.py')


        """ - Used for Config Class with config file 
        newconfig = Config("", "", "")
        initialstate = checkinventory()
        counter = 1

        newconfig.setupenv()

        while newconfig.save == 'y':
            output = checkinventory() + " | " + gettime()
            print(output)
            savedata(output, counter)
            counter += 1

            # If notifications are on and inital inventory changed with updated inventory, send notification
            if newconfig.notification == 'y' and checkinventory() != initialstate:
                sendnotification(checkinventory(), 'Stock Change!')
                initialstate = checkinventory()

            time.sleep(newconfig.refresh)

        while newconfig.save == 'n':
            output = checkinventory() + " | " + gettime()
            print(output)
            time.sleep(newconfig.refresh)
        """
    except ConnectionError:
        print(ConnectionError)
        pass
    finally:
        pass


if __name__ == "__main__":
    main()
