import json
import logging
import os
from pathlib import Path
from time import time
import requests
from uuid import uuid4
from urllib import parse
#https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class download:
    def __init__(self):
        self.url = "https://picsum.photos/1028/700"
     
    def download_image(self):
        response = requests.get(self.url)
        extension = os.path.splitext(parse.urlsplit(response.url).path)[-1]
        image_name = f'{uuid4()}{extension}'
        path = f'images/{image_name}'
        with open(path, mode='wb') as f:
            f.write(response.content)

def main():
    dobj = download()
    ts = time()
    dobj.download_image()
    logging.info('Took %s seconds', time() - ts)

if __name__ == '__main__':
    main()