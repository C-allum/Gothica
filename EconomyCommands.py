from CommonDefinitions import *

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
            print("buyquantExtract: " + fullMessage.rsplit(" ", 1)[-1])
            buyquant = int(fullMessage.rsplit(" ", 1)[-1]) #Try to extract a buy quantity from the end of the string
            
            if buyquant < 1:
                buyquant = 0
        except ValueError:
            print("Buy function Value Error")
            buyquant = 1  
        except TypeError:
            print("Buy function type error")
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

        userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ2000", majorDimension = 'ROWS').execute().get("values")

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

                    print(userinvs[r][1])

                    print(itprice)

                    print(newbal)

                    await message.channel.send(embed = buyemb)

                    if itname.replace("'","").replace("’","").lower() in str(userinvs[r]).replace("'","").replace("’","").lower():

                        for itno in range(len(userinvs[r])):

                            #If item is existing

                            if itname.replace("'","").replace("’","").lower() in userinvs[r][itno].replace("'","").replace("’","").lower():

                                newquant = int(userinvs[r][itno].split("|")[1]) + buyquant

                                if itno > 25:

                                    collet = chr(65 + math.floor(itno / 26))

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

                            collet = chr(65 + math.floor(itno / 26))

                        else:

                            collet = ""
                        
                        collet += chr(65 + (int(itno)))

                        sheet.values().update(spreadsheetId = EconSheet, range = collet + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[itdata])).execute()

                    #Set new balance
                    
                    sheet.values().update(spreadsheetId = EconSheet, range = "B" + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[newbal]])).execute()

    else:

        await message.channel.send(embed = discord.Embed(title = "We couldn't find any items matching that name.", description= "Check the spelling of the item, and look through `" + myprefix + "shop shopname` to ensure it is correct.", colour = embcol))

#Sell Item
async def sellitem(message):

    #Divide String
    mess = message.content.split(" ")
    try:
        itemname = " ".join(mess[2:])
    except IndexError:
        itemname = " ".join(mess[1:])
    try:
        quant = int(mess[1])
    except IndexError:
        quant = 1
    except ValueError:
        quant = 1

    #Check Inventory
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ2000", majorDimension = 'ROWS').execute().get("values")
    for a in range(math.ceil(len(userinvs)/4)):
        b = 4 * a 
        if str(message.author) in userinvs[b][0]:
            rowindex = b
            break
    matchingItems = []
    for c in range(len(userinvs[rowindex])):
        if itemname.lower() in userinvs[rowindex][c].lower():
            matchingItems.append(c)
    if len(matchingItems) == 0:
        await message.channel.send(embed = discord.Embed(title = "Could not find a matching item", description = "Check the spelling matches that of the item in your `%inventory`", colour = embcol))
        return
    elif len(matchingItems) == 1:
        columnindex = matchingItems[0]
    else:
        for d in range(len(matchingItems)):
            itemlist = "`" + str(d+1) + ":` " + userinvs[rowindex][matchingItems[d]].split("|")[0] 
        await message.channel.send(embed = discord.Embeds(title = "Multiple items found", description = "Select the number of the one you want:\n" + "\n".join(itemlist)))
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
    price = str(userinvs[rowindex+3][columnindex])

    await message.delete()
    #Check quantity to be sold against inventory
    invquant = int(userinvs[rowindex][columnindex].split("|")[1])
    if quant <= invquant:
        totalprice = int(quant * price) * sellpricemultiplier
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
    if columnindex > 25:
        collet = chr(65 + math.floor(columnindex / 26))
    else:
        collet = ""                        
    collet += chr(65 + (int(columnindex)))
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

