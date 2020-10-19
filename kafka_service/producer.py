# a Kafka producer which periodically checks the target
# websites and sends the check results to a Kafka topic
# The website checker should perform the checks periodically and collect the
# HTTP response time, error code returned, as well as optionally checking the
# returned page contents for a regexp pattern that is expected to be found on the
# page.

from kafka import KafkaProducer
from logging import Logger
import sys
import time
import requests
import json

logger = Logger(name='kafka-service')
message_id = 1
check_period_time = 1

try:
    producer = KafkaProducer(
        bootstrap_servers="kafka-do-ams-s2-cesschneider-66a1.aivencloud.com:28617",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
    )

    urls_to_verify = [
        {
            'url': 'https://aiven.io',
            'regex': 'body'
        },
        {
            'url': 'https://google.com',
            'regex': 'body'
        },
        {
            'url': 'https://twitterr.com',
            'regex': 'body'
        }
    ]

    while True:
        for entry in urls_to_verify:
            print('Verifying URL {}'.format(entry['url']), end=' ')
            start_time = time.time()
            try:
                response = requests.get(entry['url'], timeout=1)
                end_time = time.time()
                if response.status_code == 200:
                    state = "OK"
                elif response.status_code == 404:
                    state = "NOT_FOUND"
                else:
                    state = "UNDEFINED"
                print('{} ({})'.format(state, response.status_code))
                result = {
                    'url': entry['url'],
                    'state': state,
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'regex': entry['regex'],
                    'content': response.text,
                    'timestamp': int(time.time())
                }
                # print(result)
            except:
                end_time = time.time()
                result = {
                    'url': entry['url'],
                    'state': 'unavailable',
                    'timestamp': int(time.time())
                }
                e, m, o = sys.exc_info()
                logger.error(m)
                print('{} ({})'.format(result['state'], 'null'))

            message = "message number {}".format(message_id)
            print("Sending: {}".format(result.keys()))
            producer.send("crawler-service", json.dumps(result).encode("utf-8"))
            producer.flush()
            message_id += 1

        time.sleep(check_period_time)

except:
    e, m, o = sys.exc_info()
    logger.error(m)

