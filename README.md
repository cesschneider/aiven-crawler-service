# Running Kafka producer/consumer

```
python kafka_service/producer.py
python kafka_service/consumer.py
```


# Building and running Docker image [WIP]

```
docker build -t kafka_producer -f Dockerfile.producer .
docker build -t kafka_consumer -f Dockerfile.consumer .
docker run -it --rm --name kafka_producer kafka_producer
docker run -it --rm --name kafka_consumer kafka_consumer
```
