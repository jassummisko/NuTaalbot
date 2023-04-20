from utils.genUtils import loadYaml, saveYaml
import discord, random, string

quoteFilePath = "./modules/quotes/data/quotes.yaml"

quotes = loadYaml(quoteFilePath)
quoteIds = []
for _, entry in quotes.items(): 
    for item in entry: quoteIds.append(item['id'])

def generateUniqueQuoteId() -> str:
    def generateQuoteId() -> str:
        sel = string.ascii_lowercase + string.digits    
        code = ""
        for _ in range(5): code += random.choice(sel)
        return code
    while (quoteId := generateQuoteId()) in quoteIds: pass 
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
    quoteIds.append(id)
    saveYaml(quotes, quoteFilePath)

def getQuote(label: str) -> str:
    label = label.upper()
    assert label in quotes, f"Label {label} not found"
    return random.choice(quotes[label])

def removeQuote(id: str):
    assert id in quoteIds, f"ID {id} not found"
    quoteIds.remove(id)
    for lab in quotes:
        for item in quotes[lab]:
            if item['id'] == 'id':
                quotes[lab].remove(item)
                break
    saveYaml(quotes, quoteFilePath)