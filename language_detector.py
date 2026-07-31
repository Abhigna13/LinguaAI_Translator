from langdetect import detect


def detect_language(text):

    try:
        code = detect(text)
        return code

    except:
        return "unknown"