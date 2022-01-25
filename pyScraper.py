import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime


def checkinventory(ttr):
    while True:
        microcenter = requests.get('https://www.microcenter.com/product/621439/raspberry-pi-4-model-b-2gb-ddr4')
        soup = BeautifulSoup(microcenter.content, "html.parser")
        result = soup.find("p", class_="inventory").text.strip()

        currenttime = datetime.now().time()
        print(result.strip() + currenttime.strftime(" %H:%M:%S"))
        time.sleep(ttr)


def main():
    refreshtime = input("Enter page refresh time (sec): ")
    checkinventory(int(refreshtime))


if __name__ == "__main__":
    main()

