# a Kafka consumer storing the data to an Aiven PostgreSQL database
# For the database writer we expect to see a solution that records the check
# results into one or more database tables and could handle a reasonable amount
# of checks performed over a longer period of time.

from kafka import KafkaConsumer
from logging import Logger
import sys
import time
from psycopg2.extras import RealDictCursor
import psycopg2
import json

logger = Logger(name='kafka-service')

try:
    consumer = KafkaConsumer(
        "crawler-service",
        auto_offset_reset="earliest",
        bootstrap_servers="kafka-do-ams-s2-cesschneider-66a1.aivencloud.com:28617",
        client_id="crawler-client-1",
        group_id="crawler-group",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
    )

    uri = "postgres://avnadmin:ypa097u81nb0w5rd@pg-do-ams-hob-cesschneider-66a1.aivencloud.com:28615/defaultdb?sslmode=require"
    db_conn = psycopg2.connect(uri)

    while True:
        raw_msgs = consumer.poll(timeout_ms=1000)
        for tp, msgs in raw_msgs.items():
            #print(tp)
            for msg in msgs:
                #print(msg)
                result = json.loads(msg.value)
                fields = ','.join(list(result.keys()))
                f = []
                for k in list(result.keys()):
                    f.append('%({})s'.format(k))
                values = ','.join(f)
                print("Received msg {}: {} {}".format(msg.offset, fields, values))

                #try:
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO crawler_results ({}) VALUES ({})".format(fields, values), result)
                db_conn.commit()
                cursor.close()
                #except:
                #    e, m, o = sys.exc_info()
                #    logger.error(m)

        # Commit offsets so we won't get the same messages again
        consumer.commit()

except:
    e, m, o = sys.exc_info()
    logger.error(m)

