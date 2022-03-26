import requests
import string
from time import sleep
import urllib.parse
import csv

def write_csv(data, file_name):
    with open('data/'+file_name, 'a', newline='') as f:
        fields = ['brand', 'series', 'title', 'price', 'series_id', 'category_id', 'object_id', 'storage', 'year_manu', 'keywords']
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

def get_laptops(filters, brand):
    params = {
        'x-algolia-agent': 'Algolia for vanilla JavaScript (lite) 3.27.1;instantsearch.js 1.12.1;JS Helper 2.26.0',
        'x-algolia-application-id': 'BQ1TOTI7UG',
        'x-algolia-api-key': '974a32bba449e9d9f6ebe112ba4b9ade'
    }
    url = 'https://bq1toti7ug-dsn.algolia.net/1/indexes/*/queries'

    facetFilters = '[["brand:'+brand+'"]]'
    print(facetFilters)

    # facetFilters = urllib.parse.quote(facetFilters)
    # print(facetFilters)
    # %5B%5B%22brand%3ASager%20%2F%20Clevo%22%5D%5D

    payload = {
        "requests": [{
            "indexName": "alg_modelos",
            "params": filters,
            "facetFilters": facetFilters
        }]
    }
    r = requests.post(url, params=params, json=payload)
    # if(r.status_code == 200):
    if(r.ok):
        data = r.json()['results'][0]['hits']
        sleep(2.5)
        return data


def main(query, brand_looking_for):
    print(brand_looking_for)
    all_laptops = []

    hitsPerPage = 100
    maxValuesPerFacet=60
    page = 0
    filters = urllib.parse.quote('category:"Laptop" OR category:"Macbook"')
    # facets = urllib.parse.quote('["category","brand","series_name","processor","storage","RAM"]')
    facets = urllib.parse.quote('brand')
    tagFilters = ""

    params_string = f'query={query}&hitsPerPage={hitsPerPage}&maxValuesPerFacet={maxValuesPerFacet}&page={page}&filters={filters}&facets={facets}&tagFilters={tagFilters}'

    while True:
        print(params_string)

        laptops = get_laptops(params_string, brand_looking_for)

        if laptops:
            all_laptops.extend(laptops)
            page += 1
            params_string = f'query={query}&hitsPerPage={hitsPerPage}&maxValuesPerFacet={maxValuesPerFacet}&page={page}&filters={filters}&facets={facets}&tagFilters={tagFilters}'
        else:
            break

    for laptop in all_laptops:
        # print(laptop)

        # print(laptop['n_modelo'])

        try:
            brand = laptop['brand']
        except:
            brand = ''

        try:
            series = laptop['series_name']
        except:
            series = ''

        try:
            title = laptop['n_modelo']
        except:
            title = ''
    
        try:
            price = laptop['precio_base']
        except:
            price = ''
        
        try:
            series_id = laptop['series_id_serie']
        except:
            series_id = ''
        
        try:
            category_id = laptop['categorias_id_catego']
        except:
            category_id = ''
        
        try:
            object_id = laptop['objectID']
        except:
            object_id = ''

        try:
            storage = laptop['storage']
        except:
            storage = ''

        try:
            year_manu = laptop['year_manu']
        except:
            year_manu = ''

        try:
            keywords = laptop['keywords']
        except:
            keywords = ''

        data = {
            'brand': brand,
            'series': series,
            'title': title,
            'price': price,
            'series_id': series_id,
            'category_id': category_id,
            'object_id': object_id,
            'storage': storage,
            'year_manu': year_manu,
            'keywords': keywords
        }

        write_csv(data, 'laptops_'+brand_looking_for.replace("/", "")+'.csv')

    # print(all_laptops)
    print(len(all_laptops))

def brand_list():
    # brands = ['Lenovo', 'HP', 'Dell', 'Asus', 'Apple', 'Acer', 'MSI', 'Alienware', 'Toshiba', 'Sony', 'Samsung', 'Razer', 'Microsoft', 'Sager / Clevo', 'Gigabyte', 'Panasonic', 'Google', 'Fujitsu', 'Huawei', 'LG', 'Cyberpower', 'Eluktronics', 'VAIO', 'Aorus', 'Origin', 'Xiaomi Mi', 'Getac', 'System76', 'Vizio', 'EVGA', 'Falcon Northwest']
    brands = ['Apple']
    return brands

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

if __name__ == '__main__':

    for brand in chunker(brand_list(), 1):
        main('', brand[0])
        print(brand[0])
        sleep(60)

    # main('', 'Lenovo') # 655
    # main('', 'HP') # 627
    # main('', 'Dell') # 518
    # main('', 'Asus') # 408
    # main('', 'Apple') # 346
    # main('', 'Acer') # 247
    # main('', 'MSI') # 201 
    # main('', 'Alienware') # 113
    # main('', 'Toshiba') # 83
    # main('', 'Sony')  # 66
    # main('', 'Samsung') # 65
    # main('', 'Razer') # 63
    # main('', 'Microsoft') # 47
    # main('', 'Sager / Clevo') # 34
    # main('', 'Gigabyte') # 18
    # main('', 'Panasonic') # 15
    # main('', 'Google') # 10
    # main('', 'Fujitsu') # 8
    # main('', 'Huawei') # 8
    # main('', 'LG') # 8
    # main('', 'Cyberpower') # 7 
    # main('', 'Eluktronics') # 7
    # main('', 'VAIO') # 7
    # main('', 'Aorus') # 6
    # main('', 'Origin') # 5
    # main('', 'Xiaomi Mi') # 5
    # main('', 'Getac') # 4
    # main('', 'System76') # 4
    # main('', 'Vizio') # 4
    # main('', 'EVGA') # 1
    # main('', 'Falcon Northwest') # 1