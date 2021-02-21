import fuzzy
from num2words import num2words


dmeta = fuzzy.DMetaphone()


def s_phonetic(word):
    """
    Safe word compare function, performing some cleansing
    """
    word = word.strip()
    if word.isnumeric():
        word = num2words(word)
    return dmeta(word)


def wcmp(a, b):
    return s_phonetic(a) == s_phonetic(b)


def wil(word, lst):
    """
    Check if a word is found in a list

    :param word:    The word to check
    :param lst:     The list to check
    :returns:       Boolean
    """
    w = s_phonetic(word)
    for i in lst:
        if w == s_phonetic(i):
            return True

    return False


def wis(word, sentence):
    """
    Check if a word is found in a string

    :param word:    The word to check
    :param lst:     The sentence to check
    :returns:       Boolean
    """
    w = s_phonetic(word)
    for i in sentence.split(' '):
        if w == s_phonetic(i):
            return True

    return False


def awis(words, sentence):
    """
    Check if any of the words is found in a sentence

    :param words:   The words to check
    :param lst:     The sentence to check
    :returns:       Boolean
    """
    ws = []
    for word in words:
        ws.append(s_phonetic(word))

    for i in sentence.split(' '):
        if s_phonetic(i) in ws:
            return True

    return False


def cwis(words, sentence):
    """
    Count how many of the words are found in a sentence

    :param words:   The words to check
    :param lst:     The sentence to check
    :returns:       Count of matches
    """
    ws = []
    for word in words:
        ws.append(s_phonetic(word))

    count = 0
    # pad "." with extra spaces, so it's considered
    sentence = sentence.replace('.', ' . ')
    for i in sentence.split(' '):
        if s_phonetic(i) in ws:
            count += 1

    return count
