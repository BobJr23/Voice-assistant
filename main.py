import speech_recognition as sr
import winsound


def process(audio, r):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't get that, try again."
    except sr.RequestError:
        return "Unable to process at this time"


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


not_finished = True
while not_finished:
    response = query(beep=False)
    # Activation word is "echo" for now, prob customise later
    if "echo" in response:
        print("Activation heard!")
    else:
        print("No activation", response)
