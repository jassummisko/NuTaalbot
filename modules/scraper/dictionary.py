from dataclasses import dataclass
import discord

@dataclass
class DictEntry:
    voorvoegsel: str
    lemma: str
    ipa: str
    woordsoort: str
    vormen: str
    erk: str
    definitie: str
    voorbeeld: str

def CreateEntry(d) -> DictEntry: #d is a raw entry
    voorvoegsel = d.iloc[0] 
    lemma = str(d.get("Lemma", "/")).replace("*", "")
    ipa = str(d.get("Fonetisch", "/")).replace("*", "")
    woordsoort = str(d.get("Woordsoort", "/")).replace("*", "")
    vormen = str(d.get("Vormen", "/")).replace("*", "")
    erk = str(d.get("ERK", "/")).replace("*", "")
    definitie = str(d.get("Synoniem of definitie", "/")).replace("*", "")
    voorbeeld = str(d.get("Voorbeeldzin", "/")).replace("*", "")

    return DictEntry(
        voorvoegsel,
        lemma,
        ipa,
        woordsoort,
        vormen,
        erk,
        definitie,
        voorbeeld,
    )

def FormatNoun(de: DictEntry) -> discord.Embed:
    embed: discord.Embed

    title = f"Lemma: {de.voorvoegsel} {de.lemma}"
    
    description = f"[{de.ipa}]\n"
    description += f"__Vormen:__ {de.vormen.replace('*', '')}\n"
    description += f"__ERK-niveau:__ {de.erk}\n"
    description += f"__Definitie:__ {de.definitie}\n"
    description += f"__Voorbeeldzin:__ {de.voorbeeld}\n"
    description = description.strip()

    footer = "zelfstandig naamwoord (substantief)"

    embed = discord.Embed(title=title,description=description).set_footer(text=footer)

    return embed

def FormatVerb(de: DictEntry) -> discord.Embed:
    embed: discord.Embed

    title = f"Lemma: {de.lemma}"
    
    description = f"[{de.ipa}]\n"
    description += f"__Vormen:__ {de.vormen.replace('*', '')}\n"
    description += f"__ERK-niveau:__ {de.erk}\n"
    description += f"__Definitie:__ {de.definitie}\n"
    description += f"__Voorbeeldzin:__ {de.voorbeeld}\n"
    description = description.strip()

    footer = "werkwoord (verbum)"

    embed = discord.Embed(title=title,description=description).set_footer(text=footer)

    return embed

def GetAppropriateEmbed(de: DictEntry) -> discord.Embed:
    if "znw" in de.woordsoort:
        return FormatNoun(de)
    elif "ww" in de.woordsoort:
        return FormatVerb(de)

    raise Exception("Word type not found")
