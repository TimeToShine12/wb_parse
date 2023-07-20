import requests
import re
import csv

from models import Items


class ParseWB:

    def __init__(self, url):
        self.url = url
        self.brand_id = self.get_brand_id(url)

    @staticmethod
    def get_brand_id(url: str):
        regex = "(?<=brands.).[a-zA-Z0-9-]+"
        brand = re.search(regex, url)[0]
        response = requests.get(f"https://static.wbstatic.net/data/brands/{brand}.json")
        brand_id = response.json()['id']
        return brand_id

    def parse(self):
        i = 1
        self.__creat_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/brands/m/catalog?appType=1&brand={self.brand_id}&curr=rub&dest=-1257786&'
                f'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,66,110,48,22,31,71,114&'
                f'limit=300&sort=popular&spp=31&uclusters=7&page={i}')
            i += 1
            items_info = Items.model_validate(response.json()['data'])
            if not items_info.products:
                break
            self.__save_csv(items_info)

    def __creat_csv(self):
        with open('wb_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'price', 'brand', 'sell', 'rating', 'in_stock'])

    def __save_csv(self, items):
        with open('wb_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in items.products:
                writer.writerow([row.id, row.name, row.salePriceU, row.brand, row.sale, row.rating, row.volume])


if __name__ == '__main__':
    ParseWB("https://www.wildberries.ru/brands/apple").parse()
