import discord

# General responses
def ELK_ZINNEN_DAH() -> str: 
    return "Elk zinnen dah!"
def USE_SLASH_COMMANDS(real_command: str, used_command: str) -> str: 
    return f"We have migrated to slash commands. Please use `/{real_command}` instead of `!{used_command}`."
def NOT_STAFF_ERROR() -> str: 
    return "You must be a staff member to use this command."
def NOT_POST_OWNER_ERROR() -> str: 
    return "You must be the owner of the post."
def NOT_POST_OWNER_OR_STAFF_ERROR() -> str: 
    return "You must be the owner of the post or a staff member"
def THREAD_ALREADY_ANSWERED() -> str: 
    return "Thread already marked as answered"
def THREAD_ANSWERED() -> str: 
    return "Thread marked as answered"
def TIMED_OUT() -> str: 
    return "Timed out!"

# Role manager responses
def ROLE_GIVEN(roleName: str) -> str: 
    return f"Role '{roleName}' given"
def ROLE_REMOVED(roleName: str) -> str: 
    return f"Role '{roleName}' removed"

# Channel manager responses
def NOT_IN_FORUM_ERROR() -> str: 
    return "Not in forum"
def NOT_IN_KELDER_ERROR() -> str: 
    return "Je zit niet in #kelder"
def KELDER_LIMIET_ERROR() -> str: 
    return "De limiet moet tussen 3 en 8 liggen."
def KELDER_LIMIER_UPDATED(limit: int) -> str: 
    return f"De limiet is nu {limit}."

# FAQ responses
def UPDATING_FAQ() -> str: 
    return f"Updating FAQs..."
def FAQ_UPDATED() -> str: 
    return f"FAQ_s Updated"
def RUNNING_FAQ(label: str) -> str: 
    return f"Running FAQ {label}"
def FAQ_ENDED() -> str: 
    return f"FAQ ended."
def FAQ_DEREGISTERED(faqName: str) -> str: 
    return f"FAQ '{faqName}' verwijderd."
def FAQ_REGISTERED(faqName: str, label: str) -> str: 
    return f"FAQ '{faqName}' is geregistreerd met label '{label}' als begin."
def NOT_FAQ_ERROR(faqName: str) -> str: 
    return f"Er zit geen FAQ met de '{faqName}' in de lijst."

# Scraper responses
def DEHET_NOWORD(woord: str) -> str: 
    return f"Ik heb geen woorden kunnen vinden voor '{woord}'"
def DEHET_NONOUN(woord: str) -> str: 
    return f"Ik heb geen substantieven kunnen vinden voor '{woord}'"
def DEHET_SINGLEWORD(lidwoord: str, woord: str) -> str: 
    return f"\"**{lidwoord}** {woord}\""
def DEHET_MULTIWORD(lidwoord: str, woord: str, betekenis: str) -> str: 
    return f"\"**{lidwoord}** {woord}\" met de betekenis \"{betekenis}\"\n"

# Mod mail responses
def MAIL_EMBED_RECEIVED(message: str, author: str) -> discord.Embed:
    if author == "/": author = "Anonymous"
    return discord.Embed(
                title="Mail received",
                description=message,
            ).set_footer(text=author)
def MAIL_ISANON() -> str: return "Would you like to send the message anonymously? Type \"yes\" to send anonymously or \"no\" to have your name shown. Keep in mind that sending anonymous mail means that the staff cannot respond to your message."
def MAIL_CHOOSE_MAILTYPE() -> str: return """What kind of mail are you sending?
```
1. A user report
2. A complaint about the server or staff team
3. A suggestion for the staff
0. Other
```
Type the number as a message"""
def MAIL_TYPE_YOUR_MESSAGE() -> str: return "You may now type your message. You will be given a chance to edit the message before sending."
def MAIL_TYPE_SEND() -> str: return "If you have no more edits to make, type \"send\" to send the message."
def MAIL_SENT(recipient: str) -> str: return f"Your message has been sent to {recipient}."
def MAIL_REPLY_WITH_SENDMESSAGE() -> str: return "Reply to the message using the command `!!!sendmessage` send it."
def MAIL_NO_SPAM() -> str: return "You've already sent 3 modmails today. Please wait until tomorrow."
def MAIL_TIMED_OUT() -> str: return  "Your request timed out. Please start the mod mail process over."
def MAIL_USE_SENDMAIL(cmd: str) -> str: return f"If you want to send mod mail, first type the message \"{cmd}\"."
def MAIL_NOT_IN_THREAD() -> str: return "Not in thread."
def MAIL_NOT_IN_FORUM() -> str: return "Not in forum channel."
def MAIL_NOT_IN_MAIL_CHANNEL() -> str: return "Not in mail channel."
def MAIL_NO_REPLY_MESSAGE() -> str: return "No reply message found."
def MAIL_NOT_APPROVED(needed_count: int) -> str: return f"The message has not been approved by enough staff members ({needed_count}). Place 📨 as a reaction to the message to approve it."
def MAIL_RESPOND() -> str: return "If you would like to respond to this user, reply to a given message using `!!!sendmessage`."

