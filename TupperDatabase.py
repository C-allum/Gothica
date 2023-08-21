import sqlite3
import datetime
import numpy as np
from CommonDefinitions import *
import discord
from enum import Enum
from CommonDefinitions import sheet as SheetsService, TransactionSheet


#Initialize the tupper database: connect and create a cursor
def initTupperDatabase():
    print("Initializing tupper database...")    
    try:
        tupperDBConnection = sqlite3.connect('CLDTupper.db')
        tupperCursor = tupperDBConnection.cursor()

        table = """ CREATE TABLE IF NOT EXISTS Tuppers (
                    PlayerID TEXT NOT NULL,
                    ImgURL TEXT NOT NULL,
                    CharName TEXT NOT NULL
        );"""

        tupperCursor.execute(table)
        tupperDBConnection.commit()
        tupperDBConnection.close()

        print("Tupper Database initialized.\n")
    
    except sqlite3.Error as error:
        print('Error occured while initializing Tupper database - ', error)


#Add a transaction to the database: Takes a person, an action, an amount and optionally a date in datetime format to write to the Database
def addTupper(playerID:str, imgURL:str, charName:str):
    try:
        tupperDBConnection = sqlite3.connect('CLDTupper.db')
        tupperCursor = tupperDBConnection.cursor()

        tupperCursor.execute(f'''INSERT INTO Tuppers VALUES ('{playerID}', '{imgURL}', '{charName}')''')
        tupperDBConnection.commit()
        tupperDBConnection.close()

    except sqlite3.Error as error:
        print('Error occured while adding a Tuppers to the database - ', error)


def updateURL(playerID:str, newImgURL:str, charName:str):
    try:
        tupperDBConnection = sqlite3.connect('CLDTupper.db')
        tupperCursor = tupperDBConnection.cursor()

        tupperCursor.execute(f'''UPDATE Tuppers SET ImgURL = '{newImgURL}' WHERE PlayerID = '{playerID}' AND CharName = '{charName}' ''')
        tupperDBConnection.commit()
        tupperDBConnection.close()
    except sqlite3.Error as error:
        print('Error occured while updating a imageURL in the tupper database - ', error)
    return

def updateTupName(playerID:str, imgURL:str, newCharName:str):
    try:
        tupperDBConnection = sqlite3.connect('CLDTupper.db')
        tupperCursor = tupperDBConnection.cursor()

        tupperCursor.execute(f'''UPDATE Tuppers SET CharName = '{newCharName}' WHERE PlayerID = '{playerID}' AND ImgURL = '{imgURL}' ''')
        tupperDBConnection.commit()
        tupperDBConnection.close()
    except sqlite3.Error as error:
        print('Error occured while updating a tupper name in the tupper database - ', error)
    return

async def lookup(imgURL:str, message:discord.Message):
    tupperDBConnection = sqlite3.connect('CLDTupper.db')
    tupperCursor = tupperDBConnection.cursor()
    
    tupperCursor.execute(f'''SELECT PlayerID, ImgURL, CharName FROM Tuppers WHERE ImgURL in ('{imgURL}')''')
    data=tupperCursor.fetchall()

    #See if we found the image URL of the tupper post
    if data == []:
        #Fetch data for this tupper from bot channel
        aliasChannel = client.get_channel(aliasBotChannel)
        messages = [message async for message in aliasChannel.history(limit=800)]
        #iterate through the last 800 embedded messages
        for currMess in messages:
            #we found the message if the RP message matches, and the author (character name) matches as well.
            if message.content in currMess.embeds[0].description and message.author.name == currMess.embeds[0].title:
                playerID = currMess.embeds[0].fields[0].value.split("!")[1].split(">")[0]
                charName = currMess.embeds[0].title
                break
        
        #check if the tupper is in the database, but the url has changed
        tupperCursor.execute(f'''SELECT PlayerID, ImgURL, CharName FROM Tuppers WHERE PlayerID in ('{playerID}') AND CharName in ('{charName}')''')
        data = tupperCursor.fetchall()

        #if data is still empty (no playerID and Tup Name match in DB)
        if data == []:
            #Fetch data for this tupper from bot channel
            #initialize new tupper
            addTupper(playerID, imgURL, charName)
            data = [[playerID, imgURL, charName]]

        #In this case we found the tupper by name + playerID
        else:
            updateURL(playerID, imgURL, charName)
            print(f"Updated the img url from: {data[0][1]} to: {imgURL}.")
            data[0][1] = imgURL

    elif data[0][2] != message.author.name:
        #check if tup name needs updating.
        updateTupName(playerID, imgURL, message.author.name)
        print(f"Updated tupper name from {data[0][2]} to {message.author.name}")
        data[0][2] = message.author.name
    
    playerID = data[0][0]
    imgURL = data[0][1]
    charName = data[0][2]
    return playerID, imgURL, charName

