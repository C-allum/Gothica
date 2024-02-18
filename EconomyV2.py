from CommonDefinitions import *
import GlobalVars
from thefuzz import fuzz

async def shop(message):

    shopitems = []
    shoplist = []

    try:
        if message.content.split(" ", 1)[1].lower() in str(itemlists).lower():

            for a in range(len(itemlists)):
                if a >= 3:
                    if message.content.split(" ", 1)[1].lower() in itemlists[a].title.lower(): #Check if searchkey is in shopname
                        shoplist.append(a)

        else:
            shoplist = range(len(itemlists))
            shoplist = shoplist[3:]

    except IndexError:
        shoplist = range(len(itemlists)) #Adds all shops to list
        shoplist = shoplist[3:]

    if len(shoplist) == 1:
        i = shoplist[0] #Get index of worksheet
    else:
        shopsel = []
        for c in range(len(shoplist)):
            shopsel.append("`" + str(c+1) + "` - " + itemlists[shoplist[c]].title)

        emb = discord.Embed(title = "Which shop would you like to browse?", description = "Type the number of the one you want:\n" + "\n".join(shopsel), colour = embcol)
        emb.set_footer(text = "This message will timeout in 30 seconds")
        await message.channel.send(embed = emb)
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                i = shoplist[int(msg.content) - 1]
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return

    try:
        shopitems.append(str(itemdatabase[i][0][20]) + "\n------------------------------------------------------------\n") #Adds shop welcome message to first embed
    except IndexError:
        pass
    try:
        shopemoji = itemdatabase[i][0][22]
    except IndexError:
        shopemoji = ""
    try:
        shopcol = int(itemdatabase[i][0][24])
    except IndexError:
        shopcol = 0

    for b in range(len(itemdatabase[i])):
        if b != 0:
            nextitem = shopemoji + " **" + str(itemdatabase[i][b][1]) + "** \n  *" + str(itemdatabase[i][b][13]) + "*" + dezzieemj #Gets item name and price
            if len("\n".join(shopitems)) + len(nextitem) <= 4096:
                shopitems.append(nextitem)
            else:
                await message.channel.send(embed = discord.Embed(title = shopemoji + " " + itemlists[i].title + " " + shopemoji, description = "\n".join(shopitems), colour = shopcol))
                shopitems = []
                shopitems.append(nextitem)

    await message.channel.send(embed = discord.Embed(title = shopemoji + " " + itemlists[i].title + " " + shopemoji, description = "\n".join(shopitems), colour = shopcol))
    await message.delete()            
    
async def item(message):

    itemlist = []
    itemnames = extract(itemdatabase[0], 0)
    itemids = extract(itemdatabase[0], 11)

    if message.content.split(" ", 1)[1].lower() in str(itemnames).lower(): #Search by name

        for a in range(len(itemnames)):
            if message.content.split(" ", 1)[1].lower() in itemnames[a].lower():
                itemlist.append(a)

    elif message.content.split(" ", 1)[1].lower() in str(itemids).lower(): #Search by ID

        for a in range(len(itemnames)):
            if message.content.split(" ", 1)[1].lower() in itemids[a].lower():
                itemlist.append(a)

    else:
        await message.channel.send(embed = discord.Embed(title = "Item not found", description = "You could try `%shop` or `%browse` to find the item you're looking for?", colour = embcol))
        return
    
    if len(itemlist) > 1:
        itemsel = []
        for b in range(len(itemlist)):
            itemsel.append("`" + str(b+1) + "` - " + itemnames[itemlist[b]])

        emb = discord.Embed(title = "Which item would you like information on?", description = "Type the number of the one you want:\n" + "\n".join(itemsel), colour = embcol)
        emb.set_footer(text = "This message will timeout in 30 seconds")
        await message.channel.send(embed = emb)

        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                i = itemlist[int(msg.content) - 1]
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
    
    else:
        i = itemlist[0]
        
    #Build Embed
    
    attune = itemdatabase[0][i][3] #Set attunement text
    if attune == "No" or attune == "":
        attune = ""
    else:
        if "by" in attune:
            attune = " - Requires Attunement," + attune.split(",")
        else:
            attune = " - Requires Attunement"

    if itemdatabase[0][i][4] != "": #Set rarity
        itemdatabase[0][i][4] = ", " + itemdatabase[0][i][4]

    if itemdatabase[0][i][6] != "": #Set Flavour Line
        itemdatabase[0][i][6] += "\n\n"

    if itemdatabase[0][i][8] != "": #Set Curse
        itemdatabase[0][i][8] = "\n\n**Curses**\n||" + cursefromref(itemdatabase[0][i][8]) + "||"

    if itemdatabase[0][i][9] != "": #Set Kinks
        itemdatabase[0][i][9] = "\n\n**Associated Kinks**\n" + itemdatabase[0][i][9]

    #Extract shop items
    shops = []
    for c in range(len(itemlists)):
        if c < 2:
            pass
        else:
            try:
                row = extract(itemdatabase[c], 0).index(itemdatabase[0][i][11])
                shops.append(itemlists[c].title + " - " + str(itemdatabase[c][row][13]) + dezzieemj)
            except ValueError:
                pass
    if shops != []:
        itemlocations = "\n\nThis item is sold at:\n* " + "\n* ".join(shops)
    else:
        itemlocations = ""

    Maininfo = "**" + itemdatabase[0][i][0] + "**\n" + "*" + itemdatabase[0][i][1] + itemdatabase[0][i][4] + attune + "*\n\n" + itemdatabase[0][i][6] + itemdatabase[0][i][5] + itemdatabase[0][i][8] + itemdatabase[0][i][9] + itemlocations + "\n\n*id: " + itemdatabase[0][i][11] + "*"

    itememb = discord.Embed(title = itemnames[i], description = Maininfo, colour = embcol)
    await message.channel.send(embed = itememb)

async def inventory(message):
    #Find person in the inventory sheet

    #Get list of all items

    #Collect info about these items

    #Print list of items
    pass

async def buyitem(message):
    #Find person in the inventory sheet
    
    #Check if quantity was provided

    #Prepare the search term

    #Search for item in the item sheet with fuzzy matching

    #See if we have a 100 match
        #If we have multiple, display *all* 100 matches for choice and wait for the choice
    
        #if we only have one with score 100, suggest that one for buying
    
        #if we have none, display the top 10 matches and wait for a choice

    #ask for quantity if none was provided
    
    #complete the transaction
    
    
    pass

async def sellitem(message):
    #Find person in the inventory sheet

    #Check if quantity was provided

    #Prepare the search term

    #Search for item in the inventory sheet with fuzzy matching

    #Offer top 10 matches for selling in their inventory

    #Ask for quantity to sell if none was provided

    #Remove items from inventory

    #Add dezzies

    #Update PlayerInfo sheet, and Inventory sheet.
    pass

async def giveitem(message):
    #Find giver in the inventory sheet

    #Find recipient in the inventory sheet

    #prepare search term

    #Search for item in the givers inventory with fuzzy matching

    #Offer top 10 matches in their inventory if no 90-100 match


    pass

async def additem(message):
    #Find person in the inventory sheet

    #Check if quantity was provided

    #prepare search term

    #Search for item in the item sheet with fuzzy matching

    #See if we have a 100 match
        #If we have multiple, display *all* 100 matches for choice and wait for the choice
    
        #if we only have one with score 100, suggest that one for buying
    
        #if we have none, display the top 10 matches and wait for a choice
    
    #Ask for quantity to give if none was provided

    #Update Inventory sheet.
    pass

async def giftAll(message):
    #
    pass

async def shopDisplay(message):
    pass

async def dezReact(reaction):
    pass

async def rpDezReact(reaction):
    pass


#TODO: Rewrite the item function (Fuzzy String matching)
#TODO: Rewrite the Shop function (Fuzzy String matching)
async def copyEconomy(message):

    newSheet = message.content.split(" ")[-1]
    await loadEconomySheet()
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    newEconData = sheet.values().get(spreadsheetId = newSheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    newPlayerInvs = sheet.values().get(spreadsheetId = newSheet, range = "Inventories!A1:GZ2000", majorDimension='ROWS').execute().get("values")

    members = message.guild.members #Fetch the memberlist of the server we are in.
    i = 5
    while i < len(GlobalVars.economyData):
        #Add the fields for each player
        newEconData.append([GlobalVars.economyData[i][0]])
        newEconData[i].append(GlobalVars.economyData[i][1])
        try: #If they have never RP-messaged, special treatment
            newEconData.append([GlobalVars.economyData[i + 1][0]])
        except IndexError:
            newEconData.append([""])
        try: #If they have no scenes list, special treatment
            newEconData.append([GlobalVars.economyData[i + 2][0]])
        except IndexError:
            newEconData.append([""])
        newEconData.append([GlobalVars.economyData[i + 3][0]])


        #Add Levels in for the +1/+2/+3 roles, as well as the character slots.
        user = None
        try:
            user = discord.utils.find(lambda m: m.name == name, members) #Find the user we are currently copying.
        except:
            print(f"Couldn't find user {name} in the server.")

        additional_slots = 0
        if user != None:
            if "+1" in str(user.roles).lower():
                additional_slots = 1
            if "+2" in str(user.roles).lower():
                additional_slots = 2
            if "+3" in str(user.roles).lower():
                additional_slots = 3
                
        newEconData[i+2].append(additional_slots)

        #Add user ID to the economy sheet for future reference
        index = []
        name = GlobalVars.economyData[i][0]
        if user != None:
            user_id = user.id
            newEconData[i+1].append(user_id)
        elif any(name in sublist for sublist in kinkdata):    #See if we can grab the discord ID from the kinklist in case that the person isnt on the server anymore but might return.
            indexLine = [sublist2 for sublist2 in kinkdata if name in sublist2][0]
            index.append(kinkdata.index(indexLine))
            index.append(indexLine.index(newEconData[i][0]))

            newEconData[i+1].append(kinkdata[index[0]][index[1] + 1])
        #Port the items
        

        i+=4
    #Write PlayerInfo sheet
    sheet.values().update(spreadsheetId = newSheet, range = "A1:ZZ8000", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=newEconData)).execute()
    #Write Inventory Sheet
    sheet.values().update(spreadsheetId = newSheet, range = "Inventories!A1:ZZ8000", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=newPlayerInvs)).execute()




    

#-------------------------------Helper Functions-----------------------------------

#Updates the economy sheet - Needs to be called on startup or on manual changes to the sheet
async def loadEconomySheet():
    GlobalVars.economyData = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension='ROWS').execute().get("values")
    GlobalVars.economyData = loadInventorySheet()

    return
#Writes to the economy sheet. Optional argument "range" used for instances where we only want to write a few or a single cell of the sheet instead of all cells.
async def writeEconSheet(values, range = "A1:ZZ8000"):
    #in case we write a single value
    if not (":" in range):
        values = [[values]]
    sheet.values().update(spreadsheetId = EconSheet, range = range, valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values= values)).execute()
#Loads the current Inventory Sheet state. This is not kept internally, so we need to call this every time we work on the sheet.
async def loadInventorySheet():
    return sheet.values().get(spreadsheetId = inventorysheet, range = "Inventories!A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")

#Writes values to the Inventory sheet. Optional argument "range" used for instances where we only want to write a few or a single cell of the sheet instead of all cells.
async def writeInvetorySheet(values, range = "A1:ZZ8000"):
    #in case we write a single value
    if not (":" in range):
        values = [[values]]
    sheet.values().update(spreadsheetId = EconSheet, range = "Inventories!" + range, valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values= values)).execute()

async def getUserNamestr(message):
    if "@" in message.content:
        try:
            targid = int(str(message.content.split("@")[1]).split(" ")[0].replace("!","").replace("&","").replace(">",""))
        except ValueError:
            await message.channel.send(embed = discord.Embed(title = "Error!", description = "Make sure that the user you tagged is valid."))
            return
        targname = await client.fetch_user(targid)
    else:

        targname = message.author

    namestr = str(targname.name)

    return namestr, targid

async def getColumnLetter(columnindex):
    collet = ""
    if columnindex > 25:
        collet = chr(64 + math.floor(columnindex / 26))
    else:
        collet = ""                        
    collet += chr(65 + (int(columnindex % 26)))
    return collet

async def reloadItemSheet():
    itemsheet = gc.open_by_key("17M2FS5iWchszIoimqNzk6lzJMOVLBWQgEZZKUPQuMR8") #New for economy rewrite
    itemlists = itemsheet.worksheets()
    for a in range(len(itemlists)):
            GlobalVars.itemdatabase.append(itemlists[a].get_all_values())

async def stringMatchTest(message):
    item_name = message.content.split(" ", 1)[1]
    top10 = []
    top10 = await matchStringToItemBase(item_name, 10)
    top10_str = ""
    for i in range(0, len(top10)):
        top10_str += str(top10[i][0]) + ", Score: " + str(top10[i][1]) + "\n"
    print(f"Top 10 results for {item_name}: \n\n{top10_str}")

async def matchStringToItemBase(item_name, top_n_results):
    levenshtein_tuple_list = []
    for entry in GlobalVars.itemdatabase[0]:
        #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
        levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance_complete = fuzz.ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
        levenshtein_tuple_list.append([entry[0], levenshtein_distance])
    sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
    return sorted_list[:top_n_results]

