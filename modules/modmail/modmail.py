from utils.genUtils import saveYaml, loadYaml
from os.path import isfile as fileExists
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Mail:
    message: str
    author: str
    date: datetime

def NewMail(message: str, author: str = "/", date: datetime|None = None) -> Mail:
    if date == None: date = datetime.utcnow() 
    return Mail(message, author, date)

def MailAsDict(mail: Mail) -> dict:
    return {
        "message": mail.message,
        "author": mail.author,
        "date": mail.date.isoformat(),
    }

def DictAsMail(d: dict) -> Mail:
    message = d.get("message")
    author = d.get("author", "/")
    date = d.get("date")

    assert message
    if not date: date = datetime(1,1,1,1,1)

    return NewMail(message, author, date)

def AddNewMailToInbox(mail: Mail):
    inbox_path = "modules/modmail/data/mail.yaml"

    if fileExists(inbox_path): currentInbox = loadYaml(inbox_path)
    else: currentInbox = {}

    if not 'mail' in currentInbox: currentInbox['mail'] = []
    currentInbox['mail'].append(MailAsDict(mail))

    saveYaml(currentInbox, "modules/modmail/data/mail.yaml")