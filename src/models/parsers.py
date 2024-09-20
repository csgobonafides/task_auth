import asyncio
from bs4 import BeautifulSoup
from urllib.parse import quote
import aiohttp
import re


async def data_films(name_film: str):
    url = 'https://www.google.com/search?q=' + quote('дата выхода фильма' + name_film)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}) as response:
            soup = await response.text()
            bs = BeautifulSoup(soup, 'html.parser')
            result = bs.find('div', {'class': 'Z0LcW t2b5Cf'})
            if result:
                print(f'Дата выхода фильма {name_film} - {result.text}.')
                return {f'Дата выхода фильма {name_film}': result.text}
            else:
                print('Не удалось найти информацию об этом фильме.')
                return {'Error': 'Не удалось найти информацию об этом фильме.'}