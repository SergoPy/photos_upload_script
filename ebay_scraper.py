import requests
from bs4 import BeautifulSoup
import random
import logging
import aiohttp

logging.basicConfig(filename='scraping_log.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.read().splitlines()
    return proxies


async def scrape_ebay_images(url, proxies):
    try:
        proxy = random.choice(proxies)
        proxy_parts = proxy.split(':')

        proxy_dict = {
            'http': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}',
            'https': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}'
        }

        logging.info(f"Using proxy: {proxy_dict}")

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url, proxy=proxy_dict['http'], timeout=30) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'html.parser')

                image_divs = soup.find_all('div', class_=lambda x: x and (
                    'ux-image-carousel-item image' in x or 'ux-image-carousel-item active image' in x) and 'ux-image-carousel-item video' not in x)

                logging.info(f"Scraped {len(image_divs)} images from {url}")

                image_links = []
                for div in image_divs:
                    img_tag = div.find('img')
                    if img_tag:
                        if 'data-zoom-src' in img_tag.attrs:
                            image_links.append(img_tag['data-zoom-src'])
                        elif 'data-src' in img_tag.attrs:
                            image_links.append(img_tag['data-src'])
                        elif 'src' in img_tag.attrs:
                            image_links.append(img_tag['src'])
                    else:
                        logging.warning("Image tag not found in div")

                return image_links
    except Exception as e:
        logging.error(f"Error scraping image URLs: {e}")
        return None
