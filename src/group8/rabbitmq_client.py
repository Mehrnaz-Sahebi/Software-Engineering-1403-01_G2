import pika
import uuid
import json
import threading

class RabbitMQClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RabbitMQClient, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
            self.channel = self.connection.channel()

            # Declare the necessary queues
            self.channel.queue_declare(queue='text_queue', durable=True)
            self.channel.queue_declare(queue='meanings_queue', durable=True)
            
            #self._start_consumer()
        except Exception as e:
            print(f"RabbitMQ health check failed: {e}")
        

    def _create_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))

    def send_message(self, message, callback):
        connection = self._create_connection()
        channel = connection.channel()
        correlation_id = str(uuid.uuid4())

        channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
            ),
            body=message,
        )

        def listen_for_response():
            try:
                for method, properties, body in channel.consume(queue='meanings_queue', auto_ack=True):
                    response = json.loads(body)
                    print(f"Received response: {response}")
                    if response[0].get("correlation_id") == correlation_id:
                        callback(response)
                        break
            except Exception as e:
                callback(f"Error: {str(e)}")
            finally:
                # Close the channel and connection
                channel.close()
                connection.close()

        threading.Thread(target=listen_for_response, daemon=True).start()
