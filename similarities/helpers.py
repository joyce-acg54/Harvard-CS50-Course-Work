from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    linesa = set(a.split("\n"))
    linesb = set(b.split("\n"))

    return linesa & linesb


def sentences(a, b):
    """Return sentences in both a and b"""

    sena = set(sent_tokenize(a))
    senb = set(sent_tokenize(b))

    return sena & senb


def substring_tokenize(str, n):
    sub = []

    for i in range(len(str) - n + 1):
        sub.append(str[i:i + n])

    return sub


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    suba = set(substring_tokenize(a, n))
    subb = set(substring_tokenize(b, n))

    return suba & subb
