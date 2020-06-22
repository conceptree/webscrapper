from bs4 import BeautifulSoup
import requests
from csv import writer
import time

pages = ["https://www.amazon.co.uk","https://www.amazon.es","https://www.amazon.de"]
headers = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}

def start():
    print("The stores available are:\n 1) Amazon UK\n 2) Amazon ES \n 3) Amazon DE")
    option = input("On what store do you want to scrap? (e.g 1, 2 or 3)\n")
    if option.isdigit():
        URL = pages[int(option)-1]
        search_keyword = input("For what product do you want to scrap for?\n")
        scrap(URL, search_keyword)
    else:
        print("Please enter a valid option digit!\n")
        time.sleep(2)
        start()
        
def scrap(URL, search_keyword):
    if search_keyword != "":
        URL = URL+"/s?k="+search_keyword
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        buildData(soup)
    else:
        print("A search keyword is necessary!\n")
        time.sleep(2)
        start()

def buildData(soup):
    search_results = soup.find_all(attrs={"data-component-type": "s-search-result"})
    with open("amazon_results.csv", "w") as csv_file:
        csv_writer = writer(csv_file)
        headers = ["Name", "Ratting", "Customers", "Price"]
        csv_writer.writerow(headers)
        for result in search_results :
            name = result.find("span", class_="a-text-normal").getText()
            ratting = result.find("span", class_="a-icon-alt").getText()
            customers = result.find("span", class_="a-size-base").getText()
            price = result.find("span", class_="a-price", attrs={"data-a-color":"base"})
            price =  price.find("span", class_="a-offscreen").getText() if price else ""
            csv_writer.writerow([name,ratting,customers,price])

start()