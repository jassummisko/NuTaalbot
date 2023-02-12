from bs4 import BeautifulSoup as bs
import requests as req

def ScrapeB1(word):
    site = bs(req.get(f"https://ishetb1.nl/search?word={word}").text)
    verdict = site.find("div", {"class": "ishetb1-verdict"})
    isHetB1 = verdict.find().text.strip()
    verklaring = verdict.find("div", {"class": "my-2"}).text.strip()
    alternatieven = site.find("ul", {"class": "border-l-2"})
    if alternatieven is not None:
        alternatieven = "__Alternatieven:__ " + (', '.join([a.text.strip() for a in alternatieven.find_all("li")]))
    else:
        alternatieven = ""

    return f"**{isHetB1}**. {verklaring} \n {alternatieven}"