from ast import Index, Pass, excepthandler, literal_eval
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
from discord.ui import View
from discord.utils import get
from discord.embeds import Embed
from discord.enums import NotificationLevel
from discord.ext import commands
from datetime import date, datetime, timedelta
from discord.ext.commands.errors import NoPrivateMessage
from thefuzz import fuzz

from discord.gateway import DiscordClientWebSocketResponse
from discord.guild import Guild
from discord.utils import sleep_until

from googleapiclient.discovery import build
from google.oauth2 import service_account
from pyasn1.type.univ import Enumerated
from pyasn1_modules.rfc2459 import ExtensionPhysicalDeliveryAddressComponents, Name, RelativeDistinguishedName
from pyasn1_modules.rfc5208 import PrivateKeyInfo
from random import sample

import gspread
import GlobalVars
import botTokens

intents = discord.Intents().all()

client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='%', activity = discord.Game(name="Testing Stuff"), intents = intents)

print(" Initialised {0.user} at ".format(client) + str(datetime.now()).split(".")[0])

SERVICE_ACCOUNT_FILE = "keys.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/documents"]

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build("sheets", "v4", credentials=creds)

gc = gspread.service_account(filename = SERVICE_ACCOUNT_FILE)
config_file_path = "config.yaml"
#-----------------LIVE VERSION/BETA TOGGLE---------------
# 0 is Test Server, 1 is Live Server
liveVersion = 0
token = ""

#Sheet Locations:

if liveVersion: #Set to 1 to use the real spreadsheets, or 0 to use the testing spreadsheets.

    CharSheet = "1iHvP4HC8UQqyiMmC3Xiggx8-17e5SGWJMncEeoiZP1s"

    EconSheet = "1qTC0gn7Fe_cHDVPB8KIEjSFUwrUSEhlLy1upHIKnKF8"

    #newEconsheet
    inventorysheet = "15u6xzZsY5mZAUVmXPolRqUkPeQcGFH1_H-sNCjfNhNM"
    
    itemsheetID = "1rS4yTmVtaaCZEbfyAAEkB3KnVC_jkI9e2zhSI0AA7ws"
    itemsheet = gc.open_by_key("1rS4yTmVtaaCZEbfyAAEkB3KnVC_jkI9e2zhSI0AA7ws") #New for economy rewrite
    itemlists = itemsheet.worksheets()

    shopsheet = "1gxNPXIichzK9mSN8eHYVdJvaaUgUnN6VF8WshL_4Les"

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg"

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4"

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA"

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU"

    Randomlootsheet = "19Dc4PI-E5OubesNroJfB4zKg9bqqqbdPelodjH6ecNw"

    TransactionSheet = "1GKiiWlTPlMDj8FCiNZcNSF_FFJi6J_CKTyimdjoo9GU"

    logchannel = 918257057428279326

    aliasBotChannel = 830799558514573312

    botchannel = 1050503346374594660

    bridgechannel = 996826636358000780

    communityProjectChannel = 999810708546002994

    indexchannel = 898640028174016552

    datingchannel = 1204872179871653898

    guildid = 828411760365142076

    oocchannel = 832435243117445131
    welcchannel = 828411760847356005
    servermemberlog = 841736084362362940
    menageriechannel = 917239168969621515
    vacationthread = 1251657363425853500
    arbchannel = 1145240920296538162

else:

    CharSheet = "1Vgxa8C5j5XnEUGhaGqAANVhsWSIOra87wCE2f5C75tQ"

    #OldEconSheet
    EconSheet = "1mmWxHhDUPI0PjLC2UXJZmj5wNqXnucFMz-er9NpVC2c"
    
    shopsheet = "1tj64lIs9qvfv3wUDjU5AHplhRoXU4i-qgHj21-Q7olk"

    #newEconsheet
    inventorysheet = "14MievWBXOIhBdTOvXLht7ZOtrBkUbRU0YrzidIsyQMw"

    #itemsheetID = "17M2FS5iWchszIoimqNzk6lzJMOVLBWQgEZZKUPQuMR8"
    #itemsheet = gc.open_by_key("17M2FS5iWchszIoimqNzk6lzJMOVLBWQgEZZKUPQuMR8") #New for economy rewrite
    itemsheetID = "1rS4yTmVtaaCZEbfyAAEkB3KnVC_jkI9e2zhSI0AA7ws"
    itemsheet = gc.open_by_key("1rS4yTmVtaaCZEbfyAAEkB3KnVC_jkI9e2zhSI0AA7ws") #New for economy rewrite
    itemlists = itemsheet.worksheets()

    encountersheet = "1poNQfcqLqkiK9NaKBqNOk_DDUsTr8GuBEVQP_uQcjeg" #No change as yet

    kinksheet = "1Y3qNUEu8M6c5SL-iYlFQqmMZ0no1E2sQ5Vy_6vezzk4" #No change as yet

    gamesheet = "1S8lCkyM5puEKLAR9tNV44kWeECjqaKKBx0BqMdn9ABA" #No change as yet

    Plotsheet = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU" #No change as yet

    Randomlootsheet = "19Dc4PI-E5OubesNroJfB4zKg9bqqqbdPelodjH6ecNw"

    TransactionSheet = "1GKiiWlTPlMDj8FCiNZcNSF_FFJi6J_CKTyimdjoo9GU"

    logchannel = 1031701327169998958 #Test Server

    aliasBotChannel = 1142877836298965105

    botchannel = 891781900388159528

    bridgechannel = 891781900388159528

    communityProjectChannel = 891781900388159528

    indexchannel = 1031701327169998958

    datingchannel = 1203838135335653416

    guildid = 847968618167795782

    vacationthread = 1251656171291676723

    oocchannel = 1031671413607776327
    welcchannel = 1031671413607776327
    servermemberlog = botchannel
    menageriechannel = botchannel
    arbchannel = botchannel


sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId = CharSheet, range = "E1:AB1").execute()
values = str(result.get("values"))
values = values.replace("'","")
headers = values.split(",")

itemdatabase = []

namecol = 4

for i in range(len(headers)):
    headers[i] = headers[i].lstrip(" ")
    headers[i] = headers[i].lstrip("[")
    headers[i] = headers[i].rstrip("]")


#Slash command groups
class RoleCheckedGroup(discord.app_commands.Group):
    def __init__(self, name, description, role_name, *args, **kwargs):
        super().__init__(name=name, description=description, *args, **kwargs)
        self.required_role = role_name

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.required_role in [role.name for role in interaction.user.roles]:
            return True
        await interaction.response.send_message(f"You do not have the required role to use this command: {self.required_role}", ephemeral=True)
        return False

#@discord.app_commands.checks.has_role("Staff")
#class Staff(discord.app_commands.Group):
#    pass
#
#@discord.app_commands.checks.has_role("Admin")
#class Moderator(discord.app_commands.Group):
#    pass

staffgroup = RoleCheckedGroup(name="staff", description="Staff Commands", role_name="Staff")
admingroup = RoleCheckedGroup(name="admin", description="Moderator Commands", role_name="Admin")

#channels
if liveVersion:
    kinkcreatechannel = "1050503346374594660"
else: 
    kinkcreatechannel = "891781900388159528"
#Sheets

aliases = sheet.values().get(spreadsheetId = "1xGL06_MrOb5IIt2FHJFeW_bdcwedIKZX-j3m2djSOaw", range = "A1:W50", majorDimension='COLUMNS').execute().get("values")

plothooks = sheet.values().get(spreadsheetId = Plotsheet, range = "A2:O50", majorDimension='COLUMNS').execute().get("values")

workhooks = sheet.values().get(spreadsheetId = Plotsheet, range = "AO2:AO100", majorDimension='COLUMNS').execute().get("values")

sluthooks = sheet.values().get(spreadsheetId = Plotsheet, range = "AP2:AQ100", majorDimension='COLUMNS').execute().get("values")

rooms = ["the Unlit Passageways", "the Trapped Corridors", "the Moaning Hallways", "the Salamander Hot Springs", "the Monster Girl Cantina", "the Old Burlesque", "the Library of Carnal Knowledge", "the Cathedral", "the Gobblin' Bazaar", "the Fighting Pits"]

guildvar = client.get_guild(828411760365142076)

dezzieemj = "<:dz:844365871350808606>"

critemj = "<:crit:893767145060696064>"

embcol = 0xb700ff

botnames = ['Arcane', 'Avrae (in dice jail)', 'Dungeon\'s Herald', 'Dungeon\'s Keeper', 'Dungeon\'s Whisperer', 'Dyno', 'PartyBeast', 'Tempo', 'Thread-Watcher', 'Twitch Alerts']


awaitingsel = 0

prevchan = 0

selopts = []

column = ["F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB"]

startingslots = 5


#----------------EconomyValues----------------

auctionvars = [] # Char Name, Player Name, Character Data (excluding last line), Image URL, Embed Post, Current Bid, Current Bidder
auctionthreads = [] #Master Thread, Public Thread
bidstock = [] # Options for choosing who to bid for.
minincrease = 200

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

datingplayers = []
datingchars = []
datingsources = []
datingdests = []
datingcounts = []
datingscores = []
datingwaiting = []
datingprivatethreads = []
datingstate = 1
datingmax = 24

mazearray = [[["NEW", "NW", "NSX", "NS", "N", "NE"], ["W", "ES", "NW", "NE", "EW", "EW"], ["EW", "NW", "ES", "W", "ES", "EW"], ["ESW", "EW", "NW", "NS", "E", "EW"], ["NW", "ES", "S", "E", "SW", "E"], ["SW", "NS", "NS", "ESWB", "NSW", "ES"]],
             [["NW", "NS", "NEX", "NW", "NE", "NEW"], ["SW", "NE", "SW", "ES", "SW", "E"], ["NW", "E", "N", "NS", "N", "ES"], ["EW", "W", "SW", "NES", "SW", "NE"], ["EW", "EW", "N", "N", "NE", "EW"], ["SW", "SW", "ES", "SWB", "SW", "ES"]],
             [["NW", "NES", "NSWX", "NS", "NS", "NE"], ["SW", "N", "NE", "NW", "N", "ES"], ["NW", "E", "ESW", "EW", "SW", "NE"], ["ESW", "W", "N", "ES", "NW", "ES"], ["NW", "ES", "SW", "NES", "E", "NW"], ["SW", "NS", "NS", "NESB", "SW", "ES"]],
             [["NEW", "NW", "NX", "NS", "NS", "NE"], ["W", "ES", "EW", "NW", "NE", "EW"], ["W", "NES", "EW", "EW", "SW", "ES"], ["SW", "N", "NS", "S", "N", "E"], ["NW", "ES", "NW", "NS", "S", "NE"], ["SW", "NS", "ES", "NSB", "NS", "ES"]],
             [["NW", "NS", "NE", "NWX", "NE", "NSW", "NE"], ["SW", "NE", "EW", "EW", "SW", "N", "ES"], ["NW", "ES", "ESW", "SW", "NE", "SW", "NE"], ["EW", "NW", "NS", "NS", "ES", "NW", "E"], ["W", "ES", "NW", "NS", "NS", "ES", "EW"], ["W", "NS", "S", "NE", "NW", "N", "ES"], ["SW", "NS", "NES", "ESWB", "ESW", "SW", "NES"]],
             [["NW", "NS", "NE", "NSWX", "N", "NE", "NEW"], ["SW", "NE", "SW", "N", "E", "SW", "ES"], ["NW", "ES", "NW", "ES", "SW", "NS", "NE"], ["SW", "NE", "W", "NS", "NS", "NE", "EW"], ["NW", "E", "SW", "N", "NSW", "ES", "E"], ["EW", "N", "NS", "S", "NSW", "NE", "EW"], ["SW", "S", "S", "NSB", "NES", "SW", "ES"]],
             [["NW", "NS", "N", "NESX", "NEW", "NW", "NE"], ["EW", "NEW", "W", "NS", "S", "ES", "EW"], ["EW", "W", "S", "NS", "NES", "NW", "E"], ["ESW", "SW", "NE", "NW", "N", "E", "EW"], ["NW", "NE", "W", "E", "ESW", "W", "NE"], ["EW", "SW", "E", "SW", "NS", "ES", "EW"], ["SW", "NS", "S", "NSB", "NS", "NS", "ES"]],
             [["NW", "NE", "NSWX", "NS", "NE"], ["EW", "EW", "NW", "NE", "EW"], ["W", "S", "ES", "W", "ES"], ["EW", "NW", "NS", "S", "NE"], ["SW", "S", "NESB", "NSW", "ES"]],
             [["NEW", "NW", "NEX", "NW", "NES"], ["W", "ES", "ESW", "W", "NE"], ["W", "NS", "N", "E", "ESW"], ["EW", "NW", "ES", "W", "NE"], ["SW", "ES", "NSB", "ES", "ESW"]],
             [["NEW", "NW", "NEX", "NW", "NES"], ["W", "ES", "ESW", "W", "NE"], ["W", "NS", "N", "E", "ESW"], ["EW", "NWB", "ES", "W", "NE"], ["SW", "ES", "NSW", "ES", "ESW"]],
             [["NW", "NE", "NWX", "NE", "NW", "NE"], ["EW", "SW", "ES", "W", "ES", "EW"], ["SW", "NS", "N", "S", "NE", "EW"], ["NEW", "NW", "S", "NES", "W", "E"], ["EW", "W", "NEB", "NW", "ES", "EW"], ["SW", "ES", "SW", "S", "NS", "ES"]],
             [["NEW", "NW", "NE", "NWX", "NS", "NE", "NEW"], ["W", "ES", "W", "E", "NEW", "SW", "E"], ["SW", "NE", "EW", "SW", "S", "NS", "E"], ["NW", "E", "EW", "NW", "NS", "NE", "EW"], ["EW", "SW", "S", "", "NES", "W", "ES"], ["EW", "NW", "N", "S", "NE", "W", "NE"], ["SW", "ES", "SW", "NSB", "ES", "ESW", "ESW"]]
             ]


mazeoptions = ["the sound of hot, heavy breathing, emanating from a large minotaur, who turns to face you as you enter the space! His weighty hoof tests at the ground, as though ready to charge. You'll have to run! From now on, you can constantly hear the sound of the minotaur behind you, and if you linger too long, he might catch up with you! If you find a dead end or have to backtrack, you'll be caught!", "a seemingly bottomless pit. You manage to catch yourself just at the edge of it, and avoid falling in. You can just see the ground on the other side of it, and the square hole covers the vast majority of the floorspace in this room.", "a sudden and inexplicable urge to kiss your partner.", "that all of this running around has made you quite sweaty. Maybe you should lose a few layers?", "could it be... the way out? An archway stands on the wall, opening out to a beautiful garden. Closer inspection reveals that it is merely an illusion.", "a pair of kobolds, almost entirely entwined around each other. They seem irritated by the intrusion.", "a circle of oddly phallic mushrooms. They smell quite enticing.", "a scrap of parchment, which looks like it contains a poorly drawn map. If it is of this maze, it is quite evidently wrong.", "the floor is covered with something sticky and the room reeks of the odour of recent sex. It is difficult to move quickly through this space.", "the floor is made of a mosaic of tiles, which depict some carnal act of your two characters.", "a statue of a very beautiful woman with snakes for hair. Although she is made of stone, she is oddly enticing, and some might find themselves longing to gaze into her eyes...", "the space to be oddly quiet, and the air especially still. It is impossible to talk above a whisper in this space.", "a sense of deja vu, as though you have been in this room before, even if that isn't possible.", "the floor steps down, and this room is filled with a knee deep basin of water. Entering it feels oddly soothing.", "a set of altars devoted to various gods. It feels like you should leave an offering at one. One has small piles of " + random.choice(["tokens for use in a goblin laundromat.", "coins featuring bunnygirls.", "unused parchment, along with quills and ink.", "golden wool, alongside a partially knitted fleece."]), "the floor here seems oddly bouncy? Each step launches you into the air, and you can easily jump twice your normal maximum.", "the ceiling is incredibly low here, to the extent that you would need to crawl through. Try not to get stuck", "a chest that is *obviously* not a mimic.", "a small pillow, along with various mouse-like toys. A wooden post in the centre of the room is wrapped in heavily scratched twine and the walls are adorned with empty shelves.", "a sign pointing to the exit. Confusingly, it points in two opposite directions.", "a grey housecat, strutting happily around like she owns the place. She meows loudly, particularly if she suspects the adventurers of having food, and will happily accept being petted, though she will resist any attempt to get her to leave the room.", "a collection of glass dildos, arranged from smallest to largest.", "a pair of yellow eyes watching from the far end of the room. Should you cross the space, whoever, or *whatever* it was, has vanished...", "a functioning stockade, raised on a small podium in the middle of the room.", "four sizeable chairs set around a table. The table " + random.choice(["is covered with maps, minis, and dice.", "contains the remnants of a recent meal. The cheese in particular looks quite fresh.", "has art supplies laid neatly upon it."]), "that the contents of this room fade from your memory as soon as you stop looking at them. Whatever they were, you remember being fairly impressed.", "several rows of bookshelves, each dedicated to construction materials from around the world.", "a small slime, set into a maze of its own under the glass floor in this room.", "the makings of what appear to be a puzzle, though it hasn't yet been constructed. The tripwire is self explanatory, but it is unclear how the petrified frog fits into things.", "a large bed, occupying the middle of the room. It appears to be occupied... by a minotaur! His eyes snap open, and he throws back the blanket, gaze fixing upon your characters.You'll have to run! From now on, you can constantly hear the sound of the minotaur behind you, and if you linger too long, he might catch up with you! If you find a dead end or have to backtrack, you'll be caught!", "a goblin wearing a pinstriped suit, muttering to himself about dirty clothes.", "yourselves dancing to a mysterious beat. The tune sticks in your head even after you leave the room.", "that while in this room, you are affected as if by the " + random.choice(["fly", "haste", "slow", "enlarge", "reduce", "faerie fire"]) + " spell.", "a trio of tiny collectori, gambling with each other. The stakes appear to be coveted parts for their forms.", "an illusion that fills the space with tiny birds.", "the ground to be oddly crisscrossed with various footprints. Some are small, similar to pawprints. Others are larger, booted prints. Others still appear to be large hoof prints. There are even some footprints that look remarkably similar to your own!", "a disorienting wave of nausea. It's difficult to determine which direction you just came from.", "a strange and absolute certainty that something is uncertain."]
mazeencounters = []
mazedata = [] #First array is maze instance number. Second contains an array of: Maze Thread; Mazearray Index; Player 1; Player 2; Location in Maze, oocthread, state, tracking message, minotaur direction
mazestartmessage = []
mazestartembed = discord.Embed(title = "March's Maddening Mazes!", description = "Welcome to our March roleplay event in the dungeon!\nWhen you're ready to be randomly paired with someone to embark on a random adventure, press the 'Join' button below. Pressing the button a second time will remove you from the waiting list.", colour = embcol)
mazechannel = [0, 0]
mazelocks = []

tarotvars = []

tarotcards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King", "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Justice", "The Hermit", "Death", "Wheel of Fortune", "Strength", "Temperance", "The Devil", "The Hanged Man", "The Tower", "The Sun", "The Star", "Judgement", "The Moon", "The World"]
tarotupright = ["20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "Shuffle your deck, then look at the top 3 cards, and place them back in any order or orientation.", "Numbered cards drawn as part of this action are read as right side up, regardless of what orientation they are drawn in. Reshuffle after the Result is decided.", "You may choose one card within your Court and activate its Dismissal Effect without spending Karma or removing it from your Court, then reshuffle", " Search your Deck and add one Greater arcana of your choice to your Court, Then reshuffle", "While this card is in your court, you and allies within 30ft of you have advantage when rolling initiative.", "While this card is in your court, conjuration spells cast within 30 ft of you are cast as if one level higher.", "While this card is in your court, you and allies within 30 ft of you have advantage on insight and perception checks", "While this card is in you court, you and allies within 30 ft of you have advantage on nature checks, and can always find food and water when travelling through natural environments.", "While this card is in your court, you and allies within 30 ft of you have advantage on intimidation and persuasion checks.", "While this card is in your court, enemies within 30 ft of you have disadvantage on saving throws against ongoing effects and conditions.", "While this card is in your court, allies have advantage on attack rolls while at least 1 other ally is within 5ft of them.", "While this card is in your court, you and allies within 30 ft of you do not suffer disadvantage when making weapon attacks at long range.", "While this card is in your court, you are automatically aware of any lies told in your presence. You do not know the specifics of the lie or it’s corresponding truth, but are aware a lie has been told.", "While this card is in your court allies have advantage on insight checks and saving throws made to maintain concentration.", "While this card is in your court, the time it takes for you and allies within 30 ft of you to gain the full benefits of a short or long rest is reduced by half. This includes time required to sleep or similarly rest", "While this card is in your court, you and allies within 30 ft of you have advantage on attack rolls against enemies who are below half their maximum hit points", "While this card is in your court, you and allies within 30 ft of you have advantage on athletics checks and saving throws against intimidation and fear effects", "While this card is in your court, you and allies within 30 ft of you may add double their proficiency bonus when using passive abilities such as passive perception", "While this card is in your court, you and allies within 30 ft of you may treat any material goods as being worth twice their value for the purpose of trading, purchasing goods, or using as spellcasting components", "While this card is in your court, you and allies within 30 ft of you have advantage on spell attack rolls while below half their hit point maximum.", "While this card is in your court, enemies within 30 ft of you treat d20 rolls of 1-2 as critical failures.", "While this card is in your court, each time you or an ally reduces an enemy to 0 hit points or below, the triggering attacker gains advantage on their next attack roll or saving throw", "While this card is in your court, whenever you or allies within 30 ft of you regain hit points, they regain additional hit points equal to your proficiency bonus", "While this card is in your court, you and allies within 30 ft of you may re-roll any 1’s on damage dice", "While this card is in your court, enemies within 30 ft of you have disadvantage on checks and saving throws made to recognize illusions and deceptions", "While this card is in your court, you and allies within 30 ft of you have advantage on attack rolls if at least one other ally has successfully hit the target with an attack during the same round"]
tarotreverse = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "You suffer disadvantage on this action. Reshuffle after the result is decided.", "Numbered cards drawn as part of this action are read as Inverted, regardless of what orientation they are drawn in. Reshuffle after the result is decided.", "Discard one card from your Court without activating it’s Dismissal effect, Then reshuffle.", "Discard all cards from your Court without activating their Dismissal effects, then reshuffle.", "While this card is in your court, you and allies within 30 ft of you have advantage on opportunity attacks made against enemies", "While this card is in your court, illusion spells cast within 30 ft of you are cast as if one level higher", "While this card is in your court, you and allies within 30 ft of you have advantage on deception and slight of hand checks", "While this card is active, enemies within 30 ft of you treat all terrain as difficult terrain", "While this card is in your court, enemies within 30 ft of you have disadvantage on saving throws against charm and fear effects.", "While this card is in your court, you and allies within 30 ft of you have advantage on saving throws against ongoing effects and conditions", "While this card is in your court, enemies within 30 ft of you have disadvantage on attack rolls made within 5ft of one or more of their allies", "While this card is in your court, enemies within 30 ft of you have disadvantage to hit with ranged attacks", "While this card is in your court, you and allies within 30 ft of you have advantage on deception, stealth, and slight of hand checks.", "While this card is in your court enemies within 30 ft of you have disadvantage on saving throws while not within 5ft of one of their allies", "While this card is in your court, you and allies within 30 ft of you have advantage on death saving throws", "While this card is in your court, enemies within 30 ft of you have disadvantage on saving throws made to maintain concentration", "While this card is in your court, enemies within 30 ft of you have disadvantage on strength based attack rolls and saving throws", "While this card is in your court, creatures within 30 ft of you treat d20 rolls of 19-20 as critical successes, and d20 rolls of 1-2 as critical failures", "While this card is in your court, you and allies within 30 ft of you may can spend 5 feet of movement to automatically escape from nonmagical restraints such as shackles or another creature’s grapple", "While this card is in your court, enemies within 30 ft of you have disadvantage on melee attack rolls while below half their hit point maximum", "While this card is in your court enemies within 30 ft of you treat critical successes as regular successes, and allies within 30 ft of you treat critical failures as regular failures", "While this card is in your court each time you or an ally reduces an enemy to 0 hit points, any of it’s allies within 5 ft suffer disadvantage on attack rolls and saving throws until the end of their next turn", "While this card is in your court, when an enemy makes an attack against you or an ally and misses, it gains disadvantage on attack rolls until the end of it’s next turn", "While this card is in your court, you and your allies within 30 ft of you have advantage on opportunity attacks", "While this card is in your court, enemies within 30 ft of you must succeed on a wisdom saving throw against your spellcasting DC to cast spells that require vocal component", "While this card is in your court, enemies within 30 ft of you have disadvantage on attack rolls if at least one of their allies has successfully hit the target with an attack during the same round"]

rpcategories = ["Meta Spaces", "Shallow Dungeon", "Market Town Outskirts", "Market Town Center", "Verdant Caverns", "Middle Dungeon", "Stormpirate Seas and Coasts", "Frostveil", "Drachen Meadows"]

Fuwulchannels = []

hydrasquares = ["S", "P", "M", "P", "M", "P", "M", "P", "P", "S", "P", "G", "M", "G", "P", "L", "M", "G", "P", "S", "L", "P", "G", "L", "M", "G", "L", "P", "G", "S", "G", "G", "L", "G", "L", "L", "G", "L", "L", "S"]
hydraeffects = [["You grow taller", "You become shorter and smaller.", "Your [hair] changes to a color chosen by the previous player.", "You become more fit and muscular.", "You lose muscle and become more lean.", "Your [lips] get more plump and full.", "You lose all [body hair].", "Your [body hair] becomes more thick and full.", "Your [breasts] grow larger.", "Your [breasts] shrink.", "Your [penis] grows larger and longer.", "Your [penis] shrinks.", "Your [tongue] grows longer.", "Gain a penis. If you chose to, you may lose your [vagina].", "Gain a vagina. If you chose to, you may lose your [penis].", "Your bodily fluids become sweet and tasty.", "Gain a pair of breasts. If you already have them, they grow instead.", "Your belly swells as if there was a baby in your [uterus].", "Your [balls] grow larger and more productive.", "Your [hips] swell OR your [shoulders] broaden, your choice.", "Your [breasts] begin to lactate.", "Your [nails] grow longer and permanently polished the color of your choice.", "Your [voice] deepens.", "Your [voice] gets more high pitched.", "Your [clitoris] grows larger and more sensitive.", "Your [penis] is permanently erect.", "Your [butt] grows larger.", "Grow wings.", "Your [legs] turn into the lower half of an animal.", "Patches of scales grow on your body.", "Grow a pair of animal ears.", "Gain some claws.", "Your [feet] turn into hooves.", "Your [penis] becomes knotted.", "Gain a few tentacles. These may replace existing limbs.", "You constantly emit pheromones.", "Gain a pair of fangs or tusks.", "Grow a pair of horns.", "Grow an extra pair of arms.", "Grow a tail"], ["You become less intelligent.", "You become more intelligent.", "You fall in love with the first person you see.", "All clothes feel uncomfortable.", "You have an urge to own things... and people.", "You have an urge to obey the commands of others.", "You become a 'Tsundere', unable to admit your feelings.", "Your tongue becomes loose, saying whatever comes on your mind easily.", "You address everyone by honorifics (ex: Sir, Mistress, Queen, etc)", "You have an urgent need to breed.", "You become jealous, seeking to alway be the center of attention.", "Your speech becomes cutesy and you have trouble using complex words.", "You find pleasure in serving others.", "You become proud, seeing others as lesser.", "You have a strong urge to win, no matter the competition.", "You regularly make the sound associated with any [animal features] you have.", "You grow more chaste.", "You grow more uninhibited.", "You find yourself submissive to characters that are taller and stronger than you.", "You love to punish others.", "You act more stereotypically feminine.", "You act more stereotypically masculine.", "You forget all sexual experiences and believe yourself a virgin again.", "You have an urge to masturbate when not doing anything else.", "You find pleasure in others doing what you say"], ["Take an extra turn!", "Exchange control of any two Transformation cards.", "Discard a Transformation card affecting any player.", "Give one of your Transformation cards to another player.", "For each player, draw a Transformation card from either deck. Give each player one of these cards (this includes yourself).", "Chose a Transformation card in front of any player. It is discarded and replaced by a card from the other Transformation deck.", "Steal a Transformation card from any other player (This is not optional).", "Draw a Mental Transformation card and a Physical Transformation card. Give one to another player and keep one for yourself.", "Take a card from the player with the most cards and give it to the player with the fewest (You chose in case of draws).", "Choose a Transformation card controlled by any player and give all other players a copy of it.", "Chose a Transformation card controlled by any player. They get another copy of it.", "Discard all Lewd Action cards in front of a chosen player.", "For each other player, draw a Lewd Action card. Choose one of them and apply it to that player, discarding the rest. If that Lewd Action requires them to do something to another player, they do it to you instead.", "Draw 3 Game Action cards and pick one of them to play, discarding the other two.", "Draw a card from two different decks other than Game Actions and apply them to yourself.", "Choose a player. They draw a card corresponding to their current space.", "The player with the fewest Physical Transformations gains a Physical Transformation card. The player with the least Mental Transformation card gains a Mental Transformation card. (you choose in case of draws)", "All players without an active Lewd Action card gain one.", "Discard a Mental Transformation card and a Physical Transformation card affecting two different players.", "Choose another player. All other players give them one of their Transformation cards, then they give you one of their Transformation cards (This can be one they just received)."], ["Kiss another player. If they reciprocate, advance 1 square.", "Sit in the lap of whichever player is in the lead until someone gets ahead of them. If they orgasm while you do, you advance 3 squares and they go back 3 squares.", "Masturbate until you orgasm. Each time you roll the dice, add 1 to the result.", "Say something about another player. If you make them blush, advance 1 square.", "For each player (including yourself) you may remove a piece of clothing. Each other player may remove a piece of clothing. Advance a number of squares equal to the difference.", "You must present your genitals to a randomly chosen player. They can choose to fuck you until your next turn. If they do, you both advance 3 squares.", "You become bound and unable to move until your next turn. If you orgasm during this time, go back 2 squares.", "The player in last place may choose to perform oral sex on you. If they bring you to orgasm before your next turn, you go back to their square.", "When another player orgasms, advance 1 square if you taste their cum or equivalent.", "Choose another player. The first one of you who orgasms advances 3 squares.", "Choose another player. The last one of you who orgasms advances 3 squares.", "The player to your right gives you a sexual dare. If you do it, advance 2 squares.", "The player to your left asks you a sexual question. If you don't answer, go back 2 squares.", "Pick out costumes for every other player. If they don't put them on, they go back 1 square.", "Choose another player to sit in your lap at least until your next turn. While they are there, add 1 to your rolls."]]
hydraprogress = []

#---------------------------------------------

loadingtips = ["The ancient rivalry between Nurse and Maid is not actually ancient. It's pretty new, and everyone thinks they should just go on a date.", "Remember, you can use dezzie reacts to give out rewards to other community members without losing any of your cash. In roleplay channels the target gets a 25% bonus on top!", "There's nothing wrong with checking in periodically on your partners.", "You can use the :kinklist: emote on any message and Gothy will DM you their kink list, if they have filled it out!", "Hydrate. Or else.", "Want to RP but not sure if you want to make it canon? Try the voyeur's lounge!", "Loving yourself is just as important as loving others", "Runar first created the Potion of Reassignment to help Sophie transition. He has kept them regularly stocked ever since.", "Did you know you earn Dezzies just for being active in the RP channels?", "Players can use the %give command to give each other Dezzies, and even transfer items.", "Nubia and Nessa have been dating for half a century now. Their third, Jack is usually gone on 'Missionary' work.", "Madame Webb uses exclusively live models to display her clothes, and will occasionally provide discounts in exchange for modeling services. As long as you don't mind being paralyzed and on display for your entire shift.", "Sophie sought out the dungeon after her first attempt at being and adventurer left her trapped inside a mimic for more than a week. She has been breeding and domesticating them ever since!", "Nessa is a domestic abuse survivor, and will do anything in her power to help others in the same situation - just before she makes certain to teach their abuser a permanent lesson.", "Rumour has it that petshop owner Kat has been working on a ritual that can bond a willing humanoid to the caster like a familiar.", "The Xio took over the Cathedral after the false religion of the Keepers was exposed. They are typically welcoming to those who visits.", "The souls of the dead congregate in the haunted hallows, and ithose that stir them will find the dead relentless in persuit.", "Those of the waters know of the cruel ruler Conquest, that holds dominion over most of the waters outside of the Stormpirate Seas."]
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
  
    reacts = reacts.replace(" ", "")
    reactions = []
    a = 0
    while a < len(reacts):
        try:
            if reacts[a] == "<":
                emoji = ""
                while reacts[a] != ">":
                    emoji += reacts[a]
                    a += 1
                    if a > len(reacts):
                        break
                emoji += ">"
                reactions.append(emoji)
            else:
                reactions.append(reacts[a])
        except IndexError:
            break
        a += 1

    emojis = []
    vals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    emojilist = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]

    for n in range(len(reactions)):
        try:
            emojis.append(emojilist[vals.index(reactions[n])])
        except ValueError:
            emojis.append(reactions[n])

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

#Tour Variables:
TourNames = ["Welcome!", "This is the general chat for the server", "Next on our tour, Bots and Constructs", "Character Creation", "The market", "End of the Tour"]
Tourchannels = ["welcome-hall", "general-ooc", "bots-and-constructs", "character-creation", "market commands", "welcome-hall"]
if liveVersion:
    TourLocations = [828411760847356005, 832435243117445131, 1050503346374594660, 828412055228514325, 1065077089579044934, 828411760847356005]
else:
    TourLocations = [1147303689057488906, 1031671413607776327, 1147321466292031509, 1032400859251871825, 1147337311923753000, 1147303689057488906]
TourDescriptions = ["Welcome to Celia's Lewd Dungeon. We are Gothica, and we are both the bot that runs a lot of the functions in the discord server, and the Shoggoth maid who serves T̷͓͓̜̅̒̂̓̕ͅh̶̠̼͊ͅé̵̞͉̟̾͗̈́̎ ̵̩̯̠̫̦͔͉̃̌̎̀̔́̚ͅM̵̯͇͙̀͊̌͒̾̽͒̉̚͠į̶̛͖̙̬̘̥͊s̴̗̝̍̋̋̚t̶͍̣̜̉̑r̵̟̫̘̘͔͈͔̳̝̔ě̵̙͇͉̼͕̀̓͂͛̏͒̓̉͘ş̶̣͖͉̻̞̬̽͗̓͛͆̽̽͘͝͝s̷̪̗͙̫͓͔͛̒̀̽͊̌̇̄̚ in the dungeon\n\nThe server can be overwhelming, but this tour is designed to lead you through the key functions and areas as smoothly as possible. If you need help at any point, feel free to ping our Server Veterans. Other useful places for information include https://discord.com/channels/828411760365142076/830075671576576050 and https://discord.com/channels/828411760365142076/1081779600494972958. This channel is the Welcome Hall, where new members arrive. Press the button below to visit General OOC, where most of the conversation on the server happens.",
                    "This is where most general conversation on the server happens. Say hello to everyone! We ask that you keep image posting to a minimum here. It is also the place to discuss the main roleplay in the dungeon, and it is generally considered a good idea to create a thread for any ongoing scenes to keep things organised.\n\n Other places for general conversations are:\n\nhttps://discord.com/channels/828411760365142076/828621051268431932, for gentler conversations with no lewd elements.\nhttps://discord.com/channels/828411760365142076/1017209321773342730, for conversation that is particularly more lewd, and where you can engage in flirting and teasing with other server members.\nhttps://discord.com/channels/828411760365142076/829904540778233876, which is for memes and silliness.\nhttps://discord.com/channels/828411760365142076/1108556537900843068, for teasing and praising of a more wholesome nature.\nhttps://discord.com/channels/828411760365142076/1053107228737024050 is a forum for creating deeper conversations about particular topics.\nThere is also a channel specifically for those who are actively looking to start new scenes. This can be accessed by running the `%lfg` command and specifying a number of hours that you will be looking for RP.\n\nWhen you're ready, press the button below to continue the tour, and we'll show you some of the useful bot functions available to you.",
                    "A channel particularly close to our own hearts, this channel is used for running commands. There are several bots here, ourselves included. The other main ones are Avrae (which uses & as its command), to roll dice; Tupperbot, which replaces your messages with those of your character, and which we will cover in more depth later in the tour; Arcane, which tracks the amount of RP you do and allows you to level up, granting access to more character slots over time.\n\nWe have a large number of helpful functions as well, ranging from summoning character information, to alerting you when a scene you're in gets a new post, to comparing the kinks of various players. For a full list, try running the `%help` command here.\n\nAnother crucial use of this channel is filling out the Kink survey. This is a list of your preferences and limits, so they can better facilitate communication later. You can fill it out using the `%Kinksurvey` command, though be warned, it does take about ten minutes to complete. You can access other people's kinklists in a number of ways. For example, running `%kinkplayers` and then the name of a kink will give you a list of people who are into that kink. You can also react to any player's message with :kinklist:, and we will send you their full set of preferences in a DM.\n\nOnce you're done having a look at the bot functions here, press the button below to have a look at the channel for character creation. This is the first part of the tour that requires a role to access - Dungeon Denizen, which you can get after reading the rules for RP here: https://discord.com/channels/828411760365142076/1084038597805613076. If you don't have that role yet, go and get it now. You can remove it later if you don't want it.",
                    "Next step! This is where the players create all the amazing characters in the dungeon! To register a character with us, simply start a post with Name, and fill in each section of the pinned template line by line. You do NOT need a sheet to start rping, but if you want to enter more dangerous areas you will need to submit a character sheet through https://discord.com/channels/828411760365142076/1081782434649100308.\n\nWe allow Most published DnD content, but there is an approved library of Homebrew in https://discord.com/channels/828411760365142076/828412004905517106. We ask that you use only those approved, and make sure you check to see if you need Veteran status for the option. There is a spreadsheet listing every available option in there as well.\n\nAlso in the links and resources section, you'll find our server houserules, which include things like getting an ASI and a feat rather than just one or the other, so these are well worth looking into.\n\nOnce you have registered a character here, anyone can `%search` them to see their full details, or look at an overview of all your characters to see your full roster. Other useful things to note in character creation are the https://discord.com/channels/828411760365142076/898640028174016552 and https://discord.com/channels/828411760365142076/1050252064455925790 channels. If you have questions about the mechanics of things, you could open a thread in the https://discord.com/channels/828411760365142076/1058195362306850926.\n\nDepending on your roles, you might be able to see some of the roleplay channels already. These are divided into several categories:\n**The Market**, which is our Lorekeeper run shops where you can use in game currency to buy hundreds of lewd items for your characters;\n**Denizen Dwellings**, which are houses for characters and places for them to stay;\n**Safe Passages**, the main roleplay channels, featuring a range of comfortable locations for scenes between players;and the \n**Dangerous Depths**, for more adventurous players wanting random encounters - both carnal and combative.\n\nYou might also be able to see the https://discord.com/channels/828411760365142076/975624986603692052, which is a noncanonical place for characters to exist. It's not as much a place for roleplay, as it is for meta commentary on the ongoing roleplay elsewhere.\n\nIf you have been looking in these channels, you might have noticed that all the roleplay is done by bots. This is the work of Tupperbot, which is a bot that allows you to replace your messages with those with the name and avatar of your character.\n\nFollow us to our next destination, and we'll show you more about the in character economy we mentioned!",
                    "We have hundreds of unique lewd items created by our very own <@310756521736667137>. These can be bought for your characters using Dezzies, which are a fictional currency you can earn in a variety of ways. Currently, the main ways to earn them are by running the `%work` and `%slut` commands. Work can be run daily, while you can slut every six hours. Be warned though, slutting isn't risk free, and there is a chance that you might lose dezzies instead! We also reward engagement in the roleplay with dezzies, and everyone has a weekly pool that they can react to other people's posts to add some to their balance. Dezzies are used in the shops in the Market. You can run `%shop`, followed by the shopname to see the items for sale, and then `%item` followed by the item name to see the full details on it. They are also available to browse in the lewd handbook. You can buy these items with `%buy`.\n\nThere are also occasionally more expensive things to spend dezzies on, such as slave auctions and community projects.\n\nWe're mostly done with our tour, so if you would like to follow us back to the Welcome Hall, we'll point out a few other useful things to know.",
                    "Most of the people here are happy to help with anything you might want to ask, but if you're looking for particular help on things, you can ping our staff role.\n\nIf you want to contact us more privately, there is an option to open a ticket in https://discord.com/channels/828411760365142076/1060693504050872451. If you're looking to join or run a game separate from the dungeon, you are more than welcome to do so here. Create a forum post in https://discord.com/channels/828411760365142076/1082682655084126229 to draw up interest, and then you can create a channel for it in which you can organise threads.\n\nAnother thing we have is the Gallery of Sin, which is a vast array of lewd images that can provide you with inspiration; in whatever form that takes.\n\nBe sure to look at all the options in https://discord.com/channels/828411760365142076/880605891366375435 to ensure you're not missing out on anything you want to see.\n\nFinally, we know you read the https://discord.com/channels/828411760365142076/829442455980081204 before you were able to verify, but it is worth checking those out again to be sure of them - they are there to ensure the fun and safety of everyone.\n\nWe hope you have enjoyed this tour, and please don't hesitate to ask if you have any questions."
                    ]
Tourbuttontext = ["Take a Tour", "OOC", "Bots and Constructs", "Character Creation", "Market Commands", "Welcome Hall"]

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
        ["Money", "Inventory", "GiveMoney", "Leaderboard", "Shop", "Item", "Buy", "Sell", "GiveItem", "Invest", "Bid", "Spend"],
        ["Gag", "Emote", "Adventurer", "Verify", "Kinkencounter", "oocembed", "oocmsg", "Add-money", "Remove-Money", "AddItem", "Spellrotation", "RandLoot", "clonev2", "CommunityProject", "giftall", "rewardpoolreset", "manualmigrate", "MVP", "copysheet", "removezerodiscrim", "config"]
    ]
    helpsummary = [
        ["Calls up some welcoming information for new members", "Summons a link to the lewd rulebook", "Summons a quick reference sheet of the main rules for Sexual Advances", "Generates an embed, like this one", "You are here.", "Compares timezones", "Migrates account from old Discord username to unique username."],
        ["Registers a character to the index", "Edits a character", "Gives a character to another player", "Lists the characters owned by a player", "Provides the index entry of a character", "Retires a character", "Sets a character temporarily unactive", "Reactivates a deactivated character"],
        ["Helps you find roleplay partners", "Generates a random plothook for your character", "Checks how many plothooks you have seen", "Suggests an empty room for you to roleplay in.", "Generates a scene break", "Provides the time of the last message in each roleplay channel", "Rolls on the wildlust table", "Eats a dezzie", "Stores and recalls your list of active scenes and can DM you whenever a new message is sent in them", "Manually spawns the imptome into an RP (Only usable by the imptome wielder)."],
        ["Summons the kinks of the tagged player", "Allows you to fill out the kink survey", "Fills any holes in the kinksurvey", "Edits a kink", "Summons a list of players with the targeted kink"],
        ["Checks your balance", "Displays your items", "Gives a number of dezzies to someone else", "Shows how rich the richest people on the server are", "Displays the listed shop", "Provides details on a shop or inventory item", "Buys an item", "Sells an item, at a loss.", "Transfers an item to another player", "Spends dezzies on a community project", "Bids on an auction in the Black Market", "Removes Dezzies from yourself"],
        ["Gags a user in ooc", "Reacts to a message with emote letters", "Grants a player the Adventurer Role", "Confirms that a user is over 18", "Generates a random encounter, respecting the player's kinks", "Generates an embed in ooc", "Sends a message in ooc", "Adds money", "Removes money","Adds an item from the shop to a user's inventory", "Checks Runar's stock of spells", "Generate random loot that fits a player's kinks", "Clones the contents of a channel or thread to another channel or threads, including tupper messages.", "Registers a new community project people can %invest in!", "Gives (or takes) dezzies to every person registered in the economy.","MOD ONLY: Resets the dezzie reward pool for all players if needed.", "MOD ONLY: migrates an account from old to new naming system without automatic failsaves. Read full help before using.", "Grants the user the MVP Role", "Makes a copy of the economy sheet in a seperate worksheet.", "Removes all #0 discriminators as well as making a safety copy first.", "Allows viewing, and editing of the variables exposed in the config."]
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
        "To edit a character, type `" + GlobalVars.config['general']['gothy_prefix'] + "edit Name Field New-Value`, as a demonstration:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "edit Lalontra class Ranger`\n\nThis will match a character's name even if you only use part of the name.",
        "For obvious reasons, only the owner of a character can edit them, but there are occasions where you want to give a character to someone else, for example in an auction. To transfer the character, type `" + GlobalVars.config['general']['gothy_prefix'] + "transfer Name @New-Owner`, for example:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "transfer Lalontra @C_allum`",
        "To create a list of the characters owned by any particular player, type `" + GlobalVars.config['general']['gothy_prefix'] + "charlist`. Send the command without any arguments to see your own characters, or add a mention after it to see someone else's. As below:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "charlist @C_allum`",
        "To search for a character or attribute, type `" + GlobalVars.config['general']['gothy_prefix'] + "search Search-term`. If the search term is within the name of a character, it will provide that character's full bio. As an example, to find the bio of Lalontra you might type:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "search Lal`\n\nIf the search term is not found in the name of a character, you can instead seach by a data field, done by typing`" + GlobalVars.config['general']['gothy_prefix'] + "search Field Search-Term`, such as:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "search class Ranger`\n\nIf the first argument after the command is neither in the name of a character, nor a field name, it will search the whole database, and provide details on where the word occurs. If you were to type:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "search blue`\n\nYou would see information about any characters whos eyes, hair or skin colour (or any other attribute) was blue.",        "If you want to retire a character for any reason, type `" + GlobalVars.config['general']['gothy_prefix'] + "retire Name`, as per the below example ||which was rather painful to write!||:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "retire Lalontra`",
        "If you need to activate a previously unavailable character, whether because you made or recieved them as a transfer from another user without having a slot available; or `%deactivated` them temporarily, you can activate them by using`" + GlobalVars.config['general']['gothy_prefix'] + "activate Name`. Example:\n\n`" + GlobalVars.config['general']['gothy_prefix'] + "activate Lalontra`",
        "Deactivating a character means that they will have a ~~strikethough~~ on their name when your character list is called using `%charlist`. This is commonly because they are being used in another scene that you want to finish before starting a new one with them, or can simply be if you're looking for a new scene but don't want to play that specific character at the time."
        ],
        ["`%lfg` gives you the Looking for Role Play role, and allows you to see the #looking-for-new-roleplay channel. this role is restricted by time, so you only have access to the channel when you are actively looking for role play. You can also specify a number of hours to be active, by adding them after the command.\n\nRunning the `%kinkplayers` command in this channel will instead ping everyone with the relevant kinks (they'll only see the ping if they are also in the channel though)",
        "We can generate plothooks from your active characters, picking a scene they might be in, to act as a seed for roleplaying. These hooks are purely optional and can be ignored, even after they have been generated. They are simply ideas. The command is: `" + GlobalVars.config['general']['gothy_prefix'] + "plothook`. You can also add the name (or part of the name) of one of your characters after the command to generate a plothook for them, for example, C_allum could do `" + GlobalVars.config['general']['gothy_prefix'] + "plothook lal` to generate a plothook for Lalontra.",
        "There are a number of plothooks in the system, and by running `%plotleaderboard` you can see how many each person has found.",
        "`%room` looks at the list of roleplay rooms available, and chooses one that looks quiet enough for you to start a scene in.",
        "If you want to divide your scene from the previous one, you can run `%break` (or just `%br`). This will tell us to create a division in the room.",
        "We peek into each public room, and take a look at the last message there. Summon this check using `" + GlobalVars.config['general']['gothy_prefix'] + "recent`. Room names written in **bold** have been inactive for more than three hours.",
        "We have a custom wild magic table available to sorcerers in the dungeon. If you type `%wildlust`, Gothica will roll on that table for you.\n\nThe full table can be seen in the lewd rulebook.",
        "Eating the server currency can have some strange effects. Run `" + GlobalVars.config['general']['gothy_prefix'] + "Gobblin` or `" + GlobalVars.config['general']['gothy_prefix'] + "Crunch` to eat a dezzie. A dezzie of a good size to eat has a value of around 10 dezzies. You can also add a number after the command to eat a certain amount.",
        "Gothica can track your scenes. Running `%scenes add` followed by a brief description of the scene and then the link to it, will tell us to track that scene. You can then do `%scenes` to summon the list of scenes, and we will inform you who sent the last message in the channel. As an example, you might type: `%scenes add Lalontra and River fight an evil fae #An-Uncomfortable-Reunion` to add that scene to your watchlist. You can also remove scenes with `%scenes remove` and then the number of the one to remove. Gothica can also DM you whenever a message is sent in a tracked scene. To enable that run `%scenes notification` and select the scene you want to get notifications on. `%scenes notification all on` or `%scenes notification all off` toggles notification settings on all tracked scenes at once.",
        "If you are the imptome weilder, you can call `%imptome [message Link]` to spawn the Imp Tome in response to that message. ALWAYS CHECK WITH THE PEOPLE IN THAT RP IF THEY WANT THAT FIRST! If you are the Imp Tome wielder, but can't use this, contact Ken, he has to set a variable in the code..."
        ],
        ["This function lists a users kinks. To use it, run `%kinklist @name`. We will then summon the overview of the list of preferences that the user has filled out. You can then select further information on any particular category of kinks, such as mental domination or clothing and toys. Additionally, if you react to a message using the kinklist emote (<:kinklist:1053378814190813304>), we will direct message you their full kinklist.",
        "`%kinksurvey` is the function that allows you to complete the survey. We will open a thread in which you can tell us all about your kinks and preferences. This command can only be run in the #bots-and-constructs channel. This survey takes some time to run through.",
        "We sometimes add kinks to our list, based on user feedback. If we have added any kinks since you took your survey, you can run `%kinkfill` to generate a new thread in which to answer those questions.",
        "If you find that your preferences for a certain thing have changed, you can run `%kinkedit` to update this. Running the command on its own will bring up a navigatable list of kinks, while specifying the name of the kink in the message will edit that one directly.",
        "If you are looking for someone who is into a particular kink, you can run `%kinkplayers` followed by the name of the kink. For example, `%kinkplayers Handholding` will bring up a long list of degenerates who have that marked as a favourite. Running this in #looking-for-new-roleplay will ping everyone associated with that kink who is also looking to start a scene."
        ],
        ["We can help you check your balance in one of two ways. First, we can simply shove you, and if you make the Strength (Athletics) or Dexterity (Acrobatics) check, you do not fall prone. If you would rather we check the balance of your dezzie account, simply use `%money`",
        "To display the items you have bought, earned or found in the dungeon, you can use `%inventory`. This also displays the number of each that you have and a brief summary of each.",
        "To transfer dezzies from your account to someone else's, use the command `%givemoney @name amount`. This value will be removed from your account and added to that of the targeted player.",
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
        "`%mvp @name` will grant the tagged player the MVP role, which will be removed when the bot restarts",
        "Makes a copy of the economy sheet - Use that to do code tests on live that could mess up sheets etc.",
        "Removes all #0 discriminators from the usernames in the economy sheet. This is needed because at some point Discord removes the discriminator as a whole.",
        "%editconfig [category] [variableName] [newValue] allows editing the config variables. For variables that are an array, set the new value to [entry1, entry2, entry3].\n %printconfig prints the config.\n %printconfigraw prints the config, but doesn't reformat it. Used to debug problems.\n %reloadconfig is used when editing the config manually (in the file, not through the command), to trigger a reload of the variables in the config file."
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

def extract(lst, index):
    return [item[index] for item in lst]

def cursefromref(ref):
    curserefs = ref.split("|")
    ref = ref.replace("|", "\n")
    for a in range(len(curserefs)):
        try:
            i = extract(itemdatabase[1], 4).index(curserefs[a])
            ref = ref.replace(curserefs[a], str("**" + itemdatabase[1][i][0] + "**, *Level " + itemdatabase[1][i][1] + "*\n" + itemdatabase[1][i][2]).replace("**Generic Curse**, *Level 0*\n", ""))
        except ValueError:
            pass
    return str(ref)

#Receives a string that represents an item name, and an integer that represents the amount of results desired. Returns a list of lists. Each entry
#shows one potential item candidate in the form of [name, levenshtein distance score, unique id]
async def matchStringToItemBase(item_name, top_n_results, searchlist, add_item_name_in_list = True):
    levenshtein_tuple_list = []
    for entry in searchlist:
        #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
        
        levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry.lower(), item_name.lower())
        levenshtein_distance_complete = fuzz.ratio(entry.lower(), item_name.lower())
        levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
        if add_item_name_in_list == True:
            levenshtein_tuple_list.append([entry, levenshtein_distance, item_name])
        else:
            levenshtein_tuple_list.append([entry, levenshtein_distance])

    sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
    return sorted_list[:top_n_results]

async def selectItem(interaction, searchterm, top_n_results, searchlist):
    #Search for item in the item sheet with fuzzy matching
    item_matches = await matchStringToItemBase(searchterm, top_n_results, searchlist)
    selector_options = []
    #See if we have an almost perfect match
    if item_matches[0][1] > 93:
        #If we have multiple, display *all* almost perfect matches for choice and wait for the choice
        if item_matches[1][1] > 93:

            for i in range(0, len(item_matches)):
                if item_matches[i][1] > 93:
                    selector_options.append(item_matches[i])
        #if we only have one with score 93 or higher, suggest that one for buying
        else: selector_options.append(item_matches[0])
    #if we have none, display the top 10 matches and wait for a choice
    else:
        selector_options = item_matches #Omit the Levenshtein Score

    #Generate a message to show the top list
    selected_item = None
    if len(selector_options) > 1:
        top10_string = ""
        for i in range(0, len(selector_options)):
            top10_string += f"`{i+1}:` {selector_options[i][0]}\n"

        #Generate selector view to choose items.
        item_selection_view = Dropdown_Select_View(interaction = interaction, timeout=30, optionamount=len(selector_options), maxselectionamount=1, namelist=[i[0] for i in selector_options]) #Only let them choose one item.
        selection_message = await interaction.channel.send(embed = discord.Embed(title="Didn't find a perfect match to what you are looking for.", description="Here are the top 10 closest results. Please choose which of these you want.\n\n" + top10_string + "\n\n" + "This message will time out in 30 seconds.", colour = embcol), view = item_selection_view)
        #Wait for reply
        if await item_selection_view.wait():
            await interaction.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await interaction.followup.send("Selection Timed Out")
            return
        
        i = int(item_selection_view.button_response[0]) - 1
        await selection_message.delete()
        if i >= 0 and i < len(selector_options):
            selected_item = selector_options[i]
        else: 
            await interaction.channel.send(embed=discord.Embed(title=f"Number has to be between 1 and {len(selector_options)}", colour = embcol))
            return
    else: selected_item = selector_options[0]
    return selected_item

async def quicksel(interaction, options, title, description, dest = None):
    Drop = Dropdown_Select_View(interaction = interaction, namelist = options, timeout = 480)
    if dest == None:
        dest = interaction.channel
    msg = await dest.send(embed = discord.Embed(title = title, description = description, colour = embcol), view = Drop)
    if await Drop.wait():
        await dest.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        await interaction.followup.send("Selection Timed Out")
        return
    i = int(Drop.button_response[0]) - 1
    await msg.delete()
    return options[i], i

class Dropdown_Select_View(discord.ui.View):
    def __init__(self, interaction, timeout=120, optionamount=1, maxselectionamount = 1, namelist = [], default = "None"):
        super().__init__(timeout=timeout)
        self.button_response = []
        self.choices = []
        self.namelist = namelist
        self.interact = interaction
        #Make sure we can only choose between 1 and 25 as per specification.
        if maxselectionamount > 0 and maxselectionamount < 26:
            self.selection_amount = maxselectionamount
        elif maxselectionamount > 26:
            self.selection_amount = 25
        elif maxselectionamount < 1:
            self.selection_amount = 1

        #Make sure we can't choose more than we have options
        if self.selection_amount > max(optionamount, len(self.namelist)):
            self.selection_amount = max(optionamount, len(self.namelist))

        if self.namelist != []:
            for i in range(1, len(self.namelist) + 1):
                self.choices.append(discord.SelectOption(
                    label=f"{i}: {self.namelist[i-1]}",
                    value = i
                ))
        else:
            for i in range(1, optionamount + 1):
                self.choices.append(discord.SelectOption(
                    label=f"{i}",
                    value = i
                ))
        self.select = discord.ui.Select(
            placeholder = default, # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = max([1, self.selection_amount]), # the maximum number of values that can be selected by the users
            options = self.choices# the list of options from which users can choose, a required field)
        )       
        self.select.callback = self.callback
        self.add_item(self.select)
        
    async def callback(self, interaction: discord.Interaction):
        self.button_response = self.select.values
        await interaction.response.defer()
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        try:
            if self.interact.user.id == interaction.user.id:
                return True
            else:
                await interaction.response.send_message("That is not your dropdown to click!", ephemeral=True)
                return False
            
        except AttributeError:
            if self.interact.user.id == interaction.user.id:
                return True
            else:
                await interaction.response.send_message("That is not your dropdown to click!", ephemeral=True)
                return False