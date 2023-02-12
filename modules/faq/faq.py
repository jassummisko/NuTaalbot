import json, requests, os, pickle, re
from random import choice
from utils import loadYaml
from modules.faq.faqResponses import correct, wrong
from data import wikiApiUrl, getRecentChangesParams

faqDataPath = "./modules/faq/data"

def updateFaqFile(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def getFaqTitlesFromWiki(url):
    from data import faqTitlesParams
    jsonTitles = json.loads(
        requests.get(url, params=faqTitlesParams).text
    )['query']['prefixsearch']

    return [element['title'] for element in jsonTitles]

def checkToBeUpdated(forceUpdate=False):
    from data import faqUpdateParams
    picklePath = f"{faqDataPath}/.faqlastupdated.pickle"
    storedDates = ""
    if os.path.isfile(picklePath):
        with open(picklePath, "rb") as file:
            storedDates = pickle.load(file)

    scrapedDates = ""
    allFaqTitles = getFaqTitlesFromWiki(wikiApiUrl)
    for faqTitle in allFaqTitles:
        rawData = requests.get(wikiApiUrl, params=getRecentChangesParams(faqTitle)).text
        updateData = json.loads(rawData)
        lastUpdated = updateData['query']['recentchanges'][0]['timestamp']
        scrapedDates += faqTitle+"|"+lastUpdated+"||"
    
    isToBeUpdated = False
    if (storedDates != scrapedDates) or forceUpdate:
        isToBeUpdated = True
        with open(picklePath, "wb") as file:
            pickle.dump(scrapedDates, file)

    return isToBeUpdated

def getFaqsFromWiki():
    from data import faqTitlesTemplate
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
    aliases = loadYaml(f"{faqDataPath}/faqaliases.yaml")
    faqList = [(key, aliases[key]['description']) for key in sorted(aliases.keys())]
    return faqList

class FAQ:
    def __init__(self, startingLabel):
        self._data = loadYaml(f"{faqDataPath}/faqdata.yaml")
        aliases = loadYaml(f"{faqDataPath}/faqaliases.yaml") 
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
        if msg.content.strip().lower() in ["!stop_faq", "!stopfaq", "!faqstop", "!faq_stop"]:
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