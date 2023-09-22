from difflib import SequenceMatcher
from utils.lower_title import lower


def check_similarity(text1, text2, thresh):
    text1 = lower(text1).split()
    text2 = lower(text2).split()

    text1.sort()
    text2.sort()

    is_similar = SequenceMatcher(None, text1, text2).ratio() > thresh
    return is_similar
