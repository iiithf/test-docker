#!/usr/bin/env python3
from flask import Flask
from redis import Redis, RedisError
import socket
import os


db = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)
app = Flask(__name__)


@app.route('/')
def hello():
  try:
    visits = db.incr('counter')
  except RedisError:
    visits = '<i>cannot connect to redis, counter disabled</i>'
  html = \
    '<h3>Hello {name}!</h3>' \
    '<b>Hostname:</b> {hostname}<br>' \
    '<b>Visits:</b> {visits}'
  return html.format(name=os.getenv('NAME', 'world'), hostname=socket.gethostname(), visits=visits)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
