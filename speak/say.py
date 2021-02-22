import redis
from time import sleep
import espeakng
import os


print("Initializing speech engine")

speaker = espeakng.Speaker()
speaker.voice = 'mb-en1'
speaker.wpm = 150
speaker.pitch = 75

print("Setting up REDIS connection")

r = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=0
)

ps = r.pubsub()

ps.subscribe(os.environ.get('REDIS_TOPIC'))


print("Ready to speak")

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
