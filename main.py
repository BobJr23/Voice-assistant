import speech_recognition as sr
import winsound
from gtts import gTTS
from playsound import playsound, PlaysoundException
import os


def main(response):
    print("Activation heard!")
    print(response)
    if "disable" in response:
        return False

    return True


def process(audio, r):
    try:

        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't get that, try again."
    except sr.RequestError:
        return "Unable to process at this time"


def speak(words):
    filename = "speak.mp3"
    os.remove(filename)

    gTTS(
        words,
        lang="en",
        tld="com.au",
    ).save(filename)
    try:
        playsound(filename)
    except PlaysoundException:
        print("Error playing sound")


def query(beep=True):

    if beep:
        winsound.Beep(150, 1000)

    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.energy_threshold = 1000

        print("listening")

        audio = r.listen(source, timeout=None)
        final = process(audio, r).lower()

    return final


if __name__ == "__main__":
    not_finished = True
    while not_finished:
        response = query(beep=False)
        # Activation word is "echo" for now, prob customise later
        if "echo" in response:
            main(response)
        else:
            print("No activation", response)
