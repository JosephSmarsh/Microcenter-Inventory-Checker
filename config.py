# Used to validate productlink
import requests
import inventorycheck


# Contains all config values
class Config:
    def __init__(self, refreshtime, savecsv, sendnotification, pushsaferkey, deviceid, productlink, storenumber):
        self.refreshtime = refreshtime
        self.savecsv = savecsv
        self.sendnotification = sendnotification
        self.pushsaferkey = pushsaferkey
        self.deviceid = deviceid
        self.productlink = productlink
        self.storenumber = storenumber

    def isvalidstore(self):
        storenumbers = []
        for i in range(len(inventorycheck.checklocations())):
            storenumbers.append(inventorycheck.checklocations()[i].split(',')[0])

        if self.storenumber in storenumbers:
            return True
        else:
            return False

    # Check link contains base microcenter link, and link works
    def isvalidlink(self):
        if 'https://www.microcenter.com/product/' in self.productlink:
            if requests.get(self.productlink).status_code == 200:
                return True
            else:
                return False
        else:
            return False

    # Check to validate if a y or n answer only contains y or n
    def isvalidsavecsv(self):
        if self.savecsv.lower() == 'y' or self.savecsv.lower() == 'n':
            return True
        else:
            return False

    # Check sendnotification is only y or n
    def isvalidsendnotification(self):
        if self.sendnotification.lower() == 'y' or self.sendnotification.lower() == 'n':
            return True
        else:
            return False

    # If send noticiation is y, ensure pushsaferkey and deviceid have values that work
    # Store values in pushsafervalues.txt
    # Check for valid values
    def isvalidpushsafer(self):
        if self.sendnotification.lower() == 'y':
            try:
                with open('pushsafervalues.txt', 'r') as f:
                    values = f.readline().split(',')
                    f.close()
                    if self.pushsaferkey == values[0] and self.deviceid == values[1]:
                        return True
                    else:
                        return False
            except OSError:
                try:
                    inventorycheck.sendnotification('Test Notification', 'Test Notification')
                    with open('pushsafervalues.txt', 'w') as f:
                        f.write(self.pushsaferkey + ',' + self.deviceid)
                        f.close()
                    return True
                except:
                    return False
        else:
            return True

    # Check refresh time is an int greater than 59
    def isvalidrefresh(self):
        try:
            if int(self.refreshtime) > 59:
                return True
            else:
                return False
        except ValueError as e:
            return False

    # Set initial csv file, Writes over any existing file
    def setcsv(self):
        if self.savecsv.lower() == 'y':
            with open('historicaldata.csv', 'w') as f:
                f.write('ID, INVENTORY, TIME, DATE')
                f.close()

    @staticmethod
    # Open config.txt, print the contents line by line
    def printconfig():
        print('________________________________________________________________________')
        print('                         Current config                                 ')
        print('________________________________________________________________________')
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                print(lines[i].strip())
            f.close()
        print('________________________________________________________________________')

    @staticmethod
    def printlocations():
        print('________________________________________________________________________')
        print('Store#, State, City')
        print('________________________________________________________________________')
        for i in range(len(inventorycheck.checklocations())):
            print(inventorycheck.checklocations()[i])
        print('________________________________________________________________________')

    # Validate each item in config, print valid or invalid, then validate entire config and print valid or invalid
    def printvalidation(self):
        if self.isvalidrefresh() is True:
            print('refreshtime          VALID')
        else:
            print('refreshtime          INVALID')

        if self.isvalidsavecsv() is True:
            print('savecsv              VALID')
        else:
            print('savecsv              INVALID')

        if self.isvalidsendnotification() is True:
            print('sendnotification     VALID')
        else:
            print('sendnotification     INVALID')

        if self.isvalidpushsafer() is True:
            print('pushsaferkey         VALID')
            print('deviceid             VALID')
        else:
            print('pushsaferkey         INVALID')
            print('deviceid             INVALID')

        if self.isvalidlink() is True:
            print('microcenter          VALID')
        else:
            print('microcenter          INVALID')

        if self.isvalidstore() is True:
            print('storenumber          VALID')
        else:
            print('storenumber          INVALID')

        print('________________________________________________________________________')

        if self.isvalidconfig() is True:
            print('Current config       VALID')
        # If config is invalid, print invalid
        else:
            print('Current config       INVALID')

        print('________________________________________________________________________')

    # If all validations are true, config is valid (True), else config is invalid (False)
    def isvalidconfig(self):
        if self.isvalidrefresh() and self.isvalidlink() and \
                self.isvalidsavecsv() and self.isvalidpushsafer() and \
                self.isvalidsendnotification() and self.isvalidstore() is True:
            return True
        else:
            return False

    @staticmethod
    # Read current config.txt file, ask for input for value, write file line by line
    def buildconfig():
        # Open config and add lines to lines
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            f.close()
        # Ask user for input, edit line to include new input
        for i in range(len(lines)):
            lines[i] = lines[i].strip().split('=')[0] + '= ' + input('Input ' + str(lines[i].split(' ')[0]) + ': ')
        # Write new lines variable to config.txt
        with open('config.txt', 'w') as f:
            for i in range(len(lines)):
                f.write(lines[i].strip() + '\n')
            f.close()


# Creates a config object based on config.txt
def createconfigobj():
    with open('config.txt', 'r') as f:
        variables = [line.strip() for line in f]
        f.close()
    refreshtime = variables[0].split('=')[1].replace(' ', '')
    savecsv = variables[1].split('=')[1].replace(' ', '')
    sendnotification = variables[2].split('=')[1].replace(' ', '')
    pushsaferkey = variables[3].split('=')[1].replace(' ', '')
    deviceid = variables[4].split('=')[1].replace(' ', '')
    productlink = variables[5].split('=')[1].replace(' ', '')
    storenumber = variables[6].split('=')[1].replace(' ', '')

    config = Config(refreshtime, savecsv, sendnotification, pushsaferkey, deviceid, productlink, storenumber)
    return config


def main():
    # Initialize config object: happens everytime main is started
    config = createconfigobj()
    # Print current config
    config.printconfig()
    # Print current validation
    config.printvalidation()
    # If user wants to change config, run buildconfig, then loop main again
    if input('Edit config (y/n): ').lower() == 'y':
        if config.isvalidstore() is False and input('See store list? (y/n): ').lower() == 'y':
            config.printlocations()
            config.buildconfig()
            main()
        else:
            config.buildconfig()
            main()
    # Else escape script
    else:
        print('Closing config editor...')


if __name__ == "__main__":
    main()
