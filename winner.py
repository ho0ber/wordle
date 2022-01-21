from urllib.request import urlopen, Request
from datetime import date
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_winners():
    js_url = "https://www.powerlanguage.co.uk/wordle/main.c1506a22.js"
    headers = {"User-Agent": "Mozilla/5.0"}
    wordle_source_js = urlopen(Request(js_url, headers=headers)).read().decode("UTF-8")
    return re.search("La=\[(.+?)\],Ta", wordle_source_js).group(1).replace('"', "").split(",")

def get_winner(wordle_number=None):
    if wordle_number is None:
        wordle_number = (date.today() - date(2021,6,19)).days

    winners = get_winners()
    return winners[wordle_number]
