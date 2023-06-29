from taalbot import BOT

with open(".token", "r") as file: TOKEN = file.read()

BOT.run(TOKEN)