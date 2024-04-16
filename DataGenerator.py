from Event import DeviceEvent
from DataNormalizer import DataNormalizer
from QualysFetcher  import QualysFetcher 
from CrowdStrikeFetcher import CrowdStrikeFetcher
from kafka import  KafkaProducer
from setup_logging import get_logger
from pprint import pprint
import concurrent.futures
import json

logger = get_logger()

class FetchServer:
    CONST = 2
    def __init__(self, fetchers, max_thr=2):
        self.max_threads = max_thr
        self.fetchers = fetchers
        self.data_normalizer = DataNormalizer()
        self.kafka_client = self.create_kafka_client()

    def create_kafka_client(self):
        return KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),  bootstrap_servers='localhost:9092')  

    def poll(self, params):
        skip = params['skip']
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            while True:
                params['skip'] = skip
                logger.error(f"params are {params}")
                futures = {
                    executor.submit(fetcher.fetch_json, params) for fetcher in self.fetchers
                }
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        for r in result:
                            raw_data_event = DeviceEvent.createEvent(r)
                            data_event = self.data_normalizer.normalize(raw_data_event)
                            self.save_to_kafka(data_event)
                    else:
                        log.error("result is Null ")
                skip = str(int(skip)+ FetchServer.CONST)
                if int(skip) > 6:
                    break

    def save_to_kafka(self, processed_data):
        msg = processed_data.serialize()
        print("convert event to json", len(msg))
        future = self.kafka_client.send('my-topic', msg)
        try:
            record_metadata = future.get(timeout=10)

            logger.debug(record_metadata.topic)
            logger.debug(record_metadata.partition)
            logger.debug(record_metadata.offset)
        except Exception as e:
            # Decide what to do if produce request failed...
            logger.exception(f"exception while sending {e}")

    def save_to_file(self, processed_data, filename):
        #for debugging
        pass

    def kakfa_close(self):
        self.kafka_client.close()

    def __del__(self):
        self.kafka_client.close()

if __name__ == '__main__':
    params = {
    'skip': '0',
    'limit': '2'
    }
    _f = open ('config/config.json', "r")
    config = json.loads(_f.read())
    url_qualys= config['url_qualys']
    url_crowdstrike = config['url_crowdstrike']
    hdrs = config['hdrs']
    logger.debug(f"url qualys {url_qualys}")
    logger.debug(f"url crowdstrike {url_crowdstrike}")

    QFetcher = QualysFetcher(url_qualys, hdrs)
    CFetcher = CrowdStrikeFetcher(url_crowdstrike, hdrs)
    fetchers = [CFetcher,QFetcher]
    fs = FetchServer(fetchers)
    fs.poll(params)
    fs.kafka_close()

