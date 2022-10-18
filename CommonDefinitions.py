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
from datetime import date, datetime
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

intents = discord.Intents().all()

client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix='%', activity = discord.Game(name="Testing Stuff"), intents = intents)

print(" Initialised {0.user} at ".format(client) + str(datetime.now()).split(".")[0])

#Sheet Locations:

if 1: #Set to 1 to use the real spreadsheets, or 0 to use the testing spreadsheets.

    CharSheet = "1iHvP4HC8UQqyiMmC3Xiggx8-17e5SGWJMncEeoiZP1s"

    EconSheet = "1qTC0gn7Fe_cHDVPB8KIEjSFUwrUSEhlLy1upHIKnKF8"

    shopsheet = "1gxNPXIichzK9mSN8eHYVdJvaaUgUnN6VF8WshL_4Les"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg"

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4"

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA"

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU"

    token = "ODc2NDQwOTgwMzU2NzU1NDU2.YRkHRQ.R0QTTcjzr6YAZglNy4PU3Iyzx5o" # Main Gothica Bot

    logchannel = 918257057428279326

else:

    CharSheet = "1Vgxa8C5j5XnEUGhaGqAANVhsWSIOra87wCE2f5C75tQ"

    EconSheet = "1mmWxHhDUPI0PjLC2UXJZmj5wNqXnucFMz-er9NpVC2c"

    shopsheet = "1r_1tYCGtmanRkTGsfAz4WrOSUoi6roO-zYRHACQBD90"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg" #No change as yet

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4" #No change as yet

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA" #No change as yet

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU" #No change as yet

    token = "OTIxNTQwNzQ4MDM2NDExNDYy.GG6ouk.1aHkMKGD_0WM6MozQ5n73roXVzweY0vXjGAh0o" # Gothica Beta

    logchannel = 1031701327169998958 #Test Server

SERVICE_ACCOUNT_FILE = "keys.json"

#SERVICE_ACCOUNT_FILE = "D:\Callum\Documents\\2021\Discord Botting\Hunting\keys.json"

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

#Help

helptextintro = "**Hello, We are Gothica, the Shoggoth Servants of The Mistress. As part of our duties here in The Dungeon, we keep a registry of all the characters within the Dungeon. You can find those records either in #character-index, or in this archive:**\nhttps://docs.google.com/spreadsheets/d/1iHvP4HC8UQqyiMmC3Xiggx8-17e5SGWJMncEeoiZP1s/edit?usp=sharing"
helptextreg = "**Registering a character:**\n\nTo register a character, go to #character-creation and type some information about them. This message must start with Name, but after that, you can use as many or as few bits of information as you want. Each should be on its own line. For example:\n\n`Name: Lalontra`\n`Race: Water Genasi`\n\nPossible Fields are:\n\nName\nRace\nGender\nPronouns\nAge\nClass\nLevel\nSheet\nAlignment\nBio\nSexuality\nSkin Colour\nHair Colour\nEye Colour\nHeight\nWeight\nSummary\nImage"
helptextedit = "**Editing a character:**\n\nTo edit a character, type `" + myprefix + "edit Name Field New-Value`, as a demonstration:\n\n`" + myprefix + "edit Lalontra class Ranger`\n\nThis will match a character's name even if you only use part of the name."
helptexttrans = "**Transferring ownership of a character:**For obvious reasons, only the owner of a character can edit them, but there are occasions where you want to give a character to someone else, for example in an auction. To transfer the character, type `" + myprefix + "transfer Name @New-Owner`, for example:\n\n`" + myprefix + "transfer Lalontra @C_allum`"
helptextlist = "**Listing your characters:**\n\nTo create a list of the characters owned by any particular player, type `" + myprefix + "charlist`. Send the command without any arguments to see your own characters, or add a mention after it to see someone else's. As below:\n\n`" + myprefix + "charlist @C_allum`"
helptextsearch = "**Searching for a character or attribute:**\n\nTo search for a character or attribute, type `" + myprefix + "search Search-term`. If the search term is within the name of a character, it will provide that character's full bio. As an example, to find the bio of Lalontra you might type:\n\n`" + myprefix + "search Lal`\n\nIf the search term is not found in the name of a character, you can instead seach by a data field, done by typing`" + myprefix + "search Field Search-Term`, such as:\n\n`" + myprefix + "search class Ranger`\n\nIf the first argument after the command is neither in the name of a character, nor a field name, it will search the whole database, and provide details on where the word occurs. If you were to type:\n\n`" + myprefix + "search blue`\n\nYou would see information about any characters whos eyes, hair or skin colour (or any other attribute) was blue."
helptextretire = "**Retiring a character:**\n\nIf you want to retire a character for any reason, type `" + myprefix + "retire Name`, as per the below example||, which was rather painful to write!||:\n\n`" + myprefix + "retire Lalontra`"
helptextactivate = "**Activating a character:**\n\nIf you need to activate a previously unavailable character, whether because you made or recieved them as a transfer from another user without having a slot available, once you create space or earn another slot, you can activate them by using`" + myprefix + "activate Name`. Example:\n\n`" + myprefix + "activate Lalontra`"
helptextplothook = "**Generating a plothook:**\n\nWe can generate plothooks from your active characters, picking a scene they might be in, to act as a seed for roleplaying. These hooks are purely optional and can be ignored, even after they have been generated. They are simply ideas. The command is: `" + myprefix + "plothook`. You can also add the name (or part of the name) of one of your characters after the command to generate a plothook for them, for example, C_allum could do `" + myprefix + "plothook lal` to generate a plothook for Lalontra. You can additionally summon a leaderboard to see how many plothooks everyone has seen by using `" + myprefix + "plotleaderboard`"
helptextrooms = "**Finding an empty room to roleplay in:**\n\nThe `" + myprefix + "room` command will find you a public room that has not been used for a while, and will insert an empty message as a scene break."
helptextrecents = "**Checking the most recent message in each public room:**\n\nWe peek into each public room, and take a look at the last message there. Summon this check using `" + myprefix + "recent`. Room names written in **bold** have been inactive for more than three hours."
helptextwild = "**Rolling on the Wild and Lustful Magic Table**\n\nWe roll for you and check the result on the wild and lustful magic table. This is especially useful for people playing wild magic classes in the dungeon, though anyone can use it. To do so, type `" + myprefix + "wildlust`."
helptextshop = "**Browsing Each Shop:**\n\nWhile you *can* use `$shop` to see all the items available in the whole market, it is often easier to view the list of items for a particular shop. Using `" + myprefix + "shop searchterm`, you can see the catalogue of items from any individual store. You can also use `" + myprefix + "shop` in the shop channel itself.\n\nIn addition to this, we help the shopkeepers personalise a few messages, such as the message when you buy an item."
helptextembed = "**Generating Custom Embeds:**\n\nYou can create your own embeds with Gothica if you want to create better looking messages for announcing things or setting up private rooms or in campaigns. To do so, use: \n`" + myprefix + 'embed -t =Embed Title= -d =Embed Text=`\nBoth the title and text need equals signs on each side. You can also do -i =image link= or -m =thumbnail link=.\n\nAs an alternative, you can generate simple embeds using by not including a title or text argument, and the embed will generate using whatever you write as your command as the embed body. For example, `' + myprefix + "embed The Mistress is watching you`, will generate an embed that says just that."

helptextmoderator = "And, since you are a dungeon moderator, you also have access to the following:\n(This part of the help section is only visible in #admin-bots)\n\n"
helptextverify = "**Verifying a user:**\n\nOnce you have confirmation that a user is over 18, type `" + myprefix + "verify @user`. They will have the 'Verified' role added to them, and be made aware that they can close the ticket. We will also post that they have been verifed in the log channel (#server-member-updates) and post a welcome message in #main-camp."
helptextraid = "**Giving a member a raid role:**\n\nUsing `" + myprefix + "raid 1/2/3/lead @user`, you can grant anyone the ability to participate or run raids."
helptextlottery = "**Awarding a random player:**\n\nModerators are able to run lotteries, which reward players for registering characters. We take the names of players from the spreadsheet, with every unique name added to a list. A random name is then drawn, and a message shown with the winner. To generate this, run `" + myprefix + "lottery`. You can also add an amount of dezzies after it, for example: `" + myprefix + "lottery 100`, which will say they have won 100 dezzies. You still need to handle the transfer of dezzies yourself, of course. Another function of this command is the ability to give a reason for the lottery. Typing `" + myprefix + "lottery 100 Weekly Givaway` will include that on the embed."
helptextlogs = "**Gothica's Logs:**\n\nWe record a few things here in the dungeon. The most useful is, of course, #character-index. This stores the bios of any character created in the dungeon, and updates when they are edited. The actual data is stored on this archive:\nhttps://docs.google.com/spreadsheets/d/1iHvP4HC8UQqyiMmC3Xiggx8-17e5SGWJMncEeoiZP1s/edit?usp=sharing\nIf you would like edit access, send Callum your email address. Please don't move columns around without talking to him first.\n\nIn #gothica-logs, we keep track of things like characters being registered under the age of 18, or over level 14. This channel is also used if someone registers more characters than they have slots. On the subject of slots, we track those by searching a person's roles, and finding any with a '+' symbol beside them, and then adding the number beside that to 5.\n\nWe track users that we have verified in the same way that Dungeon Guard did, in #server-member-updates.\n\nWe currently also check the channels for tupperbot breaking, which happens when people edit messages. We ping Callum, who fixes the #alias-bot log channel. We've tried doing it ourselves, but tupper ignores us..\n\nWe also keep track of messages sent in the shops, and ping Lorekeepers if someone sends a message more than three hours after the last one."
helptextrecentsmoderator = "**Checking the most recent message in each public room:**\n\nWe peek into each public room, and take a look at the last message there. Summon this check using `" + myprefix + "recent`. As you are moderator, you can also add the word `break` after the command, which will insert a scene break in each room that has been inactive for more than three hours, which are also written in bold in the reply."

helpline = "\n\n------------------------------------------------------------------------------------------\n\n"

helptext = helptextintro + helpline + "Currently, we handle the following functions. Each has a helptext command that you can use to get more information about it:\n\n**Character Registration** - `" + myprefix + "help registration`\n**Editing a Character** - `" + myprefix + "help edit`\n**Tranferring Ownership of a Character** - `" + myprefix + "help transfer`\n**Listing a Player's Available Characters** - `" + myprefix + "help charlist`\n**Searching the Database** - `" + myprefix + "help search`\n**Retiring a Character** - `" + myprefix + "help retire`\n**Activating a Character** - `" + myprefix + "help activate`\n**Generating a Potential Plothook** - `" + myprefix + "help plothook`\n**Finding an Empty Public Space** - `" + myprefix + "help room`\n**Checking recent messages** - `" + myprefix + "help recent`\n**Rolling on the Wild and Lustful Magic Table** - `" + myprefix + "help wildlust`\n**Browsing the shops** - `" + myprefix + "help shop`\n**Custom Embeds** - `" + myprefix + "help embed`"

helptext_moderator = helptext + "\n\n" + helptextmoderator + "**Verifying a user** - `" + myprefix + "help verify`\n**Selecting a random player to win** - `" + myprefix +"help lottery`\n**Raid roles** - `" + myprefix + "help raid`\n**Gothica's Logs** - `" + myprefix + "help log`"

helptextintro = "**Hello, We are Gothica, the Shoggoth Servants of The Mistress. As part of our duties here in The Dungeon, we provide a number of services to facilitate your roleplay. These services we manage include:**"

helptextchar = "**Character Registry:** We maintain records of every character in the dungeon, allowing them to be easily accessed and edited. To see the functions we provide for this in detail, do %helpregistry"
helptextregistry = "**Economy:**We maintain the economy of the server, keeping track of everyone's dezzies and items. Dezzies are our server currency, and are used in the in game shops. "

#Help message
async def helplist(message):

    if message.content.lower().startswith("%help regis"):

        helptext = "**Character Registry:** We maintain records of every character in the dungeon, allowing them to be easily accessed and edited. Functions available for this service include:\n\n**Registering a Character:** To register a character, go to #character-creation and type some information about them. This message must start with Name, but after that, you can use as many or as few bits of information as you want. Each should be on its own line. For example:\n\n`Name: Lalontra`\n`Race: Water Genasi`\n\nPossible Fields are:\n\nName, Race, Gender, Pronouns, Age, Class, Level, Sheet, Alignment, Bio, Sexuality, Skin Colour, Hair Colour, Eye Colour, Height, Weight, Summary\n\n**Editing a character:**\n\nTo edit a character, type `" + myprefix + "edit Name Field New-Value`, as a demonstration:\n\n`" + myprefix + "edit Lalontra class Ranger`\n\nCurrently, this will match a character's name if you only use one name, as this function doesn't handle spaces yet.\n\n**Transferring ownership of a character:**For obvious reasons, only the owner of a character can edit them, but there are occasions where you want to give a character to someone else, for example in an auction. To transfer the character, type `" + myprefix + "transfer Name @New-Owner`, for example:\n\n`" + myprefix + "transfer Lalontra @C_allum`\n\n**Listing your characters:**\n\nTo create a list of the characters owned by any particular player, type `" + myprefix + "charlist`. Send the command without any arguments to see your own characters, or add a mention after it to see someone else's. As below:\n\n`" + myprefix + "charlist @C_allum`\n\n**Searching for a character or attribute:**\n\nTo search for a character or attribute, type `" + myprefix + "search Search-term`. If the search term is within the name of a character, it will provide that character's full bio. As an example, to find the bio of Lalontra you might type:\n\n`" + myprefix + "search Lal`\n\nIf the search term is not found in the name of a character, you can instead seach by a data field, done by typing`" + myprefix + "search Field Search-Term`, such as:\n\n`" + myprefix + "search class Ranger`\n\nIf the first argument after the command is neither in the name of a character, nor a field name, it will search the whole database, and provide details on where the word occurs. If you were to type:\n\n`" + myprefix + "search blue`\n\nYou would see information about any characters whos eyes, hair or skin colour (or any other attribute) was blue.\n\n**Retiring a character:**\n\nIf you want to retire a character for any reason, type `" + myprefix + "retire Name`, as per the below example||, which was rather painful to write!||:\n\n`" + myprefix + "retire Lalontra`\n\n**Activating a character:** If you need to activate a previously unavailable character, whether because you made or recieved them as a transfer from another user without having a slot available, once you create space or earn another slot, you can activate them by using`" + myprefix + "activate Name`. Example:\n\n`" + myprefix + "activate Lalontra`\n\n**Deactivating a Character:**"

    await message.channel.send(embed = discord.Embed(title = "Help", description = helptext, colour = embcol))