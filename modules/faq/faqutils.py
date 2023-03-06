import json, requests, os, pickle, re, yaml
from utils import loadYaml, saveYaml
from data import wikiApiUrl, getRecentChangesParams

faqDataPath = "./modules/faq/data"
faqFilePath = f"{faqDataPath}/faqaliases.yaml"

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

    updateFaqFile(f'{faqDataPath}/faqdata.yaml', "---\n"+"\n".join(faqPosts))

def getListOfFaqAliases():
    aliases = loadYaml(f"{faqDataPath}/faqaliases.yaml")
    faqList = [(key, aliases[key]['description']) for key in sorted(aliases.keys())]
    return faqList

def addFaqAlias(name, label, description):
    aliases = loadYaml(faqFilePath)
    aliases[name] = {
        "label": label,
        "description": description
    }
    saveYaml(aliases, faqFilePath)

def removeFaqAlias(name):
    aliases = loadYaml(faqFilePath)
    popped = aliases.pop(name, False)
    saveYaml(aliases, faqFilePath)
  
    return popped