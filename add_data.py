import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


# def batch_update_cells(sheet, data, start_row, start_col):
#     try:
#         rows = len(data)
#         cols = len(data[0]) if rows > 0 else 0

#         if rows == 0 or cols == 0:
#             return

#         end_row = start_row + rows - 1
#         end_col = start_col + cols - 1

#         cell_list = sheet.range(start_row, start_col, end_row, end_col)

#         for i in range(rows):
#             for j in range(cols):
#                 cell_list[i * cols + j].value = data[i][j]

#         sheet.update_cells(cell_list)

#     except Exception as e:
#         print(f"Error batch updating cells: {e}")


def write_links_to_sheets(sheet_key, ebay_links, start_row):
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope)
        client = gspread.authorize(credentials)

        sheet = client.open_by_key(sheet_key).worksheet('photos_url')

        start_col = 2

        all_photo_links = [
            ["-" if not links else links for links in ebay_links]]
        print(ebay_links)
        try:
            sheet.update(f'A{start_row}:A', all_photo_links)

            # time.sleep(1)
        except Exception as update_error:
            print(f"Error updating cells: {update_error}")

    except Exception as e:
        print(f"Error writing links to Google Sheets: {e}")

# def write_links_to_sheets(sheet_key, ebay_links, start_row):
#     try:
#         scope = ["https://spreadsheets.google.com/feeds",
#                  "https://www.googleapis.com/auth/drive"]
#         credentials = ServiceAccountCredentials.from_json_keyfile_name(
#             "credentials.json", scope)
#         client = gspread.authorize(credentials)

#         sheet = client.open_by_key(sheet_key).worksheet('photos_url')

#         start_col = 2

#         for row_number, photo_links in enumerate(ebay_links, start=start_row):
#             if not photo_links:
#                 photo_links = ["-"]

#             try:
#                 batch_update_cells(sheet, [photo_links], row_number, start_col)
#                 time.sleep(1)
#             except Exception as update_error:
#                 print(
#                     f"Error batch updating cells for row {row_number}: {update_error}")

    # except Exception as e:
        # print(f"Error writing links to Google Sheets: {e}")
