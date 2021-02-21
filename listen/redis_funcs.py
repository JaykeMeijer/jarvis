import redis


rd = redis.Redis(host='localhost', port=6379, db=0)


def say(text):
    """
    Perform speaking of a text, by sending it to the correct REDIS topic

    :param text:    The text to say
    """
    rd.publish('say', text)
