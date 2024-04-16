from SourceDataFetcher import DataFetcher
from setup_logging import get_logger
import requests
logger = get_logger()

class QualysFetcher(DataFetcher):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def fetch_json(self, params):
        try:
            response = requests.post(self.url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch data. Status code: {response.status_code}, {response}")
                raise Exception(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            raise Exception(e)
