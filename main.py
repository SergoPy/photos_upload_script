import asyncio
from sheets_parser import parse_sheets_links
from ebay_scraper import scrape_ebay_images
from add_data import write_links_to_sheets
from get_proxy import load_proxies
from send_to_imgbb import upload_to_imgbb
from transform_ebay_link import process_ebay_link
from update_monitor import check_trigger, update_trigger
import httpx
import asyncio
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

sheet_key = '11Thgpjvqc7RBHeZqu6km5bwF7HLbXX3L-8fqeJw3Azc'
credentials_file = 'credentials.json'
proxy_file = 'proxy.txt'
imgbb_api_key = "e52110774c888773c47a569819fc8cfd"
logging.basicConfig(filename='scraping_log.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


async def main():
    logging.info("Executing main code...")
    proxies = load_proxies(proxy_file)
    ebay_links = parse_sheets_links(sheet_key, credentials_file)

    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(sheet_key).worksheet('photos_url')

    batch_size = 25
    start_row = 2

    for i in range(0, len(ebay_links), batch_size):
        ebay_batch = ebay_links[i:i+batch_size]
        tasks = [process_ebay_link(
            ebay_link, proxies, sheet_key, imgbb_api_key) for ebay_link in ebay_batch]
        results = await asyncio.gather(*tasks)
        write_links_to_sheets(sheet_key, results, start_row)
        # sheet.update_cells(results)
        start_row += 25

if __name__ == "__main__":
    while True:
        trigger_value, sheet, sheet_url = check_trigger(
            sheet_key, credentials_file)
        if trigger_value:
            asyncio.run(main())
            update_trigger(sheet, sheet_url)
        else:
            logging.info(
                "Trigger is not set. Monitoring again in 5 seconds...")
        time.sleep(5)
