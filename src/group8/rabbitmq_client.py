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
        

    def send_message(self, message, callback):
        correlation_id = str(uuid.uuid4())

        # Publish the message to the text_queue
        self.channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
            ),
            body=message,
        )

        # Start a thread to listen for responses in meanings_queue
        def listen_for_response():
            for method, properties, body in self.channel.consume(queue='meanings_queue', auto_ack=True):
                try:
                    # Deserialize the response
                    response = json.loads(body)
                    print(response)

                    # Check if the correlation ID matches the current request
                    if response[0].get("correlation_id") == correlation_id:
                        callback(response.get("results"))
                        break
                except Exception as e:
                    callback(f"Error: {str(e)}")
                    break
        #listen_for_response()
        threading.Thread(target=listen_for_response, daemon=True).start()
    

    '''
    def listen_for_response():
        for method, properties, body in self.channel.consume(queue='meanings_queue', auto_ack=True):
            try:
                # Deserialize the response
                response = json.loads(body)
                print(f"Received response: {response}")

                # Call the callback function if it exists
                if hasattr(self, 'callback'):
                    self.callback(response)
            except Exception as e:
                print(f"Error processing message: {e}")

        # Start the consumer in a separate thread
        threading.Thread(target=listen_for_response, daemon=True).start()

    def send_message(self, message, callback):
        """Send a message to text_queue and set up a callback for the response."""
        correlation_id = str(uuid.uuid4())

        # Publish the message to the text_queue
        self.channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
            ),
            body=message,
        )

        # Store the callback function for later use
        self.callback = lambda response: callback(response) if response.get("correlation_id") == correlation_id else None
        '''
