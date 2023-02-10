from discord.ext import commands
import asyncio
from faq import FAQ
import yaml, json, requests, re, os, pickle
from data import wikiApiUrl, faqTitlesParams, faqTitlesTemplate, faqUpdateParams

def updateFaqFile(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def getFaqTitlesFromWiki(url):
    jsonTitles = json.loads(
        requests.get(url, params=faqTitlesParams).text
    )['query']['prefixsearch']

    return [element['title'] for element in jsonTitles]

def checkFaqLastUpdated(forceUpdate=False):
    date = ""
    if os.path.isfile(".faqlastupdated.pickle"):
        with open(".faqlastupdated.pickle", "rb") as file:
            date = pickle.load(file)

    rawData = requests.get(wikiApiUrl, params=faqUpdateParams).text
    updateData = json.loads(rawData)
    lastUpdated = updateData['query']['recentchanges'][0]['timestamp']
    
    isToBeUpdated = False
    if (date != lastUpdated) or forceUpdate:
        isToBeUpdated = True
        with open(".faqlastupdated.pickle", "wb") as file:
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

    updateFaqFile('faqdata/faqdata.yaml', "---\n"+"\n\n".join(faqPosts))

class faqCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("FAQ Cog is ready") 
        try:
            if checkFaqLastUpdated(forceUpdate=True):
                getFaqsFromWiki()
                print("FAQ Updated")
            else:
                print("FAQ in no need of update")
        except Exception as e:
            print(e)

    @commands.command()
    async def faqlist(self, ctx):
        with open("faqdata/faqaliases.yaml") as file:
            aliases = yaml.load(file, Loader=yaml.Loader)
        allAliases = sorted(aliases.keys())
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in allAliases:
            print(alias)
            message += f"**{alias}** - {aliases[alias]['description']}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"
        await ctx.send(message)

    @commands.command()
    async def faq(self, ctx):
        bot = self.bot
        label = " ".join(ctx.message.content.split()[1:])

        faq = FAQ(label)

        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                print("The end!")
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try:
                msg = await bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out!")
                return

            faq.check(msg)
            
async def setup(bot):
    await bot.add_cog(faqCog(bot))