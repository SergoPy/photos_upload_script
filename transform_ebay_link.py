import asyncio
from ebay_scraper import scrape_ebay_images
from get_proxy import load_proxies
# from send_to_imgbb import upload_to_imgbb
import httpx
import asyncio
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


async def upload_to_imgbb(api_key, image_url):
    # try:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.imgbb.com/1/upload",
            data={"key": api_key, "image": image_url}
        )
        result = response.json()
        return result.get("data", {}).get("url")
    # except Exception as e:
    #     print(f"Error uploading image to ImgBB: {e}")
    #     return None


async def process_ebay_link(ebay_link, proxies, sheet_key, imgbb_api_key):
    try:
        image_urls = await scrape_ebay_images(ebay_link, proxies)
        imgbb_urls = []

        for image_url in image_urls:
            imgbb_url = await upload_to_imgbb(imgbb_api_key, image_url)
            imgbb_urls.append(imgbb_url)

        return imgbb_urls
    except Exception as e:
        logging.error(f"Error processing eBay link {ebay_link}: {e}")
        new_proxies = load_proxies("new_proxy.txt")
        if new_proxies:
            logging.info(f"Retrying with new proxies: {new_proxies}")
            return await process_ebay_link(ebay_link, new_proxies, sheet_key, imgbb_api_key)
        else:
            logging.error("No new proxies available. Unable to retry.")
            return None
