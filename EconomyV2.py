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
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if message.author.name in x][0])
    
    #Get list of all items
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]
    item_list = []  #collect a list of the descriptors in order here.
    embed_string = ""
    for i in range(2, len(player_inventory[0])):
        item_descriptor = player_inventory[0][i]
        item_list.append(item_descriptor)
        #Find item in database
        item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_descriptor in x][0]
        #Collect info about this item
        item_name = item_database_info[0]
        item_short_description = item_database_info[7]
        quantity = player_inventory[1][i]
        curse_names = ""
        if player_inventory[2][i] != "-": #If the item has curses
            curses = player_inventory[2][i].split(",")
            
            #Generate the list of curses the item has.
            for curse in curses:
                curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
                if curse_names == "": #Construct the string in a way that it doesn't have trailing commas and spaces.
                    curse_names += f"{curse_info[0][0]}"
                else: curse_names += f", {curse_info[0][0]}"
        if curse_names == "":
            embed_string += (f"`{i-1}`: {quantity}x `{item_name}`: {item_short_description}\n\n")
        else: embed_string += (f"`{i-1}`: {quantity}x `{item_name}`: {item_short_description}\n__Curses__: {curse_names}\n\n")
        
    #Print list of items
    inventory_embed = discord.Embed(title = f"{player_inventory[0][0]}'s inventory", description= embed_string + "\n\nFor more information about an item and its curses, enter the according number. This message will time out in 30 seconds.", colour = embcol)
    await message.channel.send(embed = inventory_embed)


    #Wait for a response to show more info about a specific item
    i = -1
    try:
        msg = await client.wait_for('message', timeout = 30, check = check(message.author))
        try:
            i = int(msg.content) - 1
            await msg.delete()
        except TypeError or ValueError:
            await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
            await msg.delete()
            return
    except asyncio.TimeoutError:
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        await message.delete()
        return
    if i >= 0:
        #Provide information about the item and it's curses.
        item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_list[i] in x][0]
        curses = []
        curse_descriptors = player_inventory[2][i + 2] #+2 becasue the first two entries are player info
        curse_descriptors = curse_descriptors.split(",")
        for curse in curse_descriptors:
            curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
            curses.append(curse_info)
        item_name = item_database_info[0]
        #add item type and rarity
        embed_string = f"*{item_database_info[1]}, {item_database_info[4]}*"
        #add attunement to the string
        if item_database_info[3].lower() == "yes":
            embed_string += f" *(Requires Attunement)*\n\n"
        elif "by" in item_database_info[3]:
                spellcaster = item_database_info[3].replace("Yes, by ", "")
                embed_string += f" *(Requires Attunement by {spellcaster})*\n\n"
        else: embed_string += "\n\n"

        #add long description
        embed_string += item_database_info[6] + "\n\n" + item_database_info[5]
        #add default curse
        if item_database_info[8] != "":
            embed_string += f"\n\n**__Default curse:__** \n{item_database_info[8]}"
        #add additional curses
        if curses[0] != []:
            embed_string += "\n\n**__Additional curses:__**\n"
            for curse in curses:
                embed_string += f"\n**{curse[0][0]}**(Level {curse[0][1]} curse):\n{curse[0][2]}\n"

        item_embed = discord.Embed(title=f"Item Info for {item_name}", description=embed_string, colour=embcol)
        await message.channel.send(embed = item_embed)



    

async def buyitem(message):
    #Find person in the inventory sheet
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if message.author.name in x][0])

    #Check if quantity was provided and prepare the search term
    buyquant = 1
    try:
        fullMessage = message.content.split(" ", 1)[1] #cut the %buy off
        #Cut away trailing spaces
        while fullMessage.rsplit(" ")[-1] == "":
            fullMessage = fullMessage.rsplit(" ", 1)[0]

        searchterm = fullMessage.rsplit(" ", 1)[0]
        try:
            buyquant = int(fullMessage.rsplit(" ", 1)[-1]) #Try to extract a buy quantity from the end of the string
            
            if buyquant < 1:
                buyquant = 0
        except ValueError:
            print("Buy function Value Error. Probably didn't specify amount. Defaulting to 1")
            buyquant = 1  
        except TypeError:
            print("Buy function type error. Probably didn't specify amount. Defaulting to 1")
            buyquant = 1  
    except IndexError:
        searchterm = "11111111111111" #Something irrelevant cause the search was empty
    
    #Search for item in the item sheet with fuzzy matching
    item_matches = await matchStringToItemBase(searchterm, 10)
    selector_options = []
    #See if we have an almost perfect match
    if item_matches[0][1] > 93:
        #If we have multiple, display *all* almost perfect matches for choice and wait for the choice
        if item_matches[1][1] > 93:

            for i in range(0, len(item_matches)):
                if item_matches[i][1] > 93:
                    selector_options.append(item_matches[i])
        #if we only have one with score 100, suggest that one for buying
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
        await message.channel.send(embed = discord.Embed(title="Didn't find a perfect match to what you are looking for.", description="Here are the top 10 closest results. Please choose which of these you want.\n\n" + top10_string + "\n\n" + "This message will time out in 30 seconds."))
    #Wait for reply
        #ask to choose an item
        i = -1
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                i = int(msg.content) - 1
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
        if i >= 0 and i < len(selector_options):
            selected_item = selector_options[i]
        else: 
            await message.channel.send(embed=discord.Embed(title=f"Number has to be between 1 and {len(selector_options)}", colour = embcol))
            await message.delete()
            return
    else: selected_item = selector_options[0]

    #Check if item is present in multiple shops
    available_in_shops = []
    try:
        for j in range(3, 3+GlobalVars.config["general"]["number_of_shops"]):
            for row in GlobalVars.itemdatabase[j]:
                if selected_item[2] in row:
                    available_in_shops.append(GlobalVars.itemdatabase[j])
    except IndexError: 
        print("Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops")
        await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops", colour = embcol))
    

    #Check if we need to show multiple shops due to having multiple versions of the item in different shops (cursed and noncursed.)
    curses = "" #We need this one later again.
    if len(available_in_shops) > 1:
        shop_embed = "The item is available in the following shops:\n\n"
        for i in range(0, len(available_in_shops)):
            item_in_shop = [x for x in available_in_shops[i] if selected_item[2] in x][0]
            item_name = item_in_shop[1]
            price = int(item_in_shop[3]) * int(item_in_shop[12])
            quantity_available = item_in_shop[18]
            curses_identifier = item_in_shop[14].split(",")
            
            if len(curses_identifier) > 0 and curses_identifier[0] != "":
                

                n = 0
                for curse in curses_identifier:
                    try:
                        curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                    except IndexError:
                        await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
 
                    
                    if n == 0:
                        curses+= f"{curse[0]}"
                        n +=1
                    else:
                        curses+= f", {curse[0]}"

                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\nPotential Curses: {curses}\n\n"
            else: 
                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\n\n"
        
        await message.channel.send(embed=discord.Embed(title=f"There are multiple versions of this item. Which do you want?", description=shop_embed, colour = embcol))

        #Wait for user input as to which shop to choose
        userinput = -1
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                userinput = int(msg.content) - 1
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
        #Collect info for that item.
        item_database_info = [x for x in available_in_shops[userinput] if selected_item[2] in x][0]
        item_name = item_database_info[1]
        item_identifier = item_database_info[0]
        price = int(item_database_info[3]) * int(item_database_info[12])
        quantity_available = item_database_info[18]
                
    else:
        #if the item to buy is already clear, collect info.
        item_database_info = [x for x in available_in_shops[0] if selected_item[2] in x][0]
        item_name = item_database_info[1]
        item_identifier = item_database_info[0]
        price = int(item_database_info[3]) * int(item_database_info[12])
        quantity_available = item_database_info[18]

    #add item type and rarity
    embed_string = f"*{item_database_info[1]}, {item_database_info[4]}*"
    #add attunement to the string
    if item_database_info[4].lower() == "yes":
        embed_string += f" *(Requires Attunement)*\n\n"
    elif "by" in item_database_info[4]:
            spellcaster = item_database_info[4].replace("Yes, by ", "")
            embed_string += f" *(Requires Attunement by {spellcaster})*\n\n"
    else: embed_string += "\n\n"

    #add long description
    embed_string += item_database_info[7] + "\n\n" + item_database_info[6]
    #add default curse
    if item_database_info[9] != "":
        embed_string += f"**\n\n__Default curse:__** \n{item_database_info[9]}"
    #add additional curses
    if curses != "":
        embed_string += "**\n\n__Potential curses:__**\n"
        for curse in curses_identifier:
            try:
                full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
            except IndexError:
                await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
            embed_string+= f"**{full_curse[0]}**: {full_curse[2]}\n\n"


    await message.channel.send(embed=discord.Embed(title=f"Buy this item? (Y/N)", description=embed_string, colour = embcol))
    
    #complete the transaction by taking dezzies from the person, and entering the item into their inventory (ID, quantity, additional curses.). Make sure to stack stackable items.
    
    
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
    #Find quantity of dezzies to add to everyone's balance

    #Add to each balance

    #Write sheet
    pass

async def shopDisplay(message):
    #????
    pass

async def dezReact(reaction):
    #Copy the old function, change the way we write
    pass

async def rpDezReact(reaction):
    #Copy the old function, change the way we write
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
    GlobalVars.inventoryData = sheet.values().get(spreadsheetId = inventorysheet, range = "Inventories!A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")

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

#Receives a string that represents an item name, and an integer that represents the amount of results desired. Returns a list of lists. Each entry
#shows one potential item candidate in the form of [name, levenshtein distance score, unique id]
async def matchStringToItemBase(item_name, top_n_results):
    levenshtein_tuple_list = []
    for entry in GlobalVars.itemdatabase[0]:
        #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
        levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance_complete = fuzz.ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
        levenshtein_tuple_list.append([entry[0], levenshtein_distance, entry[11]])
    sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
    return sorted_list[:top_n_results]

