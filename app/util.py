import json
import math
import re
import time
import warnings
from io import BytesIO
from PIL import Image
from sys import stderr

import cv2
import numpy as np
import pandas as pd
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class RegistryRequester:
    def __init__(self, selenium_driver_path='/usr/bin/chromedriver'):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(selenium_driver_path, chrome_options=chrome_options)

    def __call__(self, lat: float, lon: float):
        result = {
                    'Тип':[],
                    'Вид':[],
                    'Кадастровый номер':[],
                    'Кадастровый квартал':[],
                    'Статус':[],
                    'Адрес':[],
                    'Категория земель':[],
                    'Форма собственности':[],
                    'Кадастровая стоимость':[],
                    'Дата определения КС':[],
                    'Дата внесения сведений о КС':[],
                    'Дата утверждения КС':[],
                    'Дата применения КС':[],
                    'Уточненная площадь':[],
                    'Разрешенное использование':[],
                    'по документу':[]
                }
        url_where = 'https://pkk.rosreestr.ru/#/search/'+str(lat)+','+str(lon)+'/13/@qih8n8v9?text='+str(lat)+'%20'+str(lon)+'&type=1&inPoint=true'
        self.driver.get(url_where)
        time.sleep(1)
        html = self.driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        try:
            find = soup.findAll('div', {'class':'expanding-box'})
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[0]))[0][7:-8]
                result['Тип'].append(res)
            except:
                result['Тип'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[1]))[0][7:-8]
                result['Вид'].append(res)
            except:
                result['Вид'].append('_')
            try:
                res = re.findall(r'tabindex="0">[\s,\S]{,}</span', str(find[2]))[0][13:-6]
                result['Кадастровый номер'].append(res)
            except:
                result['Кадастровый номер'].append('_')
            try:
                res = re.findall(r'tabindex="0">[\s,\S]{,}</span', str(find[3]))[0][13:-6]
                result['Кадастровый квартал'].append(res)
            except:
                result['Кадастровый квартал'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[4]))[0][7:-8]
                result['Статус'].append(res)
            except:
                result['Статус'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[5]))[0][7:-8]
                result['Адрес'].append(res)
            except:
                result['Адрес'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[6]))[0][7:-8]
                result['Категория земель'].append(res)
            except:
                result['Категория земель'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[7]))[0][7:-8]
                result['Форма собственности'].append(res)
            except:
                result['Форма собственности'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[8]))[0][7:-8].replace('\xa0', ' ')
                result['Кадастровая стоимость'].append(res)
            except:
                result['Кадастровая стоимость'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[9]))[0][7:-8]
                result['Дата определения КС'].append(res)
            except:
                result['Дата определения КС'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[10]))[0][7:-8]
                result['Дата внесения сведений о КС'].append(res)
            except:
                result['Дата внесения сведений о КС'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[11]))[0][7:-8]
                result['Дата утверждения КС'].append(res)
            except:
                result['Дата утверждения КС'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[11]))[0][7:-8]
                result['Дата применения КС'].append(res)
            except:
                result['Дата применения КС'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[13]))[0][7:-8].replace('\xa0',' ')
                result['Уточненная площадь'].append(res)
            except:
                result['Уточненная площадь'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[14]))[0][7:-8]
                result['Разрешенное использование'].append(res)
            except:
                result['Разрешенное использование'].append('_')
            try:
                res = re.findall(r'none;">[\s,\S]{,}</div> <', str(find[15]))[0][7:-8]
                result['по документу'].append(res)
            except:
                result['по документу'].append('_')
        except:
            pass
        return result

    def is_home(self, lat: float, lon: float):
        warnings.filterwarnings('ignore')

        url_m = 'https://pkk.rosreestr.ru/#/search/'+str(lat)+','+str(lon)+'/20/@fzn9ro91'
        self.driver.get(url_m)
        time.sleep(3)

        scr = self.driver.get_screenshot_as_png()
        scr = Image.open(BytesIO(scr))
        scr = np.asarray(scr,dtype=np.float32).astype(np.uint8)
        scr = cv2.cvtColor(scr, cv2.COLOR_BGR2RGB)

        return bool((scr[int(scr.shape[0]/2), int(scr.shape[1]/2)] != [255, 255, 255]).prod())

def pxl_to_geo(pxl_length: float, geo_to_pxl_ratio: float):
    return pxl_length * geo_to_pxl_ratio

def rotate_point2d(x: float, y: float, theta: float):
    # Multiply by 2d rotation matrix.
    return math.cos(theta)*x - math.sin(theta)*y, math.sin(theta)*x + math.cos(theta)*y

def print_err(*args, sep=' ', end='\n'):
    stderr.write(sep.join([a for a in args]) + end)
