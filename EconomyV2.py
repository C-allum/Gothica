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
    searchresults = []
    try:
        fullMessage = message.content.replace("  ", " ")
        fullMessage = fullMessage.split(" ", 1)[1] #cut the %buy off
        
        searchterm = fullMessage
    except IndexError:
        searchterm = None
    
    chosenshop = -1
    if searchterm != None:  #Show only relevant shops if the searchterm was provided
        levenshtein_tuple_list = []
        shopindex = GlobalVars.config["general"]["index_of_first_shop"]
        for entry in GlobalVars.itemdatabase[GlobalVars.config["general"]["index_of_first_shop"]:GlobalVars.config["general"]["index_of_first_shop"] + GlobalVars.config["general"]["number_of_shops"]]:
            #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
            levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[0][26].lower(), searchterm.lower())
            levenshtein_distance_complete = fuzz.ratio(entry[0][26].lower(), searchterm.lower())
            levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
            levenshtein_tuple_list.append([entry[0][26], levenshtein_distance, shopindex])
            shopindex += 1
        sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
        searchresults = [x[0::2] for x in sorted_list[:5]]
    else: #If no searchterm was provided
        for a in range(len(GlobalVars.itemdatabase)):
            if a >= int(GlobalVars.config["general"]["index_of_first_shop"]):
                searchresults.append(GlobalVars.itemdatabase[a][0][26])
        for n in range(int(GlobalVars.config["general"]["number_of_shops"])):
            searchresults[n] = [searchresults[n], n + GlobalVars.config["general"]["index_of_first_shop"]]
    shop_selection_view = Dropdown_Select_View(message = message, timeout=30, optionamount=len(searchresults), maxselectionamount=1) #Only let them choose one item.
    
    shopsel = []
    for c in range(len(searchresults)):
        shopsel.append("`" + str(c+1) + "` - " + searchresults[c][0])
    emb = discord.Embed(title = "Which shop would you like to browse?", description = "Select the number of the one you want:\n" + "\n".join(shopsel), colour = embcol)
    emb.set_footer(text = "This message will timeout in 30 seconds")
    await message.channel.send(embed = emb, view=shop_selection_view)

    #Wait for reply
    if await shop_selection_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    i = searchresults[int(shop_selection_view.button_response[0])-1][1]

    try:
        shopitems.append(str(GlobalVars.itemdatabase[i][0][20]) + "\n------------------------------------------------------------\n") #Adds shop welcome message to first embed
    except IndexError:
        pass
    try:
        shopemoji = GlobalVars.itemdatabase[i][0][22]
    except IndexError:
        shopemoji = ""
    try:
        if GlobalVars.itemdatabase[i][0][24] == "":
            shopcol = embcol
        else:
            shopcol = int(GlobalVars.itemdatabase[i][0][24])
    except IndexError:
        shopcol = 0

    for b in range(len(GlobalVars.itemdatabase[i])):
        if b != 0:
            nextitem = shopemoji + " **" + str(GlobalVars.itemdatabase[i][b][1]) + "** \n  *" + str(GlobalVars.itemdatabase[i][b][13]) + "*" + dezzieemj #Gets item name and price
            if len("\n".join(shopitems)) + len(nextitem) <= 4096:
                shopitems.append(nextitem)
            else:
                await message.channel.send(embed = discord.Embed(title = shopemoji + " " + itemlists[i].title + " " + shopemoji, description = "\n".join(shopitems), colour = shopcol))
                shopitems = []
                shopitems.append(nextitem)

    await message.channel.send(embed = discord.Embed(title = shopemoji + " " + itemlists[i].title + " " + shopemoji, description = "\n".join(shopitems), colour = shopcol))
    await message.delete()
    return
    
#Summons information about an item
async def item(message):
    #Check if quantity was provided and prepare the search term
    try:
        fullMessage = message.content.replace("  ", " ")
        fullMessage = fullMessage.split(" ", 1)[1] #cut the %buy off 
        searchterm = fullMessage
    except IndexError:
        await message.channel.send(Embed = discord.Embed(title="Please provide the name of an item you want information on with your query.", color=embcol))
        return

    #Find the wanted item, if not specific, spawn a selctor
    selected_item = await selectItem(message, searchterm, 10)

    #Check if item is present in multiple shops
    available_in_shops = []
    shopnumbers = []
    try:
        for j in range(GlobalVars.config["general"]["index_of_first_shop"], GlobalVars.config["general"]["index_of_first_shop"]+GlobalVars.config["general"]["number_of_shops"]):
            for row in GlobalVars.itemdatabase[j]:
                if selected_item[2] in row:
                    available_in_shops.append(GlobalVars.itemdatabase[j])
                    shopnumbers.append(j)
    except IndexError: 
        print("Index error in item function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops")
        await message.channel.send(embed=discord.Embed(title=f"Error in item function.", description="Index error in item function: Possibly a problem with the *number_of_shops* variable in the config. Check if that matches the amount of shops", colour = embcol))
    

    #Check if we need to show multiple shops due to having multiple versions of the item in different shops (cursed and noncursed.)
    chosenShop = -1
    item_in_shop = False
    if len(available_in_shops) > 1:
        shop_embed = "The item is available in the following shops and versions:\n\n"
        for i in range(0, len(available_in_shops)):
            item_in_shop = [x for x in available_in_shops[i] if selected_item[2] in x][0]
            try:
                if item_in_shop[22] != "":
                    shopemoji = item_in_shop[22]
                else:
                    shopemoji = available_in_shops[i][0][22]
            except IndexError:
                shopemoji = available_in_shops[i][0][22]

            item_name = shopemoji + " " + item_in_shop[1] + " " + shopemoji
            price = int(int(item_in_shop[3]) * float(item_in_shop[12]))
            quantity_available = item_in_shop[18]
            curses_identifier = item_in_shop[14].split(",")
            
            if len(curses_identifier) > 0 and curses_identifier[0] != "":
                n = 0
                curses = ""
                for curse in curses_identifier:
                    try:
                        curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                    except IndexError:
                        await message.channel.send(embed=discord.Embed(title=f"Error in Item function.", description="Index error in item function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
 
                    if n == 0:
                        curses+= f"{curse[0]}"
                        n +=1
                    else:
                        curses+= f",{curse[0]}"

                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\nPotential Curses: {curses}\n\n"
            else: 
                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\n\n"
        

        #Generate selector view to choose items.
        shop_selection_view = Dropdown_Select_View(message = message, timeout=30, optionamount=len(shopnumbers), maxselectionamount=1) #Only let them choose one item.
        await message.channel.send(embed=discord.Embed(title=f"There are multiple versions of this item. Which do you want to look at?", description=shop_embed, colour = embcol), view = shop_selection_view)
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
            item_type = item_database_info[1]
            item_identifier = item_database_info[11]
            price = int(item_database_info[2])
            quantity_available = ""
            curses_identifier = [""]  
            rarity = item_database_info[4]
            attunement_requirement = item_database_info[3]
            mechanics = item_database_info[5]
            flavour = item_database_info[6]
            default_curse = item_database_info[8]
            additional_reference = ""

    #Collect information about the item to be bought. Only do so if the item is in a shop.
    if item_in_shop == True:
        item_database_info = [x for x in GlobalVars.itemdatabase[chosenShop] if selected_item[2] in x][0]
        try:
            if item_database_info[22] != "":
                shopemoji = item_database_info[22]
            else:
                shopemoji = GlobalVars.itemdatabase[chosenShop][0][22]
        except IndexError:
            shopemoji = GlobalVars.itemdatabase[chosenShop][0][22]

        item_name = shopemoji + " " + item_database_info[1] + " " + shopemoji
        item_type = item_database_info[2]
        item_identifier = item_database_info[0]
        price = int(int(item_database_info[3]) * float(item_database_info[12]))
        quantity_available = item_database_info[18]
        curses_identifier = item_database_info[14].split(",")
        rarity = item_database_info[5]
        attunement_requirement = item_database_info[4]
        mechanics = item_database_info[7]
        flavour = item_database_info[6]
        default_curse = item_database_info[9]
        try:
            additional_reference = item_database_info[17]
        except IndexError:
            additional_reference = ""

    embed_string, potential_curses, potential_curses_string, potential_curse_names, curse_count = await showItem(item_name, item_type, price, quantity_available, curses_identifier, rarity, attunement_requirement, mechanics, flavour, default_curse, additional_reference, show_quant_and_price=False)

    await message.channel.send(embed=discord.Embed(title=f"**{item_name}**", description=embed_string.replace("**"+item_name+"**\n\n", "") + potential_curses_string, colour = embcol))
    return

#Summons the player's inventory
async def inventory(message):
    #Find person in the inventory sheet
    test = [x for x in GlobalVars.inventoryData if str(message.author.id) in x]
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(message.author.id) in x][0])
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]

    #Get list of all items
    i, item_list = await showInventoryAndChooseItem(message, author_row_index, "\n\nFor more information about an item and its curses, enter the according number. This message will time out in 30 seconds.")
    if i == -1:
        return
    if i >= 0:
        #Provide information about the item and it's curses.
        try:
            item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_list[i] in x][0]
        except TypeError:
            print(f"Error with item: {item_list[i]}")
        curses = []
        try:
            curse_descriptors = player_inventory[2][i + 2] #+2 becasue the first two entries are player info
            curse_descriptors = curse_descriptors.split(",")
            if curse_descriptors[0] != "": #Check if curse descriptors are empty (= no curses on the item). For some reason this doesn't work in the for loop.
                for curse in curse_descriptors:
                    curse = curse.replace("[", "").replace("]", "") 
                    curse_info = [x for x in GlobalVars.itemdatabase[1] if curse in x]
                    curses.append(curse_info)
        except IndexError: #This happens when a trailing item in the inventory has no curse. Just ignore it.
            pass
        

        item_name = item_database_info[0]
        item_type = item_database_info[1]
        item_identifier = item_database_info[11]
        price = int(item_database_info[2])
        quantity_available = ""
        curses_identifier = [""]  
        rarity = item_database_info[4]
        attunement_requirement = item_database_info[3]
        mechanics = item_database_info[5]
        flavour = item_database_info[6]
        default_curse = item_database_info[8]
        additional_reference = ""


        embed_string, unused, potential_curses, potential_curse_names, curseCount = await showItem(item_name, item_type, price, quantity_available, curses_identifier, rarity, attunement_requirement, mechanics, flavour, default_curse, additional_reference, show_quant_and_price=False)

        #add additional curses
        if curses != []:
            embed_string += "\n\n**__Additional curses:__**\n"
            for curse in curses:
                embed_string += f"\n**{curse[0][0]}** (Level {curse[0][1]} curse):\n{curse[0][2]}\n"

        item_embed = discord.Embed(title=f"Item Info for {item_name}", description=embed_string, colour=embcol)
        await message.channel.send(embed = item_embed)
        return

#Guides the user through buying an item
async def buyitem(message):
    

    #Check if quantity was provided and prepare the search term
    buyquant = 1
    try:
        fullMessage = message.content.replace("  ", " ")
        fullMessage = fullMessage.split(" ", 1)[1] #cut the %buy off
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
    selected_item = await selectItem(message, searchterm, 10)

    #Check if item is present in multiple shops
    available_in_shops = []
    shopnumbers = []
    try:
        for j in range(GlobalVars.config["general"]["index_of_first_shop"], GlobalVars.config["general"]["index_of_first_shop"]+GlobalVars.config["general"]["number_of_shops"]):
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
            try:
                if item_in_shop[22] != "":
                    shopemoji = item_in_shop[22]
                else:
                    shopemoji = available_in_shops[i][0][22]
            except IndexError:
                shopemoji = available_in_shops[i][0][22]
            item_name = shopemoji + " " + item_in_shop[1] + " " + shopemoji
            price = int(int(item_in_shop[3]) * float(item_in_shop[12]))
            quantity_available = item_in_shop[18]
            curses_identifier = item_in_shop[14].split(",")
            
            if len(curses_identifier) > 0 and curses_identifier[0] != "":
                

                n = 0
                curses = ""
                for curse in curses_identifier:
                    
                    try:
                        curse = [x for x in GlobalVars.itemdatabase[1] if curse.replace("[", "").replace("]", "") in x][0]
                    except IndexError:
                        await message.channel.send(embed=discord.Embed(title=f"Error in Buy function.", description="Index error in buy function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
 
                    
                    if n == 0:
                        curses+= f"{curse[0]}"
                        n +=1
                    else:
                        curses+= f",{curse[0]}"

                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\nPotential Curses: {curses}\n\n"
            else: 
                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\n\n"
        
        #Generate selector view to choose items.
        shop_selection_view = Dropdown_Select_View(message=message, timeout=30, optionamount=len(shopnumbers), maxselectionamount=1) #Only let them choose one item.
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
            return
    
    #Collect information about the item to be bought.
    item_database_info = [x for x in GlobalVars.itemdatabase[chosenShop] if selected_item[2] in x][0]
    try:
        if item_database_info[22] != "":
            shopemoji = item_database_info[22]
        else:
            shopemoji = GlobalVars.itemdatabase[chosenShop][0][22]
    except IndexError:
        shopemoji = GlobalVars.itemdatabase[chosenShop][0][22]
    item_name = shopemoji + " " + item_database_info[1] + " " + shopemoji
    item_type = item_database_info[2]
    item_identifier = item_database_info[0]
    rarity = item_database_info[5]
    price = int(int(item_database_info[3]) * float(item_database_info[12]))
    attunement = item_database_info[4]
    flavour = item_database_info[7]
    mechanics  = item_database_info[6]
    default_curse = item_database_info[9]
    quantity_available = item_database_info[18]
    curses_identifier = item_database_info[14].split(",")
    additional_reference = item_database_info[17]

    #display Item.
    embed_string, potential_curses, potential_curses_string, potential_curse_names, curse_count = await showItem(item_name, item_type, price, quantity_available, curses_identifier, rarity, attunement, mechanics, flavour, default_curse, additional_reference)
    if quantity_available == "":
            quantity_available = "Infinite"
    if quantity_available != "Infinite":
        if buyquant > int(quantity_available):
            await message.channel.send(embed=discord.Embed(title=f"You requested {buyquant} of this item, but only {quantity_available} are available. Please try again and request a lower amount.", colour = embcol))

    #Ask for confirmation or quantity change
    confirm_view = Yes_No_Quantity_View(message=message)
    await message.channel.send(embed=discord.Embed(title=f"Buy {buyquant} of this item for a total of {price * buyquant}{dezzieemj}?", description=embed_string + potential_curses_string, colour = embcol), view=confirm_view)

    if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(message=message, optionamount=25, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to buy? __Keep in mind, all items bought in bulk will have the same random curse roll.__", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        buyquant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View(message=message)
        await message.channel.send(embed=discord.Embed(title=f"Buy {buyquant} of this item for a total of {price * buyquant}{dezzieemj}?", description=embed_string + potential_curses_string, colour = embcol), view = confirm_view)
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
                rolled_curses = await addItemToPlayerWithCurseFromShop(message, playerID, item_identifier, buyquant, chosenShop, additional_reference)
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

                TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.Buy, -price * buyquant)

            else:
                await message.channel.send(embed=discord.Embed(title="Not enough funds!",description=f"Your funds are insufficient to buy this item! You have {old_balance}{dezzieemj}, and the item(s) cost {price*buyquant}{dezzieemj}", colour = embcol))
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
    if i == -1:
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
    
    confirm_view = Yes_No_Quantity_View(message=message)
    
    await message.channel.send(embed=discord.Embed(title=f"Do you want to sell {sellquant}x {itemname} for {int(int(item_price) * GlobalVars.config['economy']['sellpricemultiplier'] * sellquant)}?"), view = confirm_view)
    
    if await confirm_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(message=message, optionamount=int(GlobalVars.inventoryData[author_inventory_row_index+1][i]), maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to sell? You own {int(GlobalVars.inventoryData[author_inventory_row_index+1][i])}.", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        sellquant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View(message=message)
        await message.channel.send(embed=discord.Embed(title=f"Do you want to sell {sellquant}x {itemname} for {int(int(item_price) * GlobalVars.config['economy']['sellpricemultiplier'] * sellquant)}?"), view = confirm_view)
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return

    if confirm_view.button_response == "yes":
        deleted = False
        #Remove items from inventory
        if await removeItemFromInventory(author_inventory_row_index, i, sellquant):
            #Add stock to the inventory of the shop
            item_row_index = GlobalVars.itemdatabase[sell_shop_index].index([x for x in GlobalVars.itemdatabase[sell_shop_index] if item_identifier in x][0])
            if GlobalVars.itemdatabase[sell_shop_index][item_row_index][18] == "":
                new_stock = ""
            else:
                new_stock = int(GlobalVars.itemdatabase[sell_shop_index][item_row_index][18]) + sellquant

            #Add dezzies
            await addDezziesToPlayer(message, int(int(item_price) * GlobalVars.config['economy']['sellpricemultiplier']) * sellquant, playerID=message.author.id, write_econ_sheet=False)

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
            
            TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.Sell, int(int(item_price) * GlobalVars.config['economy']['sellpricemultiplier']) * sellquant)

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
        fullMessage = message.content.replace("  ", " ")
        fullMessage = fullMessage.split(" ", 1)[1] #cut the %buy off
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
    if i == -1:
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
        quantity_view = Dropdown_Select_View(message=message, optionamount=item_quantity, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title="Please select an amount you want to give away of the chosen item.", color=embcol), view=quantity_view)

        if await quantity_view.wait():
                await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                return
        #Wait for user input as to which shop to choose
        givequant = int(quantity_view.button_response[0])

    #Confirmation
    confirm_view = Yes_No_View(message=message)
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
        try:
            additional_reference = GlobalVars.inventoryData[author_inventory_row_index+3][i + 2]
        except IndexError:
            additional_reference = ""
        success = await addItemToInventory(recipient_inventory_row_index, item_list[i], givequant, giver_curses, additional_reference)
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
        fullMessage = message.content.replace("  ", " ")
        fullMessage = fullMessage.split(" ", 2)[2] #cut the %additem and the recipient name off

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
    selected_item = await selectItem(message, searchterm, 10)

    #Check if item is present in multiple shops
    available_in_shops = []
    shopnumbers = []
    try:
        for j in range(GlobalVars.config['general']['index_of_first_shop'], GlobalVars.config['general']['index_of_first_shop']+GlobalVars.config['general']['number_of_shops']):
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
            try:
                if item_in_shop[22] != "":
                    shopemoji = item_in_shop[22]
                else:
                    shopemoji = available_in_shops[i][0][22]
            except IndexError:
                shopemoji = available_in_shops[i][0][22]

            item_name = shopemoji + " " + item_in_shop[1] + " " + shopemoji
            price = int(int(item_in_shop[3]) * float(item_in_shop[12]))
            quantity_available = item_in_shop[18]
            curses_identifier = item_in_shop[14].split(",")
            
            if len(curses_identifier) > 0 and curses_identifier[0] != "":
                

                n = 0
                curses = ""
                for curse in curses_identifier:
                    curse = curse.replace("[", "").replace("]","")
                    try:
                        curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                    except IndexError:
                        await message.channel.send(embed=discord.Embed(title=f"Error in Additem function.", description="Index error in additem function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
                        return
                    if n == 0:
                        curses+= f"{curse[0]}"
                        n +=1
                    else:
                        curses+= f", {curse[0]}"

                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\nPotential Curses: {curses}\n\n"
            else: 
                shop_embed += f"`{i+1}:` **{available_in_shops[i][0][22]}{available_in_shops[i][0][26]}{available_in_shops[i][0][22]}**:\n{item_name}, Price: {price}, Stock: {quantity_available}\n\n"
        

        #Generate selector view to choose items.
        shop_selection_view = Dropdown_Select_View(message=message, timeout=30, optionamount=len(shopnumbers), maxselectionamount=1) #Only let them choose one item.
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
            item_type = item_database_info[1]
            item_identifier = item_database_info[11]
            price = int(item_database_info[2])
            quantity_available = ""
            curses_identifier = [""]  
            rarity = item_database_info[4]
            attunement_requirement = item_database_info[3]
            mechanics = item_database_info[5]
            flavour = item_database_info[6]
            default_curse = item_database_info[8]
            additional_reference = ""

    #Collect information about the item to be bought. Only do so if the item is in a shop.
    if item_in_shop == True:
        item_database_info = [x for x in GlobalVars.itemdatabase[chosenShop] if selected_item[2] in x][0]
        item_name = item_database_info[1]
        item_type = item_database_info[2]
        item_identifier = item_database_info[0]
        price = int(int(item_database_info[3]) * float(item_database_info[12]))
        quantity_available = item_database_info[18]
        curses_identifier = item_database_info[14].split(",")
        rarity = item_database_info[5]
        attunement_requirement = item_database_info[4]
        mechanics = item_database_info[7]
        flavour = item_database_info[6]
        default_curse = item_database_info[9]
        try:
            additional_reference = item_database_info[17]
        except IndexError:
            additional_reference = ""

    embed_string, unused, potential_curses, potential_curse_names, curseCount = await showItem(item_name, item_type, price, quantity_available, curses_identifier, rarity, attunement_requirement, mechanics, flavour, default_curse, additional_reference)
    
    #Prepare buttons
    if potential_curses != "":
        curse_view = AddItem_Curse_View(message=message)
    else:
        curse_view = AddItem_Curse_View_No_Shopcurses(message=message)
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
                if "[" in curse:
                    curse = curse.replace("[", "").replace("]", "")
                    if curses == "":
                            full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                            curse_names += f"{full_curse[0]}"
                            curses += full_curse[4]
                    else: 
                        full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                        curse_names += f", {full_curse[0]}"
                        curses += f",{full_curse[4]}"
                else:
                    if random.randint(1,2) == 2: #50% chance for every curse to occur
                        if curses == "":
                            full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                            curse_names += f"{full_curse[0]}"
                            curses += full_curse[4]
                        else:
                            full_curse = [x for x in GlobalVars.itemdatabase[1] if curse in x][0]
                            curse_names += f", {full_curse[0]}"
                            curses += f",{full_curse[4]}"
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
            select_view = Dropdown_Select_View(message=message, optionamount=curseCount - 1, maxselectionamount=25, namelist=potential_curse_names)
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
                full_curse = [x for x in GlobalVars.itemdatabase[1] if str(curses_identifier[choice - 1].replace("[", "").replace("]", "")) in x][0]
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

    confirm_view = Yes_No_Quantity_View(message=message)
    await message.channel.send(embed=discord.Embed(title=f"Give {givequant} of this item to {recipient_name}?", description=embed_string, colour = embcol), view = confirm_view)
    if await confirm_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    
    if confirm_view.button_response == "modifyquantity":
        quantity_view = Dropdown_Select_View(message=message, optionamount=25, maxselectionamount=1, namelist=[])
        await message.channel.send(embed=discord.Embed(title=f"How many of these items do you want to add to {recipient_name}'s inventory?", colour = embcol), view=quantity_view)

        if await quantity_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        givequant = int(quantity_view.button_response[0])

        #Ask if this is fine now
        confirm_view = Yes_No_View(message=message)
        await message.channel.send(embed=discord.Embed(title=f"Give {givequant} of this item to {recipient_name}?", description=embed_string, colour = embcol), view = confirm_view)
        if await confirm_view.wait():
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return

    #add item to inventory if reply is yes.
    try:
        if confirm_view.button_response == "yes":
            #Complete transaction
            await addItemToInventory(recipient_inventory_row_index, item_identifier, givequant, curses, additional_reference)
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
    if int(amount) < 0:
        await message.channel.send(embed=discord.Embed(title="Prevented you from taking dezzies from all users", colour = embcol))
        return
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
    
    i = 5
    while i < len(GlobalVars.economyData):
        TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.Add, amount)
        i += 4

#Guides a player through giving money to another player
async def giveMoney(message):
    amount = message.content.split(" ")[-1]
    if int(amount) < 1:
        await message.channel.send(embed=discord.Embed(title="Can't give zero or negative dezzies! The sentence for thievery in the dungeon is one hour in the public stocks!", colour = embcol))
        return
    recipient_name, recipient_id = await getUserNamestr(message)
    if recipient_id == message.author.id:
        await message.channel.send(embed=discord.Embed(title="Can't give yourself dezzies!", colour = embcol))
        return

    author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])

    if await removeDezziesFromPlayerWithoutMessage(amount, message.author.id):
        await addDezziesToPlayer(message, int(amount), playerID=recipient_id, write_econ_sheet=True, send_message=False)
        await message.channel.send(embed=discord.Embed(title=f"{message.author.name} has given {amount}{dezzieemj} to {recipient_name}!", description=f"{message.author.name} now has {GlobalVars.economyData[author_row_index+1][1]}{dezzieemj}\n\n{recipient_name} now has {GlobalVars.economyData[recipient_row_index+1][1]}{dezzieemj}"))
        #Log give commands.
        await client.get_channel(918257057428279326).send(embed=discord.Embed(title = message.author.name + f" gave {amount} Dezzies to " + recipient_name, url=message.jump_url))
        
        TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.Give, -int(amount))
        TransactionsDatabaseInterface.addTransaction(recipient_name, TransactionsDatabaseInterface.DezzieMovingAction.Give, int(amount))
    else:
        await message.channel.send(embed=discord.Embed(title=f"{message.author.name} has not enough {dezzieemj} to give {amount}{dezzieemj} to {recipient_name}!", description=f"{message.author.name} has {GlobalVars.economyData[author_row_index+1][1]}{dezzieemj}"))

#Guides a staff member through adding money to a players balance
async def addMoney(message):
    amount = message.content.split(" ")[-1]
    if int(amount) < 0:
        await message.channel.send(embed=discord.Embed(title="You cannot add negative amounts of dezzies!",description=f"Use %removemoney instead!", colour = embcol))
        return
    
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])
    await addDezziesToPlayer(message, int(amount), playerID=recipient_id, write_econ_sheet=True, send_message=True)
    
    TransactionsDatabaseInterface.addTransaction(recipient_name, TransactionsDatabaseInterface.DezzieMovingAction.Add, amount)

#Guides staff member through removing money from a players balance
async def removeMoney(message):
    amount = message.content.split(" ")[-1]
    recipient_name, recipient_id = await getUserNamestr(message)
    recipient_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(recipient_id) in x][0])
    if await removeDezziesFromPlayerWithoutMessage(int(amount), recipient_id):
        new_balance = GlobalVars.economyData[recipient_row_index+1][1]
        await message.channel.send(embed=discord.Embed(title=f"Removed {amount}{dezzieemj} from {GlobalVars.economyData[recipient_row_index][0]}'s balance!", description=f"Their new balance is {new_balance}{dezzieemj}.", colour = embcol))
        
        TransactionsDatabaseInterface.addTransaction(recipient_name, TransactionsDatabaseInterface.DezzieMovingAction.Remove, -int(amount))
    else:
        await message.channel.send(embed=discord.Embed(title=f"Could not remove {amount}{dezzieemj} from {GlobalVars.economyData[recipient_row_index][0]}'s balance! They only have {GlobalVars.economyData[recipient_row_index+1][1]}{dezzieemj}!", colour = embcol))

#Allows user to use item.
async def useitem(message):
    #Find person in the inventory sheet
    author_row_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(message.author.id) in x][0])
    player_inventory = GlobalVars.inventoryData[author_row_index:author_row_index+5]

    #Get list of all items
    i, item_list = await showInventoryAndChooseItem(message, author_row_index, "\n\nTo select an item to use, enter the according number. This message will time out in 30 seconds.")
    if i == -1:
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
        confirm_view = Yes_No_View(message=message)
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
                if item_list[i] == "metaObject003":
                    author_econ_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
                    GlobalVars.economyData[author_econ_row_index+2][1] = int(GlobalVars.economyData[author_econ_row_index+2][1]) + 1
                await removeItemFromInventory(author_row_index, i+2, 1)

                #TODO: Special treatment for stuff like character slot additions.

#Shows the user their dezzie balance
async def money(message):
    author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    balance = GlobalVars.economyData[author_row_index+1][1]
    leaderboard_list = []
    i = 5
    while i < len(GlobalVars.economyData):
        leaderboard_list.append([GlobalVars.economyData[i][0], int(GlobalVars.economyData[i+1][1])])
        i += 4
    leaderboard_list = sorted(leaderboard_list,key=lambda l:l[1], reverse=True)
    user_leaderboard_rank = leaderboard_list.index([a for a in leaderboard_list if message.author.name == a[0]][0])
    await message.channel.send(embed=discord.Embed(title=f"{message.author.name} has {balance}{dezzieemj}", description=f"Leaderboard Rank: {user_leaderboard_rank + 1}", colour = embcol))

#Shows the leaderboard of the top 20 richest persons
async def leaderboard(message):
    leaderboard_list = []
    i = 5
    while i < len(GlobalVars.economyData):
        leaderboard_list.append([GlobalVars.economyData[i][0], int(GlobalVars.economyData[i+1][1])])
        i += 4
    leaderboard_list= sorted(leaderboard_list,key=lambda l:l[1], reverse=True)
    leaderboard_list = leaderboard_list[0:20]
    embedstring = "The 20 people with the most dezzies in the dungeon are:\n\n"
    i = 1
    for entry in leaderboard_list:
        embedstring += f"`{i:}` **{entry[0]}**\n{entry[1]}{dezzieemj}\n\n"
        i += 1
    await message.channel.send(embed = discord.Embed(title="Dezzie Leaderboard:", description= embedstring, color=embcol))
    
async def invest(message):
    devdata = sheet.values().get(spreadsheetId = Plotsheet, range = "AS1:AX200", majorDimension='COLUMNS').execute().get("values")
    row = devdata[0].index(str(message.channel))

    if str(message.channel).lower() in str(devdata[0]).lower():
        reciprow = ""
        target = message.author
        targname = target.name
        recipient_economy_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
        
        try:
            giveamount = int(message.content.split(" ")[1].strip("-"))
        except ValueError:
            giveamount = int(message.content.split(" ")[2].strip("-"))

        if giveamount >= float((int(devdata[1][row])/4) + 1):
            giveamount = math.floor(int(devdata[1][row])/4)
            await message.channel.send(embed = discord.Embed(title = "You cannot donate that much!", description = "You cannot donate more than 1/4 of the project cost by yourself. We appreciate your generosity, and have set your donation to the maximum of " + str(math.floor(int(devdata[1][row])/4))))

        if giveamount > int(GlobalVars.economyData[recipient_economy_index+1][1]):
            await message.channel.send(embed=discord.Embed(title = "You don't have enough money to do that.", description = "You only have " + str((GlobalVars.economyData[recipient_economy_index+1][1]) + dezzieemj), colour = embcol))
        else:            
            recipnewtot = int(GlobalVars.economyData[recipient_economy_index+1][1]) - int(giveamount)

            if int(giveamount > 0):
                if await removeDezziesFromPlayerWithoutMessage(giveamount, playerName=targname):
                    await writeEconSheet(GlobalVars.economyData)
                    TransactionsDatabaseInterface.addTransaction(targname, TransactionsDatabaseInterface.DezzieMovingAction.Invest, int(-giveamount))
            if str(message.channel).lower() in str(devdata).lower():
                for a in range(len(devdata[0])):
                    if (message.channel.name).lower() in str(devdata[0][a]).lower():
                        row = a

                #Contributors
                try:
                    devconts = devdata[5][row].split("|")
                except IndexError:
                    devconts = ""
                    while len(devdata[5]) < row+1:
                        devdata[5].append("")

                if str(message.author) in devdata[5][row]:
                    prevconts = []
                    for c in range(len(devconts)):
                        if str(message.author) in devconts[c]:
                            prevconts.append(str(message.author) + "£" + str(int(devconts[c].split("£")[1]) + giveamount) + "|")
                        else:
                            prevconts.append(devconts[c] + "|")
                        contributors = "".join(prevconts)

                else:
                    contributors = str(devdata[5][row]) + str(message.author) + "£" + str(giveamount) + "|"
                
                contributors = contributors.replace("||", "|")
                highcont = 0
                highplayer = ""
                for d in range(len(contributors.split("|"))):
                    try:
                        if int(highcont) < int(contributors.split("|")[d].split("£")[1]):
                            highcont = contributors.split("|")[d].split("£")[1]
                            highplayer = contributors.split("|")[d].split("£")[0]

                    except IndexError:
                        pass

                rand20 = random.randint(1,20)

                if message.author.name == "C_allum" and "-" in message.content:
                    rand20 = int(message.content.split(" ")[0].split("-")[1])

                randDC = int(devdata[2][row])
                give1 = giveamount

                if rand20 == 1:
                    #Partial Fail
                    amountlost = random.randint(1,giveamount)
                    mess = "You rolled a " + str(rand20) + " on the dice.\n\n"
                    lost = str(amountlost)
                    remain = str(int(giveamount) - int(amountlost)) + dezzieemj
                    mess += random.choice(["The tipping jar begins to chew on your dezzies… a mimic? Wait - how did you not notice there were two with the same label? Anyways, you fed " + lost + " to the mimic. You shouldn't stick something you value more than dezzies into that one…","Someone embezzled some of the donated dezzies! " + lost + " were lost, leaving only " + remain, "Upon donating, you noticed that there was a hole in your pocket, so when you intended to give " + str(giveamount) + ", you found that you actually only had " + remain + " there.", "An irrate centaur trotted up as you were donating, and demanded the money you owed her for a *ride*. She took " + lost + ", so the donation was reduced to only " + remain, "The donation was overseen by the receptionist at the guild, and somehow came out to only " + remain + "? Janine shrugs as she pockets " + lost + ".", "It turns out that the big dezzie you had been carrying was a mimic, and it didn't want to leave your side. As you thought it was worth about " + lost + ", your donation is now only worth " + remain, "A purplish pixie was in your coin pouch, and had apparently been feasting upon the dezzies there. She managed to eat " + lost + ", so the donation was reduced to " + remain])
                    giveamount -= amountlost

                elif rand20 != 20:
                    #Success
                    mess = "You rolled a " + str(rand20) + " on the dice.\n\n"
                    mess += random.choice(["The dezzies fall into the jar with a pleasant, jingly noise. It " + random.choice(["makes you feel warm inside", "fills you with determination", "leaves you considering learning to use dezzies as a musical instrument"]),"T̴̂͗h̸̊͝e̶͛̃ ̸̑̿M̶̾͐í̸͠s̶͆͋t̷̄̊ȓ̶̂e̶̹͗s̸̽̽s̸̈́̀ smiles upon you. After the orgasm fades, you find yourself bearing a slave crest of " + random.choice(["Abundance", "Altruism", "Bestial Instinct", "Denial", "Echoes" "Emptiness", "False Dominance", "Infatuation", "Infertility", "Obsession", "Seduction", "Slavery", "Transformation", "Virility"]) + " that wasn't there before. it fades after " + str(random.randint(1,6)) + " hours", "T̴̂͗h̸̊͝e̶͛̃ ̸̑̿M̶̾͐í̸͠s̶͆͋t̷̄̊ȓ̶̂e̶̹͗s̸̽̽s̸̈́̀ knows you could have given more and is disappointed. For the next 24 hours, any cum produced within 100ft of you becomes a cum sprite that chases you and leaps into your face", "T̴̂͗h̸̊͝e̶͛̃ ̸̑̿M̶̾͐í̸͠s̶͆͋t̷̄̊ȓ̶̂e̶̹͗s̸̽̽s̸̈́̀ has offered you a great blessing.  For the next 24 hours, any cum produced within 100ft of you becomes a cum sprite that chases you and leaps into your chest", "Tony the tentacle monster gives you a high five... or is that a high one?", "Your donation, as well as your eternal loyalty is accepted . . . . Did you not read the contract?", "A handsomely scarred witch offers to thank you for your donation... personally", "An aspect of Gothica blows you ||a kiss|| as you donate.", "The Keepers offer you a place of honor in their next " + random.choice(["Initiation", "Seed-Drinking", "Breeding"]) + " ritual for your contributions.", "You were given a crumpled voucher for 100 dezzies off at participating shops (but the fine print says the only participating shop is the discount and used sex toy shop run by one of the kobolds)", "You feel T̴̂͗h̸̊͝e̶͛̃ ̸̑̿M̶̾͐í̸͠s̶͆͋t̷̄̊ȓ̶̂e̶̹͗s̸̽̽s̸̈́̀'s blessing upon you... don't go in the kobold dens... or do?", "In thanks, the Adventurer's Guild would like to present a waiver for fees of the next quest.", "", "", "", "", "", "", "", "", "", ""])

                else:
                    #Crit Success
                    mess = "You rolled a " + str(rand20) + " on the dice!\n\n"
                    mess += random.choice(["A kind hearted citizen decided to match your donation!", "You find that the dezzies you donated had been especially pure, and were worth double!", "The tiefling in line to donate after you felt " + random.choice(["intimidated", "aroused", "inspired"]) + "by your donation, and decided to match it!", "The receptionist at the Adventurer's Guild smiles at you as she take the donation, and offers you a voucher for 100" + dezzieemj + " which is valid for any store, if you buy her something nice. She also matches your donation.", "A strange portal opened right as you were depositing dezzies, and exactly the same number of dezzies fell through it - doubling your donation!"])
                    giveamount = 2 * giveamount

                await message.delete()
                namew = message.author.name
                newtotal = int(devdata[3][row]) + giveamount
                progress = str(str(round(newtotal / int(devdata[1][row]),2) * 100) + "%").replace(".0%","%")
                investemb = discord.Embed(title = str(namew) + " invested " + str(give1) + dezzieemj + " in " + str(message.channel), description = mess + "\n\nWe are now " + progress + " towards our goal." + "\n\n" + namew + " has " + str(recipnewtot) + dezzieemj + "\n\n" + str(highplayer.split("#")[0]) + " has contributed the most towards this goal, having invested " + str(highcont) + dezzieemj + " so far!", colour = embcol)
               
                if newtotal >= int(devdata[1][row]):
                    investemb.set_footer(text = str(devdata[4][row]))
                    investemb.set_image(url = "https://i.ibb.co/Nt3NCRN/loading-dezzie0100.png")
                    await client.get_channel(996826636358000780).send("A progress bar has been completed in " + str(message.channel) + "\n\nThe players that contributed to this project were:\n\n" + contributors.replace("|", str(dezzieemj + "\n")).replace("£"," - "))

                elif newtotal < 0:
                    investemb.set_footer(text = "Somehow, we're further behind than we were when we started.")
                    investemb.set_image(url = "https://i.ibb.co/qx7Hj0z/loading-dezzie0000.png")

                else:
                    percentage = newtotal / int(devdata[1][row]) * 100
                    #Image Percentage
                    percent = math.floor(percentage)
                    imglist = ["https://i.ibb.co/qx7Hj0z/loading-dezzie0000.png", "https://i.ibb.co/TPRKffZ/loading-dezzie0001.png","https://i.ibb.co/1m60NWV/loading-dezzie0002.png","https://i.ibb.co/FnfHtf3/loading-dezzie0003.png","https://i.ibb.co/28h1xK4/loading-dezzie0004.png","https://i.ibb.co/pnv2RSL/loading-dezzie0005.png","https://i.ibb.co/7nyXP9t/loading-dezzie0006.png","https://i.ibb.co/HPtc5QW/loading-dezzie0007.png","https://i.ibb.co/H7SG2rV/loading-dezzie0008.png","https://i.ibb.co/NTDGY9b/loading-dezzie0009.png","https://i.ibb.co/tqQLm7L/loading-dezzie0010.png","https://i.ibb.co/nzgJR1M/loading-dezzie0011.png","https://i.ibb.co/nD7jHjT/loading-dezzie0012.png","https://i.ibb.co/T2jVx0h/loading-dezzie0013.png","https://i.ibb.co/s3bb0Gt/loading-dezzie0014.png","https://i.ibb.co/RjCXnY8/loading-dezzie0015.png","https://i.ibb.co/3mKY69j/loading-dezzie0016.png","https://i.ibb.co/f4Xjg63/loading-dezzie0017.png","https://i.ibb.co/7Qh98cb/loading-dezzie0018.png","https://i.ibb.co/k0mW2hZ/loading-dezzie0019.png","https://i.ibb.co/wRxCQVM/loading-dezzie0020.png","https://i.ibb.co/tz7fFFg/loading-dezzie0021.png","https://i.ibb.co/pxkBpP5/loading-dezzie0022.png","https://i.ibb.co/SNLbxt1/loading-dezzie0023.png","https://i.ibb.co/HGV26LQ/loading-dezzie0024.png","https://i.ibb.co/FzxGXX1/loading-dezzie0025.png","https://i.ibb.co/4KkZcqh/loading-dezzie0026.png","https://i.ibb.co/p4mkH4x/loading-dezzie0027.png","https://i.ibb.co/z6LZgCs/loading-dezzie0028.png","https://i.ibb.co/GnQKHGS/loading-dezzie0029.png","https://i.ibb.co/rbbjzNP/loading-dezzie0030.png","https://i.ibb.co/m8D5YqF/loading-dezzie0031.png","https://i.ibb.co/nfysj4L/loading-dezzie0032.png","https://i.ibb.co/1T4f7YQ/loading-dezzie0033.png","https://i.ibb.co/tLp7RK2/loading-dezzie0034.png","https://i.ibb.co/t8Ygm5C/loading-dezzie0035.png","https://i.ibb.co/1zB0yPV/loading-dezzie0036.png","https://i.ibb.co/SBB5d6f/loading-dezzie0037.png","https://i.ibb.co/4mPvSdy/loading-dezzie0038.png","https://i.ibb.co/3S9Dhrt/loading-dezzie0039.png","https://i.ibb.co/M1XKkYB/loading-dezzie0040.png","https://i.ibb.co/b5VzVYz/loading-dezzie0041.png","https://i.ibb.co/5rwTJQj/loading-dezzie0042.png","https://i.ibb.co/cK9y4t6/loading-dezzie0043.png","https://i.ibb.co/qDYBfFs/loading-dezzie0044.png","https://i.ibb.co/grW8NsN/loading-dezzie0045.png","https://i.ibb.co/Vj84zY4/loading-dezzie0046.png","https://i.ibb.co/mX7FMBY/loading-dezzie0047.png","https://i.ibb.co/MZBmZqR/loading-dezzie0048.png","https://i.ibb.co/zSxQsbM/loading-dezzie0049.png","https://i.ibb.co/7pSkMxj/loading-dezzie0050.png","https://i.ibb.co/DG2KqYG/loading-dezzie0051.png","https://i.ibb.co/84bngKX/loading-dezzie0052.png","https://i.ibb.co/S5scHyC/loading-dezzie0053.png","https://i.ibb.co/kQsmr9q/loading-dezzie0054.png","https://i.ibb.co/r5PTVPj/loading-dezzie0055.png","https://i.ibb.co/j9KcKsf/loading-dezzie0056.png","https://i.ibb.co/3NVMCNG/loading-dezzie0057.png","https://i.ibb.co/9rfyp5h/loading-dezzie0058.png","https://i.ibb.co/7KCSQ90/loading-dezzie0059.png","https://i.ibb.co/vQVJQRp/loading-dezzie0060.png","https://i.ibb.co/HPRxwJ8/loading-dezzie0061.png","https://i.ibb.co/pbBTqS8/loading-dezzie0062.png","https://i.ibb.co/563ZBfN/loading-dezzie0063.png","https://i.ibb.co/FY065ty/loading-dezzie0064.png","https://i.ibb.co/qxCzJR3/loading-dezzie0065.png","https://i.ibb.co/T8PBnJN/loading-dezzie0066.png","https://i.ibb.co/fFm92D0/loading-dezzie0067.png","https://i.ibb.co/mcJ47qj/loading-dezzie0068.png","https://i.ibb.co/4VyvV9G/loading-dezzie0069.png","https://i.ibb.co/Y2qFHN1/loading-dezzie0070.png","https://i.ibb.co/593DGqF/loading-dezzie0071.png","https://i.ibb.co/v30RgH4/loading-dezzie0072.png","https://i.ibb.co/b351RF0/loading-dezzie0073.png","https://i.ibb.co/x3rv11r/loading-dezzie0074.png","https://i.ibb.co/ySNh943/loading-dezzie0075.png","https://i.ibb.co/BjPSpDZ/loading-dezzie0076.png","https://i.ibb.co/NNwSpKy/loading-dezzie0077.png","https://i.ibb.co/mN8mdt9/loading-dezzie0078.png","https://i.ibb.co/TK3jtVx/loading-dezzie0079.png","https://i.ibb.co/WgjtBZ5/loading-dezzie0080.png","https://i.ibb.co/BKxybMV/loading-dezzie0081.png","https://i.ibb.co/kBRxqZk/loading-dezzie0082.png","https://i.ibb.co/CzmTPbK/loading-dezzie0083.png","https://i.ibb.co/sQr72KL/loading-dezzie0084.png","https://i.ibb.co/4j3fdf0/loading-dezzie0085.png","https://i.ibb.co/x1jGjxM/loading-dezzie0086.png","https://i.ibb.co/jD4NVCY/loading-dezzie0087.png","https://i.ibb.co/S6yKQYb/loading-dezzie0088.png","https://i.ibb.co/bNkrGSn/loading-dezzie0089.png","https://i.ibb.co/d0NXt5z/loading-dezzie0090.png","https://i.ibb.co/smfYLDV/loading-dezzie0091.png","https://i.ibb.co/XS1c3x6/loading-dezzie0092.png","https://i.ibb.co/1vJtBtS/loading-dezzie0093.png","https://i.ibb.co/98BCvYt/loading-dezzie0094.png","https://i.ibb.co/cYctMPp/loading-dezzie0095.png","https://i.ibb.co/pP6SQvd/loading-dezzie0096.png","https://i.ibb.co/gSSqZGp/loading-dezzie0097.png","https://i.ibb.co/hLP8k2R/loading-dezzie0098.png","https://i.ibb.co/XyLFCn3/loading-dezzie0099.png"]
                    imlink = imglist[percent]
                    investemb.set_image(url = imlink)

                await message.channel.send(embed = investemb)
                sheet.values().update(spreadsheetId = Plotsheet, range = str("AV" + str(row+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newtotal]])).execute()
                sheet.values().update(spreadsheetId = Plotsheet, range = str("AX" + str(row+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[contributors]])).execute()

    else:
        await message.delete()
        await message.channel.send(embed = discord.Embed(title = "This channel isn't set up to receive donations", description = "If you believe this to be in error, contact the moderator team", colour = embcol))

async def bid(message, isbot):
    debugvar = message.content.lower().split(" ")
    if isbot:
        await message.delete()

    elif "setup" == message.content.lower().split(" ")[1] and "staff" in str(message.author.roles).lower():
        for a in range(len(message.content.split(" ")[2].split("|"))):
            bidstock.append(message.content.split(" ")[2].split("|")[a])
            bidprice.append(0)
            bidders.append("")
        global bidthread
        bidthreadseed = await message.channel.send(embed = discord.Embed(title = "Bidding is open!", description = "This weekend's ~~slaves~~ *wares* are:\n" + "\n".join(bidstock), colour = embcol))
        bidthread = await bidthreadseed.create_thread(name = "Bids")

    elif "results" == message.content.lower().split(" ")[1]:
        bidsummary = []
        auctiontot = 0
        for c in range(len(bidstock)):
            if bidders[c] != "":
                bidsummary.append(bidstock[c] + ": " + str(bidprice[c]) + dezzieemj + ", " + bidders[c].name)
                auctiontot += bidprice[c]
            else:
                bidsummary.append(bidstock[c] + ": No bids yet")
        await message.channel.send(embed = discord.Embed(title = "Current bids for this weekend's auctions", description = "\n".join(bidsummary) + "\n\nIn total, " + str(auctiontot) + " is being spent at this auction.",  colour = embcol))

    elif "end" == message.content.lower().split(" ")[1] and "staff" in str(message.author.roles).lower():
        bidtotal = sum(bidprice)
        bidsfinal = []
        bidwinners = []
        for d in range(len(bidstock)):
            if str(bidders[d]) in str(bidwinners):
                try:
                    bidsfinal[bidwinners.index(bidders[d])] += bidprice[d]
                except ValueError:
                    pass
            else:
                bidwinners.append(bidders[d])
                bidsfinal.append(bidprice[d]) 
        bidstatement = []

        indexes = []
        newbal = []
        balances = []

        for e in range(len(bidsfinal)):
            if await removeDezziesFromPlayerWithoutMessage(int(bidsfinal[e]), playerID=bidwinners[e].id):
                bidstatement.append(str(bidwinners[e]) + ": " + str(bidsfinal[e]))
                TransactionsDatabaseInterface.addTransaction(bidwinners[e].name, TransactionsDatabaseInterface.DezzieMovingAction.Auction, -int(bidsfinal[e]))
            else:
                await message.channel.send(embed = discord.Embed(title = "Something went wrong in concluding the auction.", description = f"Couldn't remove dezzies from {bidwinners[e].name}. We don't know why that happened. Please ask the botgods.", colour = embcol))
                return

        await writeEconSheet(GlobalVars.economyData)
        

        await message.channel.send(embed = discord.Embed(title = "Bidding concluded", description = "The following dezzies have been removed:\n\n" + "\n".join(bidstatement), colour = embcol))

    elif "reset" == message.content.lower().split(" ")[1] and "staff" in str(message.author.roles).lower():
        if len(message.content.split(" ")) > 2:
            bidtarget = " ".join(message.content.split(" ")[2:])
            try:
                if bidtarget.lower() in str(bidstock).lower():
                    for b in range(len(bidstock)):
                        if bidtarget.lower() in bidstock[b].lower():
                            slaveindex = b
                            break
                    await message.channel.send(embed = discord.Embed(title = "Reset successful!", description = "You have reset the bid for " + bidstock[slaveindex], colour = embcol))
                    bidders[slaveindex] = ""
                    bidprice[slaveindex] = 0
                    await bidthread.send(message.author.name + " has reset the bid for " + bidstock[slaveindex])

                else:
                    await message.channel.send(embed = discord.Embed(title = "Could not find a slave of that name.", description = "Current slaves for sale are:\n\n" + "\n".join(bidstock), colour = embcol))

            except ValueError:
                await message.channel.send(embed = discord.Embed(title = "The price you bid needs to be an integer  ", description = "", colour = embcol))
        
        else:
            await message.channel.send(embed = discord.Embed(title = "You didn't format that correctly.", description = "It needs to be `%bid reset slavename`.", colour = embcol))
    
    elif "set" == message.content.lower().split(" ")[1] and "staff" in str(message.author.roles).lower():
        bidsections = message.content.split(" ", 1)[2].split("|")
        try:
            if bidsections[0].lower() in str(bidstock).lower():
                for b in range(len(bidstock)):
                    if bidsections[0].lower() in bidstock[b].lower():
                        slaveindex = b
                        bidders[b] = get(client.get_all_members(), id=int(bidsections[1]))
                        bidprice[b] = int(bidsections[2])
                        break
            else:
                bidstock.append(bidsections[0])
                biduser = get(client.get_all_members(), id=int(bidsections[1]))
                bidders.append(biduser)
                bidprice.append(int(bidsections[2]))
                slaveindex = -1

            await message.channel.send(embed = discord.Embed(title = "Success!", description = "You have set the bid for " + str(bidstock[slaveindex]) + " to " + str(bidprice[slaveindex]) + " bid by " + str(bidders[slaveindex]), colour = embcol))

        except ValueError:
            await message.channel.send(embed = discord.Embed(title = "The price you bid needs to be an integer  ", description = "", colour = embcol))

    elif "thread" == message.content.lower().split(" ")[1] and "staff" in str(message.author.roles).lower():
        bidthread = message.channel
        await message.channel.send("Bidding Thread Set")

    else:
        if len(message.content.split(" ")) >= 3:
            bidtarget = " ".join(message.content.split(" ")[1:-1])
            try:
                bidamount = int(message.content.split(" ")[-1])
                bidattempt = bidamount
                author_econ_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
                if message.author.name in str(bidders):
                    for e in range(len(bidstock)):
                        if bidders[e] == message.author:
                            bidattempt += bidprice[e]

                if bidtarget.lower() in str(bidstock).lower():
                    for b in range(len(bidstock)):
                        if bidtarget.lower() in bidstock[b].lower():
                            slaveindex = b
                            break
                    if bidamount <= bidprice[slaveindex]:
                        await message.channel.send(embed = discord.Embed(title = "You need to bid more than that!", description = "The current bid for " + bidstock[slaveindex] + " is " + str(bidprice[slaveindex]) + dezzieemj + ", bid by " + bidders[slaveindex].name, colour = embcol))
                    elif bidattempt > int(GlobalVars.economyData[author_econ_index+1][1]):
                        await message.channel.send(embed = discord.Embed(title = "You can't bid that much.", description = "You only have " + GlobalVars.economyData[author_econ_index+1][1] + dezzieemj + ".", colour = embcol))
                    elif bidamount < 1000:
                        await message.channel.send(embed = discord.Embed(title = "The minimum bid is 1000" + dezzieemj, description = "Please increase your bid.", colour = embcol))
                    else:
                        await message.channel.send(embed = discord.Embed(title = "Bid successful!", description = "You have bid " + str(bidamount) + dezzieemj + " for " + bidstock[slaveindex], colour = embcol))
                        bidders[slaveindex] = message.author
                        bidprice[slaveindex] = bidamount
                        await bidthread.send(message.author.name + " has bid " + str(bidamount) + dezzieemj + " on " + bidstock[slaveindex])

                else:
                    await message.channel.send(embed = discord.Embed(title = "Could not find a slave of that name.", description = "Current slaves for sale are:\n\n" + "\n".join(bidstock), colour = embcol))

            except ValueError:
                await message.channel.send(embed = discord.Embed(title = "The price you bid needs to be an integer  ", description = "", colour = embcol))

        else:
            await message.channel.send(embed = discord.Embed(title = "You didn't format that correctly.", description = "It needs to be `%bid slavename amount`.", colour = embcol))

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
                #Update the dezzie pool of the giver
                newDezziePool = prevDezziePool - giveamount
                channel_id = reaction.channel_id
                message_id = reaction.message_id
                guild_id = reaction.guild_id
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await addDezziesToPlayer(message, giveamount, targid, send_message=False)
                GlobalVars.economyData[int(giverow)+3][0] = int(GlobalVars.economyData[int(giverow)+3][0]) - int(giveamount)

                await writeEconSheet(GlobalVars.economyData)
                #Add transaction
                TransactionsDatabaseInterface.addTransaction(target.name, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                if GlobalVars.economyData[int(giverow)+3][0] == 0:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(GlobalVars.economyData[reciprow+1][1]) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                else:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(GlobalVars.economyData[reciprow+1][1]) + dezzieemj + "\n\n" + givename + " has " + str(GlobalVars.economyData[giverow+3][0]) + dezzieemj + " in their dezzie award pool left for the week!", colour = embcol, url = mess.jump_url))

                await client.get_channel(918257057428279326).send(embed=discord.Embed(title = givename + " awarded Dezzies to " + targetName, url=mess.jump_url))

            #User has less dezzies in their pool than they reacted with
            elif prevDezziePool > 0:
                newDezziePool = 0
                giveamount = prevDezziePool
                newDezziePool = prevDezziePool - giveamount
                channel_id = reaction.channel_id
                message_id = reaction.message_id
                guild_id = reaction.guild_id
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await addDezziesToPlayer(message, giveamount, targid, send_message=False)
                GlobalVars.economyData[giverow+3][0] = 0
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
                
                newDezziePool = prevDezziePool - giveamount
                channel_id = reaction.channel_id
                message_id = reaction.message_id
                guild_id = reaction.guild_id
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await addDezziesToPlayer(message, reward, targid, send_message=False)
                GlobalVars.economyData[int(giverow)+3][0] = int(GlobalVars.economyData[int(giverow)+3][0]) - giveamount #Subtract dezzies from pool
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
                newDezziePool = prevDezziePool - giveamount
                channel_id = reaction.channel_id
                message_id = reaction.message_id
                guild_id = reaction.guild_id
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await addDezziesToPlayer(message, reward, targid, send_message=False)                
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

async def incomeWeek(message):
    income = await TransactionsDatabaseInterface.playerTransactionsInfo(message.author.name, "7 Days")
    
    incomeString = ""
    for row in income:
        for i in range(1, len(row)):
            incomeString += str(row[i]) + " "
        incomeString +="\n"

    await message.channel.send(embed = discord.Embed(title = "Your dezzie earnings over the last week:", description = incomeString, colour = embcol))
    await message.delete()

async def copyEconomy(message):
    GlobalVars.economyData = sheet.values().get(spreadsheetId = inventorysheet, range = "A1:E5", majorDimension='ROWS').execute().get("values")
    GlobalVars.inventoryData = sheet.values().get(spreadsheetId = inventorysheet, range = "Inventories!A1:E7", majorDimension = 'ROWS').execute().get("values")

    oldSheet = message.content.split(" ")[-1]
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ8000", majorDimension='ROWS').execute().get("values")
    oldEconData = sheet.values().get(spreadsheetId = oldSheet, range = "A1:GZ8000", majorDimension='ROWS').execute().get("values")

    members = message.guild.members #Fetch the memberlist of the server we are in.

    removedUserList = []

    i = 5
    while i < len(oldEconData):
        name = oldEconData[i][0] #Name

        try: #If they have never RP-messaged, special treatment
            last_message_reward = oldEconData[i + 1][0] #LastMessageRewardTime
        except IndexError:
            last_message_reward = ""
        try: #If they have no scenes list, special treatment
            scenes_list = oldEconData[i + 2][0] #Scenes List
        except IndexError:
            scenes_list= ""
        try:
            weekly_dezzie_pool = oldEconData[i + 3][0] #Dezzie pool
        except IndexError:
            weekly_dezzie_pool = ""
        dezzies = oldEconData[i][1] #Dezzies

        #Add Levels in for the +1/+2/+3 roles, as well as the character slots.
        user = None
        try:
            user = discord.utils.find(lambda m: m.name == name, members) #Find the user we are currently copying.
        except:
            print(f"Couldn't find user {name} in the server.")
            i += 4
            continue

        additional_slots = 0
        if user != None:
            if "+1" in str(user.roles).lower():
                additional_slots = 1
            if "+2" in str(user.roles).lower():
                additional_slots = 2
            if "+3" in str(user.roles).lower():
                additional_slots = 3

        character_slots = additional_slots

        #Add user ID to the economy sheet for future reference
        index = []
        if user != None:
            user_id = user.id
        else:
            #print(f"Couldn't find user {name} in the server.")
            removedUserList.append(name)
            i += 4
            continue

        if user.discriminator != "0":
            message.channel.send(f"{name} still has their old username...")
            print(f"User {name} still has an old username. Skipping.")
            i += 4
            continue
        
        await addUserToEconomy(name, user_id, last_message_reward, dezzies, scenes_list, character_slots, weekly_dezzie_pool)
        
        #Port the items
        refundedItemList = []
        embedstring = ""

        j = 2
        while j < len(oldEconData[i]):
            if oldEconData[i][j] == "":
                break
            itemname = oldEconData[i][j].split("|")[0]
            try:
                amount = oldEconData[i][j].split("|")[1]
                
            except IndexError:
                amount = 1
                print(f"Item {itemname} had no quantity attached.")
            itemamount = amount
            if itemname[0].isalpha() == False:
                itemname = itemname[1:]
            if "EasterEgg:964636527432978482" in itemname:
                itemname = itemname.split("-")[0][0:-1]            
            remappingList = [['Ring of Oras', 'ringGag001'],
                ['Crest of Seduction', 'lustbrand016'],
                ['Dancer’s Lingerie', 'haremRobes002'],
                ["Dancer's Lingerie", 'haremRobes002'],
                ['Mark of Obsession', 'lustbrand005'],
                ['Crest of Obsession', 'lustbrand005'],
                ['Rings of Shared Sensation', 'piercings004'],
                ['Rod of Olympus', 'oversizedDildo002'],
                ['Ring of Good Vibrations', 'cockRing002'],
                ['Imperial Robes', 'robes003'],
                ['Vampiric Clothes', 'fineClothes002'],
                ['Living Silk Rope', 'silkRope001'],
                ['Hell Hound Lingerie', 'lingerie012'],
                ['Curse of Breeding', 'lustbrand010'],
                ['Heels of Hobbling', 'shoes002'],
                ['Naughty Cherub Lingerie', 'lingerie013'],
                ['Shaft of Knowing', 'phallicShaft005'],
                ['Mark of Seduction', 'lustbrand016'],
                ['Corset of the Jorgumo', 'corset001'],
                ['Curse of Stimulation', 'lustbrand007'],
                ['Living Bedroll', 'bedroll001'],
                ['Curse of Allure', 'lustbrand016'],
                ['Plug of Untold Endurance', 'plug010'],
                ['Silks of the Fallen Angel', 'lingerie013'],
                ['Eager Faun Lingerie', 'lingerie011'],
                ['Ninetale Fox Lingerie', 'lingerie010'],
                ['Crest of Slavery', 'lustbrand014'],
                ['Dildo of the Deep Ones', 'dildo001'],
                ['Mask of Medical Secrets', 'mask002'],
                ['Plug of Vacuous Attention', 'plug009'],
                ['Armor of Bestiathropy', 'fetishArmor003'],
                ['Genie’s Harem Robes', 'haremRobes001'],
                ['Glass of Vacuous Desire', 'suctionGlass001'],
                ['Ring of Oral Obsession', 'ringGag001'],
                ['Flavormark Tattoo', 'tatoo008'],
                ['Dwarven Manacles', 'manacles002'],
                ['Chastity Belt of the Cuckold', 'collar010'],
                ['Dildo of Memory (Small)', 'dildo003'],
                ['Queen’s Futanari', 'doulbeDildo001'],
                ['Siren’s Song (Spell Scroll)', 'spellScroll082'],
                ['Ghostthorn Paddle', 'paddle001'],
                ['Outsider', 'doulbeDildo001'],
                ['Gyrobunny', 'otherItem004'],
                ['Cultist’s Crown', 'miscCreature007'],
                ['Confessional Robes', 'fineClothes003'],
                ['Lubricate (Spell Scroll)', 'spellScroll051'],
                ['Power Word Milk (spell scroll)', 'spellScroll049'],
                ['Power Word Orgasm (spell scroll)', 'spellScroll065'],
                ["Tali's Twinned Shaft (Spell Scroll)", 'spellScroll078'],
                ['Moaning Mushrooms', 'miscCreature008'],
                ['Runic Arm Binders', 'armBinder001'],
                ['Runic Chastity Belt', 'chastityBelt004'],
                ['Runic Harness', 'slaveHarness002'],
                ['Runic Harness (RH)',  'slaveHarness002'],
                ['Moo-Mellon Milk', 'potion014'],
                ['Crop of Command', 'crop001'],
                ['Portal Panties (Lesser)', 'panties001'],
                ['Curse of Denial', 'lustbrand006'],
                ["Housekeeper's Cube", 'otherItem005'],
                ['Imperial Robes of Comfort', 'robes003'],
                ['Crest of Echoes', 'lustbrand007'],
                ['Everfull Sack', 'ballCover001'],
                ['Rose-thorn Needle Wheel', 'needleRoller001'],
                ['Victoria’s Secret Pocket (spell scroll)', 'spellScroll096'],
                ["Xanabar's Sexual Theivery (Spell Scroll)", 'spellScroll081'],
                ['Word of Safety (Spell Scroll)', 'spellScroll102'],
                ['Crest of Denial', 'lustbrand006'],
                ['Mark of Denial', 'lustbrand006'],
                ['Harness of Many Heads', 'straponHarness001'],
                ['Crest of Altruism', 'lustbrand003'],
                ["The Widow's Shibari", 'otherItem001'],
                ['Rune of Flavoring', 'tatoo008'],
                ['Portal Mask (PM)', 'mask003'],
                ['Portal Mask', 'mask003'],
                ['Rabbithole Mask', 'mask003'],
                ['Portal Panties', 'panties001'],
                ['Portal Panties (PP)', 'panties001'],
                ['Rabbithole Panties', 'panties001'],
                ["Ruby's Mindfuck (Spell Scroll)", 'spellScroll070'],
                ['Runar’s Instant Disrobing (Spell Scroll)', 'spellScroll071'],
                ['Laundry Day (Spell Scroll)', 'spellScroll048'], 
                ["Predator's Punishment (Spell Scroll)", 'spellScroll066'],
                ["Vilga's Phallic Enchantment (Spell Scroll)", 'spellScroll097'],
                ['Mark of the Owned', 'tatoo003']
                ]
            deleteList = [['Potion Of The Goliath'],
                ['Collar Of The Good Girl'],
                ["Callum's Heart"],
                ['Prestidildo'],
                ['Welcoming Ring Of The Inconsiderate'],
                ["Bunnie's Bountiful Egg of Sweetness"]
                ]
            refundList = [['Demiplane Key'],
                ['Mask of the Hunt'],
                ['Tearless Lingerie'],
                ['Gemstone Piercing'],
                ['Bingo Bango Bongos'],
                ['Statue of Will-I-Am D-Hoe'],
                ['Drowsilk Lingerie'],
                ['Heels of Harming'],
                ['Curse of Futanari'],
                ['Xio Chrysalis'],
                ['Twinned Tentacles'],
                ['Oil Of Slipperyness'],
                ['Basic Ink'],
                ['Pitfall Trap'],
                ['Pitfall Trap+'],
                ['Wyrmleather Blindfold'],
                ['Tearless Lingerie (Uncommon)'],
                ['Tearless Lingerie (Rare)'],
                ['Tearless Lingerie (Very Rare)'],
                ['Stone of Thunderous Vibration'],
                ['Archaic Arcane Beads of Pleasure'],
                ['Plug of Insight'],
                ["Sexy Nurse's Uniform"],
                ['Plug of Insight'],
                ['Plug of Insight'],
                ['Salamander Springs Massage Oil']
                ]
            if any(itemname in sublist for sublist in remappingList): #These are the manual matchings because the item got renamed
                try:
                    item_identifier = remappingList[remappingList.index([x for x in remappingList if str(itemname) in x][0])][1]
                except IndexError:
                    print("Yote")
                try:
                    itemname = GlobalVars.itemdatabase[0][GlobalVars.itemdatabase[0].index([x for x in GlobalVars.itemdatabase[0] if item_identifier in x][0])][0]
                except IndexError:
                    print("yeet")
            elif any(itemname in sublist for sublist in deleteList):
                print(f"Skipped/Deleted item {itemname}")
                j += 1
                continue
            elif any(itemname in sublist for sublist in refundList):
                #Find previous value and add to balance
                oldEconData[i][j].split("|")[0]
                amount = int(oldEconData[i+3][j])
                await addDezziesToPlayer(message, amount, user_id, write_econ_sheet=False, send_message=False)
                refundedItemList.append([itemname, int(itemamount) * int(amount)])
                print(f"Refunded item {itemname}")
                j += 1
                continue

            new_item = await matchStringToItemBase(itemname, 1, add_item_name_in_list=True)

            if new_item[0][1] >= 89.0:
                new_item_name = new_item[0][0]
            else:
                #Manual matching goes here.
                new_item_name = "Scroll03"
            additional_references = ""
            if itemname.startswith("Mark of"):
                additional_references = "lustBrand,nessaConsent"
            if itemname.startswith("Curse"):
                additional_references = "lustBrand"
            if itemname.startswith("Crest of"):
                additional_references = "lustBrand"

            user_inventory_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(user_id) in x][0])
            try:
                item_identifier = GlobalVars.itemdatabase[0][GlobalVars.itemdatabase[0].index([x for x in GlobalVars.itemdatabase[0] if new_item_name in x][0])][11]
            except IndexError:
                print("Oopsie!")
                j = j+1
                continue
            await addItemToInventory(user_inventory_index, item_identifier, amount, "", additional_references)
            j += 1
        for item in refundedItemList:
            embedstring += f"{item[0]} for {item[1]}{dezzieemj}\n"
        if embedstring != "":
            await client.get_channel(1050503346374594660).send(embed = discord.Embed(title = f"Refunded the follwing items for {user.name} because they got changed.", description = embedstring + f"\n\n<@{user_id}>", colour=embcol))
        i+=4
    print(removedUserList)
    #Write PlayerInfo sheet
    await writeEconSheet(GlobalVars.economyData)
    #Write Inventory Sheet
    await writeInvetorySheet(GlobalVars.inventoryData)
    await message.channel.send(embed=discord.Embed(title="Economy Copy to economy V2 is done!"))

async def computeAllLevenshteinDistancesOldEconItems(message, oldEconData):
    item_match_list = []
    i = 5
    while i < len(oldEconData):
        j = 2
        while j < len(oldEconData[i]):
            itemname = oldEconData[i][j].split("|")[0]
            if "EasterEgg:964636527432978482" in itemname:
                itemname = itemname.split("-")[0][0:-1]
            if itemname[0].isalpha() == False:
                itemname = itemname[1:]
            item_match_list.append((await matchStringToItemBase(itemname, 1, add_item_name_in_list=True))[0])
            j += 1
        i += 4
    sorted_list = sorted(item_match_list, key=lambda l:l[1], reverse=True)
    #remove duplicates
    res = []
    [res.append(x) for x in sorted_list if x not in res]
    res = [[x[3], x[0], x[1], x[2]] for x in res]
    with open("output.txt", "a",encoding="utf8") as f:
        for element in res:
            print(element)
            print(element, file=f)

async def addUserToEconomy(name, id, last_message_time = datetime.timestamp(datetime.now()), total_dezzies = 0, scenes_list = "", additional_charslots = 0, weekly_award_pool = 500):
    async with economy_lock:
        #Line 1: Name & ID
        GlobalVars.economyData.append([name])
        GlobalVars.economyData[-1].append(str(id))
        #Line 2: Last Message Award & Total Dezzies
        GlobalVars.economyData.append([last_message_time])
        GlobalVars.economyData[-1].append(total_dezzies)
        #Line 3: Scene list & Additional Charslots
        GlobalVars.economyData.append([scenes_list])
        GlobalVars.economyData[-1].append(additional_charslots)
        #Line 4: Weekly award pool and an empty field for the new dailies system.
        GlobalVars.economyData.append([weekly_award_pool])
        GlobalVars.economyData[-1].append(0)
        #-----------------Inventory------------
        if len(GlobalVars.inventoryData) != 7:
            while (len(GlobalVars.inventoryData )- 7) % 6 != 5:
                GlobalVars.inventoryData.append([""])
        ##Line 1: Name & ID
        GlobalVars.inventoryData.append([name])
        GlobalVars.inventoryData[-1].append(str(id))
    #await writeEconSheet(GlobalVars.economyData)
    #await writeInvetorySheet(GlobalVars.inventoryData)
    return


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
    #itemsheet = gc.open_by_key("17M2FS5iWchszIoimqNzk6lzJMOVLBWQgEZZKUPQuMR8") #New for economy rewrite
    itemsheet = gc.open_by_key("1rS4yTmVtaaCZEbfyAAEkB3KnVC_jkI9e2zhSI0AA7ws") #New for economy rewrite
    itemlists = itemsheet.worksheets()
    GlobalVars.itemdatabase = []
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
async def matchStringToItemBase(item_name, top_n_results, add_item_name_in_list = False):
    levenshtein_tuple_list = []
    for entry in GlobalVars.itemdatabase[0][1:]:
        #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
        
        levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance_complete = fuzz.ratio(entry[0].lower(), item_name.lower())
        levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
        if add_item_name_in_list == True:
            levenshtein_tuple_list.append([entry[0], levenshtein_distance, entry[11], item_name])
        else:
            levenshtein_tuple_list.append([entry[0], levenshtein_distance, entry[11]])

    sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
    return sorted_list[:top_n_results]

async def selectItem(message, searchterm, top_n_results):
    #Search for item in the item sheet with fuzzy matching
    item_matches = await matchStringToItemBase(searchterm, top_n_results)
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
        item_selection_view = Dropdown_Select_View(message = message, timeout=30, optionamount=len(selector_options), maxselectionamount=1, namelist=[i[0] for i in selector_options]) #Only let them choose one item.
        await message.channel.send(embed = discord.Embed(title="Didn't find a perfect match to what you are looking for.", description="Here are the top 10 closest results. Please choose which of these you want.\n\n" + top10_string + "\n\n" + "This message will time out in 30 seconds.", colour = embcol), view = item_selection_view)
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
    return selected_item


async def removeDezziesFromPlayerWithoutMessage( amount, playerID = None, playerName = None):

    if playerID != None:
        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(playerID) in x][0])
    elif playerName != None:
        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if playerName in x][0])
    else:
        await message.channel.send(embed = discord.Embed(title="Player to remove dezzies from not found."))
        return False

    if int(GlobalVars.economyData[author_row_index+1][1]) > int(amount):
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

async def showItem(item_name, item_type, price, quantity_available, curses_identifier, rarity, attunement_requirement, mechanics, flavour, default_curse, additional_reference, show_quant_and_price = True):
        #add item type and rarity
    if item_type[0] == " ":
        item_type = item_type[1:]
    embed_string = f"**{item_name}**\n\n*{item_type}, {rarity}*"
    #add attunement to the string
    if attunement_requirement.lower() == "yes":
        embed_string += f" *(Requires Attunement)*\n\n"
    elif "by" in attunement_requirement:
            spellcaster = attunement_requirement.replace("Yes, by ", "")
            embed_string += f" *(Requires Attunement by {spellcaster})*\n\n"
    else: embed_string += "\n\n"

    if (show_quant_and_price == True):
        if quantity_available == "":
            quantity_available = "Infinite"
        embed_string += f"**Quantity Available: {quantity_available}, Price per unit: {price}{dezzieemj}** \n\n"

    #add long description
    if mechanics != "":
        embed_string += flavour + "\n\n" + mechanics
    else:
        embed_string += flavour
    #add additional reference
    if additional_reference != "":
        split_references = additional_reference.replace(" ", "").split(",")
        first = 0
        for entry in split_references:
            add_ref_data = [x for x in GlobalVars.itemdatabase[2] if entry.replace("[", "").replace("]", "") in x][0]
            if first == 0:
                embed_string += f"\n\n**{add_ref_data[0]}**: {add_ref_data[1]}"
                first == 1
            else:
                embed_string += f"\n**{add_ref_data[0]}**: {add_ref_data[1]}"

    #add default curse
    if default_curse != "":
        embed_string += f"**\n\n__Default curse:__** \n{default_curse}"
   
    #add additional curses
    potential_curses_string = ""
    potential_curses = []
    potential_curse_names = []
    curseCount = 0
    if curses_identifier[0] != "":
        potential_curses_string += "**\n\n__Potential curses:__**\n"
        curseCount = 1
        for curse in curses_identifier:
            try:
                full_curse = [x for x in GlobalVars.itemdatabase[1] if curse.replace("[", "").replace("]", "") in x][0]
                potential_curses.append(full_curse)

            except IndexError:
                await message.channel.send(embed=discord.Embed(title=f"Error in additem function.", description="Index error in additem function: Possibly a problem with the curses in the item sheet. Check for spaces that shouldn't be there, and correct identifiers. Please notify the bot gods.", colour = embcol))
            if "[" in curse:
                potential_curses_string+= f"`{curseCount}:` **[Mandatory] {full_curse[0]}** Level {full_curse[1]} curse): {full_curse[2]}\n\n"
                potential_curse_names.append(full_curse[0].replace("[", "").replace("]", ""))
            else:
                potential_curses_string+= f"`{curseCount}:` **{full_curse[0]}** (Level {full_curse[1]} curse): {full_curse[2]}\n\n"
                potential_curse_names.append(full_curse[0])
            curseCount += 1
    return embed_string, potential_curses, potential_curses_string, potential_curse_names, curseCount

async def addItemToPlayerWithCurseFromShop(message, playerID, itemID, amount, shop_number, additional_reference):

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
            if "[" in curse:
                rolled_curses.append(i)
                if curses == "":
                    curses += curse.replace("[", "").replace("]", "")
                else: curses += f",{curse}"
            else:
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
                if curses == GlobalVars.inventoryData[author_row_index+2][item_instance] and additional_reference == GlobalVars.inventoryData[author_row_index+3][item_instance]:
                    GlobalVars.inventoryData[author_row_index+1][item_instance] = int(GlobalVars.inventoryData[author_row_index+1][item_instance]) + amount
                    already_in_inventory = True
                    await writeInvetorySheet(GlobalVars.inventoryData)
                    await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your already present items!", description="You already owned that exact item, so we just added the requested quantity.", colour = embcol))
                    return rolled_curses
            except IndexError: #This happens when a trailing item has no curse.
                try:
                    if curses == "" and additional_reference == GlobalVars.inventoryData[author_row_index+3][item_instance]:
                        GlobalVars.inventoryData[author_row_index+1][item_instance] = int(GlobalVars.inventoryData[author_row_index+1][item_instance]) + amount
                        already_in_inventory = True
                        await writeInvetorySheet(GlobalVars.inventoryData)
                        await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your already present items!", description="You already owned that exact item, so we just added the requested quantity.", colour = embcol))
                        return rolled_curses
                    else: 
                        pass
                except IndexError:
                    if curses == "" and additional_reference == "":
                        GlobalVars.inventoryData[author_row_index+1][item_instance] = int(GlobalVars.inventoryData[author_row_index+1][item_instance]) + amount
                        already_in_inventory = True
                        await writeInvetorySheet(GlobalVars.inventoryData)
                        await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your already present items!", description="You already owned that exact item, so we just added the requested quantity.", colour = embcol))
                        return rolled_curses
                    else: 
                        pass
        if already_in_inventory == False: #If curses do not match on any instance
            await addItemToInventory(author_row_index, itemID, amount, curses, additional_reference)
            await writeInvetorySheet(GlobalVars.inventoryData)
            await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your inventory!", description="Seems to be your first one. Go and have fun with it!", colour = embcol))
            return rolled_curses

    else: #If Item is new in the inventory
        await addItemToInventory(author_row_index, itemID, amount, curses, additional_reference)
        await writeInvetorySheet(GlobalVars.inventoryData)
        await message.channel.send(embed=discord.Embed(title=f"{amount}x {item_database_info[1]} added to your inventory!", description="Seems to be your first one. Go and have fun with it!", colour = embcol))
        return rolled_curses

async def addItemToInventory(recipient_inventory_row_index, item_identifier, quantity, curses, additional_reference):
    if int(quantity) <= 0:
        print("Quantity must be above 0")
        return
    #Add item to recipient inventory
    try:
        item_match = -1
        if item_identifier in GlobalVars.inventoryData[recipient_inventory_row_index]: #if the recipient has the *exact* item in their inv already:
            for j in range(0, len(GlobalVars.inventoryData[recipient_inventory_row_index])):
                try:
                    recipient_curses = GlobalVars.inventoryData[recipient_inventory_row_index+2][j]
                except IndexError:
                    recipient_curses = ""
                try:
                    recipient_additional_reference = GlobalVars.inventoryData[recipient_inventory_row_index+3][j]
                except IndexError:
                    recipient_additional_reference = ""
                if GlobalVars.inventoryData[recipient_inventory_row_index][j] == item_identifier and recipient_curses == curses and recipient_additional_reference == additional_reference:
                    item_match = j
        if item_match != -1:
                #Add +amount to the item quantity.
            GlobalVars.inventoryData[recipient_inventory_row_index + 1][item_match] = int(GlobalVars.inventoryData[recipient_inventory_row_index + 1][item_match]) + int(quantity)
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
            while len(GlobalVars.inventoryData[recipient_inventory_row_index+3]) < len(GlobalVars.inventoryData[recipient_inventory_row_index]) - 1:
                GlobalVars.inventoryData[recipient_inventory_row_index+3].append("")
            try:
                GlobalVars.inventoryData[recipient_inventory_row_index+3].append(additional_reference)
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
    elif quantity == int(GlobalVars.inventoryData[inventory_row_index+1][item_inventory_index]):
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
    else:
        await message.channel.send(embed=discord.Embed(title=f"You have less than {quantity} of selected item in your inventory!", description="You cannot sell more than you own! It's not the stock market!", colour = embcol))
        return False
        
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
            return -1, None
    except asyncio.TimeoutError:
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        await message.delete()
        return -1, None
    if i > len(player_inventory[0]):
        await message.channel.send(embed=discord.Embed(title=f"Number must be between 1 and {len(player_inventory[0]) - 2}", colour = embcol))
        return -1, None
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
    def __init__(self, message, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
        self.message = message
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.message.author.id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message("That is not your button to click!", ephemeral=True)
            return False

class AddItem_Curse_View_No_Shopcurses(discord.ui.View):
    def __init__(self, message, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
        self.message = message
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.message.author.id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message("That is not your button to click!", ephemeral=True)
            return False

class Yes_No_View(discord.ui.View):
    def __init__(self, message, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
        self.message = message
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.message.author.id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message("That is not your button to click!", ephemeral=True)
            return False

class Yes_No_Quantity_View(discord.ui.View):
    def __init__(self, message, timeout=90):
        super().__init__(timeout=timeout)
        self.button_response = ""
        self.message = message
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.message.author.id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message("That is not your button to click!", ephemeral=True)
            return False

class Dropdown_Select_View(discord.ui.View):
    def __init__(self, message, timeout=120, optionamount=1, maxselectionamount = 1, namelist = []):
        super().__init__(timeout=timeout)
        self.button_response = []
        self.choices = []
        self.namelist = namelist
        self.message = message
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.message.author.id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message("That is not your dropdown to click!", ephemeral=True)
            return False