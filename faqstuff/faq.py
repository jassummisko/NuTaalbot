import yaml
from random import choice
from faqResponses import correct, wrong

class FAQ:
    def __init__(self, startingLabel):
        with open("faqdata/faqdata.yaml") as file:
            self._data = yaml.load(file, Loader=yaml.Loader)
        with open("faqdata/faqaliases.yaml") as file:
            aliases = yaml.load(file, Loader=yaml.Loader)
        if (startingLabel := startingLabel.lower()) in aliases:
            self._label = aliases[startingLabel]['label']
        else:
            self._message = f"No FAQ found with name '{startingLabel}'"
            self.isContinue = False
            return
        self.isContinue = True
        self.updateMessage()

    def getMessage(self): return self._message 

    def updateMessage(self, prefix=""):
        message = self._data[self._label]["MESSAGE"]
        self._message = f"{prefix}\n{message}".strip()

    def check(self, msg):
        if msg.content.strip() == "!stop_faq":
            self.isContinue, self._message = False, "FAQ stopped"
            return
        labelData = self._data[self._label]
        answers = labelData["ANSWERS"]
        if (answer := msg.content.strip()) in answers:
            self.switchToLabel(answers[answer])
            prefix = choice(correct) if "MATCH" not in labelData else labelData["MATCH"]
            self.updateMessage(prefix)
        else:
            self._message = choice(wrong) if "NO_MATCH" not in labelData else labelData["NO_MATCH"]
        
    def switchToLabel(self, label):
        self._label = label
        labelData = self._data[self._label]
        if "END" in labelData and labelData["END"]: self.isContinue = False