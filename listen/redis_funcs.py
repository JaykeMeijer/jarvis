import redis
import os


r = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=0
)


def say(text):
    """
    Perform speaking of a text, by sending it to the correct REDIS topic

    :param text:    The text to say
    """
    r.publish(os.environ.get('REDIS_TOPIC'), text)
