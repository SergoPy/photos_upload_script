import asyncio
import httpx
import asyncio
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

async def upload_to_imgbb(api_key, image_url):
    # try:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.imgbb.com/1/upload",
            data={"key": api_key, "image": image_url}
        )
        result = response.json()
        return result.get("data", {}).get("url")
    # except Exception as e:
    #     print(f"Error uploading image to ImgBB: {e}")
    #     return None
