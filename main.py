import configparser
import arrow
import requests
import json
from InstagramAPI import InstagramAPI
from subprocess import call
from PIL import Image, ImageOps
import os

### Definitions

def resizeImage(path):
    image = Image.open(path)
    width, height = image.size
    if width > height:
        padding_size = (width-height)/2
        padding = (0,padding_size,0,padding_size)
        new_image = ImageOps.expand(image,padding,(255,255,255))
        new_image.save(path)
    else:
        padding_size = int((height-width)/2)
        padding = (padding_size,0,padding_size,0)
        new_image = ImageOps.expand(image,padding,(255,255,255))
        new_image.save(path)

hashtags = '#space #universe #art #galaxy #trippy #stars #moon #meditation #spirituality #imagination #fantasy #astronomy #psychedelic #nature #science #nasa #spiritual #universe #galaxy #daily #picoftheday #followme #follow #sky #night #instadaily #followback #amazing'

date = arrow.utcnow()
date.to('local')
date = date.format('YYYY-MM-DD')

configs = configparser.RawConfigParser()
configs.read('./config.ini')

INSTA_USER=configs['DEFAULT']['INSTA_USER']
INSTA_PASS=configs['DEFAULT']['INSTA_PASS']

call(['python', 'getimages.py'])

locations = configparser.RawConfigParser()
locations.read('./locations.ini')

photo_path = locations['IMAGES'][date]
title = locations['TITLES'][date]
title = title.ljust(500)
captions = title + '\n'  + '\n' + '.' + '\n' + '.' + '\n' + '.' + '\n' + '.' + '\n' + '.' + '\n' + '.' + '\n' + '.' + hashtags
resizeImage(photo_path)

print (captions)

instagram = InstagramAPI(INSTA_USER,INSTA_PASS)
instagram.login()

error_link = instagram.LastJson.get("challenge")
if error_link:
    error_link = error_link.get("url")
    print(error_link)
try:
    instagram.uploadPhoto(photo_path,captions)
except Exception as err:
    print(err)

os.remove(photo_path)
