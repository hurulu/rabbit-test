#!/usr/bin/env python

#Ensure the python-pika is installed before running this script.Otherwise run: apt-get install python-pika 

import ConfigParser
import string, os, sys
import pika

conf="./rabbit.conf"
cf = ConfigParser.ConfigParser()
cf.read(conf)
rabbit_host = cf.get("rabbit","host")
rabbit_port = int(cf.get("rabbit","port"))
rabbit_user = cf.get("rabbit", "user")
rabbit_password = cf.get("rabbit", "password")
queue_name = cf.get("rabbit", "queue_name")

credentials = pika.PlainCredentials(rabbit_user,rabbit_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,port=rabbit_port,credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=queue_name,auto_delete=True)
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!')
print " [x] Sent 'Hello World!'"

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
try:
	channel.start_consuming()
except KeyboardInterrupt:
	channel.stop_consuming()
#	channel.queue_declare(queue=queue_name)

connection.close()
