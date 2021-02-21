import redis
from time import sleep
import espeakng


speaker = espeakng.Speaker()
speaker.voice = 'mb-en1'
speaker.wpm = 150
speaker.pitch = 75

r = redis.Redis(host='localhost', port=6379, db=0)

ps = r.pubsub()

ps.subscribe('say')


while True:
    msg = ps.get_message()
    if msg is not None:
        if msg['type'] == 'message':
            text = msg['data'].decode('utf8')
            print(text)
            speaker.say(text)
        else:
            print("unknown msg:", msg)

    sleep(0.1)
