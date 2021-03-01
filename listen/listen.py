import speech_recognition as sr
from speechtree import SpeechTree
from time import sleep, time
from redis_funcs import say
import os


r = sr.Recognizer()
r.pause_threshold = 0.5
m = sr.Microphone()
speech_timeout = 30


tree = SpeechTree("tree.json")


def handle(recognizer, audio):
    """
    Handle received audio

    :param recognizer:  Recognizer object to use
    :param audio:       Audio received
    """
    if os.environ.get("DEBUG", False):
        print("Processing...")
    try:
        if tree.active:
            text = recognizer.recognize_google_cloud(audio).lower()
        else:
            text = recognizer.recognize_google(audio).lower()
        print("I got:" + text)
        tree.process_text(text)
        return True
    except sr.UnknownValueError as e:
        if tree.active:
            tree.please_repeat()
            return True
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return False


with m as source:
    r.adjust_for_ambient_noise(source)

last_adjust = time()

say("Jarvis is online")

while True:
    with m as source:
        try:
            audio = r.listen(
                source,
                phrase_time_limit=5,
                timeout=10
            )
            require_pause = handle(r, audio)
        except sr.WaitTimeoutError:
            # Timeout reached, run loop to check for 
            require_pause = False

    if tree.active and (time() - tree.last) > speech_timeout:
        # Havent had a command in a while now, cancel active state
        tree.deactivate(True)
        require_pause = True

    if require_pause:
        sleep(3)
    else:
        sleep(0.1)

    if time() - last_adjust > 600:
        print("->Readjusting Audio")
        with m as source:
            r.adjust_for_ambient_noise(source)
        last_adjust = time()
