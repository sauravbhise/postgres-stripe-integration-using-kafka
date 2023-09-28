from confluent_kafka.avro import AvroConsumer
from util import add_customer, update_customer, delete_customer


default_group_name = "consumer-group"
topic = "postgres.public.customers"

consumer_config = {
    "bootstrap.servers": "localhost:19092",
    "schema.registry.url": "http://localhost:8081",
    "group.id": default_group_name,
    "auto.offset.reset": "latest",
}

consumer = AvroConsumer(consumer_config)

consumer.subscribe([topic])

while True:
    try:
        message = consumer.poll(5)
    except Exception as e:
        print(f"Exception while trying to poll messages - {e}")
    else:
        if message:
            print(
                f"Successfully poll a record from "
                f"Kafka topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()}\n"
                f"message key: {message.key()} || message value: {message.value()}"
            )
            msg = message.value()
            before = msg["before"]
            after = msg["after"]
            if before == None and after != None:
                add_customer(after["id"], after["name"], after["email"])
            if after == None and before != None:
                delete_customer(before["id"])
            else:
                update_customer(after["id"], after["name"], after["email"])

            consumer.commit()
        else:
            print("No new messages at this point. Try again later.")
