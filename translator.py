from deep_translator import GoogleTranslator


def translate_text(text, source, target):

    language_codes = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "French": "fr",
        "German": "de",
        "Spanish": "es"
    }

    translated = GoogleTranslator(
        source=language_codes[source],
        target=language_codes[target]
    ).translate(text)

    return translated