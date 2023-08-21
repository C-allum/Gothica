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
import time as timeos
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

    TransactionSheet = "1GKiiWlTPlMDj8FCiNZcNSF_FFJi6J_CKTyimdjoo9GU"

    logchannel = 918257057428279326

    aliasBotChannel = 830799558514573312

    bridgechannel = 996826636358000780

    communityProjectChannel = 999810708546002994

else:

    CharSheet = "1Vgxa8C5j5XnEUGhaGqAANVhsWSIOra87wCE2f5C75tQ"

    EconSheet = "1mmWxHhDUPI0PjLC2UXJZmj5wNqXnucFMz-er9NpVC2c"

    shopsheet = "1tj64lIs9qvfv3wUDjU5AHplhRoXU4i-qgHj21-Q7olk"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg" #No change as yet

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4" #No change as yet

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA" #No change as yet

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU" #No change as yet

    Randomlootsheet = "19Dc4PI-E5OubesNroJfB4zKg9bqqqbdPelodjH6ecNw"

    TransactionSheet = "1GKiiWlTPlMDj8FCiNZcNSF_FFJi6J_CKTyimdjoo9GU"

    logchannel = 1031701327169998958 #Test Server

    aliasBotChannel = 1142877836298965105

    bridgechannel = 891781900388159528

    communityProjectChannel = 891781900388159528

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

roleplay_categories_id = [917234637359702057, 1058839161735483462, 831894394877509682, 952251327143084092, 853176266077110302, 832433588363853845]

guildvar = client.get_guild(828411760365142076)

myprefix = "%"

dezzieemj = "<:dz:844365871350808606>"

critemj = "<:crit:893767145060696064>"

embcol = 0xb700ff

indexchannel = 898640028174016552

tupperID = 1071257376088412204

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

weeklyDezzieBonusPatronT1 = 100
weeklyDezzieBonusPatronT2 = 100
weeklyDezzieBonusPatronT3 = 100
weeklyDezzieBonusPatronT4 = 100

sellpricemultiplier = 0.5 #Use this to change how much things are sold for, relative to their purchase price

global bidstock
global bidders
global bidprice
bidstock = []
bidders = []
bidprice = []

#----------------Fiendtome Wielder---------------
imptomeWielder = -1
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

lewdtab = ["Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls", "Your arousal increases to its maximum value and you immediately begin making climax saving throws.", "Your clothes and armor disappear until you complete a long rest. You are unaware of this fact, and utterly deny any suggestions to the contrary, or attempts to make you wear clothes.", "Your body begins to compulsively masturbate. For the next minute, you must succeed on a DC 15 strength check at the start of each of your turns, or spend the turn pleasuring yourself to the best of your ability.", "You cast Enlarge/Reduce on your genitals or other sexual traits. Roll 1d6: on a roll of 1-3, you enlarge these parts of your body; on a roll of 4-6 you reduce these parts of your body.", "For the next hour whenever you open your mouth to speak, you experience the sensation and of a phantom cock in your mouth.", "The last creature you had sexual intercourse with immediately climaxes, and is aware of the source of their climax.", "You are petrified for 1d6 hours. While petrified in this way, your erogenous zones remain soft and fleshy, and you experience stimulation as normal.", "You immediately grow a 12 inch cock if you do not already have one. If you already have a cock, ignore this result and roll again. This effect lasts until you climax.", "For the next 1d6 hours, you can see the genitals and sexual characteristics of other creatures through their clothes.", "For the next hour, anytime you climax, all other creatures within 30 ft must also make a climax saving throw, regardless of their current arousal.", "You gain a powerful fetish for a random body part. For the next 24 hours, sexual acts or advances using that body part are made against you with advantage.", "You lose any and all sexual characteristics, including genitals, until you complete a long rest. While transformed in this way, you may gain arousal, but automatically succeed on climax saving throws", "Your pubic hair grows to a length of 12 inches, and is silky soft. It cannot be cut until you complete a long rest, after which it falls out and returns to its natural state.", "Your erogenous zones become fully and almost painfully erect for the next 4 hours.", "You are infatuated by the next creature you see for 1 hour, or until you climax.", "A tiny fey appears on your shoulder and proceeds to kink-shame you for the next 24 hours.", "A tiny imp appears on your shoulder and verbally encourages your most perverted sexual appetites for the next 24 hours.", "Your breasts increase in size by one size category and begin lactating at high volume and pressure for the next 1d4 hours.", "For next 1d4 hours, an ethereal squirrel proceeds to whisper your darkest sexual fantasies into the ear of any creature within 20 ft of you. If the squirrel is killed, 2 more take its place.", "For the next 24 hours, you find yourself aroused by the silliest of things. Each time you hear a joke, pun, or other comedic retort, you gain 1d4 psychic arousal.", "An illusionary copy of you appears within 5 ft of your current position, and lasts for 1d8 hours. The duplicate shares your appearance, but none of your ingame statistics, and is only interested in helping you get laid.", "1d12 spectres appear at random locations within 20 ft of you. They move with you, and perform no actions other than watching you and pleasuring themselves.", "For the next hour, the only words you can speak or write in any language are “Fuck Me”", "For the next 24 hours, each time you climax, each creature within a 10ft cone must succeed on a dexterity saving throw or be covered in cum and gain 2d6 acid stimulation.", "You smell strongly of sex for the next 24 hours. Any attempt to clean or remove this smell instead makes it stronger.", "A magical seal appears above your genitals. For the next 1d6 days, you automatically succeed on climax saving throws.", "You climax immediately, and the sound and image of your climax is magically broadcast to every creature of age within 1 mile.", "A powerful fey appears at a point within 20 ft of you and demands to be brought to climax. If you fail to fulfil their request, they cast bestow curse upon you. If you succeed, they may grant you some form of boon or aid.", "Your clothes magically transform to resemble a sexy maid’s outfit. For the next 24 hours, you feel the magical compulsion to cook and clean, after which your clothes return to normal", "You cast Arcane Eye. The magical sensor appears within 10 ft a creature currently engaged in sexual intercourse, regardless of range, and projects it’s observations 5 ft in front of you for all to see.", "The lower half of your clothes fall to the ground or are otherwise doffed, leaving your naked from the waist down.", "If you have a cock, it is transformed into an enormous limp noodle for the next 1d6 hours. If you do not have a cock, ignore this result and roll again.", "For the next hour, each of your fingers becomes tipped with a tiny cock", "For the next 24 hours, any container you open contains an erect disembodied cock, in addition to any other contents.", "A small rainstorm of flexible dildos falls on you, striking you for 1d4 bludgeoning damage. The dildos disappear shortly after falling to the ground.", "You cast Grease, centred on yourself", "If you have balls, they burst into harmless magical flame. For the next 24 hours, you produce powerful alcoholic drink in place of semen, after which your balls return to normal. If you do not have balls, ignore this result and roll again.", "If you have tits, they become covered in a thin layer of frost, and feel cool to the touch. For the next 24 hours, squeezing them causes you to lactate ice-cream, after which your tits return to normal if you do not have tits, ignore this result and roll again.", "Your senses are magically altered. For the next minute, you treat damage done to you as stimulation, and stimulation done to you as damage.", "You gain the cock of a dragon or similarly sized monster, chosen by the DM. This lasts for 1 hour.", "For the next 24 hours, each time you succeed on a knowledge check, you must make a climax saving throw, regardless of your current arousal.", "Each creature within 20 ft of you must succeed on a wisdom saving throw or become hyperaroused for 1d4 rounds.", "Even the lightest touch thrills your mind with mental pleasure. You gain an extra 1d6 psychic stimulation whenever you gain stimulation from a physical source.", "Your hair transforms into 1d4 tentacles for the next hour. These tentacles act on your initiative each round. If you do not command them, they make a sexual act against the nearest creature, or you, if there are no other targets.", "You and a random creature within 30 ft swap genitals for the next hour. Stimulation and other sensations affect the original owner of the genitals, rather than the current owner", "Your genitals detach from your body and become a tiny creature with the statistics of a homunculus. They reattach or reappear after 24 hours, or if reduced to 0 hit points", "For the next 24 hours, your skin flashes through vibrant colors to display your emotions and arousal. Insight checks against you are made at advantage.", "For the next 1d6 days, each time you climax, your cum animates into a small elemental sprite with the statistics of a water mephit.", "For the next 24 hours, when you climax, your genitals release a small cloud of colourful confetti and the sound of a birthday cheer in place of cum. ", "You and all creatures within 30 ft of you must succeed on a constitution saving throw or become intoxicated for the next minute", "You Cast Evards Black Tentacles centered on yourself. The tentacles deal stimulation instead of damage.", "Your Cast the Light Spell targeted on your erogenous zones.", "Your Clothes Animate and begin pleasuring you. You gain 1d6 bludgeoning stimulation at the start of each of your turns. This effect lasts until you remove your clothes by succeeding on a strength saving throw.", "You Grow Animal Ears and a tail. For the next 24 hours, your speech is magically altered to include cute animal noises and puns, after which the tail and ears disappear.", "You transform into a gargantuan dildo for one minute.", "For the next minute, if you move more than 5 ft on your turn, your ass cheeks cast the thundeclap cantrip as a free action.", "A pair of phallic horns appear on your head, crowned with a halo of flames. These horns remain for one hour, after which they disappear", "14 werewolves appear at random points within 30 ft of you. They are fully erect and violently horny.", "You cast charm person, targeting a random creature within range.", "It all goes to your hips. For the next minute, your size category increases by one, and your intelligence score becomes 8", "A large, phallic mushroom bursts from the ground at a point within 5 ft of you. If touched, it moans loudly.", "For the next hour, you can only speak or vocalize in animal noises. This does not impact your ability to cast spells with verbal components Wild and Lustful Magic", "You cast entangle, centered on yourself. Creatures that end their turn within the spell’s area take 1d4 bludgeoning stimulation.", "Your undergarments teleport to the top of your head. If you are not wearing undergarments, someone else’s undergarments teleport to the top of your head.", "Error 404, your sex is missing", "A succubus appears at a point within 20 ft of you, and makes it their personal mission to seduce you into lecherous acts.", "You regain your virginity. You lose proficiency with all sexual implements (including your natural implements) until you cause another creature to climax.", "For the next 24 hours, faint and seductive music can be heard playing by any creature within 30 ft of you. Nice.", "Your tongue grows to a length of 2 ft, and counts as a +1 sexual implement for the next hour.", "You cast Time Stop. Sexual acts you perform while under the effects of this spell do not cause the spell to end.", "A wolf or other large canine appears at a point within 5 ft of you and immediately attempts to hump your leg", "A random object within 30 ft of you becomes a mimic.", "You cast prestidigitation, soiling the pants of the nearest creature other than yourself that is wearing pants.", "A market stall full of bread appears within 30 ft of you. Everyone is uncomfortable.", "A Ghost appears at a point within 5 ft of you and proceeds to perform oral sex on you for the next minute, or until you climax.", "You are showered with the loose pages of a large journal. Each page contains a beautifully rendered images of feet", "Sexually degrading writing appears all over your body. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.", "You cast Enthral, targeting all creatures within range.", "2d6 poisonous snakes appear within 20 ft of you. They have a fly speed of 30 ft, and their bite attacks deal stimulation instead of damage.", "A strange nun appears, spanking you for 1d8 bludgeoning damage before disappearing", "You cast suggestion on yourself and your nearest ally. The suggestion is to kiss", "You are showered in coins and tips. Gain 2cp for every sexual act or advance you have made in the past 24 hours", "A bullywug appears from the nearest body of water, and attempts to persuade you into kissing it. The bullywug claims to be royalty of some sort.", "You cast haste on yourself. Your skin turns blue for the duration of the spell.", "Your genitals are swarmed by an array of tiny harmless lizards for the next 24 hours. The lizards spread to any creature you have sexual intercourse with.", " I disembodied voice calls from the distance, encouraging you to “do it for the exposure” each creature that can hear the voice must make a performance check, and lose a number of CP equal to the result.", "A for the next minute, an ethereal greatclub hovers over you, attacking any creature you can see that performs a sexual act or advance. The club uses your spell attack modifier when making attacks", "If you have a pussy, it transforms into a fragrant flower for the next 1d6 hours. If you do not have a pussy, ignore this result and roll again.", "An incredibly attractive goblin appears at a point within 5 ft of you, wearing leather pants and singing words of power. He claims to be a king, and will not leave until you agree to marry him.", "You begin drooling uncontrollably, and are unable to close your mouth.", "A random barmaid appears, slapping you for 1d4 bludgeoning damage before calling you a pig or a whore and then disappears", "If you have tits, you magically grow an additional single breast", "A talking squirrel appears at a point within 5 ft of you, and drunkenly accosts you for money before asking if you know where he lives. He seems to be having a very bad day.", "For the next minute, any food you touch magically transforms into dick-shaped candies.", "A portal to your genitals appears on a random surface within 1000 miles. The portal lasts for 24 hours, and can be used to perform sexual acts.", "You cast Hypnotic pattern, centered on your nipples.", "If you have a cock, it magically splits into two duplicates of itself for the next 24 hours.", "A scarlet “A” appears on your left breast, and is visible through your clothing. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.", "You violently climax in a burst of magical energy, regaining all expended spell slots."]

curses = ["Clinging Arousal: A thick aura of deep arousal clings to you, making it difficult to resist the wiles of others. While cursed in this way, you become permanently hyperaroused, and have disadvantage on saving throws against the charmed and infatuated conditions, as well as persuasion checks made to seduce you."]

speechcursed = []
speechcurses = []

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

def checkreact(message):
    print(message)
    def inner_check(message, react):
        if message.id == int(eggsfound[-1]):
            return True
        else:
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

emoteCursed = []
emoteCurses = []
emoteCursechance = []

eggtimer = 0
egglimit = 0
eggfinders = []
eggsfound = []
eggnexttime = 0
eggwaittimer = 300

#Staff Functions
functionnames = ["Writing Lore", "Creating Areas", "Creating NPCs", "Writing Stories/Quests", "Running Stories/Quests", "Running Encounters", "Organising Player Facing Lore", "Organising Deep Lore", "Running NPCs", "Creating And Running Events", "Running Auctions", "Running Non-con Encounters", "Generating Loot", "Generating Statblocks", "Creating Homebrew", "Balance Checking Homebrew", "Approving Character Sheets", "Verifying New Members", "Video Verifying New Members", "Creating Server Rules", "Reporting Broken Rules", "Enforcing Rules", "Issuing Strikes And Bans", "Checking Art Channels For Inappropriate Images", "Managing the Economy", "Balancing Economy Prices", "Writing Bot Functions", "Bug Fixing Gothica", "Managing Channels, Forums And Threads", "Responding To User Issues"]
functiondesc = ["This involves creating the deeper lore of the dungeon, involving things that players wouldn't know or won't have more than hints of for a while.",
                "This relates to the development of new spaces within the dungeon, whether safe areas, dangerous depths, or housing districts.",
                "The creation of people to live in the world of the dungeon.",
                "Developing stories that feature several encounters, usually for some larger reward, such as a new area opening.",
                "Running the stories that are developed above, and acting as the main DM for them.",
                "Encounters can be things such as single combats or lewd scenes, either standalone or as part of a quest.",
                "This involves determining what lore players have access to, and answering questions on that lore.",
                "Like the above, this function involves deciding what lore is easily accessed by the team creating quests.",
                "Primarily running shopkeepers and other small encounters to make the world feel alive.",
                "Events might range from hosting in character games to orchastrating wider roleplay situations.",
                "Auctions are for the sale of playable characters as slaves or pets. This function is about creating these and ensuring they run smoothly.",
                "This involves running traps and other non consensual encounters, geared towards people who intend to lose, rather than other encounters which might be a more standard fight.",
                "The creation of items as rewards for quests etc.",
                "This role helps to develop a bestiary for the server, creating interesting creatures to fight/fuck.",
                "This is mostly related to the development of the Lewd Handbook.",
                "This ensures that our created material matches correct levels of balance.",
                "Checking character sheets to ensure balance and correct implementation of features.",
                "Checking Yoti and picture based verifications to ensure people are of age to enter the server.",
                "Verifying people via video chat.",
                "These determine what is acceptable behavior on the server.",
                "Bringing rule breaking to the attention of the team so that it may be addressed.",
                "Informing people of their misbehavior, issuing tempmutes.",
                "Determining if behavior was bad enough to warrant a strike or even a ban.",
                "Deleting any images showing underaged people or real porn from the Gallery of Sin.",
                "Importing homebrew items into the economy spreadsheet, managing available quantites and descriptions, and managing the amount of dezzies people earn and have access to.",
                "Setting the price of items against their balance.",
                "Coding Gothica in Python, for example to implement a new feature.",
                "~~An entirely unneccessary function. Gothica has no bugs.~~\n\nFixing Callum's poor coding, using the Python coding language.",
                "Creating channels and managing their positions and permissions.",
                "Preventing arguments, directing people to correct channels, being pinged by users, and responding to tickets."
                ]
functionreqs = [0, 0, 0, 0, "Naming a Co-Pilot", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Fucksmith Exam?", 0, 0, 0, 0, 0, 0, "Voted Role", 0, 0, 0, "A lack of sanity", "A greater lack of sanity", 0, 0]

playerreqsnames = ["Run a shopkeeper", "Run another NPC", "Run an encounter", "Run a noncon scene or trap", "Run a longer quest", ""]

async def stafffunc(mess, resp, memb):
    index = functionnames.index(mess.channel.name)
    if mess.channel.name == "Running NPCs":
        if mess.embeds[0].title == "Tools for running NPCs":
            if resp == 1:
                await mess.channel.send(embed = discord.Embed(title = "Which NPC are you looking to run?", description = "This message will timeout in 60 seconds", colour = embcol))
                try:
                    msg = await client.wait_for('message', timeout = 60)#, check = check(memb))
                    if "webb" in msg.content.lower():
                        await mess.channel.send(embed = discord.Embed(title = "Madame Webb", description = "Name: Madame Webb\nCommon location: ⁠🧵widows-boutique🧵\nRace and Class: Lvl 16 Jorogumo (japanese drider) Enchantress\nSexuality: Pansexual\nGeneral traits: Refined, High-Class, Dominant. Commanding. Venemous. Masked. Closed-off.\nMannerism: Webb does not negotiate. She issues commands and expects them to be carried out. She demands respect, and offers the same in return, until she is given reason not to. Play her like you would a powerful fae. (After all, that's what Jorogumo actually are)\nSpeech patterns: Refined and tasteful, with just a hint of 'I'm better than you, and you know it'. Very 'Ara Ara' vampire/fae Speech example: ' Why, My Darling little fly, it would seem you have found yourself cought in somewhat of a predicament. Now, I would be more than happy to waive some of that debt - In exchange for certain... Services.'\nBond: Webb remains mostly aloof within the Dungeon, and tries not to form any strong bonds or connections with anyone. She is exceptionally closed off, and one of the few people in the dungeon who she does feel comfortable opening up to is Reverend Mother Serena, who has helped her com to terms with much of her past.\nQuirk: While it is not exactly a secret the Webb is a Spider of sorts, she almost never reveals her true form, even in private. She takes more satisfaction than she probably should from controlling others, and actually rather enjoys extortion and blackmail. She is also a Shibari Expert of the highest Caliber, and considers herself an artist. Often valuing her subjects more as peices of art than as people. Values: Respect, Decorum, and Pretense. While Webb is actually far less pretentious than the rest of her royal family, she still values position and appearance. It is important that all things she does are seen as graceful and beautiful.\nSecret/Hook: Web was cast out from her family for fraternizing with those blow her station, and has a complicated history that, best as she can tell, ended in her death at the hands of male rival. Then she woke up in the dungeon. Serena has been halping her work through the confusion and trauma, to understand what happened. Reactions: What does this character do when - (Any other key reactions welcome) Threatened: Return in kind, never dropping the mask of pleasant conversation. And use her power to ensure said person will never threaten her again. Flirted with: flirt back using every tool of seduction in her arsenal. Sex is one of the easiest ways to manipulate a person, and she makes sure she is in control of any such manipulations from the start. Asked for help: it depends on what is being asked. She rarely offers goods or services for free, but she will go out of her way to help someone who truly needs it. Her help generally comes with strings attached though. Everything is an exchange. Bonus: Webb offers discounts on her wares to customers she would like to use as display peices in her shop. Generally, that means being suspended or posed as a paralyzed mannequin for several hours at a time. These displays are purely 'Look, do not touch' Important links below: Webb from NPC questionnaire: https://cdn.discordapp.com/attachments/1020227364371845172/1061987049479098458/Madame_Webb.txt (edited)"))
                except asyncio.TimeoutError:
                    await mess.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                await msg.delete()

#Help message
async def helplist(message):

    helptextmain = ["**Hello, We are Gothica, the Shoggoth Servants of T̶̤̻̘͙̩̖̿ͅḩ̷̲̣̙͚̯̮̐͂̃͜͠e̴̳̦͍̮̹̦̠͛͒̅́ ̵͚̥̯̫̼̦̦̻͌͑̑̑̕Ḿ̷͓̀͗̇̊͆͒̀i̴̻̼̙̺͙͂̃͘͝s̵͖̝͈̤̖͓̬̖͗̃͘ͅt̷̢̫̠̼̭͚́̅͒̐͋̃̈́̂͠r̶̡̧̭͓͇̝̥͖̺͑̆̅͑͂̉̊̋͘͝e̸̦͈̩̠̩̣̔̊̎̀̔͒̊̎͜͝s̵̛̛̭̙̜͑̓̒̾͜ͅs̶̢̝͍̯͚̰͛́̾. We facilitate a number of functions in the dungeon. A summary of some of those functions is given below. If you would like more information on any function, type the number that corresponds to it. You can also specify it when you call the help command, such as by doing `%help registration`**"]
    
    helpcategories = ["General Functions", "Character Index Functions", "Roleplay Functions", "Kink Functions", "Economy Functions", "Lorekeeper Only Functions"]
    helpnames = [
        ["Start", "Rulebook", "LewdReference", "Embed", "Help", "Timestamp", "Migrate"],
        ["Character Registration", "Edit", "Transfer", "Charlist", "Search", "Retire", "Deactivate", "Activate"],
        ["LFG", "Plothook", "Plotlead", "Room", "Break", "Recent", "Wildlust", "Gobblin", "Scenes", "imptome"],
        ["Kinklist", "Kinksurvey", "Kinkfill", "KinkEdit", "Kinkplayers"],
        ["Work", "Slut", "Money", "Inventory", "Give-Money", "Leaderboard", "Shop", "Item", "Buy", "Sell", "GiveItem", "Invest", "Bid", "Spend"],
        ["Gag", "Emote", "Adventurer", "Verify", "Kinkencounter", "oocembed", "oocmsg", "Add-money", "Remove-Money", "AddItem", "Spellrotation", "RandLoot", "clonev2", "CommunityProject", "giftall", "rewardpoolreset", "manualmigrate", "MVP"]
    ]
    helpsummary = [
        ["Calls up some welcoming information for new members", "Summons a link to the lewd rulebook", "Summons a quick reference sheet of the main rules for Sexual Advances", "Generates an embed, like this one", "You are here.", "Compares timezones", "Migrates account from old Discord username to unique username."],
        ["Registers a character to the index", "Edits a character", "Gives a character to another player", "Lists the characters owned by a player", "Provides the index entry of a character", "Retires a character", "Sets a character temporarily unactive", "Reactivates a deactivated character"],
        ["Helps you find roleplay partners", "Generates a random plothook for your character", "Checks how many plothooks you have seen", "Suggests an empty room for you to roleplay in.", "Generates a scene break", "Provides the time of the last message in each roleplay channel", "Rolls on the wildlust table", "Eats a dezzie", "Stores and recalls your list of active scenes and can DM you whenever a new message is sent in them", "Manually spawns the imptome into an RP (Only usable by the imptome wielder)."],
        ["Summons the kinks of the tagged player", "Allows you to fill out the kink survey", "Fills any holes in the kinksurvey", "Edits a kink", "Summons a list of players with the targeted kink"],
        ["Earns daily dezzies", "Earns more dezzies, with a risk to lose some instead", "Checks your balance", "Displays your items", "Gives a number of dezzies to someone else", "Shows how rich the richest people on the server are", "Displays the listed shop", "Provides details on a shop or inventory item", "Buys an item", "Sells an item, at a loss.", "Transfers an item to another player", "Spends dezzies on a community project", "Bids on an auction in the Black Market", "Removes Dezzies from yourself"],
        ["Gags a user in ooc", "Reacts to a message with emote letters", "Grants a player the Adventurer Role", "Confirms that a user is over 18", "Generates a random encounter, respecting the player's kinks", "Generates an embed in ooc", "Sends a message in ooc", "Adds money", "Removes money","Adds an item from the shop to a user's inventory", "Checks Runar's stock of spells", "Generate random loot that fits a player's kinks", "Clones the contents of a channel or thread to another channel or threads, including tupper messages.", "Registers a new community project people can %invest in!", "Gives (or takes) dezzies to every person registered in the economy.","MOD ONLY: Resets the dezzie reward pool for all players if needed.", "MOD ONLY: migrates an account from old to new naming system without automatic failsaves. Read full help before using.", "Grants the user the MVP Role"]
    ]
    helpfull = [
        ["The `%start` command provides an overview of how new players can start making characters and roleplaying in the dungeon, highlighting how to get roles and create a character and tupper.",
        "Summons the dropbox link to the latest version of the Lewd Rulebook, as well as some useful quick stats on inhibition and arousal. The command is `%rulebook`",
        "Summons a reference sheet for things like lewd statuses, natural implement stimulation values, and other common things needing to be looked up. The command is %LewdReference",
        "Allows you to generate a message in a fancy embed. If you simply type `%embed`, followed by your message, it will use the message as the title.\n\nIf you want different fields like descriptions and images, it is a bit more complex. In this mode, to write a title and description, you would do: `%embed -t =Title goes here= -d =Desciption between these equals signs=` You can also add -i =image link= or -m =thumbnail link=. Obviously, this means that you can't use equals signs in the content of your embed.",
        "Summons this interface. You can use just `%help` on its own, which pulls up the full list of commands, or you can specify the category (So `%help economy` will pull up only the economy commands) or the specific command (`%help help`, for example, will bring up this message).",
        "This command allows you to specify a time and timezone, for which we will create an embed that shows that time in the timezone as a timestamp that is correct for anyone reading it. The syntax is `%timestamp HH:MM code`, where HH:MM is the hour and minute and code is the code for the timezone.",
        "This command migrates your account from the old username system (username#0000) to the new unique username system (uniquename). For this to work you must have filled in your kinklist while you still had your old username. If you did not do that, contact mods, they can manually migrate you."
        ],
        ["To register a character, go to #character-creation and type some information about them. This message must start with Name, but after that, you can use as many or as few bits of information as you want. Each should be on its own line. For example:\n\n`Name: Lalontra`\n`Race: Water Genasi`\n\nDo not use a tupper when creating your character.\n\nPossible Fields are:\n\nName\nRace\nGender\nPronouns\nAge\nClass\nLevel\nSheet\nAlignment\nBio\nSexuality\nSkin Colour\nHair Colour\nEye Colour\nHeight\nWeight\nSummary\nImage",
        "To edit a character, type `" + myprefix + "edit Name Field New-Value`, as a demonstration:\n\n`" + myprefix + "edit Lalontra class Ranger`\n\nThis will match a character's name even if you only use part of the name.",
        "For obvious reasons, only the owner of a character can edit them, but there are occasions where you want to give a character to someone else, for example in an auction. To transfer the character, type `" + myprefix + "transfer Name @New-Owner`, for example:\n\n`" + myprefix + "transfer Lalontra @C_allum`",
        "To create a list of the characters owned by any particular player, type `" + myprefix + "charlist`. Send the command without any arguments to see your own characters, or add a mention after it to see someone else's. As below:\n\n`" + myprefix + "charlist @C_allum`",
        "To search for a character or attribute, type `" + myprefix + "search Search-term`. If the search term is within the name of a character, it will provide that character's full bio. As an example, to find the bio of Lalontra you might type:\n\n`" + myprefix + "search Lal`\n\nIf the search term is not found in the name of a character, you can instead seach by a data field, done by typing`" + myprefix + "search Field Search-Term`, such as:\n\n`" + myprefix + "search class Ranger`\n\nIf the first argument after the command is neither in the name of a character, nor a field name, it will search the whole database, and provide details on where the word occurs. If you were to type:\n\n`" + myprefix + "search blue`\n\nYou would see information about any characters whos eyes, hair or skin colour (or any other attribute) was blue."
        "If you want to retire a character for any reason, type `" + myprefix + "retire Name`, as per the below example ||which was rather painful to write!||:\n\n`" + myprefix + "retire Lalontra`",
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
        "Eating the server currency can have some strange effects. Run `" + myprefix + "Gobblin` or `" + myprefix + "Crunch` to eat a dezzie. A dezzie of a good size to eat has a value of around 10 dezzies. You can also add a number after the command to eat a certain amount.",
        "Gothica can track your scenes. Running `%scenes add` followed by a brief description of the scene and then the link to it, will tell us to track that scene. You can then do `%scenes` to summon the list of scenes, and we will inform you who sent the last message in the channel. As an example, you might type: `%scenes add Lalontra and River fight an evil fae #An-Uncomfortable-Reunion` to add that scene to your watchlist. You can also remove scenes with `%scenes remove` and then the number of the one to remove. Gothica can also DM you whenever a message is sent in a tracked scene. To enable that run `%scenes notification` and select the scene you want to get notifications on. `%scenes notification all on` or `%scenes notification all off` toggles notification settings on all tracked scenes at once.",
        "If you are the imptome weilder, you can call `%imptome [message Link]` to spawn the Imp Tome in response to that message. ALWAYS CHECK WITH THE PEOPLE IN THAT RP IF THEY WANT THAT FIRST! If you are the Imp Tome wielder, but can't use this, contact Ken, he has to set a variable in the code..."
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
        "You can sell items from your inventory, based on the cost you paid for them. We will return them to the shop or to other areas of the dungeon for you, and will award you half the dezzies they are worth. To use this command, do `%sell itemname amount`",
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
        "To reward a player with randomised loot, you can run the `%randloot @name` command. This generates a piece of loot and compares it to their kinks - so they cannot get a piece of loot that crosses one of their limits. You can also specify the rarity of the item, or a range of rarities to roll from, for example, `%randloot @C_allum very rare` or `%randloot @C_allum common-rare`. It will then ask if you want to cancel, edit the item, or add it to the player's inventory as is.",
        "Clones the contents (all messages) of the channel the command is called from to another channel/thread. `%clonev2 destinationchannel destinationthread`. These can either be #links or just channel IDs. Note that the destination channel must contain the destination thread, and the command has to be called in the thread you want to copy!",
        "Registers a new community project that people can invest in. `%communityproject -[projectName] -[projectDescription] -[dezzAmountNeededToComplete] -[FailChance(Put 1 for 1%, 5 for 5% etc)] -[VictoryMessage]`. Project name is the name, for example `Rebuilding the Burlesque`. Project Description is what appears in the initial embed. DezzAmountToComplete and fail chance are self explanatory. Victory message is the message used when the project reached its investment goal.",
        "Gives a specified amount of dezzies to each person registered in the economy if the specified amount is positive, or takes that amount from everyone if it is negative. %giveall [amount]",
        "Resets the dezzie reward pool (for reactions) if something went wrong with the weekly reset. If the underlying function doesn't work, this won't work either as it just manually calls the reset function.",
        "Allows to migrate a players account from old to new naming system without failsaves of checking if the two accounts are actually linked. MAKE SURE THAT THE NAME THE PLAYER GIVES YOU ACTUALLY BELONGS TO THEM! You can see old usernames on the badge in the top right of their account. Command is `%manualmigrate [newUsername] [oldname#4-digit-number]`",
        "`%mvp @name` will grant the tagged player the MVP role, which will be removed when the bot restarts"
        ]
        ]

    #Check for lorekeeper channels
    if message.channel.category.name != "﴿─﴾ 𝙻𝚘𝚛𝚎𝚔𝚎𝚎𝚙𝚎𝚛'𝚜 𝙲𝚊𝚋𝚊𝚕 ﴿─﴾" and message.channel.category.name != "▐ ₪₪ ▌𝙱𝚊𝚌𝚔 𝚘𝚏 𝙷𝚘𝚞𝚜𝚎▐ ₪₪ ▌" and message.channel.category.name != "Secret Lore":
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
                if helpnames[a][b] == "Character Registration":
                    helptextcatmain.append("`" + str(index) + "`: *" + helpnames[a][b] + ":* " + helpsummary[a][b])
                else:
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

        #check if message is too long, else split
        if len("\n".join(helptextmain)) > 3800:
            half_length = len(helptextmain) // 2
            await message.channel.send(embed = discord.Embed(title = "Gothica Help", description = "\n".join(helptextmain[:half_length]), colour = embcol))
            await message.channel.send(embed = discord.Embed(title = "Gothica Help", description = "\n".join(helptextmain[half_length:]), colour = embcol))
        else:
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
