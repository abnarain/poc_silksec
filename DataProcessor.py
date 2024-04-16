from kafka import  KafkaConsumer
from kafka import TopicPartition
from DBClient import MongoDBClient
from setup_logging import get_logger
import random
import json
import ast

logger = get_logger()

class DataProcessor:
    def __init__(self, topic, group_id, servers):
        self._topic = topic
        self._group_id = group_id
        self._servers = servers
        self.k_consumer = self.create_kafka_client()
        self.k_consumers = self.create_multiple_kafka_clients()
        self._db_client  = self.create_db_client()

    def high_throughput_process_data(self):
        consumer_1, consumer_2 = self.create_multiple_kafka_client()
        #ideal design to use futures and process asynchronously
        for message in consumer_partition_0:
            log.debug("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                  message.offset, message.key,
                                                  message.value))
        for message in consumer_partition_1:
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                  message.offset, message.key,
                                                  message.value))

    def process_data(self):
        #process it, here just copying it over
        for message in self.k_consumer:
            self.save_to_db(json.loads(message.value))

    def create_db_client(self, url="localhost", port=27017, db_name="machines", collection_name="c_machines"):
        return MongoDBClient(url, port, db_name, collection_name)

    def create_multiple_kafka_clients(self):
        consumer_partition_0 = KafkaConsumer(bootstrap_servers= self._servers,
                                             group_id=self._group_id,
                                             auto_offset_reset='earliest',
                                             max_poll_records = 10000)
        consumer_partition_0.assign([TopicPartition(self._topic, 0)])
        consumer_partition_0.subscription()

        consumer_partition_1 = KafkaConsumer(bootstrap_servers= self._servers,
                                             group_id=self._group_id,
                                             auto_offset_reset='earliest',
                                             max_poll_records = 10000)
        consumer_partition_1.assign([TopicPartition(self._topic, 1)])
        consumer_partition_1.subscription()
        return [consumer_partition_0, consumer_partition_1]

    def create_kafka_client(self):
        consumer_client = KafkaConsumer(self._topic, group_id= self._group_id, 
                                 bootstrap_servers= self._servers, consumer_timeout_ms=10000,
                                 auto_offset_reset='earliest')
        return consumer_client

    def save_to_db(self, processed_data):
        try:
            t = ast.literal_eval(processed_data)
            self._db_client.insert_document(t)
        except Exception as e:
            logger.error(f"unable to save to mongodb {e}")

    def aggregator(self):
        query = [{"$group" : {"_id": "$agent_version", "count":{"$sum":1}}}] 
        ans = self._db_client.agg_documents(query)
        ans = list(ans)
        logger.debug("the aggregation is {ans}")

    def save_to_file(self, processed_data, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(processed_data, file, indent=4)
            print("Data saved to", filename)
        except IOError as e:
            print("Error saving data to file:", e)

if  __name__ == '__main__':
    topic = 'my-topic'
    group_id = "ab-"+str(random.randint(1,1000)) 
    servers = ['localhost:9092']
    data_processor = DataProcessor(topic, group_id, servers)
    data_processor.process_data()
    data_processor.aggregator()
