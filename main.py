from pifinder import checkinventory
from pifinder import sendnotification
from pifinder import gettime
from pifinder import savedata
from pifinder import setupscript
import time


def main():
    try:
        # Read CONFIG file and assign refresh time, save to csv, and send notification values
        # IF save == 'y', setupscript() creates and writes the first line to the historicaldata.csv
        setupscript()
        refresh = setupscript()[0]
        save = setupscript()[1]
        notification = setupscript()[2]

        # Initial State used to check inventory on startup for comparison checking for change
        initialstate = checkinventory()
        # Counter used for ID# in historicaldata.csv
        counter = 1

        # If config SAVE == y, save to file as well as console output
        while save == 'y':
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
            time.sleep(refresh)

        # if config SAVE == 'n', only output to console
        while save == 'n':
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
            time.sleep(refresh)


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

    finally:
        pass


if __name__ == "__main__":
    main()
