import speech_recognition as sr
import winsound, time, os
from playsound import playsound, PlaysoundException
from email_sender import send_email
from gtts import gTTS
from tkinter import simpledialog

not_finished = True


def main(response):
    print("Activation heard!")
    print(response)
    if "disable" in response:
        return False
    elif "email" in response:
        email(response.split()[-1])
    return True


def query(prompt=None, beep=True):
    if prompt:
        speak(prompt)
    if beep:
        winsound.Beep(150, 1000)

    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.energy_threshold = 1000

        print("listening")

        audio = r.listen(source, timeout=None)
        final = process(audio, r).lower()

    return final


def speak(words):
    os.remove("speak.mp3")

    filename = rf"peak.mp3"
    gTTS(
        words,
        lang="en",
        tld="com.au",
    ).save(filename)
    try:
        playsound(filename)
    except PlaysoundException:
        print("Error playing sound")


def process(audio, r):
    try:

        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't get that, try again."
    except sr.RequestError:
        return "Unable to process at this time"


def email(username):
    # Contacts

    speak("Enter the user's email in")
    user = "custom"
    address = simpledialog.askstring("Email", "User's Email")

    ###
    while True:
        contents = query(f"Emailing {user}, what would you like to say?")
        print("Now confirming")
        confirm = query("You said" + contents + " . Do you want to send?")

        if "yes" in confirm:
            print("Sending...")
            send_email(address, contents)
            speak(f"Email sent to {user}")
            break


while not_finished:
    response = query(beep=False)
    if "echo" in response:
        not_finished = main(response)
    else:
        print("No activation", response)
speak("Okay, disabling...")
print("all finished")
