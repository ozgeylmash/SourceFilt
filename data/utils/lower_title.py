def lower(text):
    lower_map = {
        ord('I'): 'ı',
        ord('İ'): 'i',
    }

    return text.translate(lower_map).lower()

def title(text):
    upper_map = {
        ord('ı'): 'I',
        ord('i'): 'İ',
    }

    text = lower(text)

    return ' '.join(word[0].translate(upper_map).upper() + word[1:] for word in text.split())