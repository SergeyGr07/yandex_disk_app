from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'
    DOWNLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
