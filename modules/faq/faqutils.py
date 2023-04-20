import json, requests, os, pickle, re
from utils.genUtils import loadYaml, saveYaml
import utils.queries as queries

faqDataPath = "./modules/faq/data"
faqFilePath = f"{faqDataPath}/faqaliases.yaml"

def updateFaqFile(filename: str, data: str):
    with open(filename, 'w') as file:
        file.write(data)

def getFaqTitlesFromWiki(url: str):
    jsonTitles = json.loads(
        requests.get(url, params=queries.faqTitlesParams).text
    )['query']['prefixsearch']

    return [element['title'] for element in jsonTitles]

def checkToBeUpdated(forceUpdate=False):
    picklePath = f"{faqDataPath}/.faqlastupdated.pickle"
    storedDates = ""
    if os.path.isfile(picklePath):
        with open(picklePath, "rb") as file:
            storedDates = pickle.load(file)

    scrapedDates = ""
    allFaqTitles = getFaqTitlesFromWiki(queries.wikiApiUrl)
    for faqTitle in allFaqTitles:
        rawData = requests.get(queries.wikiApiUrl, params=queries.getRecentChangesParams(faqTitle)).text
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
    faqPosts = []
    for title in getFaqTitlesFromWiki(queries.wikiApiUrl):
        faqPosts.append(
            re.sub(
                "</?pre>", "", 
                requests.get(
                    queries.faqTitlesTemplate.format(title)
                ).text
            )
        )

    updateFaqFile(f'{faqDataPath}/faqdata.yaml', "---\n"+"\n".join(faqPosts))

def getListOfFaqAliases():
    aliases = loadYaml(f"{faqDataPath}/faqaliases.yaml")
    return [(key, aliases[key]['description']) for key in sorted(aliases.keys())]

def addFaqAlias(name: str, label: str, description: str):
    aliases = loadYaml(faqFilePath)
    aliases[name] = {
        "label": label,
        "description": description
    }
    saveYaml(aliases, faqFilePath)

def removeFaqAlias(name: str):
    aliases = loadYaml(faqFilePath)
    popped = aliases.pop(name, False)
    saveYaml(aliases, faqFilePath)
  
    return popped