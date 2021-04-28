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
    res = []
    if "error" not in r:
        for dict in r["results"]:
            for key, value in dict.items():
                if key == "lexicalEntries":
                    for lexEnt in value:
                        for key, value in lexEnt.items():
                            if key == "entries":
                                for ent in value:
                                    for key, value in ent.items():
                                        if key == "senses":
                                            for sens in value:
                                                for key, value in sens.items():
                                                    if key == "definitions":
                                                        if len(res) == 0:
                                                            res.append(value[0])
                                                        else:
                                                            res.append("\t" + value[0])
                                                    elif key == "examples":
                                                        res[-1] += "\"" + value[0]["text"] + "\""
                                                    elif key == "subsenses":
                                                        for subsens in value:
                                                            for key, value in subsens.items():
                                                                if key == "definitions":
                                                                    res.append("\t\t" + value[0])
                                                                elif key == "examples":
                                                                    res[-1] += "\"" + value[0]["text"] + "\""

    return res


def process_file():
    filename = "wordList.txt"
    with open(filename) as f:
        word_list = f.readlines()
    pattern = re.compile(r'(?i)^(?:(?![×Þß÷þø])[\'0-9a-zÀ-ÿ\s])+')
    failed = []
    for line in word_list:
        word = pattern.search(line)
        if word is not None:
            req_res = send_req(word.group(0))
            res = process_req(req_res)
            if len(res)!=0:
                res[0] = word.group(0) + " - " + res[0]
            else:
                failed.append(word.group(0) + " - ")
            with open('output.txt', 'a') as f:
                for listitem in res:
                    f.write('%s\n' % listitem)
    with open('output.txt', 'a') as f:
        for listitem in failed:
            f.write('%s\n' % listitem)


process_file()
