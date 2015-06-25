#!/usr/bin/env python
import ConfigParser
import string, os, sys
import pika

conf="./rabbit.conf"
cf = ConfigParser.ConfigParser()
cf.read(conf)
rabbit_host = cf.get("rabbit", "host")
rabbit_user = cf.get("rabbit", "user")
rabbit_password = cf.get("rabbit", "password")
queue_name = "nectar_test"

credentials = pika.PlainCredentials(rabbit_user,rabbit_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=queue_name)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()
