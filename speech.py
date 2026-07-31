import speech_recognition as sr
from gtts import gTTS
import os


def speech_to_text(language_code="en-US"):

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(audio, language=language_code)

        return text

    except sr.WaitTimeoutError:
        return "Could not understand speech. Please try again."

    except sr.UnknownValueError:
        return "Could not understand speech."

    except sr.RequestError:
        return "Speech service unavailable."

    except Exception as e:
        return f"Error: {e}"


def text_to_speech(text, lang="en"):

    try:
        tts = gTTS(
            text=text,
            lang=lang
        )

        file = "output.mp3"

        tts.save(file)

        os.startfile(file)

    except Exception as e:
        return str(e)