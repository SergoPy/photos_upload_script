import logging
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

logging.basicConfig(filename='scraping_log.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def check_trigger(sheet_key, credentials_file, sheet_name='photos_settings', cell='A1'):
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, scope)
        client = gspread.authorize(credentials)

        sheet = client.open_by_key(sheet_key).worksheet(sheet_name)
        sheet_url = client.open_by_key(sheet_key).worksheet('photos_url')
        cell_value = sheet.acell(cell).value

        if cell_value == '1':
            sheet_url.update_acell('A1', 'ВНИМАНИЕ!!! Работает СБУ! Ничего не трогать.')
            return True, sheet, sheet_url
        return cell_value == '1', sheet, sheet_url

    except Exception as e:
        logging.error(f"Error checking trigger: {e}")
        return False, None


def update_trigger(sheet, sheet_url, cell='A1', value='0'):
    try:
        sheet.update_acell(cell, value)
        sheet_url.update_acell('A1', 'ОТБОЙ!!! Можно трогать.')
    except Exception as e:
        logging.error(f"Error updating trigger: {e}")
