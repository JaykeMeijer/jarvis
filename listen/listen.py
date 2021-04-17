import speech_recognition as sr
from speechtree import SpeechTree
from time import time
from redis_funcs import say
import os


last_adjust = time()


DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
USE_GLOUD = os.environ.get("USE_GCLOUD", "false").lower() == "true"
ENERGY_THRESHOLD_MULTIPLIER = float(
    os.environ.get("ENERGY_THRESHOLD_MULTIPLIER", 2)
)
SPEECH_TIMEOUT = 30
READJUST_TIMEOUT = 600


def print_status(recognizer):
    print("Running with following config:")
    print("SR settings:")
    print(f"\tPause threshold: {recognizer.pause_threshold}")
    print(f"\tEnergy threshold multiplier: {ENERGY_THRESHOLD_MULTIPLIER}")
    print(f"\tUse GCloud: {USE_GLOUD}")
    print("System settings:")
    print(f"\tSpeech timeout: {SPEECH_TIMEOUT}")
    print(f"\tDebug: {DEBUG}")


def handle(recognizer, audio, tree):
    """
    Handle received audio

    :param recognizer:  Recognizer object to use
    :param audio:       Audio received
    :param tree:        The conversation tree to use
    """
    if DEBUG:
        print("Processing...")

    try:
        if USE_GLOUD and tree.active:
            text = recognizer.recognize_google_cloud(audio).lower()
        else:
            text = recognizer.recognize_google(audio).lower()
        print("I got:" + text)
        tree.process_text(text)
    except sr.UnknownValueError as e:
        if tree.active:
            tree.please_repeat()
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def readjust(recognizer, microphone):
    global last_adjust
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    recognizer.energy_threshold *= ENERGY_THRESHOLD_MULTIPLIER
    last_adjust = time()


def main():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.5
    recognizer.dynamic_energy_threshold = False
    microphone = sr.Microphone()

    print_status(recognizer)

    readjust(recognizer, microphone)
    tree = SpeechTree("tree.json")

    # Ready to go!
    say("Jarvis is online")

    while True:
        with microphone as source:
            try:
                audio = recognizer.listen(
                    source,
                    phrase_time_limit=5,
                    timeout=3
                )
                handle(recognizer, audio, tree)
            except sr.WaitTimeoutError:
                # Timeout reached, run loop to check for
                if DEBUG:
                    print("timeout")

        if tree.active and (time() - tree.last) > SPEECH_TIMEOUT:
            # Havent had a command in a while now, cancel active state
            tree.deactivate(True)

        if time() - last_adjust > READJUST_TIMEOUT:
            print("->Readjusting Audio")
            readjust(recognizer, microphone)

        if DEBUG:
            print(recognizer.energy_threshold)


if __name__ == "__main__":
    main()
