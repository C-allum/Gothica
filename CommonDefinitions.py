from ast import Index, Pass, excepthandler
from dis import dis, disco
from email import message_from_string
from hashlib import new
from json.decoder import JSONDecoder
from logging import currentframe, exception, lastResort, log
from ntpath import join
from posixpath import split
from pydoc import describe
#from selectors import EpollSelector
from sqlite3 import Timestamp
from typing import MutableSet
from unittest.loader import VALID_MODULE_NAME
import discord
import os
import random
import re
import asyncio
import math
import copy

import datetime, time
from discord import message
from discord import guild
from discord import channel
from discord import player
from discord import embeds
from discord.utils import get
from discord.embeds import Embed
from discord.enums import NotificationLevel
from discord.ext import commands
from datetime import date, datetime, timedelta
from discord.ext.commands.errors import NoPrivateMessage

from discord.gateway import DiscordClientWebSocketResponse
from discord.guild import Guild
from discord.utils import sleep_until

from googleapiclient.discovery import build
from google.oauth2 import service_account
from pyasn1.type.univ import Enumerated
from pyasn1_modules.rfc2459 import ExtensionPhysicalDeliveryAddressComponents, Name, RelativeDistinguishedName
from pyasn1_modules.rfc5208 import PrivateKeyInfo
from random import sample

import botTokens

intents = discord.Intents().all()

client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix='%', activity = discord.Game(name="Testing Stuff"), intents = intents)

print(" Initialised {0.user} at ".format(client) + str(datetime.now()).split(".")[0])

#-----------------LIVE VERSION/BETA TOGGLE---------------
liveVersion = 0
token = ""

#Sheet Locations:

if liveVersion: #Set to 1 to use the real spreadsheets, or 0 to use the testing spreadsheets.

    CharSheet = "1iHvP4HC8UQqyiMmC3Xiggx8-17e5SGWJMncEeoiZP1s"

    EconSheet = "1qTC0gn7Fe_cHDVPB8KIEjSFUwrUSEhlLy1upHIKnKF8"

    shopsheet = "1gxNPXIichzK9mSN8eHYVdJvaaUgUnN6VF8WshL_4Les"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg"

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4"

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA"

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU"

    Randomlootsheet = "19Dc4PI-E5OubesNroJfB4zKg9bqqqbdPelodjH6ecNw"

    logchannel = 918257057428279326

    bridgechannel = 996826636358000780

else:

    CharSheet = "1Vgxa8C5j5XnEUGhaGqAANVhsWSIOra87wCE2f5C75tQ"

    EconSheet = "1mmWxHhDUPI0PjLC2UXJZmj5wNqXnucFMz-er9NpVC2c"

    shopsheet = "1r_1tYCGtmanRkTGsfAz4WrOSUoi6roO-zYRHACQBD90"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg" #No change as yet

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4" #No change as yet

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA" #No change as yet

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU" #No change as yet

    Randomlootsheet = "19Dc4PI-E5OubesNroJfB4zKg9bqqqbdPelodjH6ecNw"

    logchannel = 1031701327169998958 #Test Server

    bridgechannel = 891781900388159528

SERVICE_ACCOUNT_FILE = "keys.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build("sheets", "v4", credentials=creds)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId = CharSheet, range = "E1:Y1").execute()
values = str(result.get("values"))
values = values.replace("'","")
headers = values.split(",")

namecol = 4

for i in range(len(headers)):
    headers[i] = headers[i].lstrip(" ")
    headers[i] = headers[i].lstrip("[")
    headers[i] = headers[i].rstrip("]")

#channels
if liveVersion:
    kinkcreatechannel = "1050503346374594660"
else: 
    kinkcreatechannel = "891781900388159528"
#Sheets

aliases = sheet.values().get(spreadsheetId = "1xGL06_MrOb5IIt2FHJFeW_bdcwedIKZX-j3m2djSOaw", range = "A1:T50", majorDimension='COLUMNS').execute().get("values")

plothooks = sheet.values().get(spreadsheetId = Plotsheet, range = "A2:O50", majorDimension='COLUMNS').execute().get("values")

workhooks = sheet.values().get(spreadsheetId = Plotsheet, range = "AO2:AO100", majorDimension='COLUMNS').execute().get("values")

sluthooks = sheet.values().get(spreadsheetId = Plotsheet, range = "AP2:AQ100", majorDimension='COLUMNS').execute().get("values")

rooms = ["the Unlit Passageways", "the Trapped Corridors", "the Moaning Hallways", "the Salamander Hot Springs", "the Monster Girl Cantina", "the Old Burlesque", "the Library of Carnal Knowledge", "the Cathedral", "the Gobblin' Bazaar", "the Fighting Pits"]

guildvar = client.get_guild(828411760365142076)

myprefix = "%"

dezzieemj = "<:dz:844365871350808606>"

critemj = "<:crit:893767145060696064>"

embcol = 0xb700ff

indexchannel = 898640028174016552

awaitingsel = 0

prevchan = 0

selopts = []

column = ["F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB"]

#This defines the art forum channel for the cuffs emote
artClaimForumID = 1050252064455925790

#These variables define which channels are toggled with %vacation
LKVacationChannels = [912559434969022534, 996826636358000780, 1058951770870657166, 1008283892177965106]
ModVacationChannels = [829477815782866956]

#----------------EconomyValues----------------

reactdz = 20
reactCashMoney = 100
reactMakeItRain = 200

weeklyDezziePoolVerified = 500
weeklyDezziePoolP1 = 650
weeklyDezziePoolP2 = 800
weeklyDezziePoolP3 = 1000

weeklyDezzieBonusFucksmith = 500
weeklyDezzieBonusBoost = 100
weeklyDezzieBonusVeteran = 100

sellpricemultiplier = 0.5 #Use this to change how much things are sold for, relative to their purchase price

#----------------KinkValues----------------

rarities = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary"]

commonpercent = 30
uncommonpercent = 70
rarepercent = 95
veryrarepercent = 98

limitloopmax = 5 #The number of attempts to generate loot if limits are found

races = ["dragonborn", "dwarf", "elf", "gnome", "half-elf", "halfling", "half-orc", "human", "tiefling", "leonin", "satyr", "owlin", "aarakocra", "aasimar", "air genasi", "bugbear", "centaur", "changeling", "deep gnome", "duergar", "earth genasi", "eladrin", "fairy", "firbolg", "fire genasi", "githyanki", "githzerai", "goblin", "goliath", "harengon", "hobgoblin", "kenku", "kobold", "lizardfolk", "minotaur", "orc", "sea elf", "shadar-kai", "shifter", "tabaxi", "tortle", "triton", "water genasi", "yuan-ti", "kalashtar", "warforged", "astral elf", "autognome", "giff", "hadozee", "plasmoid", "loxodon", "simic hybrid", "vedalken", "verdan", "locathah", "grung", "babbage", "seedling", "chakara"]
colours = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black", "white", "transparent", "cream", "luminous pink"]
materials = ["stone", "wood", "brass", "marble", "bone", "glass", "crystalised lust", "a strange glowing material", "solid gold", "beeswax"]
sextoys = ["dildo", "butt-plug", "set of anal beads", "cock-sleeve", "penis ring", "set of ben wa balls", "cock cage", "double ended dildo", "set of nipple clamps"]
sextoykinks = [["Dildos", "Strap-Ons"], ["Butt Plugs"], ["Butt Plugs"], [], [], ["Male Chastity Devices"], ["Dildos", "Female:Female"], ["Light Torture"]]
gags = ["ball", "bit", "butterfly", "cleave", "dildo", "bandit", "fornophilic" "inflatable", "knotted", "mouth corset", "mouthguard", "muzzle", "ring", "rope", "spider", "tube"]
gagkinks = [[], ["Ponyplay"], [], ["Bondage"], ["Dildos"], [], ["Objectification"], [], [], ["Bondage"], [], ["Petplay"], ["Male Oral Sex (Blowjob/Fellatio)"], ["Bondage"], ["Male Oral Sex (Blowjob/Fellatio)"], ["Male Oral Sex (Blowjob/Fellatio)"]]
sizes = ["tiny", "small", "medium", "large", "huge", "gargantuan", "fucking gigantic"]

#---------------------------------------------

def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return inner_check

def checkstr(author):
    def inner_check(message): 
        if message.author != author:
            return False
        str(message.content) 
        return True 
    return inner_check

def checkAuthor(author):
    def inner_check(message):
        if message.author != author:
            return False
        else: return True
    return inner_check

def fracture(word):
    return [str(char) for char in word]

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def reactletters(reacts):

    emojis = ""

    for n in range(len(reacts)):

        if reacts[n] == "A":

            emojis += "🇦"

        elif reacts[n] == "B":

            emojis += "🇧"

        elif reacts[n] == "C":

            emojis += "🇨"

        elif reacts[n] == "D":

            emojis += "🇩"

        elif reacts[n] == "E":

            emojis += "🇪"

        elif reacts[n] == "F":

            emojis += "🇫"

        elif reacts[n] == "G":

            emojis += "🇬"

        elif reacts[n] == "H":

            emojis += "🇭"

        elif reacts[n] == "I":

            emojis += "🇮"

        elif reacts[n] == "J":

            emojis += "🇯"

        elif reacts[n] == "K":

            emojis += "🇰"

        elif reacts[n] == "L":

            emojis += "🇱"

        elif reacts[n] == "M":

            emojis += "🇲"

        elif reacts[n] == "N":

            emojis += "🇳"

        elif reacts[n] == "O":

            emojis += "🇴"

        elif reacts[n] == "P":

            emojis += "🇵"

        elif reacts[n] == "Q":

            emojis += "🇶"

        elif reacts[n] == "R":

            emojis += "🇷"

        elif reacts[n] == "S":

            emojis += "🇸"

        elif reacts[n] == "T":

            emojis += "🇹"

        elif reacts[n] == "U":

            emojis += "🇺"

        elif reacts[n] == "V":

            emojis += "🇻"

        elif reacts[n] == "W":

            emojis += "🇼"

        elif reacts[n] == "X":

            emojis += "🇽"

        elif reacts[n] == "Y":

            emojis += "🇾"

        elif reacts[n] == "Z":

            emojis += "🇿"

    return emojis

#Establish deck of cards

cardnames = []

for a in range(4):
    for b in range(14):
        if a == 0:
            suit = "Wombs"

            if b == 10:
                cardnames.append("Asesu - Jack of " + suit)
            elif b == 11:
                cardnames.append("Vasuki - Queen of " + suit)
            elif b == 12:
                cardnames.append("Aril - King of " + suit)

        elif a == 1:
            suit = "Cock"

            if b == 10:
                cardnames.append("Recluse - Jack of " + suit)
            elif b == 11:
                cardnames.append("Ash - Queen of " + suit)
            elif b == 12:
                cardnames.append("Devotion - King of " + suit)

        elif a == 2:
            suit = "Plugs"

            if b == 10:
                cardnames.append("Athena - Jack of " + suit)
            elif b == 11:
                cardnames.append(" - Queen of " + suit)
            elif b == 12:
                cardnames.append("Corbin - King of " + suit)

        elif a == 3:
            suit = "Pussy"

            if b == 10:
                cardnames.append(" - Jack of " + suit)
            elif b == 11:
                cardnames.append("Tabris - Queen of " + suit)
            elif b == 12:
                cardnames.append("Layla - King of " + suit)

        if b < 9:
            cardnames.append(str(b+2) + " of " + suit)

        elif b == 13:
            cardnames.append("Ace of " + suit)

cardtemp = cardnames

smallblind = 50
bigblind = 100

saferooms = ["unlit-passageways", "salamander-hot-springs", "monster-girl-cantina", "the-ole-burlesque", "backstage-burlesque", "library-of-carnal-knowledge", "the-cathedral", "mermaid-cove-resort", "spectators-stands"]
shops = ["💎the-gobblin-bazaar💎", "🏺the-golden-jackal🏺", "🐍venom-ink🐍", "🧵widows-boutique🧵", "🍄sophies-garden🍄", "📜menagerie-magiks📜", "🐾purrfect-petshop🐾", "🔔the-polished-knob🔔", "🏥the-clinic🏥", "💰adventurers-guild💰", "⛓black-market⛓"]
depths = ["trapped-corridors", "moaning-hallways", "unlicensed-fights", "sparring-pit", "kobold-dens", "wild-gardens", "twilight-groves", "sirens-grotto", "the-dollhouse", "frostveil-tundra"]

#Help message
async def helplist(message):

    helptextmain = ["**Hello, We are Gothica, the Shoggoth Servants of T̶̤̻̘͙̩̖̿ͅḩ̷̲̣̙͚̯̮̐͂̃͜͠e̴̳̦͍̮̹̦̠͛͒̅́ ̵͚̥̯̫̼̦̦̻͌͑̑̑̕Ḿ̷͓̀͗̇̊͆͒̀i̴̻̼̙̺͙͂̃͘͝s̵͖̝͈̤̖͓̬̖͗̃͘ͅt̷̢̫̠̼̭͚́̅͒̐͋̃̈́̂͠r̶̡̧̭͓͇̝̥͖̺͑̆̅͑͂̉̊̋͘͝e̸̦͈̩̠̩̣̔̊̎̀̔͒̊̎͜͝s̵̛̛̭̙̜͑̓̒̾͜ͅs̶̢̝͍̯͚̰͛́̾. We facilitate a number of functions in the dungeon. A summary of some of those functions is given below. If you would like more information on any function, type the number that corresponds to it. You can also specify it when you call the help command, such as by doing `%help registration`**"]
    
    helpcategories = ["General Functions", "Character Index Functions", "Roleplay Functions", "Kink Functions", "Economy Functions", "Lorekeeper Only Functions"]
    helpnames = [
        ["Start", "Rulebook", "Embed", "Help"],
        ["Character Registration", "Edit", "Transfer", "Charlist", "Search", "Retire", "Deactivate", "Activate"],
        ["LFG", "Plothook", "Plotlead", "Room", "Break", "Recent", "Wildlust", "Scenes"],
        ["Kinklist", "Kinksurvey", "Kinkfill", "KinkEdit", "Kinkplayers"],
        ["Work", "Slut", "Money", "Inventory", "Give-Money", "Leaderboard", "Shop", "Item", "Buy", "Sell", "GiveItem", "Invest", "Bid", "Spend"],
        ["Gag", "Emote", "Adventurer", "Verify", "Kinkencounter", "oocembed", "oocmsg", "Add-money", "Remove-Money", "AddItem", "Spellrotation", "RandLoot"]
    ]
    helpsummary = [
        ["Calls up some welcoming information for new members", "Summons a link to the lewd rulebook", "Generates an embed, like this one", "You are here."],
        ["Registers a character to the index", "Edits a character", "Gives a character to another player", "Lists the characters owned by a player", "Provides the index entry of a character", "Retires a character", "Sets a character temporarily unactive", "Reactivates a deactivated character"],
        ["Helps you find roleplay partners", "Generates a random plothook for your character", "Checks how many plothooks you have seen", "Suggests an empty room for you to roleplay in.", "Generates a scene break", "Provides the time of the last message in each roleplay channel", "Rolls on the wildlust table", "Stores and recalls your list of active scenes and can DM you whenever a new message is sent in them"],
        ["Summons the kinks of the tagged player", "Allows you to fill out the kink survey", "Fills any holes in the kinksurvey", "Edits a kink", "Summons a list of players with the targeted kink"],
        ["Earns daily dezzies", "Earns more dezzies, with a risk to lose some instead", "Checks your balance", "Displays your items", "Gives a number of dezzies to someone else", "Shows how rich the richest people on the server are", "Displays the listed shop", "Provides details on a shop or inventory item", "Buys an item", "Sells an item, at a loss.", "Transfers an item to another player", "Spends dezzies on a community project", "Bids on an auction in the Black Market", "Removes Dezzies from yourself"],
        ["Gags a user in ooc", "Reacts to a message with emote letters", "Grants a player the Adventurer Role", "Confirms that a user is over 18", "Generates a random encounter, respecting the player's kinks", "Generates an embed in ooc", "Sends a message in ooc", "Adds money", "Removes money","Adds an item from the shop to a user's inventory", "Checks Runar's stock of spells", "Generate random loot that fits a player's kinks"]
    ]
    helpfull = [
        ["The `%start` command provides an overview of how new players can start making characters and roleplaying in the dungeon, highlighting how to get roles and create a character and tupper.",
        "Summons the dropbox link to the latest version of the Lewd Rulebook, as well as some useful quick stats on inhibition and arousal. The command is `%rulebook`",
        "Allows you to generate a message in a fancy embed. If you simply type `%embed`, followed by your message, it will use the message as the title.\n\nIf you want different fields like descriptions and images, it is a bit more complex. In this mode, to write a title and description, you would do: `%embed -t =Title goes here= -d =Desciption between these equals signs=` You can also add -i =image link= or -m =thumbnail link=. Obviously, this means that you can't use equals signs in the content of your embed.",
        "Summons this interface. You can use just `%help` on its own, which pulls up the full list of commands, or you can specify the category (So `%help economy` will pull up only the economy commands) or the specific command (`%help help`, for example, will bring up this message)."
        ],
        ["To register a character, go to #character-creation and type some information about them. This message must start with Name, but after that, you can use as many or as few bits of information as you want. Each should be on its own line. For example:\n\n`Name: Lalontra`\n`Race: Water Genasi`\n\nDo not use a tupper when creating your character.\n\nPossible Fields are:\n\nName\nRace\nGender\nPronouns\nAge\nClass\nLevel\nSheet\nAlignment\nBio\nSexuality\nSkin Colour\nHair Colour\nEye Colour\nHeight\nWeight\nSummary\nImage",
        "To edit a character, type `" + myprefix + "edit Name Field New-Value`, as a demonstration:\n\n`" + myprefix + "edit Lalontra class Ranger`\n\nThis will match a character's name even if you only use part of the name.",
        "For obvious reasons, only the owner of a character can edit them, but there are occasions where you want to give a character to someone else, for example in an auction. To transfer the character, type `" + myprefix + "transfer Name @New-Owner`, for example:\n\n`" + myprefix + "transfer Lalontra @C_allum`",
        "To create a list of the characters owned by any particular player, type `" + myprefix + "charlist`. Send the command without any arguments to see your own characters, or add a mention after it to see someone else's. As below:\n\n`" + myprefix + "charlist @C_allum`",
        "To search for a character or attribute, type `" + myprefix + "search Search-term`. If the search term is within the name of a character, it will provide that character's full bio. As an example, to find the bio of Lalontra you might type:\n\n`" + myprefix + "search Lal`\n\nIf the search term is not found in the name of a character, you can instead seach by a data field, done by typing`" + myprefix + "search Field Search-Term`, such as:\n\n`" + myprefix + "search class Ranger`\n\nIf the first argument after the command is neither in the name of a character, nor a field name, it will search the whole database, and provide details on where the word occurs. If you were to type:\n\n`" + myprefix + "search blue`\n\nYou would see information about any characters whos eyes, hair or skin colour (or any other attribute) was blue."
        "If you want to retire a character for any reason, type `" + myprefix + "retire Name`, as per the below example||, which was rather painful to write!||:\n\n`" + myprefix + "retire Lalontra`",
        "If you need to activate a previously unavailable character, whether because you made or recieved them as a transfer from another user without having a slot available; or `%deactivated` them temporarily, you can activate them by using`" + myprefix + "activate Name`. Example:\n\n`" + myprefix + "activate Lalontra`",
        "Deactivating a character means that they will have a ~~strikethough~~ on their name when your character list is called using `%charlist`. This is commonly because they are being used in another scene that you want to finish before starting a new one with them, or can simply be if you're looking for a new scene but don't want to play that specific character at the time."
        ],
        ["`%lfg` gives you the Looking for Role Play role, and allows you to see the #looking-for-new-roleplay channel. this role is restricted by time, so you only have access to the channel when you are actively looking for role play. You can also specify a number of hours to be active, by adding them after the command.\n\nRunning the `%kinkplayers` command in this channel will instead ping everyone with the relevant kinks (they'll only see the ping if they are also in the channel though)",
        "We can generate plothooks from your active characters, picking a scene they might be in, to act as a seed for roleplaying. These hooks are purely optional and can be ignored, even after they have been generated. They are simply ideas. The command is: `" + myprefix + "plothook`. You can also add the name (or part of the name) of one of your characters after the command to generate a plothook for them, for example, C_allum could do `" + myprefix + "plothook lal` to generate a plothook for Lalontra.",
        "There are a number of plothooks in the system, and by running `%plotleaderboard` you can see how many each person has found.",
        "`%room` looks at the list of roleplay rooms available, and chooses one that looks quiet enough for you to start a scene in.",
        "If you want to divide your scene from the previous one, you can run `%break` (or just `%br`). This will tell us to create a division in the room.",
        "We peek into each public room, and take a look at the last message there. Summon this check using `" + myprefix + "recent`. Room names written in **bold** have been inactive for more than three hours.",
        "We have a custom wild magic table available to sorcerers in the dungeon. If you type `%wildlust`, Gothica will roll on that table for you.\n\nThe full table can be seen in the lewd rulebook.",
        "Gothica can track your scenes. Running `%scenes add` followed by a brief description of the scene and then the link to it, will tell us to track that scene. You can then do `%scenes` to summon the list of scenes, and we will inform you who sent the last message in the channel. As an example, you might type: `%scenes add Lalontra and River fight an evil fae #An-Uncomfortable-Reunion` to add that scene to your watchlist. You can also remove scenes with `%scenes remove` and then the number of the one to remove. Gothica can also DM you whenever a message is sent in a tracked scene. To enable that run `%scenes notification` and select the scene you want to get notifications on."
        ],
        ["This function lists a users kinks. To use it, run `%kinklist @name`. We will then summon the overview of the list of preferences that the user has filled out. You can then select further information on any particular category of kinks, such as mental domination or clothing and toys. Additionally, if you react to a message using the kinklist emote (<:kinklist:1053378814190813304>), we will direct message you their full kinklist.",
        "`%kinksurvey` is the function that allows you to complete the survey. We will open a thread in which you can tell us all about your kinks and preferences. This command can only be run in the #bots-and-constructs channel. This survey takes some time to run through.",
        "We sometimes add kinks to our list, based on user feedback. If we have added any kinks since you took your survey, you can run `%kinkfill` to generate a new thread in which to answer those questions.",
        "If you find that your preferences for a certain thing have changed, you can run `%kinkedit` to update this. Running the command on its own will bring up a navigatable list of kinks, while specifying the name of the kink in the message will edit that one directly.",
        "If you are looking for someone who is into a particular kink, you can run `%kinkplayers` followed by the name of the kink. For example, `%kinkplayers Handholding` will bring up a long list of degenerates who have that marked as a favourite. Running this in #looking-for-new-roleplay will ping everyone associated with that kink who is also looking to start a scene."
        ],
        ["This is the main way that dezzies are earned in the server. Each day, you are able to run `%work`, which awards a random number of dezzies. Running this command every day earns a streak, which gets extra dezzies.",
        "If working isn't getting enough dezzies, you can also try `%slut`. This has the potential to earn more dezzies, and can be run every six hours. This does also have the risk that you will instead lose dezzies, so use carefully.",
        "We can help you check your balance in one of two ways. First, we can simply shove you, and if you make the Strength (Athletics) or Dexterity (Acrobatics) check, you do not fall prone. If you would rather we check the balance of your dezzie account, simply use `%money`",
        "To display the items you have bought, earned or found in the dungeon, you can use `%inventory`. This also displays the number of each that you have and a brief summary of each.",
        "To transfer dezzies from your account to someone else's, use the command `%give-money @name amount`. This value will be removed from your account and added to that of the targeted player.",
        "The richest players in the dungeon can be displayed using the `%leaderboard` command.",
        "The inventories of the various shops in the market can be shown using the `%shop shopname` command, for example running `%shop widow` will pull up the listing for the Widow's Boutique.",
        "To display the details of an item, either from the shop or one that has been given to you through a quest or other reward, you can run `%item itemname`.",
        "Buying an item can be done by running `%buy item amount`. We will remove the dezzies and add the item to your inventory. We will also relay a message from the shopkeeper.",
        "You can sell items from your inventory, based on the cost you paid for them. We will return them to the shop or to other areas of the dungeon for you, and will award you half the dezzies they are worth. To use this command, do `%sell amount itemname`",
        "To move an item from your inventory to that of another player, you can do `%giveitem @name itemname`.",
        "We sometimes run community projects - areas of the dungeon that require funding from the denizens within. This allows you to have your characters contribute to these schemes to further the development of the dungeon. In a thread that has been set up as a community project, you simply use `%invest amount`",
        "When a market is on, you can bid on *wares* using the `%bid amount` command. Your bid will go to the name of the ware in whos thread you bid.",
        "If you wish to remove dezzies from yourself for some reason (often because a lorekeeper suggests it, or if you are eating them), you can use `%spend amount`."
        ],
        ["You can gag a user for 69 seconds in #ooc. This replaces all their messages with mmMhing. The command is `%gag @name`",
        "Gothica can react to a message with letters. By using `%emote messagelink words`, you can have them react to the linked message with the words of your choice. Be aware that you can only use each letter once per word, so trying to get Gothy to react a word like Callum to a post would end up with the awful seplling of Calum.",
        "Approving a character sheet for use in the dungeon depths is done through the `%adventurer @name charactername` command. Tagging them allows us to know which user to give the role to.",
        "The verify command gives a user the Verified role, and welcomes them to the server. This is only available to moderators. The syntax is `%verify @name`",
        "Generating encouters that are cross referenced with a user's kinks can be done with `%kinkencounter @name`. At the moment, this draws from a limited list and is for a single player, but future plans involve multiple characters and more in depth encounters from a larger list.",
        "If you want to send an embed to #ooc, you can use `%oocembed` This follows the same rules as `%embed` in terms of adding images, titles and thumbnails.",
        "We encourage you to send messages as us in ooc to give us a bit of personality. Using `%oocmsg` somewhere hidden like the lorekeeper bot channel, you will be able to type a message without showing as typing, or being able to be queried as a tupper would be.",
        "If you wish to add dezzies to a player (rather than giving them from your own balance), you can use `%add-money @name amount`.",
        "Like adding dezzies, you can remove dezzies from a user using the `%remove-money @name amount` command. This is especially useful if they are recieving a custom item from the shops or need to pay a fee in the guild.",
        "To add an item to a player's inventory from the shop, you can run `%additem @name item`. For example, `%additem @Callum basic ink` would give Callum a basic tattoo.",
        "The spell scrolls that Runar has available are constantly changing. When someone requests one, you can run `%spellrotation`, which will provide a list of the spells he has in stock, along with their prices.",
        "To reward a player with randomised loot, you can run the `%randloot @name` command. This generates a piece of loot and compares it to their kinks - so they cannot get a piece of loot that crosses one of their limits. You can also specify the rarity of the item, or a range of rarities to roll from, for example, `%randloot @C_allum very rare` or `%randloot @C_allum common-rare`. It will then ask if you want to cancel, edit the item, or add it to the player's inventory as is."
        ]
        ]

    #Check for lorekeeper channels
    if message.channel.category.name != "﴿─﴾ 𝙻𝚘𝚛𝚎𝚔𝚎𝚎𝚙𝚎𝚛'𝚜 𝙲𝚊𝚋𝚊𝚕 ﴿─﴾":
        helpcategories = helpcategories[:-1]
        helpnames = helpnames[:-1]
        helpsummary = helpsummary[:-1]
        helpfull = helpfull[:-1]


    if " " in message.content: #User specified query matches category name
        helpquery = message.content.split(" ", 1)[1].lower().replace("functions", "")
        if helpquery.lower() in str(helpcategories).lower():
            catindex = len(helpcategories) +1
            for a in range(len(helpcategories)):
                if helpquery.lower() in helpcategories[a].lower():
                    catindex = a
                    break
            helptextcatmain = []
            index = 0
            for b in range(len(helpnames[catindex])):
                index += 1
                helptextcatmain.append("`" + str(index) + "`: *%" + helpnames[a][b] + ":* " + helpsummary[a][b])
            await message.channel.send(embed = discord.Embed(title = "Gothica Help: " + helpcategories[catindex], description = "\n".join(helptextcatmain), colour = embcol))
            try:
                msg = await client.wait_for('message', timeout = 30, check = check(message.author))
                try:
                    helpindex = int(msg.content)-1
                    await msg.delete()
                except TypeError or ValueError:
                    await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                    await msg.delete()
                    return
            except asyncio.TimeoutError:
                await message.channel.send("Selection Timed Out")
                await message.delete()
                return
            try:
                await message.channel.send(embed=discord.Embed(title = helpnames[catindex][helpindex].title() + " Help", description = helpfull[catindex][helpindex], colour = embcol))
            except IndexError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer between 1 and " + str(index), colour = embcol))
            await message.delete()
        elif helpquery.lower() in str(helpnames).lower(): #User specified query matches command name
            for a in range(len(helpcategories)):
                for b in range(len(helpnames[a])):
                    if helpquery.lower() in helpnames[a][b].lower():
                      await message.channel.send(embed=discord.Embed(title = helpnames[a][b].title() + " Help", description = helpfull[a][b], colour = embcol))
        else:
            await message.channel.send(embed = discord.Embed(title = "Gothica Help", description = "Your search query was not found", colour = embcol))
    else: #Default Help Menu
        index = 0
        for a in range(len(helpcategories)):
            helptextmain.append("\n**" + helpcategories[a] + ":**")
            for b in range(len(helpnames[a])):
                index += 1
                helptextmain.append("`" + str(index) + "`: *%" + helpnames[a][b] + ":* " + helpsummary[a][b])
        await message.channel.send(embed = discord.Embed(title = "Gothica Help", description = "\n".join(helptextmain), colour = embcol))
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                helpindex = int(msg.content)
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send("Selection Timed Out")
            await message.delete()
            return
        catindex = len(helpcategories) +1
        for c in range(len(helpcategories)):
            if helpindex > len(helpnames[c]):
                helpindex -= len(helpnames[c])
            else:
                catindex = c
                break
        helpindex -= 1
        try:
            await message.channel.send(embed=discord.Embed(title = helpnames[catindex][helpindex].title() + " Help", description = helpfull[catindex][helpindex], colour = embcol))
        except IndexError:
            await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer between 1 and " + str(index), colour = embcol))
        await message.delete()

#Dice Converter
async def diceroll(message):
    messwords = message.split(" ")
    words = []
    for a in range(len(messwords)):
        if re.search("\[\d{1,}d\d{1,}\]", messwords[a]) != None:
            numdice = int(messwords[a].split("d")[0].lstrip("["))
            dicesize = int(messwords[a].split("d")[1].rstrip("]"))
            dicetot = 0
            for b in range(numdice):
                dicetot += random.randint(1, dicesize)
            words.append(str(dicetot))
        else:
            words.append(messwords[a])
    return(" ".join(words))
