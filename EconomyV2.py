from CommonDefinitions import *
import GlobalVars
from thefuzz import fuzz
import asyncio
import TupperDatabase
import TransactionsDatabaseInterface

economy_lock = asyncio.Lock() 
add_dezzie_lock = asyncio.Lock()
#Summons the list of shops, and allows looking at one
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
    
#Summons information about an item
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

#Summons the player's inventory
async def inventory(message):
    #Find person in the inventory sheet
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if message.author.name in x][0])
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]

    #Get list of all items
    i, item_list = await showInventoryAndChooseItem(message, author_row_index, "\n\nFor more information about an item and its curses, enter the according number. This message will time out in 30 seconds.")
    if i == False and i != 0:
        return
    if i >= 0:
        #Provide information about the item and it's curses.
        item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_list[i] in x][0]
        curses = []
        try:
            curse_descriptors = player_inventory[2][i + 2] #+2 becasue the first two entries are player info
            curse_descriptors = curse_descriptors.split(",")
            if curse_descriptors[0] != "": #Check if curse descriptors are empty (= no curses on the item). For some reason this doesn't work in the for loop.
                for curse in curse_descriptors:
                    curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
                    curses.append(curse_info)
        except IndexError: #This happens when a trailing item in the inventory has no curse. Just ignore it.
            pass
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
        if curses != []:
            embed_string += "\n\n**__Additional curses:__**\n"
            for curse in curses:
                embed_string += f"\n**{curse[0][0]}**(Level {curse[0][1]} curse):\n{curse[0][2]}\n"

        item_embed = discord.Embed(title=f"Item Info for {item_name}", description=embed_string, colour=embcol)
        await message.channel.send(embed = item_embed)

#Guides the user through buying an item
async def buyitem(message):
    

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
        #Generate top10 dropdown selector
        top10_view = Dropdown_Select_View(timeout=30, optionamount=len(selector_options), maxselectionamount=1, namelist=[a[0] for a in selector_options])
        await message.channel.send(embed = discord.Embed(title="Didn't find a perfect match to what you are looking for.", description="Here are the top 10 closest results. Please choose which of these you want.\n\n" + top10_string + "\n\n" + "This message will time out in 30 seconds."), view=top10_view)
        #Wait for reply
        #ask to choose an item
        if await top10_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        i = int(top10_view.button_response[0])-1
        selected_item = selector_options[i]

    else: selected_item = selector_options[0]

    #Check if item is present in multiple shops
    available_in_shops = []
    shopnumbers = []
    try:
        for j in range(3, 3+GlobalVars.config["general"]["number_of_shops"]):
            for row in GlobalVars.itemdatabase[j]:
                if selected_item[2] in row:
                    available_in_shops.append(GlobalVars.itemdatabase[j])
                    shopnumbers.append(j)
    except IndexError: 
        print("Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops")
        await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops", colour = embcol))
    

    #Check if we need to show multiple shops due to having multiple versions of the item in different shops (cursed and noncursed.)

    chosenShop = -1
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
                curses = ""
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
        
        #Generate selector view to choose items.
        shop_selection_view = Dropdown_Select_View(timeout=30, optionamount=len(shopnumbers), maxselectionamount=1) #Only let them choose one item.
        await message.channel.send(embed=discord.Embed(title=f"There are multiple versions of this item. Which do you want to choose?", description=shop_embed, colour = embcol), view = shop_selection_view)
        #Wait for reply
        if await shop_selection_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        userinput = int(shop_selection_view.button_response[0])-1
        
        #note the shop ID
        chosenShop = shopnumbers[userinput]
                
    else:
        #if the item to buy is already clear, collect info.
        try:
            chosenShop = shopnumbers[0]
        except IndexError:
            await message.channel.send(embed=discord.Embed(title="Sorry, that item is currently not in any shop. It may be an event item. If not, contact staff.", color=embcol))
    
    #Collect information about the item to be bought.
    item_database_info = [x for x in GlobalVars.itemdatabase[chosenShop] if selected_item[2] in x][0]
    item_name = item_database_info[1]
    item_identifier = item_database_info[0]
    price = int(item_database_info[3]) * int(item_database_info[12])
    quantity_available = item_database_info[18]
    curses_identifier = item_database_info[14].split(",")
    #add item type and rarity
    embed_string = f"*{item_database_info[1]}, {item_database_info[5]}*"
    #add attunement to the string
    if item_database_info[4].lower() == "yes":
        embed_string += f" *(Requires Attunement)*\n\n"
    elif "by" in item_database_info[4]:
            spellcaster = item_database_info[4].replace("Yes, by ", "")
            embed_string += f" *(Requires Attunement by {spellcaster})*\n\n"
    else: embed_string += "\n\n"

    if quantity_available == "":
        quantity_available = "Infinite"
    embed_string += f"**Quantity Available: {quantity_available}, Price per unit: {price}** \n\n"

    #add long description
    embed_string += item_database_info[7] + "\n\n" + item_database_info[6]
    #add default curse
    if item_database_info[9] != "":
        embed_string += f"**\n\n__Default curse:__** \n{item_database_info[9]}"
    #add additional curses
    potential_curses_string = ""
    potential_curses = []
    if curses_identifier[0] != "":
        potential_curses_string += f"**\n\n__Potential curses (50% chance for each to appear):__**\n"

        for curse in curses_identifier:
            try:
                full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                potential_curses.append(full_curse)
            except IndexError:
                await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
            potential_curses_string+= f"**{full_curse[0]}**: {full_curse[2]}\n\n"
    if quantity_available != "Infinite":
        if buyquant > int(quantity_available):
            await message.channel.send(embed=discord.Embed(title=f"You requested {buyquant} of this item, but only {quantity_available} are available. Please try again and request a lower amount.", colour = embcol))

    #Ask for confirmation or quantity change
    confirm_view = Yes_No_Quantity_View()
    await message.channel.send(embed=discord.Embed(title=f"Buy {buyquant} of this item for a total of {price * buyquant}?", description=embed_string + potential_curses_string, colour = embcol), view=confirm_view)

    if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(optionamount=25, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to buy? __Keep in mind, all items bought in bulk will have the same random curse roll.__", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        buyquant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View()
        await message.channel.send(embed=discord.Embed(title=f"Buy {buyquant} of this item for a total of {price * buyquant}?", description=embed_string + potential_curses_string, colour = embcol), view = confirm_view)
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
    
    #complete the transaction by taking dezzies from the person, and entering the item into their inventory (ID, quantity, additional curses.). Make sure to stack stackable items.
    try:
        if confirm_view.button_response == "yes":
            #Complete transaction
            #Find person in the inventory sheet
            author_row_index_inventory = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(message.author.id) in x][0])
            playerID = GlobalVars.inventoryData[author_row_index_inventory][1]
            author_row_index_economy = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
            old_balance = GlobalVars.economyData[author_row_index_economy+1][1]
            success = await removeDezziesFromPlayerWithoutMessage(price * buyquant, playerID=playerID)
            if success:
                rolled_curses = await addItemToPlayerWithCurseFromShop(message, playerID, item_identifier, buyquant, chosenShop)
                new_balance = GlobalVars.economyData[author_row_index_economy+1][1]
                if quantity_available != "Infinite":
                    #Update the Stock of the item.
                    itemindex = GlobalVars.itemdatabase[chosenShop].index(item_database_info)
                    GlobalVars.itemdatabase[chosenShop][itemindex][18] = int(quantity_available) - buyquant
                    await writeItemsheetCell(chosenShop, itemindex, 18, int(quantity_available) - buyquant)
                await message.channel.send(embed=discord.Embed(title="Success!",description=f"Before this transaction you had {old_balance}{dezzieemj}. You paid {price}{dezzieemj} and your new balance is {new_balance}{dezzieemj}", colour = embcol))
                rolled_curse_string = ""
                if potential_curses != []:
                    rolled_curse_string += "\n\n**__Actual Curses:__**\n\n"
                    for curse in rolled_curses:
                        rolled_curse_string += f"**{potential_curses[curse][0]}**: {potential_curses[curse][2]}\n\n"
                    await message.channel.send(embed=discord.Embed(title="Take a look at the item and it's rolled curses!",description=embed_string + rolled_curse_string, colour = embcol))

            else:
                await message.channel.send(embed=discord.Embed(title="Not enough funds!",description="Your funds are insufficient to buy this item!", colour = embcol))
        else:
            await message.channel.send(embed=discord.Embed(title="Buy process cancelled!", colour = embcol))
    except TypeError:
        await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="Reply must be yes or no (or y / n)", colour = embcol))
        return
    return

#Guides the user through selling an item
async def sellitem(message):
    #Find person in the inventory sheet
    author_inventory_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(message.author.id) in x][0])
    author_economy_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    #Check if quantity was provided and prepare the search term
    sellquant = 1
    quantProvided = False
    try:
        fullMessage = message.content.split(" ", 1)[1] #cut the %sellitem off
        #Cut away trailing spaces
        while fullMessage.rsplit(" ")[-1] == "":
            fullMessage = fullMessage.rsplit(" ", 1)[0]
        try:
            sellquant = int(fullMessage.rsplit(" ", 1)[-1]) #Try to extract a buy quantity from the end of the string
            quantProvided = True
            if sellquant < 1:
                await message.channel.send(embed=discord.Embed(title="Sell quantity must be 1 or higher.", color=embcol))
        except ValueError:
            print("Buy function Value Error. Probably didn't specify amount. Defaulting to 1")
            sellquant = 1  
        except TypeError:
            print("Buy function type error. Probably didn't specify amount. Defaulting to 1")
            sellquant = 1  
    except IndexError:
        pass

    #Show inventory to select item
    i, item_list = await showInventoryAndChooseItem(message, author_inventory_row_index, "\n\n__To choose which item to sell, enter the according number.__ This message will time out in 30 seconds.")
    if i == False:
        return
    if i >= 0:
        i = i+2 #Because the first two columns are for personal info.

    
    #Ask for quantity to sell if none was provided
    if quantProvided == False:
        sellquant = 1

    item_identifier = GlobalVars.inventoryData[author_inventory_row_index][i]
    
   

    #find the shop that sells this item to later add stock to it.
    shops_containing_sold_item = []
    for y in range(3, len(GlobalVars.itemdatabase)):
        try:
            GlobalVars.itemdatabase[y].index([x for x in GlobalVars.itemdatabase[y] if item_identifier in x][0])
            success = True
        except IndexError:
            success = False
        if success == True:
            shops_containing_sold_item.append(y)
    #If multiple shops have the item, choose one at random.
    if len(shops_containing_sold_item) > 1:
        sell_shop_index = shops_containing_sold_item[random.randint(1, len(shops_containing_sold_item)) - 1]
    elif len(shops_containing_sold_item) == 1: 
        sell_shop_index = shops_containing_sold_item[0]
    else:
        await message.channel.send(embed=discord.Embed(title="Did not find a shop that sells, and therefore buys this item. Talk to the Bot Gods about that.", color=embcol))

    #ask for confirmation
    
    item_index = GlobalVars.itemdatabase[sell_shop_index].index([x for x in GlobalVars.itemdatabase[sell_shop_index] if item_identifier in x][0])
    item_price = GlobalVars.itemdatabase[sell_shop_index][item_index][13]
    itemname = GlobalVars.itemdatabase[sell_shop_index][item_index][1]
    
    confirm_view = Yes_No_Quantity_View()
    await message.channel.send(embed=discord.Embed(title=f"Do you want to sell {sellquant}x {itemname} for {int(int(item_price) * GlobalVars.config["economy"]["sellpricemultiplier"] * sellquant)}?"), view = confirm_view)
    
    if await confirm_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(optionamount=int(GlobalVars.inventoryData[author_inventory_row_index+1][i]), maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to sell? You own {int(GlobalVars.inventoryData[author_inventory_row_index+1][i])}.", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        sellquant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View()
        await message.channel.send(embed=discord.Embed(title=f"Do you want to sell {sellquant}x {itemname} for {int(int(item_price) * GlobalVars.config["economy"]["sellpricemultiplier"] * sellquant)}?"), view = confirm_view)
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return

    if confirm_view.button_response == "yes":
        deleted = False
        #Remove items from inventory
        await removeItemFromInventory(author_inventory_row_index, i, sellquant)

        #Add stock to the inventory of the shop
        item_row_index = GlobalVars.itemdatabase[sell_shop_index].index([x for x in GlobalVars.itemdatabase[sell_shop_index] if item_identifier in x][0])
        if GlobalVars.itemdatabase[sell_shop_index][item_row_index][18] == "":
            new_stock = ""
        else:
            new_stock = int(GlobalVars.itemdatabase[sell_shop_index][item_row_index][18]) + sellquant

        #Add dezzies
        await addDezziesToPlayer(message, int(int(item_price) * GlobalVars.config["economy"]["sellpricemultiplier"]) * sellquant, playerID=message.author.id, write_econ_sheet=False)

        #Update PlayerInfo sheet, and Inventory sheet.
        await writeEconSheet(GlobalVars.economyData)
        await writeInvetorySheet(GlobalVars.inventoryData)
        await writeItemsheetCell(sell_shop_index, item_row_index, 18, new_stock)

        if deleted == True: #Clean up the internal inventory representation from trailing spaces
            del GlobalVars.inventoryData[author_inventory_row_index][-1]
            del GlobalVars.inventoryData[author_inventory_row_index+1][-1]
            try:
                del GlobalVars.inventoryData[author_inventory_row_index+2][-1]
            except IndexError: #If we get an index error, that cell wasn't occupied anyways and was a trailing cell.
                pass

#Guides the user through giving an item
async def giveitem(message):
    #Find giver in the inventory sheet
    author_inventory_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(message.author.id) in x][0])

    #Find recipient in the inventory sheet
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_inventory_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(recipient_id) in x][0])

    
    #Check if quantity was provided
    givequant = 1
    quantProvided = False
    try:
        fullMessage = message.content.split(" ", 1)[1] #cut the %sellitem off
        #Cut away trailing spaces
        while fullMessage.rsplit(" ")[-1] == "":
            fullMessage = fullMessage.rsplit(" ", 1)[0]
        try:
            givequant = int(fullMessage.rsplit(" ", 1)[-1]) #Try to extract a buy quantity from the end of the string
            quantProvided = True
            if givequant < 1:
                await message.channel.send(embed=discord.Embed(title="Sell quantity must be 1 or higher.", color=embcol))
        except ValueError:
            print("Buy function Value Error. Probably didn't specify amount. Defaulting to 1")
            givequant = 1  
        except TypeError:
            print("Buy function type error. Probably didn't specify amount. Defaulting to 1")
            givequant = 1  
    except IndexError:
        pass

    #Show inventory to select item
    i, item_list = await showInventoryAndChooseItem(message, author_inventory_row_index, "\n\nTo choose which item to sell, enter the according number. This message will time out in 30 seconds.")
    if i == False:
        if i == 0:
            pass
        else:
            return
    if i >= 0:
        i = i #Because the first two columns are for personal info.

    itemname = GlobalVars.itemdatabase[0][GlobalVars.itemdatabase[0].index([x for x in GlobalVars.itemdatabase[0] if item_list[i] in x][0])][0]
    player_inventory = GlobalVars.inventoryData[author_inventory_row_index:author_inventory_row_index+5]
    item_quantity = int(player_inventory[1][i+2])
    #Ask for quantity to sell if none was provided
    if quantProvided == False:
        quantity_view = Dropdown_Select_View(optionamount=item_quantity, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title="Please select an amount you want to give away of the chosen item.", color=embcol), view=quantity_view)

        if await quantity_view.wait():
                await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                return
        #Wait for user input as to which shop to choose
        givequant = int(quantity_view.button_response[0])

    #Confirmation
    confirm_view = Yes_No_View()
    await message.channel.send(embed=discord.Embed(title=f"Do you want to give {givequant}x {itemname} to {recipient_name}?", colour=embcol), view=confirm_view)
    
    if await confirm_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    if confirm_view.button_response == "yes":
        
        #Add item to recipient inventory
        try:
            giver_curses = GlobalVars.inventoryData[author_inventory_row_index+2][i + 2]
        except IndexError:
            giver_curses = ""

        success = await addItemToInventory(recipient_inventory_row_index, item_list[i], givequant, giver_curses)
        if success == False:
            await message.channel.send(embed=discord.Embed(title=f"Failed to add item to inventory. Contact the botgods for help.", colour=embcol))
            return
        success = await removeItemFromInventory(author_inventory_row_index, i+2, givequant) #This also writes the inventory sheet.
        if success == False:
            await message.channel.send(embed=discord.Embed(title=f"Failed to remove item from inventory. Contact the botgods for help, your inventory might be corrupted.", colour=embcol))
            return
        await message.channel.send(embed=discord.Embed(title=f"Success!", description=f"You gave {givequant}x {itemname} to {recipient_name}.", colour=embcol))

#Guides a staff member through adding an item to a players inventory
async def additem(message):
    #Find person in the inventory sheet
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_inventory_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(recipient_id) in x][0])

    #Check if quantity was provided
    givequant = 1
    try:
        fullMessage = message.content.split(" ", 2)[2] #cut the %additem and the recipient name off
        #Cut away trailing spaces
        while fullMessage.rsplit(" ")[-1] == "":
            fullMessage = fullMessage.rsplit(" ", 1)[0]

        searchterm = fullMessage.rsplit(" ", 1)[0]
        try:
            givequant = int(fullMessage.rsplit(" ", 1)[-1]) #Try to extract a buy quantity from the end of the string
            
            if givequant < 1:
                givequant = 0
        except ValueError:
            print("Buy function Value Error. Probably didn't specify amount. Defaulting to 1")
            givequant = 1  
        except TypeError:
            print("Buy function type error. Probably didn't specify amount. Defaulting to 1")
            givequant = 1  
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

        #Generate selector view to choose items.
        item_selection_view = Dropdown_Select_View(timeout=30, optionamount=len(selector_options), maxselectionamount=1, namelist=[i[0] for i in selector_options]) #Only let them choose one item.
        await message.channel.send(embed = discord.Embed(title="Didn't find a perfect match to what you are looking for.", description="Here are the top 10 closest results. Please choose which of these you want.\n\n" + top10_string + "\n\n" + "This message will time out in 30 seconds."), view = item_selection_view)
        #Wait for reply
        if await item_selection_view.wait():
                await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                return
        
        i = int(item_selection_view.button_response[0]) - 1
        if i >= 0 and i < len(selector_options):
            selected_item = selector_options[i]
        else: 
            await message.channel.send(embed=discord.Embed(title=f"Number has to be between 1 and {len(selector_options)}", colour = embcol))
            await message.delete()
            return
    else: selected_item = selector_options[0]

    #Check if item is present in multiple shops
    available_in_shops = []
    shopnumbers = []
    try:
        for j in range(3, 3+GlobalVars.config["general"]["number_of_shops"]):
            for row in GlobalVars.itemdatabase[j]:
                if selected_item[2] in row:
                    available_in_shops.append(GlobalVars.itemdatabase[j])
                    shopnumbers.append(j)
    except IndexError: 
        print("Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops")
        await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops", colour = embcol))
    

    #Check if we need to show multiple shops due to having multiple versions of the item in different shops (cursed and noncursed.)

    chosenShop = -1

    item_in_shop = False
    if len(available_in_shops) > 1:
        shop_embed = "The item is available in the following shops and versions:\n\n"
        for i in range(0, len(available_in_shops)):
            item_in_shop = [x for x in available_in_shops[i] if selected_item[2] in x][0]
            item_name = item_in_shop[1]
            price = int(item_in_shop[3]) * int(item_in_shop[12])
            quantity_available = item_in_shop[18]
            curses_identifier = item_in_shop[14].split(",")
            
            if len(curses_identifier) > 0 and curses_identifier[0] != "":
                

                n = 0
                curses = ""
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
        

        #Generate selector view to choose items.
        shop_selection_view = Dropdown_Select_View(timeout=30, optionamount=len(shopnumbers), maxselectionamount=1) #Only let them choose one item.
        await message.channel.send(embed=discord.Embed(title=f"There are multiple versions of this item. Which do you want to choose?", description=shop_embed, colour = embcol), view = shop_selection_view)
        #Wait for reply
        if await shop_selection_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        userinput = int(shop_selection_view.button_response[0])-1
        
        #note the shop ID
        chosenShop = shopnumbers[userinput]
        item_in_shop = True
                
    else:
        #if the item to buy is already clear, collect info.
        try:
            chosenShop = shopnumbers[0]
            item_in_shop = True
        except IndexError:  #This happens if the item is not in any shop
            item_in_shop = False
            item_database_info = [x for x in GlobalVars.itemdatabase[0] if selected_item[2] in x][0]
            item_name = item_database_info[0]
            item_identifier = item_database_info[11]
            price = int(item_database_info[2])
            quantity_available = ""
            curses_identifier = [""]  
            rarity = item_database_info[4]
            attunement_requirement = item_database_info[3]
            mechanics = item_database_info[5]
            flavour = item_database_info[6]
            default_curse = item_database_info[8]

    #Collect information about the item to be bought. Only do so if the item is in a shop.
    if item_in_shop == True:
        item_database_info = [x for x in GlobalVars.itemdatabase[chosenShop] if selected_item[2] in x][0]
        item_name = item_database_info[1]
        item_identifier = item_database_info[0]
        price = int(int(item_database_info[3]) * float(item_database_info[12]))
        quantity_available = item_database_info[18]
        curses_identifier = item_database_info[14].split(",")
        rarity = item_database_info[5]
        attunement_requirement = item_database_info[4]
        mechanics = item_database_info[7]
        flavour = item_database_info[6]
        default_curse = item_database_info[9]

    #add item type and rarity
    embed_string = f"*{item_name}, {rarity}*"
    #add attunement to the string
    if attunement_requirement.lower() == "yes":
        embed_string += f" *(Requires Attunement)*\n\n"
    elif "by" in attunement_requirement:
            spellcaster = attunement_requirement.replace("Yes, by ", "")
            embed_string += f" *(Requires Attunement by {spellcaster})*\n\n"
    else: embed_string += "\n\n"

    if quantity_available == "":
        quantity_available = "Infinite"
    embed_string += f"**Quantity Available: {quantity_available}, Price per unit: {price}** \n\n"

    #add long description
    if mechanics != "":
        embed_string += mechanics + "\n\n" + flavour
    else:
        embed_string += flavour
    if default_curse != "":
        embed_string += f"**\n\n__Default curse:__** \n{default_curse}"
    #add additional curses
    potential_curses = ""
    if curses_identifier[0] != "":
        potential_curses += "**\n\n__Potential curses:__**\n"
        curseCount = 1
        potential_curse_names = []
        for curse in curses_identifier:
            try:
                full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
            except IndexError:
                await message.channel.send(embed=discord.Embed(title=f"Error in additem function.", description="Index error in additem function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
            potential_curses+= f"`{curseCount}:` **{full_curse[0]}**: {full_curse[2]}\n\n"
            potential_curse_names.append(full_curse[0])
            curseCount += 1
    #Prepare buttons
    if potential_curses != "":
        curse_view = AddItem_Curse_View()
    else:
        curse_view = AddItem_Curse_View_No_Shopcurses()
    await message.channel.send(embed=discord.Embed(title=f"Should the item contain curses?", description=embed_string + potential_curses + "\n\nThis selection will time out in 90 seconds.", colour = embcol), view =curse_view)
    
    #Wait for button press 
    if await curse_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return

    #Check for the button response
    curse_names = ""
    curses = ""
    if curse_view.button_response == "yes": #If we want randomly generated curses from the list
        #roll curses
        if curses_identifier[0] != "":
            for curse in curses_identifier:
                if random.randint(1,2) == 2: #50% chance for every curse to occur
                    if curses == "":
                        full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                        curse_names += f"{full_curse[0]}"
                        curses += curse
                    else: curses += f",{curse}"
        else: 
            curses = ""
    elif curse_view.button_response == "no": #If we want no curses
        curses = ""
    elif curse_view.button_response == "custom": #If we want custom entered curses without restrictions
        curseprint = ""
        embed_string_custom_curses = [""]
        curses_identifier = []
        y = 0
        for i in range(1, len(GlobalVars.itemdatabase[1])):
            curseprint = f"`{i}`: {GlobalVars.itemdatabase[1][i][0]}, {GlobalVars.itemdatabase[1][i][2]}\n\n"
            curses_identifier.append(GlobalVars.itemdatabase[1][i][4])
            if len(embed_string_custom_curses[y]) + len(curseprint) > 4096:
                embed_string_custom_curses.append(curseprint)
                y += 1
            else:
                embed_string_custom_curses[y] += curseprint
        
        #Print list of items
        embed_bottom_note = "\n\n **Enter a list of numbers(1,3,4...) that corresponds to the curses you want on the item!**\n\nThis selection will time out in 120 seconds."
        if len(embed_string_custom_curses) == 1:
            embed_string_custom_curses[0] += embed_bottom_note

        curse_embed = discord.Embed(title = f"Which curses should the item have?\n\nEnter a list of numbers shown (1,3,4...)", description= embed_string_custom_curses[0], colour = embcol)
        await message.channel.send(embed = curse_embed)
        if len(embed_string_custom_curses) > 1:
            for i in range(1, len(embed_string_custom_curses)):
                    if i == len(embed_string_custom_curses) - 1:
                        if len(embed_string_custom_curses[i]) + len(embed_bottom_note) < 4096:
                            curse_embed = discord.Embed(description= embed_string_custom_curses[i] + embed_bottom_note, colour = embcol)
                        else:
                            curse_embed = discord.Embed(description= embed_string_custom_curses[i] , colour = embcol)
                            await message.channel.send(embed = curse_embed)
                            curse_embed = discord.Embed(description= embed_bottom_note , colour = embcol)
                    else:
                        curse_embed = discord.Embed(description= embed_string_custom_curses[i], colour = embcol)

                    await message.channel.send(embed = curse_embed)
        #let user choose the curses (input a list of numbers)
        userinput = "-"
        try:
            msg = await client.wait_for('message', timeout = 90, check = checkstr(message.author))
            try:
                userinput = msg.content
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="Reply must be yes, no, or a comma separated list of numbers.", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
        #add curses to the list.
        curse_names = ""
        user_text_curse_choices = userinput.replace(" ", "").split(",")
        curse_choices = []
        for choice in user_text_curse_choices:
            try:
                curse_choices.append(int(choice) - 1)
            except TypeError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="Reply must be yes, no, or a comma separated list of numbers.", colour = embcol))
        curse_choices = sorted(curse_choices)

        for choice in curse_choices:
            full_curse = [x for x in GlobalVars.itemdatabase[1] if str(curses_identifier[choice]) in x][0]
            if curses == "":
                curse_names += f"{full_curse[0]}"
                curses += full_curse[4]
            else: 
                curse_names += f", {full_curse[0]}"
                curses += f",{full_curse[4]}"


    elif curse_view.button_response == "shopcurses": #Here we ask for a list of integers.
        if curseCount > 0:
            #Create dropdown and wait for user to select
            select_view = Dropdown_Select_View(optionamount=curseCount - 1, maxselectionamount=25, namelist=potential_curse_names)
            await message.channel.send(embed=discord.Embed(title="Select the numbers of the curses above that you want on the item. (Max. 25)",description="This selection will time out in 120 seconds.", colour = embcol),view=select_view)
            
            if await select_view.wait():
                await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                return
    
            curse_names = ""
            user_text_curse_choices = select_view.button_response
            curse_choices = []
            for choice in user_text_curse_choices:
                try:
                    curse_choices.append(int(choice))
                except TypeError:
                    await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="Reply must be yes, no, or a comma separated list of numbers.", colour = embcol))
            curse_choices = sorted(curse_choices)

            for choice in curse_choices:
                full_curse = [x for x in GlobalVars.itemdatabase[1] if str(curses_identifier[choice - 1]) in x][0]
                if curses == "":
                    curse_names += f"{full_curse[0]}"
                    curses += full_curse[4]
                else: 
                    curse_names += f", {full_curse[0]}"
                    curses += f",{full_curse[4]}"

    elif curse_view.button_response == "cancel":
        await message.channel.send(embed=discord.Embed(title="GiveItem process cancelled!", colour = embcol))
        return

    if curses != "":
        embed_string += f"\n\n**Selected Curses:**\n\n{curse_names}"

    confirm_view = Yes_No_Quantity_View()
    await message.channel.send(embed=discord.Embed(title=f"Give {givequant} of this item to {recipient_name}?", description=embed_string, colour = embcol), view = confirm_view)
    if await confirm_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(optionamount=25, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to add to {recipient_name}'s inventory?", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        givequant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View()
        await message.channel.send(embed=discord.Embed(title=f"Give {givequant} of this item to {recipient_name}?", description=embed_string, colour = embcol), view = confirm_view)
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return

    #add item to inventory if reply is yes.
    try:
        if confirm_view.button_response == "yes":
            #Complete transaction
            await addItemToInventory(recipient_inventory_row_index, item_identifier, givequant, curses)
            await writeInvetorySheet(GlobalVars.inventoryData)
            await message.channel.send(embed=discord.Embed(title="Success!",description=f"Added {givequant}x {item_name} to {recipient_name}'s inventory", colour = embcol))
        else:
            await message.channel.send(embed=discord.Embed(title="GiveItem process cancelled!", colour = embcol))
            return
    except TypeError:
        await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="Reply must be yes or no (or y / n)", colour = embcol))
        return

#Allows a staff member to gift dezzies to everyone
async def giftAll(message):
    #Find quantity of dezzies to add to everyone's balance
    amount = message.content.split(" ")[-1]
    async with economy_lock:
        #Add to each balance
        i = 5
        while i < len(GlobalVars.economyData):
            await addDezziesToPlayer(message, int(amount), playerID=GlobalVars.economyData[i][1], write_econ_sheet=False, send_message=False)
            i += 4
        print(f"Someone gifted {amount} dezzies to everyone")
        #Write sheet
        await writeEconSheet(GlobalVars.economyData)
    await message.channel.send(embed=discord.Embed(title="You gifted dezzies to all players!",description=f"You gifted {amount}{dezzieemj} to everyone!", colour = embcol))

#Guides a player through giving money to another player
async def giveMoney(message):
    amount = message.content.split(" ")[-1]
    recipient_name, recipient_id = await getUserNamestr(message)
    author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])
    await addDezziesToPlayer(message, int(amount), playerID=recipient_id, write_econ_sheet=True, send_message=False)
    await removeDezziesFromPlayerWithoutMessage(amount, message.author.id)
    await message.channel.send(embed=discord.Embed(title=f"{message.author.name} has given {amount}{dezzieemj} to {recipient_name}!", description=f"{message.author.name} now has {GlobalVars.economyData[author_row_index+1][1]}{dezzieemj}\n\n{recipient_name} now has {GlobalVars.economyData[recipient_row_index+1][1]}{dezzieemj}"))
    if int(amount) > 15000:
        await client.get_channel(918257057428279326).send(embed=discord.Embed(title = message.author.name + f" gave {amount} Dezzies to " + recipient_name, url=message.jump_url))

#Guides a staff member through adding money to a players balance
async def addMoney(message):
    amount = message.content.split(" ")[-1]
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])
    await addDezziesToPlayer(message, int(amount), playerID=recipient_id, write_econ_sheet=True, send_message=True)

#Guides staff member through removing money from a players balance
async def removeMoney(message):
    amount = message.content.split(" ")[-1]
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])
    await removeDezziesFromPlayerWithoutMessage(int(amount), recipient_id)
    new_balance = GlobalVars.economyData[recipient_row_index+1][1]
    await message.channel.send(embed=discord.Embed(title=f"Removed {amount}{dezzieemj} from {GlobalVars.economyData[recipient_row_index][0]}'s balance!", description=f"Their new balance is {new_balance}{dezzieemj}.", colour = embcol))

#Allows user to use item.
async def useitem(message):
    #Find person in the inventory sheet
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if message.author.name in x][0])
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]

    #Get list of all items
    i, item_list = await showInventoryAndChooseItem(message, author_row_index, "\n\nTo select an item to use, enter the according number. This message will time out in 30 seconds.")
    if i == False and i != 0:
        return
    #Show chosen item
    if i >= 0:
        #Provide information about the item and it's curses.
        item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_list[i] in x][0]
        curses = []
        try:
            curse_descriptors = player_inventory[2][i + 2] #+2 becasue the first two entries are player info
            curse_descriptors = curse_descriptors.split(",")
            if curse_descriptors[0] != "": #Check if curse descriptors are empty (= no curses on the item). For some reason this doesn't work in the for loop.
                for curse in curse_descriptors:
                    curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
                    curses.append(curse_info)
        except IndexError: #This happens when a trailing item in the inventory has no curse. Just ignore it.
            pass
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
        if curses != []:
            embed_string += "\n\n**__Additional curses:__**\n"
            for curse in curses:
                embed_string += f"\n**{curse[0][0]}**(Level {curse[0][1]} curse):\n{curse[0][2]}\n"

        item_embed = discord.Embed(title=f"Do you want to use {item_name}?", description=embed_string, colour=embcol)
        confirm_view = Yes_No_View()
        await message.channel.send(embed = item_embed, view = confirm_view)

        #Wait for response
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return

        if confirm_view.button_response == "yes":
            use_response = item_database_info[10]
            if use_response == "":
                await message.channel.send(embed=discord.Embed(title="Nothing happened",description="This item is not a consumable. It cannot be used in this way.", colour = embcol))
                return
            else:
                user = message.author
                await message.channel.send(embed=discord.Embed(title=f"You used 1x {item_name}",description=use_response.replace("{user.mention}", message.author.name), colour = embcol))
                if item_list[i] == "CharSlot00":
                    author_econ_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if message.author.name in x][0])
                    GlobalVars.economyData[author_econ_row_index+2][1] = GlobalVars.economyData[author_econ_row_index+2][1] + 1
                await removeItemFromInventory(author_row_index, i+2, 1)

                #TODO: Special treatment for stuff like character slot additions.


    

#Shows the user their dezzie balance
async def money(message):
    author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    balance = GlobalVars.economyData[author_row_index+1][1]
    leaderboard_list = []
    i = 5
    while i < len(GlobalVars.economyData):
        leaderboard_list.append([GlobalVars.economyData[i][0], GlobalVars.economyData[i+1][1]])
        i += 4
    sorted(leaderboard_list,key=lambda l:l[1], reverse=True)
    user_leaderboard_rank = leaderboard_list.index([a for a in leaderboard_list if message.author.name == a[0]][0])
    await message.channel.send(embed=discord.Embed(title=f"{message.author.name} has {balance}{dezzieemj}", description=f"Leaderboard Rank: {user_leaderboard_rank + 1}", colour = embcol))

#Shows the leaderboard of the top 20 richest persons
async def leaderboard(message):
    leaderboard_list = []
    i = 5
    while i < len(GlobalVars.economyData):
        leaderboard_list.append([GlobalVars.economyData[i][0], GlobalVars.economyData[i+1][1]])
        i += 4
    sorted(leaderboard_list,key=lambda l:l[1], reverse=True)
    leaderboard_list = leaderboard_list[0:20]
    embedstring = "The 20 people with the most dezzies in the dungeon are:\n\n"
    i = 1
    for entry in leaderboard_list:
        embedstring += f"`{i:}` **{entry[0]}**\n{entry[1]}{dezzieemj}\n\n"
        i += 1
    await message.channel.send(embed = discord.Embed(title="Dezzie Leaderboard:", description= embedstring, color=embcol))
    
async def dezReact(reaction):
    mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

    #economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension='ROWS').execute().get("values")

    reciprow = ""
    targid = mess.author.id
    target = await client.fetch_user(targid)
    targetName = target.name

    giverow = ""
    giveid = reaction.member.id
    giver = await client.fetch_user(giveid)
    givename = giver.name

    #Find recipients row in the economy sheet
    try:
        for a in range(math.floor(len(GlobalVars.economyData)/4)):
            b = a * 4 + 5

            if str(targetName) == str(GlobalVars.economyData[b][0]):
                reciprow = b
                break

    except IndexError:
        if not mess.author.bot:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))
    
    #Find giver row in the economy sheet
    try:
        for a in range(math.floor(len(GlobalVars.economyData)/4)):
            b = a * 4 + 5

            if str(givename) == str(GlobalVars.economyData[b][0]):
                giverow = b
                break
    except IndexError:
        if not mess.author.bot:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(givename) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))


    #Determine gift amount - Values in CommonDefinitions.py
    if reaction.emoji.name == "dz":
        giveamount = GlobalVars.config["economy"]["reactdz"]

    elif reaction.emoji.name == "cashmoney":
        giveamount = GlobalVars.config["economy"]["reactcashmoney"]

    elif reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart":
        giveamount = GlobalVars.config["economy"]["reactmakeitrain"]

    else:
        giveamount = random.randint(100,500)


    #Retrieve users current react dezzie pool
    try:
        prevDezziePool = int(GlobalVars.economyData[giverow+3][0])

    except IndexError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]

    except ValueError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]

    except TypeError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]


    #Check if given amount is smaller than the pool of dezzies left for the user
    if reaction.channel_id != 828545311898468352: #Disable Noticeboard Reacts

        if reaction.member.name == targetName:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = "No.", description = targetName + ", you can't just award dezzies to yourself.", colour = embcol))
            await client.get_channel(918257057428279326).send(targetName + " tried to award dezzies to themself.")

        else:
            #Enough dezzies left in users dezzie pool:
            if giveamount <= prevDezziePool:
                try:
                    #Update the dezzie balance of the recipient
                    GlobalVars.economyData[int(reciprow)+1][1] = int(GlobalVars.economyData[int(reciprow)+1][1]) + int(giveamount)
                except ValueError:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " seems to not be in the economy", description = targetName + "This should not be the case. Please talk one of the @bot gods as there is most likely something wrong with your entry in our data.", colour = embcol, url = mess.jump_url))
                    return

                #Update the dezzie pool of the giver
                newDezziePool = prevDezziePool - giveamount
                GlobalVars.economyData[giverow+3][0] = int(GlobalVars.economyData[giverow+3][0])- giveamount
                await writeEconSheet(GlobalVars.economyData)
                #Add transaction
                TransactionsDatabaseInterface.addTransaction(target.name, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                

                if newDezziePool == 0:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(GlobalVars.economyData[reciprow+1][1]) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                else:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(GlobalVars.economyData[reciprow+1][1]) + dezzieemj + "\n\n" + givename + " has " + str(GlobalVars.economyData[giverow+3][0]) + dezzieemj + " in their dezzie award pool left for the week!", colour = embcol, url = mess.jump_url))

                await client.get_channel(918257057428279326).send(embed=discord.Embed(title = givename + " awarded Dezzies to " + targetName, url=mess.jump_url))

            #User has less dezzies in their pool than they reacted with
            elif prevDezziePool > 0:
                newDezziePool = 0
                giveamount = prevDezziePool
                GlobalVars.economyData[giverow+3][0] = newDezziePool
                GlobalVars.economyData[reciprow+1][1] = int(GlobalVars.economyData[reciprow+1][1]) + int(giveamount)
                await writeEconSheet(GlobalVars.economyData)
                TransactionsDatabaseInterface.addTransaction(target.name, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))
                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(GlobalVars.economyData[reciprow+1][1]) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))
                await client.get_channel(918257057428279326).send(embed=discord.Embed(title = givename + " awarded Dezzies to " + targetName, url=mess.jump_url))

            #User dezzie pool is empty:
            else:
                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + "'s dezzie award pool for the week is empty!" , description = "You will receive a fresh pool of dezzies to award to others at the start of next week!", colour = embcol, url = mess.jump_url))

    else:
        await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = "You can't award dezzies in this channel.", colour = embcol, url = mess.jump_url))

async def rpDezReact(reaction):
    mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
    #Get unique tupper img id
    tup_image_url = mess.author.display_avatar

    #Check if tupper img id in database, if not, check if name + player id combination is. If name + playerid is, update image.
    try:
        playerID, imgURL, charName = await TupperDatabase.lookup(tup_image_url, mess)
    except TypeError:
        giveid = reaction.member.id
        giver = await client.fetch_user(giveid)
        await client.get_channel(botchannel).send(embed=discord.Embed(title = str(giver.display_name) + ": The post you tried to award is too old, or was too long (< ~2000 characters) and edited.", description = "The first time a character is awarded dezzies, the post has to be rather new and can't be a long, edited post! Try awarding a different, unedited post of that character. If the issue persists, contact the bot gods.", colour = embcol, url = mess.jump_url))
        return

    #economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension='ROWS').execute().get("values")

    reciprow = ""
    targid = playerID
    target = await client.fetch_user(targid)
    targetName = target.name

    giverow = ""
    giveid = reaction.member.id
    giver = await client.fetch_user(giveid)
    givename = giver.name

    #Find recipients row in the economy sheet
    try:
        reciprow = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(targid) in x][0])
    except IndexError:
        if not mess.author.bot:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))
    
    #Find giver row in the economy sheet
    try:
        giverow = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(giveid) in x][0])
    except IndexError:
        if not mess.author.bot:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = str(givename) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))


    #Determine gift amount - Values in CommonDefinitions.py
    if reaction.emoji.name == "dz":
        giveamount = GlobalVars.config["economy"]["reactdz"]

    elif reaction.emoji.name == "cashmoney":
        giveamount = GlobalVars.config["economy"]["reactcashmoney"]

    elif reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart":
        giveamount = GlobalVars.config["economy"]["reactmakeitrain"]

    else:
        giveamount = random.randint(100,500)


    #Retrieve users current react dezzie pool
    try:
        prevDezziePool = int(GlobalVars.economyData[giverow+3][0])

    except IndexError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]

    except ValueError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]

    except TypeError:
        prevDezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]


    #Check if given amount is smaller than the pool of dezzies left for the user
    if reaction.channel_id != 828545311898468352: #Disable Noticeboard Reacts

        if reaction.member.name == targetName:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = "No.", description = targetName + ", you can't just award dezzzies to yourself.", colour = embcol))
            await client.get_channel(918257057428279326).send(targetName + " tried to award dezzies to themself.")

        else:
            #Enough dezzies left in users dezzie pool:
            if giveamount <= prevDezziePool:
                
                reward = int(giveamount * GlobalVars.config["economy"]["rpreactmodifier"])
                GlobalVars.economyData[int(reciprow)+1][1] = int(GlobalVars.economyData[int(reciprow)+1][1]) + reward
                GlobalVars.economyData[int(giverow)+3][0] = int(GlobalVars.economyData[int(giverow)+3][0]) - giveamount
                await writeEconSheet(GlobalVars.economyData)
                TransactionsDatabaseInterface.addTransaction(target.name, TransactionsDatabaseInterface.DezzieMovingAction.React, int(reward))
                
                if GlobalVars.economyData[int(giverow)+3][0] == 0:
                    await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(GlobalVars.economyData[int(reciprow)+1][1]) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                else:
                    await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(GlobalVars.economyData[int(reciprow)+1][1]) + dezzieemj + "\n\n" + givename + " has " + str(GlobalVars.economyData[int(giverow)+3][0]) + dezzieemj + " in their dezzie award pool left for the week! (RP Rewards award 25% more while costing the same!)", colour = embcol, url = mess.jump_url))

                await client.get_channel(918257057428279326).send(embed=discord.Embed(title = givename + " awarded Dezzies to " + targetName, url=mess.jump_url))

            #User has less dezzies in their pool than they reacted with
            elif prevDezziePool > 0:
                reward = prevDezziePool * int( GlobalVars.config["economy"]["rpreactmodifier"])
                GlobalVars.economyData[int(reciprow)+1][1] = int(GlobalVars.economyData[reciprow+1][1]) + int(reward)
                GlobalVars.economyData[int(giverow)+3][0] = 0
                await writeEconSheet(GlobalVars.economyData)

                TransactionsDatabaseInterface.addTransaction(target.name, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(GlobalVars.economyData[int(reciprow)+1][1]) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))
                await client.get_channel(918257057428279326).send(embed=discord.Embed(title = givename + " awarded Dezzies to " + targetName, url=mess.jump_url))

            #User dezzie pool is empty:
            else:
                await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + "'s dezzie award pool for the week is empty!" , description = "You will receive a fresh pool of dezzies to award to others at the start of next week!", colour = embcol, url = mess.jump_url))

    else:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = "You can't use this at the here.", colour = embcol, url = mess.jump_url))



#TODO: Rewrite the item function (Fuzzy String matching)
#TODO: Rewrite the Shop function (Fuzzy String matching)
#TODO: Add leaderboard rank to money function

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
        newEconData.append([GlobalVars.economyData[i][0]]) #Name
        
        try: #If they have never RP-messaged, special treatment
            newEconData.append([GlobalVars.economyData[i + 1][0]]) #LastMessageRewardTime
        except IndexError:
            newEconData.append([""])
        newEconData[i+1].append(GlobalVars.economyData[i][1]) #Dezzies
        try: #If they have no scenes list, special treatment
            newEconData.append([GlobalVars.economyData[i + 2][0]]) #Scenes List
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
            newEconData[i].append(user_id)
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
    async with economy_lock:
        GlobalVars.economyData = sheet.values().get(spreadsheetId = inventorysheet, range = "A1:ZZ8000", majorDimension='ROWS').execute().get("values")
    GlobalVars.inventoryData = await loadInventorySheet()

    return
#Writes to the economy sheet. Optional argument "range" used for instances where we only want to write a few or a single cell of the sheet instead of all cells.
async def writeEconSheet(values, range = "A1:ZZ8000"):
    #in case we write a single value
    async with economy_lock:
        if not (":" in range):
            values = [[values]]
        sheet.values().update(spreadsheetId = inventorysheet, range = range, valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values= values)).execute()

#Loads the current Inventory Sheet state. This is not kept internally, so we need to call this every time we work on the sheet.
async def loadInventorySheet():
    async with economy_lock:
        GlobalVars.inventoryData = sheet.values().get(spreadsheetId = inventorysheet, range = "Inventories!A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")

#Writes values to the Inventory sheet. Optional argument "range" used for instances where we only want to write a few or a single cell of the sheet instead of all cells.
async def writeInvetorySheet(values, range = "A1:ZZ8000"):
    async with economy_lock:
        #in case we write a single value
        if not (":" in range):
            values = [[values]]
        sheet.values().update(spreadsheetId = inventorysheet, range = "Inventories!" + range, valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values= values)).execute()

async def loadItemSheet():
    itemsheet = gc.open_by_key("17M2FS5iWchszIoimqNzk6lzJMOVLBWQgEZZKUPQuMR8") #New for economy rewrite
    itemlists = itemsheet.worksheets()
    for a in range(len(itemlists)):
            GlobalVars.itemdatabase.append(itemlists[a].get_all_values())

async def writeItemsheetCell(shopnumber, row, column, values):
    async with economy_lock:
        itemsheet.worksheets()[shopnumber].update_cell(row + 1, column + 1, values)



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
    for entry in GlobalVars.itemdatabase[0][1:]:
        #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
        levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance_complete = fuzz.ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
        levenshtein_tuple_list.append([entry[0], levenshtein_distance, entry[11]])
    sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
    return sorted_list[:top_n_results]

async def removeDezziesFromPlayerWithoutMessage( amount, playerID = None, playerName = None):

    if playerID != None:
        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(playerID) in x][0])
    elif playerName != None:
        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if playerName in x][0])
    else:
        await message.channel.send(embed = discord.Embed(title="Player to remove dezzies from not found."))
        return False

    if int(GlobalVars.economyData[author_row_index][1]) > int(amount):
        #Remove the money from the player
        GlobalVars.economyData[author_row_index+1][1] = int(GlobalVars.economyData[author_row_index+1][1]) - int(amount)

        #Write to sheet
        await writeEconSheet(GlobalVars.economyData)

        return True
    return False


async def addDezziesToPlayer(message, amount, playerID=None, playerName=None, write_econ_sheet=True, send_message=True):
    async with add_dezzie_lock: #THIS LOCK COULD LEAD TO INSANE GOTHY LAG IF OOC MESSAGES TRIGGER THIS.
        if playerID != None:
            author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(playerID) in x][0])
        elif playerName != None:
            author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if playerName in x][0])
        else:
            await message.channel.send(embed = discord.Embed(title="Player to give dezzies to not found."))
            return
        old_balance = int(GlobalVars.economyData[author_row_index+1][1])
        new_balance = old_balance + amount

        GlobalVars.economyData[author_row_index+1][1] = new_balance
        #Write to sheet
        if write_econ_sheet == True:
            await writeEconSheet(GlobalVars.economyData)
        if send_message == True:
            await message.channel.send(embed=discord.Embed(title=f"Added {amount}{dezzieemj} to {GlobalVars.economyData[author_row_index][0]}'s balance!", description=f"Before this transaction you had {old_balance}{dezzieemj}, now you have {new_balance}{dezzieemj}. Don't spend it all in one place!", colour = embcol))
        return True

async def addItemToPlayerWithCurseFromShop(message, playerID, itemID, amount, shop_number):

    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(playerID) in x][0])

    already_in_inventory = False

    #Roll curses on the item
    item_database_info = [x for x in GlobalVars.itemdatabase[shop_number] if itemID in x][0]
    curses_identifier = item_database_info[14].split(",")
    curses = ""
    rolled_curses = []
    i = 0
    if curses_identifier[0] != "":
        for curse in curses_identifier:
            if random.randint(1,2) == 2: #50% chance for every curse to occur
                rolled_curses.append(i)
                if curses == "":
                    curses += curse
                else: curses += f",{curse}"
            i = i+1
    #Check if item is already in the player's inventory
    if itemID in GlobalVars.inventoryData[author_row_index]:
        #Check if rolled curses align with curses already present on an instance of the item in the inventory
        item_inv_index = GlobalVars.inventoryData[author_row_index].index(itemID)
        item_inv_indices = [y for y, x in enumerate(GlobalVars.inventoryData[author_row_index]) if x  == itemID] #Find all occurences of the item in the player's inventory
        for item_instance in item_inv_indices:
            try:
                if curses == GlobalVars.inventoryData[author_row_index+2][item_instance]:
                    GlobalVars.inventoryData[author_row_index+1][item_instance] = int(GlobalVars.inventoryData[author_row_index+1][item_instance]) + amount
                    already_in_inventory = True
                    await writeInvetorySheet(GlobalVars.inventoryData)
                    await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your already present items!", description="You already owned that exact item, so we just added the requested quantity.", colour = embcol))
                    return rolled_curses
            except IndexError: #This happens when a trailing item has no curse.
                if curses == "":
                    GlobalVars.inventoryData[author_row_index+1][item_instance] = int(GlobalVars.inventoryData[author_row_index+1][item_instance]) + amount
                    already_in_inventory = True
                    await writeInvetorySheet(GlobalVars.inventoryData)
                    await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your already present items!", description="You already owned that exact item, so we just added the requested quantity.", colour = embcol))
                    return rolled_curses
                else: 
                    pass
        if already_in_inventory == False: #If curses do not match on any instance
            GlobalVars.inventoryData[author_row_index].append(itemID)
            while len(GlobalVars.inventoryData) < author_row_index + 3:    #Enlarge the inventory sheet if the last person on it is trying to buy an item, and their additional cells arent on it yet
                GlobalVars.inventoryData.append(["",""])
            GlobalVars.inventoryData[author_row_index+1].append(amount)
            while len(GlobalVars.inventoryData[author_row_index+2]) < len(GlobalVars.inventoryData[author_row_index]) - 1:
                GlobalVars.inventoryData[author_row_index+2].append("")
            GlobalVars.inventoryData[author_row_index+2].append(curses)
            await writeInvetorySheet(GlobalVars.inventoryData)
            await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your inventory!", description="Seems to be your first one. Go and have fun with it!", colour = embcol))
            return rolled_curses


    else: #If Item is new in the inventory
        GlobalVars.inventoryData[author_row_index].append(itemID)
        GlobalVars.inventoryData[author_row_index+1].append(amount)
        while len(GlobalVars.inventoryData[author_row_index+2]) < len(GlobalVars.inventoryData[author_row_index]) - 1:
                GlobalVars.inventoryData[author_row_index+2].append("")
        GlobalVars.inventoryData[author_row_index+2].append(curses)
        await writeInvetorySheet(GlobalVars.inventoryData)
        await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your inventory!", description="Seems to be your first one. Go and have fun with it!", colour = embcol))
        return rolled_curses


async def addItemToInventory(recipient_inventory_row_index, item_identifier, quantity, curses):

    #Add item to recipient inventory
    try:
        item_match = -1
        if item_identifier in GlobalVars.inventoryData[recipient_inventory_row_index]: #if the recipient has the *exact* item in their inv already:
            for j in range(0, len(GlobalVars.inventoryData[recipient_inventory_row_index])):
                try:
                    recipient_curses = GlobalVars.inventoryData[recipient_inventory_row_index+2][j]
                except IndexError:
                    recipient_curses = ""
                if GlobalVars.inventoryData[recipient_inventory_row_index][j] == item_identifier and recipient_curses == curses:
                    item_match = j
        if item_match != -1:
                #Add +amount to the item quantity.
            GlobalVars.inventoryData[recipient_inventory_row_index + 1][item_match] = int(GlobalVars.inventoryData[recipient_inventory_row_index + 1][item_match]) + quantity
        else: 
            GlobalVars.inventoryData[recipient_inventory_row_index].append(item_identifier)
            while len(GlobalVars.inventoryData) < recipient_inventory_row_index + 3:    #Enlarge the inventory sheet if the last person on it is trying to buy an item, and their additional cells arent on it yet
                GlobalVars.inventoryData.append(["", ""])
            #Make sure we hit the correct column
            while len(GlobalVars.inventoryData[recipient_inventory_row_index + 1]) < len(GlobalVars.inventoryData[recipient_inventory_row_index]) - 1:
                GlobalVars.inventoryData[recipient_inventory_row_index + 1].append("")
            GlobalVars.inventoryData[recipient_inventory_row_index+1].append(quantity)
            while len(GlobalVars.inventoryData[recipient_inventory_row_index+2]) < len(GlobalVars.inventoryData[recipient_inventory_row_index]) - 1:
                GlobalVars.inventoryData[recipient_inventory_row_index+2].append("")
            try:
                GlobalVars.inventoryData[recipient_inventory_row_index+2].append(curses)
            except IndexError:
                pass
    except: 
        return False
    return True

async def removeItemFromInventory(inventory_row_index, item_inventory_index, quantity):
    deleted = False
    #Remove items from inventory
    if quantity < int(GlobalVars.inventoryData[inventory_row_index+1][item_inventory_index]):
        GlobalVars.inventoryData[inventory_row_index+1][item_inventory_index] = int(GlobalVars.inventoryData[inventory_row_index+1][item_inventory_index]) - quantity
    else:
        del GlobalVars.inventoryData[inventory_row_index][item_inventory_index]
        GlobalVars.inventoryData[inventory_row_index].append("")
        del GlobalVars.inventoryData[inventory_row_index+1][item_inventory_index]
        GlobalVars.inventoryData[inventory_row_index+1].append("")
        deleted = True
        try:
            del GlobalVars.inventoryData[inventory_row_index+2][item_inventory_index]
            GlobalVars.inventoryData[inventory_row_index+2].append("")
        except IndexError: #If we get an index error, that cell wasn't occupied anyways and was a trailing cell.
            pass
        
    await writeInvetorySheet(GlobalVars.inventoryData)
    if deleted == True: #Clean up the internal inventory representation from trailing spaces
        del GlobalVars.inventoryData[inventory_row_index][-1]
        del GlobalVars.inventoryData[inventory_row_index+1][-1]
        try:
            del GlobalVars.inventoryData[inventory_row_index+2][-1]
        except IndexError: #If we get an index error, that cell wasn't occupied anyways and was a trailing cell.
            pass
    pass
    return True

'''
Function that prints the inventory, and waits for a selection. Embed_bottom_note is a string that is shown at the 
very bottom of the last inventory embed to tell the user what the selection is for
'''
async def showInventoryAndChooseItem(message, author_row_index, embed_bottom_note):
    #Get list of all items
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]
    item_list = []  #collect a list of the descriptors in order here.
    embed_string = [""]
    y = 0
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
        try:
            if player_inventory[2][i] != "": #If the item has curses
                curses = player_inventory[2][i].split(",")

                #Generate the list of curses the item has.
                for curse in curses:
                    curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
                    if curse_names == "": #Construct the string in a way that it doesn't have trailing commas and spaces.
                        curse_names += f"{curse_info[0][0]}"
                    else: curse_names += f", {curse_info[0][0]}"
        except IndexError: #This happens when a trailing item in the inventory has no curse. Just ignore it.
            pass
        if curse_names == "":
            add_string = f"`{i-1}`: {quantity}x `{item_name}`: {item_short_description}\n\n"
        else: 
            add_string = f"`{i-1}`: {quantity}x `{item_name}`: {item_short_description}\n__Curses__: {curse_names}\n\n"

        if len(embed_string[y]) + len(add_string) > 4096:
            embed_string.append(add_string)
            y += 1
        else:
            embed_string[y] += add_string

    #Print list of items
    if len(embed_string) == 1:
        embed_string[0] += embed_bottom_note

    inventory_embed = discord.Embed(title = f"{player_inventory[0][0]}'s inventory", description= embed_string[0], colour = embcol)
    await message.channel.send(embed = inventory_embed)
    if len(embed_string) > 1:
        for i in range(1, len(embed_string)):
                if i == len(embed_string) - 1:
                    inventory_embed = discord.Embed(title = f"{player_inventory[0][0]}'s inventory", description= embed_string[i] + embed_bottom_note, colour = embcol)
                else:
                    inventory_embed = discord.Embed(title = f"{player_inventory[0][0]}'s inventory", description= embed_string[i], colour = embcol)

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
            return False, None
    except asyncio.TimeoutError:
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        await message.delete()
        return False, None
    return i, item_list

async def getUserNamestr(message):
    if "@" in message.content:
        try:
            targid = int(str(message.content.split("@")[1]).split(" ")[0].replace("!","").replace("&","").replace(">","").split(" ")[0])
        except ValueError:
            await message.channel.send(embed = discord.Embed(title = "Error!", description = "Make sure that the user you tagged is valid."))
            return
        targname = await client.fetch_user(targid)
    else:

        targname = message.author

    namestr = str(targname.name)

    return namestr, targid



#----------------------------------Views---------------------------------
class AddItem_Curse_View(discord.ui.View):
    def __init__(self, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
    async def on_timeout(self):
        # This method is called when the view times out (if a timeout is set)
        pass

    @discord.ui.button(label="Yes, Random (50% per curse from above)", style = discord.ButtonStyle.green, custom_id="yes")
    async def button1_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "yes"
        self.stop()

    @discord.ui.button(label="No", style = discord.ButtonStyle.green, custom_id="no")
    async def button2_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "no"
        self.stop()

    @discord.ui.button(label="From Potential Curses", style = discord.ButtonStyle.green, custom_id="shopcurses")
    async def button3_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "shopcurses"
        self.stop()

    @discord.ui.button(label="Custom From All Curses", style = discord.ButtonStyle.green, custom_id="custom")
    async def button4_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "custom"
        self.stop()

    @discord.ui.button(label="Cancel", style = discord.ButtonStyle.red, custom_id="cancel")
    async def button5_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "cancel"
        self.stop()

class AddItem_Curse_View_No_Shopcurses(discord.ui.View):
    def __init__(self, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
    async def on_timeout(self):
        # This method is called when the view times out (if a timeout is set)
        pass

    @discord.ui.button(label="No", style = discord.ButtonStyle.green, custom_id="no")
    async def button2_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "no"
        self.stop()

    @discord.ui.button(label="Custom From All Curses", style = discord.ButtonStyle.green, custom_id="custom")
    async def button4_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "custom"
        self.stop()

    @discord.ui.button(label="Cancel", style = discord.ButtonStyle.red, custom_id="cancel")
    async def button5_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "cancel"
        self.stop()


class Yes_No_View(discord.ui.View):
    def __init__(self, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
    async def on_timeout(self):
        # This method is called when the view times out (if a timeout is set)
        pass

    @discord.ui.button(label="Yes", style = discord.ButtonStyle.green, custom_id="yes")
    async def button1_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "yes"
        self.stop()

    @discord.ui.button(label="No", style = discord.ButtonStyle.red, custom_id="no")
    async def button2_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "no"
        self.stop()



class Yes_No_Quantity_View(discord.ui.View):
    def __init__(self, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
    async def on_timeout(self):
        # This method is called when the view times out (if a timeout is set)
        pass

    @discord.ui.button(label="Yes", style = discord.ButtonStyle.green, custom_id="yes")
    async def button1_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "yes"
        self.stop()

    @discord.ui.button(label="No", style = discord.ButtonStyle.red, custom_id="no")
    async def button2_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "no"
        self.stop()
    
    @discord.ui.button(label="Modify Quantity", style = discord.ButtonStyle.blurple, custom_id="modquant")
    async def button3_callback(self, interaction: discord.Interaction, item):
        await interaction.response.defer()
        self.button_response = "modifyquantity"
        self.stop()

class Dropdown_Select_View(discord.ui.View):
    def __init__(self, timeout=120, optionamount=1, maxselectionamount = 1, namelist = []):
        super().__init__(timeout=timeout)
        self.button_response = []
        self.choices = []
        self.namelist = namelist
        #Make sure we can only choose between 1 and 25 as per specification.
        if maxselectionamount > 0 and maxselectionamount < 26:
            self.selection_amount = maxselectionamount
        elif maxselectionamount > 26:
            self.selection_amount = 25
        elif maxselectionamount < 1:
            self.selection_amount = 1

        #Make sure we can't choose more than we ahve options
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
            placeholder = "None", # the placeholder text that will be displayed if nothing is selected
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