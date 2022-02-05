from pifinder import checkinventory
from pifinder import sendnotification
from pifinder import gettime
from pifinder import savedata
from pifinder import setupscript
import time


def main():
    try:
        setup = setupscript()
        ttr = setup[0]
        save = setup[1]
        counter = 1

        while save == 'y':
            output = checkinventory() + " | " + gettime()
            print(output)
            savedata(output, counter)
            counter += 1
            time.sleep(ttr)

        while save == 'n':
            output = checkinventory() + " | " + gettime()
            print(output)
            time.sleep(ttr)

    finally:
        breakpoint(print('There was an error with main setupscript() call'), main())


if __name__ == "__main__":
    main()