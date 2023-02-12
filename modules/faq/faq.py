import yaml, json, requests, os, pickle, re
from random import choice
from modules.faq.faqResponses import correct, wrong
from data import wikiApiUrl, faqTitlesParams, faqTitlesTemplate, faqUpdateParams

faqDataPath = "./modules/faq/data"

def updateFaqFile(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def getFaqTitlesFromWiki(url):
    jsonTitles = json.loads(
        requests.get(url, params=faqTitlesParams).text
    )['query']['prefixsearch']

    return [element['title'] for element in jsonTitles]

def checkToBeUpdated(forceUpdate=False):
    picklePath = f"{faqDataPath}/.faqlastupdated.pickle"
    date = ""
    if os.path.isfile(picklePath):
        with open(picklePath, "rb") as file:
            date = pickle.load(file)

    rawData = requests.get(wikiApiUrl, params=faqUpdateParams).text
    updateData = json.loads(rawData)
    lastUpdated = updateData['query']['recentchanges'][0]['timestamp']
    
    isToBeUpdated = False
    if (date != lastUpdated) or forceUpdate:
        isToBeUpdated = True
        with open(picklePath, "wb") as file:
            pickle.dump(lastUpdated, file)

    return isToBeUpdated

def getFaqsFromWiki():
    faqPosts = []
    for title in getFaqTitlesFromWiki(wikiApiUrl):
        faqPosts.append(
            re.sub(
                "</?pre>", "", 
                requests.get(
                    faqTitlesTemplate.format(title)
                ).text
            )
        )

    updateFaqFile(f'{faqDataPath}/faqdata.yaml', "---\n"+"\n\n".join(faqPosts))

def getListOfFaqAliases():
    with open(f"{faqDataPath}/faqaliases.yaml") as file:
        aliases = yaml.load(file, Loader=yaml.Loader)
    faqList = [(key, aliases[key]['description']) for key in sorted(aliases.keys())]
    return faqList

class FAQ:
    def __init__(self, startingLabel):
        with open(f"{faqDataPath}/faqdata.yaml") as file:
            self._data = yaml.load(file, Loader=yaml.Loader)
        with open(f"{faqDataPath}/faqaliases.yaml") as file:
            aliases = yaml.load(file, Loader=yaml.Loader)
        if (startingLabel := startingLabel.lower()) in aliases:
            self._label = aliases[startingLabel]['label']
        else:
            self._message = f"No FAQ found with name '{startingLabel}'"
            self.isEnd = True
            return
        self.caseSensitive = False
        self.isEnd = False
        self.updateMessage()
        self.checkParams()

    def getMessage(self): return self._message 

    def checkParams(self):
        labelData = self._data[self._label]
        self.caseSensitive = False
        if "CASE" in labelData: self.caseSensitive = labelData["CASE"]
        if "END" in labelData and labelData["END"]: self.isEnd = True

    def updateMessage(self, prefix=""):
        message = self._data[self._label]["MESSAGE"]
        self._message = f"{prefix}\n{message}".strip()

    def check(self, msg):
        if msg.content.strip() == "!stop_faq":
            self.isEnd, self._message = True, "FAQ stopped"
            return
        labelData = self._data[self._label]
        answers = labelData["ANSWERS"]
        answer = msg.content.strip()
        if not self.caseSensitive:
            answer = answer.upper()
            answers = {answer.upper(): answers[answer] for answer in answers}
        if answer in answers:
            self.switchToLabel(answers[answer])
            prefix = choice(correct) if "MATCH" not in labelData else labelData["MATCH"]
            self.updateMessage(prefix)
        else:
            self._message = choice(wrong) if "NO_MATCH" not in labelData else labelData["NO_MATCH"]
    
    def switchToLabel(self, label):
        self._label = label
        self.checkParams()