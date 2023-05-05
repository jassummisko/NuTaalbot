import requests, json, dataclasses

@dataclasses.dataclass
class WordEntry:
    lemma: str
    partOfSpeech: str
    grammaticalInfo: dict

def scrapeWoordenlijst(woord: str):
    headers = {'Referer': 'https://woordenlijst.org/'}
    params = {
        'm': 'search',
        'searchValue': woord,
        'tactical': 'true',
    }
    response = requests.get('https://woordenlijst.org/api-proxy/', headers=headers, params=params)
    test = json.loads(response.text)
    lemmas = [w for w in filter(lambda x:x['lemma']==woord, test["_embedded"]['exact'])]
    return lemmas

def getLemma(woord: dict):
    return woord['lemma']

def getNounForms(noun: dict):
    dict = {}

    if 'gloss' in noun: dict['gloss'] = noun['gloss']
    else: dict['gloss'] = ''
    
    if 'art' in noun['gram']: dict['art'] = noun['gram']['art']
    else: dict['art'] = ''

    for form in noun['positions']:
        orth = form['forms'][0]['orth'].lower()
        if form['label'] == 'mv':       dict["pl"]   = orth
        if form['label'] == 'dim_ev':   dict["dim"]  = orth

    return dict

def getVerbForms(vrb: dict):
    dict = {}    
    for form in vrb['positions']:
        orth = form['forms'][0]['orth'].lower()
        if form['label'] == 'vtd':      dict["part"]  = orth
        if form['label'] == '1evovt':   dict["1pst"]  = orth
        if form['label'] == '1evott':   dict["1prs"]  = orth
    return dict

def getAdjectiveForms(adj: dict):
    dict = {}    
    for form in adj['positions']:
        orth = form['forms'][0]['orth'].lower()
        if form['label'] == 'verbogen': dict["vbg"]   = orth
        if form['label'] == 'com':      dict["com"]   = orth
        if form['label'] == 'sup':      dict["sup"]   = orth
    return dict

def getWordType(word: dict):
    keydict = {
        "NOU-C": "znw",
        "NOU-P": "znw",
        "VRB": "ww",
        "ADV": "bw",
        "COLL": "afk",
        "AA": "bnw",
        "CONJ": "ovw",
        "INT": "tsw",
        "NUM": "tw",
        "PD": "vnw",
        "ADP": "vz",
        "RES": "afk",
        "ART": "",
    }
    return keydict[word['gram']['pos']]

def getForms(word: dict):
    if word['gram']['pos'] == "NOU-C":  return getNounForms(word)
    if word['gram']['pos'] == "NOU-P":  return getNounForms(word)
    if word['gram']['pos'] == "VRB":    return getVerbForms(word)
    if word['gram']['pos'] == "AA":     return getAdjectiveForms(word)
    if word['gram']['pos'] == "NUM":    return getAdjectiveForms(word)
    return {}

def checkWoordenlijst(word: str) -> list[WordEntry] | None:
    words = scrapeWoordenlijst(word)
    if len(words) == 0: return None
    return [WordEntry(getLemma(word), getWordType(word), getForms(word)) for word in words]