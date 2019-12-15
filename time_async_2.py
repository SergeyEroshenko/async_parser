import json
import time
import logging
import asyncio
import requests
import aiohttp
import ssl
from bs4 import BeautifulSoup

'''Creating an async HEAD request'''
async def request(url, num):
    '''Creating connection'''
    async with aiohttp.ClientSession() as session:
            try:
                '''Sending request/ Waiting responce'''
                async with await asyncio.wait_for(
                    session.head(url,
                                ssl=ssl.SSLContext(ssl.PROTOCOL_TLS)
                                ), timeout = 0.7) as resp:
                    responce = resp.status
                    '''Logging responce'''
                    logging.info(
                        'Task {}. Responce: {}\t\t{}'.format(
                            num, responce, time.time()
                            )
                        )
            except: pass

'''Logger setups'''
logging.basicConfig(filename = 'time_async_2.log',
                    filemode = 'w',
                    level=logging.INFO
                    )

'''Main function for manage tasks in event loop'''
async def main(urls):
    tasks = []
    num = 0
    for url in urls:
        '''Creating tasks for every url on page'''
        task = asyncio.create_task(request(url, num))
        tasks.append(task)
        num +=1
        if num % 30 == 0:
            '''Sending tasks to the event loop in batches of 30'''
            await asyncio.gather(*tasks)
            tasks = []

'''Getting URLs on a page'''
r = requests.get('https://yandex.ru/').text
soup = BeautifulSoup(r, 'html.parser') 
urls = [a['href'] for a in soup.select('a[href]')]       

'''Creating an event loop'''
asyncio.run(main(urls))
