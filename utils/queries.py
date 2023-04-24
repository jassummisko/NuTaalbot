faqTitlesTemplate = 'https://dutch.miraheze.org/wiki/{}?action=raw'
faqTitlesParams = {
    "format": "json",
    "list": "prefixsearch",
    "action": "query",
    "pssearch": "Taalbot/faq/",
    "pslimit": 500
}
wikiApiUrl = 'https://dutch.miraheze.org/w/api.php'
faqUpdateParams = {
    "format": "json",
    "list": "recentchanges",
    "action": "query",
    "rclimit": "1",
    "rctitle": "Taalbot/faq"
}

def getRecentChangesParams(title):
    return {
        "format": "json",
        "list": "recentchanges",
        "action": "query",
        "rclimit": "1",
        "rctitle": title
    }