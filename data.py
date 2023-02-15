from enum import Enum

kelderID = 824352622605500416
faqTitlesTemplate = 'https://dutch.miraheze.org/wiki/{}?action=raw'
faqTitlesParams = {
    "format": "json",
    "list": "prefixsearch",
    "action": "query",
    "pssearch": "Taalbot/faq/"
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

class staffRoles(Enum): 
    Moderator = 527510064941105183
    Developer = 656502076062564382
    Mentor = 259993681950408704
    Admin = 1074343711602917396
    Staff = 1074395170423980046

emojiAnsweredID = 1075380174381649963
tagAnsweredID = 1075378374043771001