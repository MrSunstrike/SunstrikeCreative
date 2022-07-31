import requests
from bs4 import BeautifulSoup
import csv

URL = {
    'Суши': 'https://sushivostok.com/products/sushi/',
    'Роллы': 'https://sushivostok.com/products/rolly/',
    'Горячие роллы': 'https://sushivostok.com/products/goryachie-rolly/',
    'Сеты': 'https://sushivostok.com/products/sety/',
    'Минисеты': 'https://sushivostok.com/products/mini-sety/',
    'Соусы': 'https://sushivostok.com/products/sousy/',
    'Напитки': 'https://sushivostok.com/products/napitki/',
    'Аппетайзеры': 'https://sushivostok.com/products/dopolnitelno/'
}

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'accept': '*/*'
}

FILE = 'Цены СушиВосток.csv'

def get_html(url): # Получает исходный код страницы url
    r = requests.get(url, headers=HEADERS)
    return r

def get_content(html): # Собирает со страницы: имя продукта (title), цену на доставку (price1) и цену на самовывоз (price2)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    positions = []
    for item in items:
        positions.append({
            'title': item.find('a', class_='t1').get_text(strip=True),
            'price1': item.find('div', class_='price1').find_next('div').get_text(strip=True).replace('руб.',''),
            'price2': item.find('div', class_='price2').find_next('div').get_text(strip=True).replace('руб.','')
        })
    return positions

def safe_file(items, path): # Функция записи полученных данных в табличку Excel
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование позиции', 'Стоимость на доставку', 'Стоимость при самовывозе'])
        for item in items:
            writer.writerow([item['title'], item['price1'], item['price2']])

def parse(URL): # Основная функция парсинга. Перебирает все значения из словаря URL и благодаря функции get_content,
                # упаковывает значения в список position
    position = []
    for page in URL:
        print(f'Происходит сбор информации со страницы "{page}"')
        html = get_html(URL[page])
        if html.status_code == 200:
            position.extend(get_content(html.text))
            safe_file(position, FILE)
        else:
            print('Что-то пошло не так')
    print(f'Получено {len(position)} позиций')


parse(URL)