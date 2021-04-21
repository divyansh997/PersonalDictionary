import requests
import re
import json


def get_id_key():
    with open("idkey.txt") as f:
        new = f.readlines()
    return new[0].rstrip("\n"), new[1].rstrip("\n")

def send_req(word):
    app_id, app_key = get_id_key()
    language = "en-gb"
    url = "https://od-api.oxforddictionaries.com/api/v2/entries/" + language + "/" + word.lower() \
            + "?fields=definitions%2Cexamples&strictMatch=false"
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    return r

def process_req(req):
    r = req.json()
    print(r)

def process_file():
    with open("oneword.txt") as f:
        word_list = f.readlines()
    pattern = re.compile(r'(?i)^(?:(?![×Þß÷þø])[\'0-9a-zÀ-ÿ])+')
    for line in word_list:
        word = pattern.search(line)
        if word is not None:
            res = send_req(word.group(0))
            process_req(res)

process_file()

