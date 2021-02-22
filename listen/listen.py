import speech_recognition as sr
from speechtree import SpeechTree
from time import sleep, time
from redis_funcs import say


r = sr.Recognizer()
r.pause_threshold = 0.5
m = sr.Microphone()


tree = SpeechTree("tree.json")


def handle(recognizer, audio):
    """
    Handle received audio

    :param recognizer:  Recognizer object to use
    :param audio:       Audio received
    """
    print("Processing...")
    try:
        text = recognizer.recognize_google(audio).lower()
        print("I got:" + text)
        tree.process_text(text)
        return True
    except sr.UnknownValueError as e:
        if tree.active:
            tree.please_repeat()
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return False


with m as source:
    r.adjust_for_ambient_noise(source)

last_adjust = time()

say("Jarvis is online")

while True:
    with m as source:
        audio = r.listen(
            source,
            phrase_time_limit=5
        )
    require_pause = handle(r, audio)

    if require_pause:
        sleep(5)
    else:
        sleep(0.1)

    if time() - last_adjust > 600:
        print("->Readjusting Audio")
        with m as source:
            r.adjust_for_ambient_noise(source)
        last_adjust = time()
