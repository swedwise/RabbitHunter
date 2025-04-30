import json
import click
import pika
import ssl

@click.group()
def cli():
    """RabbitMQ Utility Tool"""
    pass


def connect_to_rabbitmq(host, port, username, password, vhost):
    """Establish and return a RabbitMQ connection and channel, using SSL if needed."""
    credentials = pika.PlainCredentials(username, password)

    if port == 5672:
        # Non-SSL connection
        connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=credentials
        )
    else:
        # SSL connection
        ssl_context = ssl.create_default_context()
        ssl_options = pika.SSLOptions(context=ssl_context, server_hostname=host)
        connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=credentials,
            ssl_options=ssl_options
        )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    return connection, channel


@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
def peek(host, port, username, password, vhost, queue):
    """Fetch one message from a queue without acknowledging it."""
    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)

        if method_frame:
            print("Received message:")
            print("Body:", body.decode())
            print("Delivery tag:", method_frame.delivery_tag)
        else:
            print("No message returned.")

        connection.close()
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
def pop(host, port, username, password, vhost, queue):
    """Fetch one message from a queue and acknowledge (remove) it."""
    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)

        if method_frame:
            print("Received message:")
            print("Body:", body.decode())
            print("Delivery tag:", method_frame.delivery_tag)

            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            print("Message acknowledged.")
        else:
            print("No message returned.")

        connection.close()
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
def requeue(host, port, username, password, vhost, queue):
    """Fetch one message from a queue and requeue (reject + requeue=True)."""
    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)

        if method_frame:
            print("Received message:")
            print("Body:", body.decode())
            print("Delivery tag:", method_frame.delivery_tag)

            # Reject and requeue the message
            channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True)
            print("Message rejected and requeued.")
        else:
            print("No message returned.")

        connection.close()
    except Exception as e:
        print(f"Error: {e}")

@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
def reject(host, port, username, password, vhost, queue):
    """Fetch one message from a queue and reject (discard) it."""
    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)

        if method_frame:
            print("Received message (discarding):")
            print("Body:", body.decode())
            print("Delivery tag:", method_frame.delivery_tag)

            # Reject the message without requeuing
            channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            print("Message rejected and discarded.")
        else:
            print("No message returned.")

        connection.close()
    except Exception as e:
        print(f"Error: {e}")

@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
def purge(host, port, username, password, vhost, queue):
    """Purge (clear) all messages from the given queue, with confirmation prompt."""
    confirm = click.prompt(
        f"Are you sure you want to purge all messages from queue '{queue}'? [y/N]",
        default="N"
    )
    if confirm.lower() != "y":
        print("Purge aborted.")
        return

    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        message_count = channel.queue_purge(queue=queue)
        print(f"Queue '{queue}' purged. {message_count} messages removed.")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Queue name')
@click.option('--output', required=True, help='Output JSON file to save messages')
def drain(host, port, username, password, vhost, queue, output):
    """Drain all messages from the queue and save them to a JSON file.
    
    This effectively removes all messages from the queue and saves them to a file.
    """
    try:
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)
        messages = []
        while True:
            method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)
            if method_frame:
                messages.append({
                    'body': body.decode(),
                    'properties': {
                        'delivery_mode': method_frame.delivery_mode,
                        'routing_key': method_frame.routing_key
                    },
                    'headers': header_frame.headers if header_frame else {},
                    'delivery_tag': method_frame.delivery_tag
                })
                # Acknowledge the message after storing
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            else:
                break

        # Write messages to JSON file
        with open(output, 'w') as f:
            json.dump(messages, f, indent=4)
        print(f"All messages from queue '{queue}' saved to '{output}'.")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=True, help='Target queue name')
@click.option('--input', required=True, help='Input JSON file containing messages')
def bulk_upload(host, port, username, password, vhost, queue, input):
    """Read messages from a JSON file and bulk upload them to the specified queue."""
    try:
        with open(input, 'r') as f:
            messages = json.load(f)

        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)

        for message in messages:
            body = message['body'].encode()
            properties = pika.BasicProperties(
                delivery_mode=message['properties']['delivery_mode'],
                routing_key=message['properties']['routing_key'],
                headers=message['headers']
            )
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=body,
                properties=properties
            )
            print(f"Message re-enqueued to '{queue}'.")

        connection.close()
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@click.option('--host', required=True, help='RabbitMQ host')
@click.option('--port', required=True, type=int, help='SSL port')
@click.option('--username', required=True, help='Username')
@click.option('--password', required=True, help='Password')
@click.option('--vhost', required=True, help='Virtual host')
@click.option('--queue', required=False, help='Target queue name')
@click.option('--exchange', required=False, help='Target exchange name')
@click.option('--input', required=True, help='Input JSON file containing messages')
def bulk_upload(host, port, username, password, vhost, queue, exchange, input):
    """Read messages from a JSON file and bulk upload them to the specified queue or exchange."""
    try:
        if not queue and not exchange:
            print("Error: You must specify either a queue or an exchange.")
            return

        # Read the messages from the JSON file
        with open(input, 'r') as f:
            messages = json.load(f)

        # Establish connection and channel
        connection, channel = connect_to_rabbitmq(host, port, username, password, vhost)

        for message in messages:
            # Prepare the message body and properties
            body = message['body'].encode()
            properties = pika.BasicProperties(
                delivery_mode=message['properties']['delivery_mode'],
                headers=message['headers']
            )

            # Determine where to send the message: queue or exchange
            if queue:
                # If queue is specified, use the queue name as the routing key
                routing_key = queue
                channel.basic_publish(
                    exchange='',  # Default exchange for direct routing
                    routing_key=routing_key,
                    body=body,
                    properties=properties
                )
                print(f"Message re-enqueued to queue '{queue}'.")
            elif exchange:
                # If exchange is specified, use the routing key from message properties
                routing_key = message['properties']['routing_key']
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=body,
                    properties=properties
                )
                print(f"Message published to exchange '{exchange}' with routing key '{routing_key}'.")

        # Close the connection after publishing
        connection.close()

    except Exception as e:
        print(f"Error: {e}")




if __name__ == "__main__":
    cli()
