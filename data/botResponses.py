# General responses
def ELK_ZINNEN_DAH(): 
    return "Elk zinnen dah!"
def USE_SLASH_COMMANDS(real_command: str, used_command: str): 
    return f"We have migrated to slash commands. Please use `/{real_command}` instead of `!{used_command}`."
def NOT_STAFF_ERROR(): 
    return "You must be a staff member to use this command."
def NOT_POST_OWNER_ERROR(): 
    return "You must be the owner of the post."
def NOT_POST_OWNER_OR_STAFF_ERROR(): 
    return "You must be the owner of the post or a staff member"
def THREAD_ALREADY_ANSWERED(): 
    return "Thread already marked as answered"
def THREAD_ANSWERED(): 
    return "Thread marked as answered"
def TIMED_OUT(): 
    return "Timed out!"

# Role manager responses
def ROLE_GIVEN(roleName: str): 
    return f"Role '{roleName}' given"

def ROLE_REMOVED(roleName: str): 
    return f"Role '{roleName}' removed"

# Channel manager responses
def NOT_IN_FORUM_ERROR(): 
    return "Not in forum"
def NOT_IN_KELDER_ERROR(): 
    return "Je zit niet in #kelder"
def KELDER_LIMIET_ERROR(): 
    return "De limiet moet tussen 3 en 8 liggen."
def KELDER_LIMIER_UPDATED(limit: int): 
    return f"De limiet is nu {limit}."

# FAQ responses
def UPDATING_FAQ(): 
    return f"Updating FAQs..."
def FAQ_UPDATED(): 
    return f"FAQ_s Updated"
def RUNNING_FAQ(label: str): 
    return f"Running FAQ {label}"
def FAQ_ENDED(): 
    return f"FAQ ended."
def FAQ_DEREGISTERED(faqName: str): 
    return f"FAQ '{faqName}' verwijderd."
def FAQ_REGISTERED(faqName: str, label: str): 
    return f"FAQ '{faqName}' is geregistreerd met label '{label}' als begin."
def NOT_FAQ_ERROR(faqName: str): 
    return f"Er zit geen FAQ met de '{faqName}' in de lijst."

# Scraper responses
def DEHET_NOWORD(woord: str): 
    return f"Ik heb geen woorden kunnen vinden voor '{woord}'"
def DEHET_NONOUN(woord: str): 
    return f"Ik heb geen substantieven kunnen vinden voor '{woord}'"
def DEHET_SINGLEWORD(lidwoord: str, woord: str): 
    return f"\"**{lidwoord}** {woord}\""
def DEHET_MULTIWORD(lidwoord: str, woord: str, betekenis: str): 
    return f"\"**{lidwoord}** {woord}\" met de betekenis \"{betekenis}\"\n"