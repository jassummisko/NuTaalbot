from utils.genUtils import saveYaml, loadYaml
from os.path import isfile as fileExists
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MailType(Enum):
    OTHER = 0
    FEEDBACK = 1
    REPORT = 2
    NIVEAU = 3
    SESSIE = 4
    BOT = 5

@dataclass
class Mail:
    message: str
    mailtype: MailType
    author: str
    date: datetime

def newMail(
    message: str, 
    mailtype: MailType,
    author: str = "/",
    date: datetime|None = None) -> Mail:
    if date == None: date = datetime.utcnow() 
    return Mail(message, mailtype, author, date)

def mailAsDict(mail: Mail) -> dict:
    return {
        "message": mail.message,
        "mailtype": mail.mailtype.value,
        "author": mail.author,
        "date": mail.date.isoformat(),
    }

def dictAsMail(d: dict) -> Mail:
    message = d.get("message")
    mailtype = d.get("mailtype")
    author = d.get("author", "/")
    date = d.get("date")

    assert message
    if not mailtype: mailtype = MailType.OTHER
    if not date: date = datetime(1,1,1,1,1)

    return newMail(message, mailtype, author, date)

def addNewMailToInbox(mail: Mail):
    inbox_path = "modules/modmail/data/mail.yaml"

    if fileExists(inbox_path): currentInbox = loadYaml(inbox_path)
    else: currentInbox = {}

    if not 'mail' in currentInbox: currentInbox['mail'] = []
    currentInbox['mail'].append(mailAsDict(mail))

    saveYaml(currentInbox, "modules/modmail/data/mail.yaml")