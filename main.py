import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from tabulate import tabulate
import json


def get_weather_data():
    url = 'https://world-weather.info/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Cookie': 'celsius=1'}
    response = requests.get(url, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        resorts = soup.find('div', id='resorts')
        # print(type(resorts))
        re_cities = r'">([\w\s]+)<\/a><span>'
        cities = re.findall(re_cities, str(resorts))
        re_temps = r'<span>(\+\d+|-\d+)<span'
        temps = re.findall(re_temps, str(resorts))
        tepms_int = [int(temp) for temp in temps]
        conditions_tag = resorts.find_all('span', class_='tooltip')
        conditions = [condition.get('title') for condition in conditions_tag]
        data = zip(cities, tepms_int, conditions)
        # print(list(data))
        return list(data)

        # print(resorts)
    else:
        print('Not OK.')


def data_txt(data):
    if data:
        today = date.today().strftime('%b-%d-%Y')
        with open('output.txt', 'w', encoding="utf-8") as file:
            file.write('Popular Cities Forecast' + '\n')
            file.write(today + '\n')
            file.write('=' * 20 + '\n')
            table = tabulate(data, headers=['City', 'Temperture', 'Condition'], tablefmt='mixed_outline')
            file.write(table)
    else:
        print('No Data')


def data_json(data):
    if data:
        today = date.today().strftime('%b-%d-%Y')
        cities = [{'city': city, 'temp': temp, 'condition': condition} for city, temp, condition in data]
        data_js = {'title': 'Popular Cities Forecast', 'date': today, 'Cities': cities}
        with open('output.json', 'w') as file:
            json.dump(data_js, file, ensure_ascii = False)
    else:
        print('No Data')


if __name__ == '__main__':
    data = get_weather_data()
    data_txt(data)
    data_json(data)
