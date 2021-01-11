from googletrans import Translator


# The function returns translated text from source lang to destination lang
def translator(text, source, destination):
    translator_object = Translator()
    try:
        return translator_object.translate(text, src=source, dest=destination).text
    except:
        return ''

