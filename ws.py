from bs4 import BeautifulSoup
import requests
from csv import writer

response = requests.get('https://www.amazon.co.uk')

soup = BeautifulSoup(response.text, 'html.parser')
    
print(soup)