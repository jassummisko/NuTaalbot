from bs4 import BeautifulSoup as bs
import requests as req, bs4

def ScrapeB1(word: str):
    site = bs(req.get(f"https://ishetb1.nl/search?word={word}").text)
    assert isinstance(verdict := site.find("div", {"class": "ishetb1-verdict"}), bs4.Tag)
    isHetB1 = verdict.find().text.strip() # type: ignore
    verklaring = verdict.find("div", {"class": "my-2"}).text.strip() # type: ignore
    alternatieven = site.find("ul", {"class": "border-l-2"})
    if alternatieven is not None:
        alternatieven = "__Alternatieven:__ " + (', '.join([a.text.strip() for a in alternatieven.find_all("li")])) # type: ignore
    else:
        alternatieven = ""

    return f"**{isHetB1}**. {verklaring} \n {alternatieven}"