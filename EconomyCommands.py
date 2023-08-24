import TransactionsDatabaseInterface
import TupperDatabase
from CommonDefinitions import *
from TransactionsDatabaseInterface import addTransaction, DezzieMovingAction


#Buy Item
async def buyitem(message):
    #Search Shop for item match
    shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")
    buyquant = 1
    try:
        fullMessage = message.content.replace("'","").replace("’","").lower()
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
    
    itindex = ""

    
    #try:
    #    buyquant = int(message.content.split(" ", 1)[1].lower().rsplit(" ", 1)[-1])
    #except ValueError:
    #    buyquant = 1

    #Temp variables to present possible options
    matchnames = []

    searchnames = []

    matchno = 0

    #Collect all instances of the searched term
    for n in range(len(shopdata[0])):
        if searchterm in str(shopdata[1][n]).replace("'","").replace("’","").lower():

            matchno += 1

            matchnames.append("`" + str(matchno) + "` " + shopdata[0][n] + shopdata[1][n] + ", sold at" + shopdata[3][n].replace("#", " ").replace("-", " ").title())

            searchnames.append(shopdata[1][n])

    #Give user a choice which instance they want
    if matchno > 1:
        await message.channel.send(embed = discord.Embed(title = "Multiple Matches Found", description = "Type the number of the one you want.\n\n" + "\n".join(matchnames) + "\n\nThis message will timeout after 30 seconds.", colour = embcol))

        try:

            msg = await client.wait_for('message', timeout = 30, check = check(message.author))

            try:

                valu = int(msg.content)

                searchterm = searchnames[valu-1]

                await msg.delete()

            except TypeError or ValueError:

                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))

                await msg.delete()

        except asyncio.TimeoutError:

            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))

            await message.delete()

    elif matchno == 1: #Replace searchterm with the exact item name if only one match is present.
        searchterm = searchnames[0]


    #Grab index of the item    
    for n in range(len(shopdata[0])):
        if searchterm.replace("'","").replace("’","").lower() == shopdata[1][n].replace("'","").replace("’","").lower():
            itindex = n


    #Get Item and Shop Data

    if itindex != "":

        failpur = 0

        itname = shopdata[1][itindex]

        itprice = shopdata[2][itindex]

        itshop = shopdata[3][itindex]

        itnpc = shopdata[5][itindex]

        itresp = shopdata[6][itindex]

        itrep = shopdata[7][itindex]

        try:
            
            itstock = int(shopdata[8][itindex])

        except ValueError:

            itstock = ""
        
        except IndexError:

            itstock = ""

        if itstock == "":

            reciept = message.author.name.split("#")[0] + " bought " + str(buyquant) + " " + itname + " for " + str(int(itprice) * int(buyquant)) + dezzieemj

            stockupdate = ""

        elif buyquant <= itstock:

            reciept = message.author.name.split("#")[0] + " bought " + str(buyquant) + " " + itname + " for " + str(int(itprice) * int(buyquant)) + dezzieemj

            stockupdate = itstock - buyquant

        else:

            reciept = message.author.name.split("#")[0] + " attempted to buy " + str(buyquant) + " " + itname + ", but there were not enough in stock!"

            stockupdate = 0

            failpur = 1

        #Shop Specific Stuff:

        if itnpc == "Nubia":

            npcthumb = "https://cdn.discordapp.com/attachments/912879579260125184/917863713514590228/Nubia-icon.png"

            npccol = 0xded233

        elif itnpc == "Nessa":

            npcthumb = "https://cdn.discordapp.com/attachments/912882341091876915/917863626151456818/Nessa.png"

            npccol = 0x18cdd3

        elif itnpc == "Madame Webb":

            npcthumb = "https://cdn.discordapp.com/attachments/917870118342647808/917878405473656862/webb_avatar.png"

            npccol = 0x222222

        elif itnpc == "Sophie":

            npcthumb = "https://cdn.discordapp.com/attachments/918575985669062727/919379824986976356/sophie_avatar.png"

            npccol = 0xaed318

        elif itnpc == "Runar":

            npcthumb = "https://cdn.discordapp.com/attachments/912759640008298577/926340769344798730/RunarToken.png"

            npccol = 0x4a97df

        elif itnpc == "Voivode":

            npcthumb = "https://cdn.discordapp.com/attachments/912758732142837761/921654371903750144/D-9576iWwAAPgcP.jpeg"

            npccol = 0x96470c

        elif itnpc == "Amelia":

            npcthumb = ""

            npccol = 0x9ac7fc

        else:

            itnpc = "an NPC"

            npcthumb = ""

            npccol = 0x000000

        if buyquant == 1:

            buymess = "It was sold by "

        else:

            buymess = "They were sold by "

        if stockupdate == "":

            buyemb = discord.Embed(title= reciept, description= buymess + itnpc + " at " + str(itshop).strip("#").replace("-", " ").title() + "\n-------------------------------------------------------\n*" + itresp + "*", colour = npccol)

        elif failpur:

            if itstock > 0:

                buyemb = discord.Embed(title= reciept, description= itnpc + " was only able to sell " + str(itstock) + " at " + str(int(itstock) * int(itprice)) + "\n-------------------------------------------------------\n*" + itresp + "*", colour = npccol)

                buyquant = itstock

            else:

                buyemb = discord.Embed(title= reciept, description= itnpc + " was unable to sell this item", colour = npccol)

                buyquant = 0

        else:

            if stockupdate == 0:

                stockmess = "There are none of these left in the shop!"

            elif stockupdate == 1:

                stockmess = "There is only one of these left in the shop!"

            else:

                stockmess = "There are " + str(stockupdate) + " left in the shop!"

            buyemb = discord.Embed(title= reciept, description= buymess + itnpc + " at " + str(itshop).strip("#").replace("-", " ").title() + "\n-------------------------------------------------------\n*" + itresp + "*" + "\n\n-------------------------------------------------------\nThis item is limited in stock. " + stockmess, colour = npccol)        

        buyemb.set_thumbnail(url = npcthumb)

        if itrep != "This item was not supposed to be used this way.":

            buyemb.set_footer(text = "-------------------------------------------------------\n\n*This item is consumable. Before using it in roleplay, ensure to $use " + itname + " to consume it*")

        await message.delete()

        sheet.values().update(spreadsheetId = shopsheet, range = str("I" + str(itindex + 1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[stockupdate]])).execute()

        userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")

        for n in range(math.ceil(len(userinvs)/4)):

            r = 4 * n 

            if str(message.author) in userinvs[r][0]:

                #Check Balance!

                if int(userinvs[r][1]) < (int(buyquant) * int(itprice)):

                    await message.channel.send(embed = discord.Embed(title = "You can't afford this", description= "To buy " + str(buyquant) + " " + itname + ", you need " + str(int(buyquant) * int(itprice)) + dezzieemj + ". You only have " + userinvs[r][1], colour = embcol))
                    
                    sheet.values().update(spreadsheetId = shopsheet, range = str("I" + str(itindex + 1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[itstock]])).execute()

                    break

                else:

                    newbal = int(userinvs[r][1]) - (int(buyquant) * int(itprice))

                    await message.channel.send(embed = buyemb)

                    if itname.replace("'","").replace("’","").lower() in str(userinvs[r]).replace("'","").replace("’","").lower():

                        for itno in range(len(userinvs[r])):

                            #If item is existing

                            if itname.replace("'","").replace("’","").lower() in userinvs[r][itno].replace("'","").replace("’","").lower():

                                newquant = int(userinvs[r][itno].split("|")[1]) + buyquant

                                if itno > 25:

                                    collet = chr(64 + math.floor(itno / 26))

                                else:

                                    collet = ""
                                
                                collet += chr(65 + (int(itno)))

                                sheet.values().update(spreadsheetId = EconSheet, range = collet + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[userinvs[r][itno].split("|")[0] + "|" + str(newquant)]])).execute()

                                break

                    else:

                        #If item is new

                        itno = len(userinvs[r])

                        itdata = [shopdata[0][itindex] + shopdata[1][itindex] + "|" + str(buyquant), "", shopdata[4][itindex], shopdata[2][itindex]]

                        if itno > 25:

                            collet = chr(64 + math.floor(itno / 26))

                        else:

                            collet = ""
                        
                        collet += chr(65 + (int(itno % 26)))
                        sheet.values().update(spreadsheetId = EconSheet, range = collet + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[itdata])).execute()

                    #Set new balance
                    
                    sheet.values().update(spreadsheetId = EconSheet, range = "B" + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[newbal]])).execute()

                    addTransaction(message.author.name + "#" + str(message.author.discriminator), DezzieMovingAction.Buy, int(-(int(buyquant) * int(itprice))))

    else:

        await message.channel.send(embed = discord.Embed(title = "We couldn't find any items matching that name.", description= "Check the spelling of the item, and look through `" + myprefix + "shop shopname` to ensure it is correct.", colour = embcol))

#Sell Item
async def sellitem(message):

    #Divide String
    mess = message.content.split(" ")
    itemname = ""
    try:
        quant = int(mess[-1])
    except (IndexError, ValueError) as e:
        quant = 1
        itemname = " ".join(mess[1:])

    if itemname == "":
        itemname = " ".join(mess[1:-1])


    #Check Inventory
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")
    for a in range(math.ceil(len(userinvs)/4)):
        b = 4 * a 
        if str(message.author) in userinvs[b][0]:
            rowindex = b
            break
    matchingItems = []
    for c in range(len(2, userinvs[rowindex])):
        if itemname.lower() in userinvs[rowindex][c].lower():
            matchingItems.append(c)
    if len(matchingItems) == 0:
        await message.channel.send(embed = discord.Embed(title = "Could not find a matching item", description = "Check the spelling matches that of the item in your `%inventory`", colour = embcol))
        return
    elif len(matchingItems) == 1:
        columnindex = matchingItems[0]
    else:
        itemlist = []
        for d in range(len(matchingItems)):
            itemlist.append("`" + str(d+1) + ":` " + userinvs[rowindex][matchingItems[d]].split("|")[0])
        optionStr = "\n".join(itemlist)
        await message.channel.send(embed = discord.Embed(title = "Multiple items found", description = "Select the number of the one you want:\n" + optionStr, colour = embcol))
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                columnindex = matchingItems[int(msg.content) - 1]
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
    invItemname = str(userinvs[rowindex][columnindex].split("|")[0])
    price = int(userinvs[rowindex+3][columnindex])

    await message.delete()
    #Check quantity to be sold against inventory
    invquant = int(userinvs[rowindex][columnindex].split("|")[1])
    if quant <= invquant:
        totalprice = int(quant * price) * float(sellpricemultiplier)
        newitemtotal = invquant - quant
    else:
        #Selling more than they have. Tell them no and set to max.
        await message.channel.send(embed = discord.Embed(title = "You don't have enough of those in your inventory to be able to sell " + str(quant), description = "We are fairly sure that " + str(invquant) + " is less than " + str(quant) + ". Selling " + str(invquant), colour = embcol))
        quant = invquant
        totalprice = int(math.floor(float(quant) * float(price) * float(sellpricemultiplier)))
        newitemtotal = invquant - quant
    newbal = int(int(userinvs[rowindex][1]) + totalprice)
    sellreturnmessage = random.choice(["We hope you washed that first", "Dezzies may be returned to your account within 6-9 working days. Probably.", "Were you not satisfied with your purchase?", "Cum again!", "We had been looking for one of those ourself..."])
    await message.channel.send(embed = discord.Embed(title = "Sold " + str(quant) + " " + str(invItemname) + " for " + str(int(totalprice)) + " Dezzies!", description = sellreturnmessage + "\n\n" + message.author.name + " now has " + str(newbal) + " " + dezzieemj, colour = embcol))

    #update sheet
    sheet.values().update(spreadsheetId = EconSheet, range = "B" + str(rowindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[newbal]])).execute()
    addTransaction(message.author.name + "#" + str(message.author.discriminator), DezzieMovingAction.Sell, int(totalprice))
    collet = await getColumnLetter(columnindex)
    if newitemtotal == 0: #Shift everything else over
        newitemlist = userinvs[rowindex][columnindex+1:]
        newshortdesclist = userinvs[rowindex+1][columnindex+1:]
        newlongdesclist = userinvs[rowindex+2][columnindex+1:]
        newpricelist = userinvs[rowindex+3][columnindex+1:]
        newitemlist.append("")
        newshortdesclist.append("")
        newlongdesclist.append("")
        newpricelist.append("")
        newinvdata = [newitemlist, newshortdesclist, newlongdesclist, newpricelist]
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(rowindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=newinvdata)).execute()
    else:
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(rowindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[str(invItemname) + "|" + str(newitemtotal)]])).execute()

    #update stock on the shop it came from
    shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")

    shopItemName = invItemname[1:]
    for n in range(len(shopdata[0])):
        if shopItemName == shopdata[1][n]:
            newStock = int(shopdata[8][n]) + quant
            sheet.values().update(spreadsheetId = shopsheet, range = "I" + str(n + 1), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[str(newStock)]])).execute()

            return

async def giveitem(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")

    #make sure *someone* is tagged to give the item to.
    if "@" in message.content:
        namestr, targid = await getUserNamestr(message)
    else:
        await message.channel.send(embed = discord.Embed(title = "Wrong use of the %giveitem command!", description = "Please make sure to stick to the `%giveitem [@user] [item name] [amount]` format! You need to specify a person to give the item to!", colour = embcol))
        return
        
    #prevent giving yourself items
    if namestr == message.author.name + "#" + message.author.discriminator:
        await message.channel.send(embed = discord.Embed(title = "No, you can't give yourself an item that you own...", description = "Giving yourself an item is weird. Maybe a case of split personalities?", colour = embcol))
        return
    
    #make sure target is in the economy
    if not str(namestr) in str(userinvs):
        await message.channel.send(embed = discord.Embed(title = "Could not find " + namestr.split("#")[0] + "'s inventory", description = "Make sure that <@" + str(targid) + "> is registered in the economy."))
        return

    targetindex = [row[0] for row in userinvs[::4]].index(namestr)
    targetindex *= 4
    targetinv = userinvs[targetindex]
 
    authorindex = [row[0] for row in userinvs[::4]].index(message.author.name + "#" + message.author.discriminator)
    authorindex *= 4
    authorinv = userinvs[authorindex]

    messageParts = message.content.split(" ")

    amount = 0
    #try to retrieve the amount.
    try:
        amount = int(messageParts[-1])
        amount = int(messageParts.pop())
    except ValueError:
        amount = 1
    except IndexError:
        await message.channel.send(embed = discord.Embed(title = "Wrong use of the %giveitem command!", description = "Please make sure to stick to the `%giveitem [@user] [item name] [amount]` format!", colour = embcol))

    #itemname should be the last parameter after removing the amount.
    itemName = messageParts.pop()

    #fetch correct item name and handle multiple matches.
    matchingItems = []
    for c in range(len(authorinv)):
        if itemName.lower() in authorinv[c].lower():
            matchingItems.append(c)
    if len(matchingItems) == 0:
        await message.channel.send(embed = discord.Embed(title = "Could not find a matching item", description = "Check the spelling matches that of the item in your `%inventory`", colour = embcol))
        return
    elif len(matchingItems) == 1:
        columnindex = matchingItems[0]
    else:
        itemlist = []
        for d in range(len(matchingItems)):
            itemlist.append("`" + str(d+1) + ":` " + authorinv[matchingItems[d]].split("|")[0])
        optionStr = "\n".join(itemlist)
        await message.channel.send(embed = discord.Embed(title = "Multiple items found", description = "Select the number of the one you want:\n" + optionStr, colour = embcol))
        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                columnindex = matchingItems[int(msg.content) - 1]
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()
            return
    itemname = str(userinvs[authorindex][columnindex].split("|")[0])
    invquant = int(userinvs[authorindex][columnindex].split("|")[1])
    
    collet = await getColumnLetter(columnindex)
    itemshortdesc = sheet.values().get(spreadsheetId = EconSheet, range = str(collet) + str(authorindex+7), majorDimension = 'ROWS').execute().get("values")

    #This needs to be none if there is no description, but if there is an item with a short descr. further to the right in that players inventory, it would be [[' ']] instead of none... And google doesn't like that.
    if itemshortdesc == [[' ']]:
        itemshortdesc = None

    itemdescr = str(userinvs[authorindex+2][columnindex])
    price = int(userinvs[authorindex+3][columnindex])
    

    #TODO: Remove item from msg.author inventory, add to target inventory. Send a log of the transaction to the botchannel
    #Check quantity to be given against inventory

    if amount > invquant:
        #Giving more than they have. Tell them no and cancel.
        await message.channel.send(embed = discord.Embed(title = "You don't have enough of those in your inventory to be able to give " + str(amount), description = "We are fairly sure that " + str(invquant) + " is less than " + str(amount) + ". Please enter a valid amount.", colour = embcol))
        return
    newitemtotal = invquant - amount
    #Check if an item of the same type is already in the recipients inventory
    targetInvItemIndex = -1
    for c in range(len(targetinv)):
        if itemName.lower() in targetinv[c].lower():
            targetInvItemIndex = c
            targetinvquant = int(userinvs[targetindex][targetInvItemIndex].split("|")[1])

    #update sheet of the author
    print(f"Taking {amount} {itemname} from {message.author.display_name}")
    collet = await getColumnLetter(columnindex)
    if newitemtotal == 0: #Shift everything else over
        newitemlist = userinvs[authorindex][columnindex+1:]
        newshortdesclist = userinvs[authorindex+1][columnindex+1:]
        newlongdesclist = userinvs[authorindex+2][columnindex+1:]
        newpricelist = userinvs[authorindex+3][columnindex+1:]
        newitemlist.append("")
        newshortdesclist.append("")
        newlongdesclist.append("")
        newpricelist.append("")
        newinvdata = [newitemlist, newshortdesclist, newlongdesclist, newpricelist]
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(authorindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=newinvdata)).execute()
    else:
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(authorindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[str(itemname) + "|" + str(newitemtotal)]])).execute()
    print("Done taking from Author")

    #update the sheet of the target but check if the item is already existent
    if targetInvItemIndex == -1: #In this case the item is not present in the recipients list.
        newinvdata = [itemname+"|"+str(amount), itemshortdesc, itemdescr, price]
        collet = await getColumnLetter(len(userinvs[targetindex]))
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(targetindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[newinvdata])).execute()
    else:
        collet = await getColumnLetter(targetInvItemIndex)
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(targetindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[str(itemname) + "|" + str(targetinvquant + amount)]])).execute()

    print("Done giving to the recipient")

    #Confirm transaction with an embed.
    givereturnmessage = random.choice(["We hope you washed that first", "We had been looking for one of those ourself..."])
    targetusername = await message.guild.fetch_member(targid)
    targetusername = targetusername.display_name
    await message.channel.send(embed = discord.Embed(title = f"{message.author.display_name} gave " + str(amount) + " " + str(itemname) + f" to " + targetusername, description = givereturnmessage + "\n\n\n<@" + str(targid) + ">, you have been given an item!", colour = embcol))

    
    await message.delete()
    

async def additem(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")
    #make sure *someone* is tagged to give the item to.
    if "@" in message.content:
        namestr, targid = await getUserNamestr(message)
    else:
        await message.channel.send(embed = discord.Embed(title = "Wrong use of the %additem command!", description = "Please make sure to stick to the `%additem [@user] [item name] [amount]` format! You need to specify a person to give the item to!", colour = embcol))
        return

    #make sure target is in the economy
    if not str(namestr) in str(userinvs):
        await message.channel.send(embed = discord.Embed(title = "Could not find " + namestr.split("#")[0] + "'s inventory", description = "Make sure that <@" + str(targid) + "> is registered in the economy."))
        return

    targetindex = [row[0] for row in userinvs[::4]].index(namestr)
    targetindex *= 4
    targetinv = userinvs[targetindex]

    messageParts = message.content.split(" ")

    amount = 0
    #try to retrieve the amount.
    try:
        amount = int(messageParts[-1])
        amount = int(messageParts.pop())
    except ValueError:
        amount = 1
    except IndexError:
        await message.channel.send(embed = discord.Embed(title = "Wrong use of the %giveitem command!", description = "Please make sure to stick to the `%giveitem [@user] [item name] [amount]` format!", colour = embcol))

    #itemname should be the last parameter after removing the amount.
    searchterm = messageParts.pop()

    #Search Shop for item match
    shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")
    
    itindex = ""

    #Temp variables to present possible options
    matchnames = []
    searchnames = []
    matchno = 0

    #Collect all instances of the searched term
    for n in range(len(shopdata[0])):
        if searchterm in str(shopdata[1][n]).replace("'","").replace("’","").lower():
            matchno += 1
            matchnames.append("`" + str(matchno) + "` " + shopdata[0][n] + shopdata[1][n] + ", sold at" + shopdata[3][n].replace("#", " ").replace("-", " ").title())
            searchnames.append(shopdata[1][n])

    #Give user a choice which instance they want
    if matchno > 1:
        await message.channel.send(embed = discord.Embed(title = "Multiple Matches Found", description = "Type the number of the one you want.\n\n" + "\n".join(matchnames) + "\n\nThis message will timeout after 30 seconds.", colour = embcol))

        try:
            msg = await client.wait_for('message', timeout = 30, check = check(message.author))
            try:
                valu = int(msg.content)
                searchterm = searchnames[valu-1]
                await msg.delete()

            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()

        except asyncio.TimeoutError:
            await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            await message.delete()

    elif matchno == 1: #Replace searchterm with the exact item name if only one match is present.
        searchterm = searchnames[0]
        
    #Grab index of the item    
    for n in range(len(shopdata[0])):
        if searchterm.replace("'","").replace("’","").lower() == shopdata[1][n].replace("'","").replace("’","").lower():
            itindex = n


    #Get Item and Shop Data

    if itindex != "":
        failpur = 0
        itname = shopdata[1][itindex]
        itprice = shopdata[2][itindex]
        itshop = shopdata[3][itindex]
        itnpc = shopdata[5][itindex]
        itresp = shopdata[6][itindex]
        itrep = shopdata[7][itindex]



        userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")
        for n in range(math.ceil(len(userinvs)/4)):
            r = 4 * n 
            if str(namestr) in userinvs[r][0]:
                if itname.replace("'","").replace("’","").lower() in str(userinvs[r]).replace("'","").replace("’","").lower():
                    for itno in range(len(userinvs[r])):
                        
                        #If item is existing
                        if itname.replace("'","").replace("’","").lower() in userinvs[r][itno].replace("'","").replace("’","").lower():
                            newquant = int(userinvs[r][itno].split("|")[1]) + amount
                            collet = await getColumnLetter(itno)
                            sheet.values().update(spreadsheetId = EconSheet, range = collet + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[userinvs[r][itno].split("|")[0] + "|" + str(newquant)]])).execute()
                            break

                else:
                    #If item is new
                    itno = len(userinvs[r])
                    itdata = [shopdata[0][itindex] + shopdata[1][itindex] + "|" + str(amount), "", shopdata[4][itindex], shopdata[2][itindex]]
                    collet = await getColumnLetter(itno)
                    sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[itdata])).execute()

        targetusername = await message.guild.fetch_member(targid)
        targetusername = targetusername.display_name
        await message.channel.send(embed = discord.Embed(title = f"Added {itname} to {targetusername}'s inventory!", description= "Congratulations, <@" + str(targid) + ">, you have been given an item!", colour = embcol))
                 
    else:
        await message.channel.send(embed = discord.Embed(title = "We couldn't find any items matching that name.", description= "Check the spelling of the item, and look through `" + myprefix + "shop shopname` to ensure it is correct.", colour = embcol))

    await message.delete()
    #TODO: Make sure to send a log of the item given to the botchannel!


    return

async def giftAll(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")

    amount = int(message.content.split(" ")[-1])

    i = 0

    while i < len(userinvs):
        userinvs[i][1] = int(userinvs[i][1]) + amount
        i += 4

    sheet.values().update(spreadsheetId = EconSheet, range = "A6", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute()
    if amount >= 0:
        await message.channel.send(embed = discord.Embed(title = "Everyone received a gift!", description = f"Every denizen of the dungeon was blessed with {amount}<:dz:844365871350808606> right into their pockets!"))
    else:
        await message.channel.send(embed = discord.Embed(title = "Everyone got robbed!", description = f"Every denizen of the dungeon got {amount}<:dz:844365871350808606> taken right out of their pockets!"))

async def dezReact(reaction):
    mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension='ROWS').execute().get("values")

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
        for a in range(math.floor(len(economydata)/4)):
            b = a * 4 + 5

            if str(targetName + "#" + str(target.discriminator)) in str(economydata[b][0]):
                reciprow = b + 1
                break

    except IndexError:
        if not mess.author.bot:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))
    
    #Find giver row in the economy sheet
    try:
        for a in range(math.floor(len(economydata)/4)):
            b = a * 4 + 5

            if str(givename + "#" + str(giver.discriminator)) in str(economydata[b][0]):
                giverow = b + 1
                break
    except IndexError:
        if not mess.author.bot:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(givename) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))


    #Determine gift amount - Values in CommonDefinitions.py
    if reaction.emoji.name == "dz":
        giveamount = reactdz

    elif reaction.emoji.name == "cashmoney":
        giveamount = reactCashMoney

    elif reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart":
        giveamount = reactMakeItRain

    else:
        giveamount = random.randint(100,500)


    #Retrieve users current react dezzie pool
    try:
        prevDezziePool = int(economydata[giverow+2][0])

    except IndexError:
        prevDezziePool = weeklyDezziePoolVerified

    except ValueError:
        prevDezziePool = weeklyDezziePoolVerified

    except TypeError:
        prevDezziePool = weeklyDezziePoolVerified


    #Check if given amount is smaller than the pool of dezzies left for the user
    if reaction.channel_id != 828545311898468352: #Disable Noticeboard Reacts

        if reaction.member.name == targetName:
            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = "No.", description = targetName + ", you can't just award dezzzies to yourself.", colour = embcol))
            await client.get_channel(918257057428279326).send(targetName + " tried to award dezzies to themself.")

        else:
            #Enough dezzies left in users dezzie pool:
            if giveamount <= prevDezziePool:
                recipNewTot = int(economydata[int(reciprow)-1][1]) + int(giveamount)
                newDezziePool = prevDezziePool - giveamount
                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipNewTot]])).execute()

                TransactionsDatabaseInterface.addTransaction(target.name + '#' + target.discriminator, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(int(giverow)+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()

                if newDezziePool == 0:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                else:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has " + str(newDezziePool) + dezzieemj + " in their dezzie award pool left for the week!", colour = embcol, url = mess.jump_url))

                await client.get_channel(918257057428279326).send(givename + " awarded Dezzies to " + targetName)

            #User has less dezzies in their pool than they reacted with
            elif prevDezziePool > 0:
                newDezziePool = 0
                giveamount = prevDezziePool
                recipNewTot = int(economydata[reciprow-1][1]) + int(giveamount)
                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipNewTot]])).execute()

                TransactionsDatabaseInterface.addTransaction(target.name + '#' + target.discriminator, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(giverow+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()
                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))
                await client.get_channel(918257057428279326).send(givename + " awarded Dezzies to " + targetName)

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
        await client.get_channel(botchannel).send(embed=discord.Embed(title = str(giver.display_name) + ": The post you tried to award is too old, or was edited.", description = "The first time a character is awarded dezzies, the post has to be rather new and unedited! Try awarding a different, unedited post of that character. If the issue persists, contact the bot gods.", colour = embcol))
        return

    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension='ROWS').execute().get("values")

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
        for a in range(math.floor(len(economydata)/4)):
            b = a * 4 + 5

            if str(targetName + "#" + str(target.discriminator)) in str(economydata[b][0]):
                reciprow = b + 1
                break

    except IndexError:
        if not mess.author.bot:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))
    
    #Find giver row in the economy sheet
    try:
        for a in range(math.floor(len(economydata)/4)):
            b = a * 4 + 5

            if str(givename + "#" + str(giver.discriminator)) in str(economydata[b][0]):
                giverow = b + 1
                break
    except IndexError:
        if not mess.author.bot:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = str(givename) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))


    #Determine gift amount - Values in CommonDefinitions.py
    if reaction.emoji.name == "dz":
        giveamount = reactdz

    elif reaction.emoji.name == "cashmoney":
        giveamount = reactCashMoney

    elif reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart":
        giveamount = reactMakeItRain

    else:
        giveamount = random.randint(100,500)


    #Retrieve users current react dezzie pool
    try:
        prevDezziePool = int(economydata[giverow+2][0])

    except IndexError:
        prevDezziePool = weeklyDezziePoolVerified

    except ValueError:
        prevDezziePool = weeklyDezziePoolVerified

    except TypeError:
        prevDezziePool = weeklyDezziePoolVerified


    #Check if given amount is smaller than the pool of dezzies left for the user
    if reaction.channel_id != 828545311898468352: #Disable Noticeboard Reacts

        if reaction.member.name == targetName:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = "No.", description = targetName + ", you can't just award dezzzies to yourself.", colour = embcol))
            await client.get_channel(918257057428279326).send(targetName + " tried to award dezzies to themself.")

        else:
            #Enough dezzies left in users dezzie pool:
            if giveamount <= prevDezziePool:
                reward = int(giveamount * rpReactModifier)
                recipNewTot = int(economydata[int(reciprow)-1][1]) + reward
                newDezziePool = prevDezziePool - giveamount
                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipNewTot]])).execute()

                TransactionsDatabaseInterface.addTransaction(target.name + '#' + target.discriminator, TransactionsDatabaseInterface.DezzieMovingAction.React, int(reward))

                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(int(giverow)+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()

                if newDezziePool == 0:
                    await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                else:
                    await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has " + str(newDezziePool) + dezzieemj + " in their dezzie award pool left for the week! (RP Rewards award 25% more while costing the same!)", colour = embcol, url = mess.jump_url))

                await client.get_channel(918257057428279326).send(givename + " awarded Dezzies to " + targetName)

            #User has less dezzies in their pool than they reacted with
            elif prevDezziePool > 0:
                newDezziePool = 0
                giveamount = prevDezziePool
                recipNewTot = int(economydata[reciprow-1][1]) + int(giveamount)
                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipNewTot]])).execute()

                TransactionsDatabaseInterface.addTransaction(target.name + '#' + target.discriminator, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))

                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(giverow+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()
                await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(reward) + dezzieemj + " to " + targetName + " for an RP message", description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))
                await client.get_channel(918257057428279326).send(givename + " awarded Dezzies to " + targetName)

            #User dezzie pool is empty:
            else:
                await client.get_channel(botchannel).send(embed=discord.Embed(title = reaction.member.name + "'s dezzie award pool for the week is empty!" , description = "You will receive a fresh pool of dezzies to award to others at the start of next week!", colour = embcol, url = mess.jump_url))

    else:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = "You can't use this at the here.", colour = embcol, url = mess.jump_url))
#---------Helper functions----------

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

    namestr = str(targname.name + "#" + targname.discriminator)

    return namestr, targid

async def getColumnLetter(columnindex):
    collet = ""
    if columnindex > 25:
        collet = chr(64 + math.floor(columnindex / 26))
    else:
        collet = ""                        
    collet += chr(65 + (int(columnindex % 26)))
    return collet