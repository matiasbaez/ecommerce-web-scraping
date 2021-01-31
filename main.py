import json
import string
import random
import os.path
import requests

from os.path import basename
from bs4 import BeautifulSoup

def barcode(size=15, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

url = input('URL: ')
API = 'http://api.ecommercesy.com/api/'
print('reading url: ', url)

req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

products = soup.find_all('div', class_='product-item')

for product in products:
    
    name = product.find(class_='product-title-link').string.strip()
    price = product.find('span', class_='price-label').string.strip().replace('.', '')
    img = product.find('div', class_='picture').find('img')

    print('name: ', name)
    print('price: ', price)

    if img and 'http' in img.get('src'):
        lnk = img.get('src')
        path = os.path.join('images', basename(lnk))
        print('downloading file: ', lnk)
        with open(path, "wb") as f:
            f.write(requests.get(lnk).content)

        data = {
            'id_linea': 1,
            'id_tipo_impuesto': random.randint(1, 2),
            'id_marca': 1,
            'vr_unidad_medida': 'UN',
            'descripcion': name,
            'costo_unitario': price,
            'precio_venta': price,
            'codigo_barras': barcode()
        }

        files = { 'file0': open(path, 'rb') }

        req = requests.post(API + 'producto/upload', files=files, headers=headers)
        response = json.loads(req.text)

        if response['success']:
            data['imagen'] = response['data']
            req = requests.post(API + 'producto', files=files, data=data, headers=headers)
            response = json.loads(req.text)

            if response['success']:
                print('Producto registrado correctamente')
