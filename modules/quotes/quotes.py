from utils.genUtils import loadYaml, saveYaml
import discord, random, string, dataclasses
from discord.ext.commands import CommandError
from discord.ext import menus
from utils.genUtils import MultiPageEmbed

@dataclasses.dataclass
class Quote:
    id: str
    label: str
    text: str
    authorName: str
    authorId: str

quoteFilePath = "./modules/quotes/data/quotes.yaml"
quotes = loadYaml(quoteFilePath)

def getAllQuoteIds():
    quoteIds = []
    for _, entry in quotes.items(): 
        for item in entry: quoteIds.append(item['id'])
    return quoteIds

def generateUniqueQuoteId() -> str:
    def generateQuoteId() -> str:
        sel = string.ascii_lowercase + string.digits    
        code = ""
        for _ in range(5): code += random.choice(sel)
        return code
    while (quoteId := generateQuoteId()) in getAllQuoteIds(): pass 
    return quoteId

def createQuoteDict(quoteId: str, author: discord.Member, quote: str):
    return {
        'id': quoteId,
        'aid': author.id,
        'an': author.name,
        'txt': quote,
    }

def addQuote(author: discord.Member, label: str,  quote: str):
    label = label.upper()
    id = generateUniqueQuoteId()
    if not (label in quotes): quotes[label] = []
    quotes[label].append(createQuoteDict(id, author, quote))
    saveYaml(quotes, quoteFilePath)

def getQuote(label: str) -> str:
    label = label.upper()
    if not label in quotes: raise CommandError(f"Label {label} not found")
    return random.choice(quotes[label])

def getQuoteById(id: str):
    for lab in quotes:
        for item in quotes[lab]:
            if item['id'] == id:
                return item
    raise CommandError(f"ID {id} not found")

def removeQuote(id: str):
    for lab in quotes:
        for item in quotes[lab]:
            if item['id'] == id:
                quotes[lab].remove(item)
                cleanQuotes()
                return
    raise CommandError(f"ID {id} not found")

def cleanQuotes():
    quotes = {k: v for k, v in quotes.items() if v}
    saveYaml(quotes, quoteFilePath)

def getAllQuotes():
    allQuotes = []
    for lab in quotes:
        for item in quotes[lab]:
            allQuotes.append(Quote(item['id'], lab, item['txt'], item['an'], item['aid']))
    return allQuotes 

def getQuoteEmbed():
    allLines = []
    qs = getAllQuotes()
    qs = sorted(qs, key=lambda x: x.label)
    for q in qs: allLines.append(f"`{q.id}` {q.label} by {q.authorName}") 
    allDescs = []
    while len(allLines) > 15:
        allDescs.append("\n".join(allLines[0:15]))
        allLines = allLines[15:]
    allDescs.append("\n".join(allLines))

    pages = []
    for idx, desc in enumerate(allDescs):
        pages.append(discord.Embed(
            description = f"Page {idx+1} out of {len(allDescs)}\n\n{desc}"
        ))
    
    return menus.MenuPages(MultiPageEmbed(pages, per_page=1))