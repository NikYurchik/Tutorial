import random

import pika
import faker

from crud import contact_create, contsct_find, contact_count, contact_set_send

CONTACT_COUNT = 20
flags = [False, True]

fake = faker.Faker()

EXCHANGE = 'message_exchange'
EMAIL_KEY = 'email_queue'
SMS_KEY = 'sms_queue'

def send_message(channel, message, routing_key):
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=message.encode(),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=EMAIL_KEY, durable=True)
    channel.queue_declare(queue=SMS_KEY, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=EMAIL_KEY)
    channel.queue_bind(exchange=EXCHANGE, queue=SMS_KEY)

    cnt = contact_count()
    if  cnt < CONTACT_COUNT:
        for _ in range(CONTACT_COUNT - cnt):
            fullname = fake.name()
            email = fake.email()
            is_email = random.choice(flags)
            phone = fake.phone_number()
            is_phone = random.choice(flags) if is_email else True
            contact = contact_create(fullname=fullname, email=email, is_email=is_email, phone=phone, is_phone=is_phone)

    contacts = contsct_find(is_send=True)

    for contact in contacts:
        message = str(contact.id)
        contact_set_send(_id=contact.id, is_send=False)

        if contact.is_phone and contact.is_email:
            print(f" [x] Queuing SMS- and eMail-messages to the client {contact.fullname}({contact.id})")
        elif contact.is_phone:
            print(f" [x] Queuing an SMS-message to the client {contact.fullname}({contact.id})")
        elif contact.is_email:
            print(f" [x] Queuing an eMail message to the client {contact.fullname}({contact.id})")
    
        if contact.is_email:
            send_message(channel=channel, message=message, routing_key=EMAIL_KEY)
    
        if contact.is_phone:
            send_message(channel=channel, message=message, routing_key=SMS_KEY)
    
    connection.close()


if __name__ == '__main__':
    print('Start producer')
    main()
    print('Stop producer')

