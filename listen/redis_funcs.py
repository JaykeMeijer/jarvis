import redis
import os
from time import time

timeout = 10


r = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=0
)
ps = r.pubsub()
ps.subscribe("speaking")


def say(text):
    """
    Perform speaking of a text, by sending it to the correct REDIS topic

    :param text:    The text to say
    """
    r.publish(os.environ.get('REDIS_TOPIC'), text)
    msg = ps.get_message()
    start = time()
    while time() - start < timeout:
        msg = ps.get_message()
        if msg is not None:
            if msg['type'] == 'message' and msg['data'].decode('utf8') == "0":
                break
    else:
        print("ERROR TIMED OUT ON SPEECH WAIT")

def command(topic, command):
    r.publish(topic, command)

