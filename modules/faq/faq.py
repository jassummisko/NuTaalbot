import json, requests, os, pickle, re
from random import choice
from utils import loadYaml
from modules.faq.faqResponses import correct, wrong
from modules.faq.faqutils import *

class FAQ:
    def __init__(self, startingLabel, debug=False):
        self._data = loadYaml(f"{faqDataPath}/faqdata.yaml")
        aliases = loadYaml(f"{faqDataPath}/faqaliases.yaml")
        if debug and (startingLabel in self._data):
            self._label = startingLabel
        elif (startingLabel := startingLabel.lower()) in aliases:
            self._label = aliases[startingLabel]['label']
        else:
            self._message = f"No FAQ found with name '{startingLabel}'\nUse `!faqlist` for a full list of FAQs."
            self.isEnd = True
            return
        self.caseSensitive = False
        self.isEnd = False
        self.updateMessage()
        self.checkParams()

    def getMessage(self): return self._message 

    def checkParams(self):
        labelData = self._data[self._label]
        self.caseSensitive = False
        if "CASE" in labelData: self.caseSensitive = labelData["CASE"]
        if "END" in labelData and labelData["END"]: self.isEnd = True

    def updateMessage(self, prefix=""):
        message = self._data[self._label]["MESSAGE"]
        self._message = f"{prefix}\n{message}".strip()

    def check(self, msg):
        if msg.content.strip().lower() in ["!stop_faq", "!stopfaq", "!faqstop", "!faq_stop"]:
            self.isEnd, self._message = True, "FAQ stopped manually."
            return
        labelData = self._data[self._label]
        answers = labelData["ANSWERS"]
        answer = msg.content.strip()
        if not self.caseSensitive:
            answer = answer.upper()
            answers = {answer.upper(): answers[answer] for answer in answers}
        if answer in answers:
            self.switchToLabel(answers[answer])
            prefix = choice(correct) if "MATCH" not in labelData else labelData["MATCH"]
            self.updateMessage(prefix)
        else:
            self._message = choice(wrong) if "NO_MATCH" not in labelData else labelData["NO_MATCH"]
    
    def switchToLabel(self, label):
        self._label = label
        self.checkParams()