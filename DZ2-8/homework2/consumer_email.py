import sys

import pika

from crud import contsct_read, contact_set_send

EXCHANGE = 'message_exchange'
EMAIL_KEY = 'email_queue'
SMS_KEY = 'sms_queue'

def on_email_message(ch, method, properties, body):
    message = body.decode()
    contact = contsct_read(message)
    if contact:
        print(f" [x] Send eMail to contact {contact.fullname}({contact.id})")
        contact_set_send(_id=contact.id, is_send=True)
    else:
        print(f" [!] Contact {message} is not found")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=SMS_KEY, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=EMAIL_KEY)

    while True:
        channel.basic_consume(queue=EMAIL_KEY, on_message_callback=on_email_message)
        channel.start_consuming()


if __name__ == '__main__':
    try:
        print('Start eMail consumer')
        main()
    except KeyboardInterrupt:
        print('Stop eMail consumer')
        sys.exit(0)
