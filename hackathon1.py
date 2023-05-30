import requests
from bs4 import BeautifulSoup
import csv
import re

URL = 'https://www.mashina.kg/search/all/'

def csv_mashina(data):
    with open('mashina.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['image'], data['price'], data['title'], data['description']])

def mashina_html(link):
    request = requests.get(link)
    return request.text

def get_data(html):
    sp = BeautifulSoup(html,'lxml')
    list_cars = sp.find_all('div', class_="list-item list-label")
   
    for car in list_cars:
        image = car.find('img', class_='lazy-image').get('data-src') if car.find('img', class_='lazy-image') != None else 'None'
        title = car.find('h2', class_="name").text.strip()
        price = car.find('strong').text
        description = re.sub(r'\s+', ' ', car.find('div', class_="block info-wrapper item-info-wrapper").text).strip()
        dict_ = {'image':image,'title':title, 'price':price, 'description':description}
        csv_mashina(dict_)    

def main():
    count = 1
    for i in range(1,10):
        url = f'https://www.mashina.kg/search/all/?page={str(count)}'
        get_data(mashina_html(url))
        count += 20
main()

