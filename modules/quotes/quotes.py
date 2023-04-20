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

def addQuote(author: discord.Member, trigger: str,  quote: str):
    if not (trigger in quotes): quotes[trigger] = []
    quotes[trigger].append(createQuoteDict(generateUniqueQuoteId(), author, quote))
    saveYaml(quotes, quoteFilePath)

def getQuote(trigger: str) -> str:
    trigger = trigger.lower()
    if trigger in quotes: return random.choice(quotes[trigger])
    return None