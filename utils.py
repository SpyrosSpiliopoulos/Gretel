from bs4 import BeautifulSoup
import requests
import re

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

def get_cookie_info(cookie_name):
    page = requests.get("https://cookiepedia.co.uk/cookies/"+cookie_name)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs=soup.findAll('p')
    h2=soup.find('h2').getText()
    if not re.match("[sS]orry",h2):
        content=paragraphs[0].getText()
        purpose=paragraphs[1].getText()
        if not re.search("not yet",content):
            return content,purpose
    return None,None

def get_tracker_info(tracker):
    page = requests.get("https://better.fyi/trackers/"+tracker)
    soup = BeautifulSoup(page.content, 'html.parser')
    description=soup.find('p').getText()
    if not re.search("not find",description):
        return description
