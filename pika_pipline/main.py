import time

from threading import Thread
from central_controller import CentralController
from pipeline_controller import PipelineController
from workers import AMQPConsumer, RabbitMQProducer

controller_consumer = AMQPConsumer(
    queue_name="service-1",
    exchange_name="services",
)

controller_producer = RabbitMQProducer(
    queue_name="service-1",
    exchange_name="services",
)

pipeline_consumer = AMQPConsumer(
    queue_name="service-2",
    exchange_name="services",
)

pipeline_producer = RabbitMQProducer(
    queue_name="service-2",
    exchange_name="services",
)

central_controller = CentralController(
    consumer=pipeline_consumer,
    producer=controller_producer,
)
pipeline_consumer.handler = central_controller.handle_message

pipeline_controller = PipelineController(
    consumer=controller_consumer,
    pipline_producer=pipeline_producer,
)
controller_consumer.handler = pipeline_controller.handle_message


def main():
    t1 = Thread(target=pipeline_consumer.run)
    t2 = Thread(target=pipeline_producer.run)
    t3 = Thread(target=controller_consumer.run)
    t4 = Thread(target=controller_producer.run)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    time.sleep(10)

    while True:
        controller_producer.publish(repr({"message": "Hello, World!"}))
        time.sleep(10)


if __name__ == "__main__":
    main()
