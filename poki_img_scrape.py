import requests
import time
import os
import shutil
import multiprocessing as mp
from PIL import Image
from io import BytesIO
from functools import partial
from threading import Thread

if 'images' not in os.listdir():
    print('Making a new images directory...')
    os.mkdir('images')
else:
    print('Removing the old images directory and making a new one...')
    shutil.rmtree('images')
    os.mkdir('images')


def scrape(start, end):
    for i in range(start, end):
        try:
            url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:03d}'.format(
                i) + '.png'
            response = requests.get(url)
            binary_str = response.content
            stream = BytesIO(binary_str)
            image = Image.open(stream)
            image.save('images/{:03d}'.format(i) + '.png')
            print('{:03d}'.format(i))
        except Exception as e:
            print(str(e))


imgs = 890
thread_count = 16
thread_list = []
for i in range(thread_count):
    start = ((i * imgs)//thread_count) + 1
    end = (((i+1) * imgs)//thread_count) + 1
    print('start and end: ', start, end)
    thread_list.append(Thread(target=scrape, args=(start, end)))

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()
