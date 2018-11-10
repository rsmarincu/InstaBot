import configparser
import arrow
import requests
from urllib import request
import json

configs = configparser.RawConfigParser()
configs.read('./config.ini')
locations = configparser.RawConfigParser()

API_KEY = configs['DEFAULT']['API_KEY']
BASE_URL = 'https://api.nasa.gov/planetary/apod?api_key={}'

date = arrow.utcnow()
date.to('local')
date = date.format('YYYY-MM-DD')

REQ_URL = BASE_URL.format(API_KEY)

response = requests.get(REQ_URL)
data = response.json()

title = data['title']
image_url = data['hdurl']
photo_path = r'./Images/{}.jpg'.format(title)

locations['IMAGES'] = {}
locations['IMAGES'][date] = photo_path
locations['TITLES'] = {}
locations['TITLES'][date] = title

with open('locations.ini', 'w') as configfile:
    locations.write(configfile)

image = request.urlretrieve(image_url, photo_path)

quit()
