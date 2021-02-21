import redis
from time import sleep


r = redis.Redis(host='localhost', port=6379, db=0)

ps = r.pubsub()

ps.subscribe('say')


while True:
    msg = ps.get_message()
    if msg is not None:
        print(msg)

    sleep(0.1)
