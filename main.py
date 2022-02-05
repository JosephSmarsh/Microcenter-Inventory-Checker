import pifinder
import Constants


def main():
    refreshtime = input("Enter page refresh time (sec): ")
    pifinder.checkinventory(int(refreshtime))


if __name__ == "__main__":
    main()