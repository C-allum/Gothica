from CommonDefinitions import *
from thefuzz import fuzz
import EconomyV2

#Character Index Update
async def updatereg(message):

    print("Refreshing Index")

    await message.channel.send("Updating Index")

    charlist = await client.get_channel(indexchannel).history(limit=4000, oldest_first=True).flatten()

    for a in range(len(charlist)):

        if a > 0:

            await charlist[a].delete()

    await client.get_channel(indexchannel).send(embed = discord.Embed(title = "Break", description= "", colour = embcol))

    chardata = sheet.values().get(spreadsheetId = CharSheet, range = "A1:Z4000" ).execute().get("values")

    for a in range(len(chardata)):

        if a != 0:

            #Collect Spreadsheet Data

            chararg = []

            for b in range(len(chardata[0])):

                if chardata[a][b] != "":

                    if b > 4 and chardata[0][b] != "Status" and chardata[0][b] != "Image" and chardata[0][b] != "Link":

                        chararg.append(chardata[0][b] + ": " + chardata[a][b])

            #Create Embed

            emb = discord.Embed(title = chardata[a][5], description = "\n".join(chararg), colour = embcol)

            emb.set_footer(text = "------------------------------------------------------------------------------------------------------------\n\nOwned by " + chardata[a][1])

            #Image Tracking

            if chardata[a][24] != []:

                if "|" in chardata[a][24]:

                    emb.set_image(url = chardata[a][24].split("|")[0])

                else:

                    emb.set_image(url = chardata[a][24])

            elif ".jpg" in chardata[a][14] or ".jpeg" in chardata[a][14] or ".png" in chardata[a][14]:

                biowords = chardata[a][14].split("\n").split(" ")

                for c in range(len(biowords)):

                    if ".jpg" in biowords[c] or ".jpeg" in biowords[c] or ".png" in biowords[c]:

                        emb.set_image(url = biowords[c])

            await client.get_channel(indexchannel).send(embed = emb)

#Character Creation Subroutine
async def charcreate(message):

    args = message.content.split("\n")

    args = list(filter(lambda x: x != "", args))

    argsprev = ""

    tit = str(message.author.name) + " registered a new character!"
    desc = ""
    argprev = ""

    #Default Entries

    char = [message.author.name, message.author.name, date.today().strftime("%d/%m/%Y"), "Never Transferred", ""]

    for i in range(len(headers)-5):
        char.append("")

    #Test for image

    if message.attachments:
        char.append(message.attachments[0].url)
        hasimage = 1
    else:
        char.append("")
        hasimage = 0

    #Add Link

    char.append(message.jump_url)
    char.append("")
    char.append("")

    for j in range(len(args)):

        if args[j] != None:

            #Reset variable for tracking multiline args

            argmatched = 0

            #Test against each header

            for i in range(len(headers)):

                for n in range(len(aliases[i-1])):

                    #Test for discontinuous paragraph

                    if " " in args[j]:

                        #Test for space in header, for example, eye colour

                        #Then, set arg to the value and argtype to the User inputted field

                        if " " in aliases[i-1][n]:
                            argsplit = args[j].split(" ", 2)
                            if len(argsplit) != 2:
                                arg = argsplit[2]
                                argtype = str(argsplit[0]) + " " + str (argsplit[1])
                            else:
                                arg = ""
                                argtype = ""
                        else:
                            argsplit = args[j].split(" ", 1)
                            if len(argsplit) != 1:
                                arg = argsplit[1]
                                argtype = str(argsplit[0])
                            else:
                                arg = ""
                                argtype = ""

                    else:

                        #Arg alone

                        arg = args[j]
                        argtype = args[j]

                    #Exception - Sex in Sexuality

                    if "sex" in argtype.lower():
                        if "sexual" in argtype.lower() and headers[i] != "Sexuality":
                            arg = ""
                            argtype = ""

                    #Test if Headers is in argtype. This allows the user to customise it - so "Name:", "Name=" and 69Name69 all work the same way.

                    if i != 0 and str(aliases[i-1][n]).lower() in argtype.lower():
                    
                        #Set variable for tracking multiline args

                        argmatched = 1
                        argprev = i

                        #Warnings

                        #Test Character age

                        if str(headers[i]) == "Age" and isinstance(arg,int):
                            if int(arg) < 18:
                                await client.get_channel(logchannel).send(str(message.author) + " has tried to register a character under 18")

                        if str(headers[i]) == "Class":

                            #Sum levels from class

                            classlevels = [int(s) for s in re.findall(string=str(arg), pattern="[0-9]+")]
                            lvltot = sum(classlevels)

                            #Test Character Level from sum

                            if lvltot > 14:
                                await client.get_channel(logchannel).send(str(message.author) + " has tried to register a character over level 14")

                            char[i+namecol+1] = lvltot

                        #Test Character Level

                        if str(headers[i]) == "Level" and isinstance(arg,int):
                            if int(arg) > 14:
                                await client.get_channel(logchannel).send(str(message.author) + " has tried to register a character over level 14")

                        if str(headers[i]) == "Image" and hasimage:
                            arg = message.attachments[0].url

                        #Append the filled field to desc, for use in the user facing output

                        desc += headers[i] + ": " + str(arg) + "\n"

                        #Set the list item for char - for the back of house output
                        if headers[i] != "Link" and headers[i] != "Approved" and headers[i] != "Played by: (NPCs only)": 
                            if "colour" in arg.lower() or "color" in arg.lower():
                                if not " " in arg:
                                    break
                            else:
                                char[i+namecol] = arg
                            break
                        elif headers[i] == "Players" and message.channel.name == "NPC Creation":
                            char[i+namecol] = arg

                    #Test Multiline Variable

                    if i+1 == len(headers) and not argmatched and args[j] != argsprev:
                        #Append to previous Arg
                        char[argprev+namecol] += "\n\n" + args[j]
                        desc += "\n" + str(args[j]) + "\n"
                        argsprev = args[j]

    #Send user output embed

    emb = discord.Embed(title=char[namecol+1], description = desc, colour = embcol)
    emb2 = discord.Embed(title=tit, description = "You have added " + char[namecol+1] + " to your character list.", colour = embcol)

    if hasimage:
        emb.set_image(url=message.attachments[0].url)
        emb2.set_thumbnail(url=message.attachments[0].url)

    auth = message.author.name

    autres = sheet.values().get(spreadsheetId = CharSheet, range = "B2:B4000").execute()
    authvalues = str(autres.get("values"))
    authvalues = authvalues.replace("'","")
    pnames = authvalues.split(",")

    statres = sheet.values().get(spreadsheetId = CharSheet, range = "X2:X4000").execute()
    statvalues = str(statres.get("values"))
    statvalues = statvalues.replace("'","")
    charstats = statvalues.split(",")

    pcharsreg = 0

    for g in range(len(pnames)):
        if pnames[g] == auth:
            if g <= len(charstats):
                if "Active" in charstats[g]:
                    pcharsreg += 1

    roles = str(message.author.roles)

    player_econ_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    maxchars = startingslots + int(GlobalVars.economyData[player_econ_index + 2][1])

    for a in range(len(headers)):
        if headers[a] == "Status":
            char[a+namecol] = "Active"
        elif headers[a] == "Pronouns":
            if "/" in char[a+namecol]:
                nouns = str(char[a+namecol]).split("/")
                determiner = nouns[1].lower()
                pronoun = nouns[0].lower()
            else:
                determiner = "them"
                pronoun = "they"

    if not auth in str(pnames):
        #First Character
        emb2.set_footer(text="\n\n----------------------------------\n\nCongratulations! You've registered your first character! Create a tupper for " + determiner + " in #Tupper Setup")

    elif pcharsreg > maxchars-1:
        #Above maximum
        emb2.set_footer(text="\n\n----------------------------------\n\nYou have more characters registered than you have slots! This character has been set as unavailable. Please retire one of your characters using `$retire name` if you want to play " + determiner + " in the dungeon")

        await client.get_channel(logchannel).send(str(message.author) + " has too many characters registered!")

        #Set Unavailable
        for a in range(len(headers)):
            if headers[a] == "Status":
                char[a+namecol] = "Unavailable"

    elif pcharsreg == maxchars-1:

        emb2.set_footer(text="\n\n----------------------------------\n\nThis is the last character you can register before you run out of slots")

    if message.channel.name == "NPC Creation":
        char[23] = "DMPC"

    emb.set_footer(text = "------------------------------------------------\n\nOwned by " + message.author.name)

    print(message.author.name + " registered a character")

    #Send message to character index
    await client.get_channel(indexchannel).send(embed=emb)
    await message.channel.send(embed=emb2)

    #Convert to list of lists

    charoutput = [char]

    #Append line to sheet

    sheet.values().append(spreadsheetId = CharSheet, range = "A2", valueInputOption = "USER_ENTERED", body = {'values':charoutput}).execute()

#Character Edit Subroutine
async def charedit(message):

    cargs = sheet.values().get(spreadsheetId = CharSheet, range = "F1:Z4000" ).execute().get("values")

    autres = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

    auth = message.author.name

    charedited = 0

    tit = ""
    desc = ""
    foot = ""
    imgurl = None

    args = message.content.lower().rstrip(" ").split(" ", 3)

    fieldnames = ["Name", "Race", "Sex/Gender", "Pronouns", "Age", "Class", "Level", "Sheet", "Alignment", "Bio", "Sexuality", "Role", "Skin", "Hair", "Eye", "Height", "Weight", "Summary", "Image"]

    if len(args) <= 3 and not message.attachments:

        await message.channel.send(embed = discord.Embed(title = "Unable to edit character", description = "You didn't provide enough data!", colour = embcol))

    else:

        for a in range(len(fieldnames)):

            if args[2] == fieldnames[a].lower():

                for b in range(len(cargs)):

                    if auth in autres[b] and args[1].lower() in cargs[b][0].lower():

                        if message.attachments:

                            if args[2].lower() == "image":

                                sheet.values().update(spreadsheetId = CharSheet, range = str(colnum_string(a+7)) + str(b+1), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[message.attachments[0].url]])).execute()

                                print(message.author.name + " edited the image of " + cargs[b][0])

                                imgemb = discord.Embed(title = "Edited the image of " + cargs[b][0], description = "It is now:", colour = embcol)

                                imgemb.set_image(url = message.attachments[0].url)

                                await message.channel.send(embed = imgemb)

                        elif args[2] == "image":

                            sheet.values().update(spreadsheetId = CharSheet, range = str(colnum_string(a+7)) + str(b+1), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[message.content.split(" ", 3)[3]]])).execute()

                            imgemb = discord.Embed(title = "Edited the image of " + cargs[b][0], description = "It is now:", colour = embcol)

                            if not "|" in message.content.split(" ", 3)[3]:

                                imgemb.set_image(url = message.content.split(" ", 3)[3])

                            else:

                                imgemb.set_image(url = message.content.split(" ", 3)[3].split("|")[0])

                            await message.channel.send(embed = imgemb)

                            #await message.delete()

                            print(message.author.name + " edited the image of " + cargs[b][0] + " to a link")

                        else:
                                
                            sheet.values().update(spreadsheetId = CharSheet, range = str(colnum_string(a+6)) + str(b+1), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[message.content.split(" ", 3)[3]]])).execute()

                            #await message.delete()

                            print(message.author.name + " edited the " + fieldnames[a] + " of " + cargs[b][0])

                            await message.channel.send(embed = discord.Embed(title = "Edited the " + fieldnames[a] + " of " + cargs[b][0], description = "It is now:\n\n" + message.content.split(" ", 3)[3], colour  = embcol))

                        charedited = 1

                        cargs = sheet.values().get(spreadsheetId = CharSheet, range = "F" + str(b+1) + ":Z" + str(b+1) ).execute().get("values")

                        #for c in range(len(cargs[0])):

                        #indexupdateemb = discord.Embed(title = cargs[0][0], description = "Test", colour = embcol)

                        #print(str(cargs))

                        #print(cargs[0])

                        break

        if not charedited:

            if not args[2] in str(fieldnames):

                await message.channel.send(embed = discord.Embed(title = "Unable to edit character", description = "You didn't format it correctly. It's `%edit name **field** new data`", colour = embcol))

            else:

                await message.channel.send(embed = discord.Embed(title = "Unable to edit character", description = "Format this as `%edit <charname> <field> <edited data>` The character name and field should not contain spaces and the character name can be partial rather than full, so for example to edit the eye colour of Cleasa Sithitce, I would do: `%edit clea eye blue`", colour = embcol))



async def charedit2(message):

    fragments = message.content.split(" ")

    chardatabase = gc.open_by_key(CharSheet).get_worksheet(0) #These lines can be removed once we are no longer pulling from the sheet every time we need to update things.
    charreg = chardatabase.get_all_values()

    chars = []
    charindexes = []
    charregindex = ""
    field = ""
    newval = ""

    for a in range(len(charreg)):
        if charreg[a][1] == message.author.name:
            chars.append(charreg[a][5])
            charindexes.append(a)
    if len(chars) == 0:
        await message.channel.send(embed = discord.Embed(title = "You don't have any characters. Register one by going to https://discord.com/channels/828411760365142076/828412055228514325 and filling out their information."))

    else:
        if len(fragments) != 1: 
            if fragments[1] in str(chars): #Need to get fuzzy searching in here.
                chas = []
                for a in range(len(chars)):
                    if fragments[1] in chars[a]:
                        chas.append(charindexes[a])

                chas = list(dict.fromkeys(chas)) #Cull duplicates, ie if someone includes first and last names in command        
                if len(chas) == 1:
                    charregindex = charindexes[a]
                else:
                    charregindex = ""
                
                for b in range(len(fragments)):
                    for c in range(len(charreg[0][5:-3])):

                        if fragments[b].lower() == charreg[0][c+5].lower():
                            field = charreg[0][c+5]
                            attind = c+5
                            try:
                                if field != "Status":
                                    newval = message.content.split(" ", b+1)[b+1]
                            except IndexError:
                                newval = ""
                            break
            if charregindex == "": #If finding the typed character failed, use full process.
                fragments = [""]

        if len(fragments) == 1:
            userinp = int(await getsel(message, discord.Embed(title = "Which of your characters would you like to edit?", description = "Select them from the dropdown below:", colour = embcol).set_footer(text = "Paradesium Tip: " + random.choice(loadingtips)), chars))-1
            charregindex = charindexes[userinp]

        try:

            if field == "":
                chardata = []
                for a in range(len(charreg[0][5:-3])):
                    chardata.append(charreg[0][a+5] + ": " + charreg[charregindex][a+5])
                attind = int(await getsel(message, discord.Embed(title = "Which attribute would you like to edit?", description = "Here's our current entry for " + charreg[charregindex][5] + ":\n\n" + "\n".join(chardata), colour = embcol), charreg[0][5:-3]))+4
                field = charreg[0][attind]

            if field != "" and newval == "":
                try:
                    pronoun = charreg[charregindex][8].split("/")[1].lower().replace("him", "his")
                except IndexError:
                    pronoun = "their"
                if charreg[0][attind] != "Status":
                    if charreg[0][attind] != "Image":
                        await message.channel.send(embed = discord.Embed(title = "What should " + charreg[charregindex][5] + "'s new " + charreg[0][attind] + " be?", description= "Please type " + pronoun + " updated " + charreg[0][attind] + " below.", colour= embcol))
                    else:
                        await message.channel.send(embed = discord.Embed(title = "What should " + charreg[charregindex][5] + "'s new image(s) be?", description= "Please send " + pronoun + " updated images below, either attached to a message or as a hyperlink. If you are sending multiple images, they should all be attached to the same image, or should be links separated by pipe symbols (|).", colour= embcol))

                    try:
                        msg = await client.wait_for('message', check = checkstr(message.author))
                        if charreg[0][attind] != "Image":
                            newval = msg.content
                        else:
                            if msg.attachments:
                                imgs = []
                                for a in range(len(msg.attachments)):
                                    imgs.append(msg.attachments[a].url)
                                newval = "|".join(imgs)
                            else:
                                newval = msg.content

                    except asyncio.TimeoutError:
                        await message.channel.send("Selection Timed Out")
                        await message.delete()
                        return
                else:
                    statoptions = []
                    currentstat = charreg[charregindex][attind]

                    if currentstat == "Retired" and not "staff" in str(message.author.roles).lower():
                        await message.channel.send(embed = discord.Embed(title= "You cannot edit this value.", description= "You need a member of staff to unretire a character.", colour = embcol))

                    else:
                        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
                        additionalCharSlots = GlobalVars.economyData[author_row_index+2][1]
                        maxchars = startingslots + int(additionalCharSlots)

                        if len(chars) < maxchars:
                            if currentstat != "Unavailable":
                                statoptions.append("Unavailable")
                            if currentstat != "Active":
                                statoptions.append("Active")
                        else:
                            statoptions.append("Unavailable")

                        if currentstat != "Retired":
                            statoptions.append("Retired")
                        
                        if "staff" in str(message.author.roles).lower():
                            statoptions.append("DMPC")
                            statoptions.append("NPC")

                        try:
                            pronoun = charreg[charregindex][8].split("/")[1].lower().replace("him", "his")
                        except IndexError:
                            pronoun = "their"

                        statind = int(await getsel(message, discord.Embed(title = "What should " + charreg[charregindex][5] + "'s new status be?", description= "This controls whether their availability for things like starting new scenes. " + pronoun + "'s current Status is: " + currentstat + "\n\nSelect an option below.", colour= embcol), statoptions)-1)
                        newval = statoptions[statind]
        
        except AttributeError:
            newval = ""
            
        if newval != "":
            charreg[charregindex][attind] = newval
            chardatabase.update_cell(charregindex + 1, attind + 1, charreg[charregindex][attind])
            await message.channel.send(embed = discord.Embed(title = "Your changes have been made!", description = charreg[charregindex][5] + "'s " + charreg[0][attind] + " is now " + newval, colour = embcol))

async def getsel(message, emb, choices):
    sel = SelectView(message, 120, 1, 1, choices)
    await message.channel.send(embed = emb, view = sel)
    if await sel.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return("")
    return(int(sel.button_response[0]))

class SelectView(discord.ui.View):
    def __init__(self, message, timeout=120, optionamount=1, maxselectionamount = 1, namelist = []):
        super().__init__(timeout=timeout)
        self.button_response = []
        self.choices = []
        self.namelist = namelist
        self.message = message

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
            max_values = 1, # the maximum number of values that can be selected by the users
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


#Character Transfer Subroutine
async def chartransfer(message):
    
    #Get Message Author Name

    auth = message.author.name

    autres = sheet.values().get(spreadsheetId = CharSheet, range = "B2:B4000").execute()
    authvalues = str(autres.get("values"))
    authvalues = authvalues.replace("'","")
    pnames = authvalues.split(",")

    msgspl = message.content.split(" ", 4)

    pchars = None

    chartransferred = 0

    tit = None
    desc = ""
    foot = None
    imgurl = None

    for i in range(len(pnames)):

        if auth in pnames[i]:

            pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F" + str(i+2)).execute().get("values")
            
            pchars = str(pchars).replace("[","")
            pchars = str(pchars).replace("]","")
            pchars = str(pchars).replace("'","")

            #Test for char name in Name string
            #Allows partial name matches, so can just type a first name to match the full thing.

            if msgspl[1] in str(pchars):

                recipidpar = message.content.split("@")[1]

                recip ="<@" + recipidpar

                recipid = recipidpar.replace("!","")
                recipid = recipid.replace("&","")
                recipid = int(recipid.replace(">",""))

                recipname = await client.fetch_user(recipid)

                recipname = str(recipname).split("#")[0]

                if auth == recipname:

                    tit = "You cannot transfer a character to yourself"

                    chartransferred = 1

                else:

                    tit = "Transferred " + pchars + " to " + recipname

                    #Update Owner and Transfer Date

                    sheet.values().update(spreadsheetId = CharSheet, range = str("B" + str(i+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipname]])).execute()
                    sheet.values().update(spreadsheetId = CharSheet, range = str("D" + str(i+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[date.today().strftime("%d/%m/%Y")]])).execute()

                    #Test Recipient's Slots

                    pnames = str(sheet.values().get(spreadsheetId = CharSheet, range = "B2:B4000").execute().get("values")).replace("'","").split(",")
                    charstats = str(sheet.values().get(spreadsheetId = CharSheet, range = "X2:X4000").execute().get("values")).replace("'","").split(",")
                    origowner = str(sheet.values().get(spreadsheetId = CharSheet, range = "A2:A4000").execute().get("values")).replace("'","").split(",")

                    if origowner[i] == pnames[i]:

                        await client.get_channel(logchannel).send(str(message.author) + " just transferred a character to " + recipname + ", who was the original owner. This may be an attempt to circumvent the inability to un-retire characters. Check this channel to see if " + pchars + " should be retired.")

                    pcharsreg = 0

                    for g in range(len(pnames)):
                        if recipname in pnames[g]:
                            if g <= len(charstats):
                                if "Active" in charstats[g]:
                                    pcharsreg += 1

                    roles = str(str(message.author.roles))

                    player_econ_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
                    maxchars = startingslots + int(GlobalVars.economyData[player_econ_index + 2][1])

                    if pcharsreg > maxchars:
                        foot ="\n\n----------------------------------\n\n" + recipname + " does not have an available slot, so this character has been marked as Unavailable"
                        sheet.values().update(spreadsheetId = CharSheet, range = str("X" + str(i+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Unavailable"]])).execute()
                    else:
                        sheet.values().update(spreadsheetId = CharSheet, range = str("X" + str(i+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Active"]])).execute()

                    chartransferred = 1

                    imgurl = str(sheet.values().get(spreadsheetId = CharSheet, range = "Y" + str(i+2)).execute().get("values")).strip("[]").strip("'")

                    break
            
    if chartransferred == 0:

        tit = "You don't have a character called " + msgspl[1]

    if pchars == None:

        #Error message for no characters

        tit = "You have no characters registered"

    emb = discord.Embed(title = tit, description = desc, colour = embcol)

    if foot != None:
        emb.set_footer(text=foot)

    if imgurl != None:
        emb.set_thumbnail(url=imgurl)

    print(message.author.name + " transferred a character")

    await message.channel.send(embed = emb) 

    await message.delete()       

#Character List Subroutine
async def charlist(message):

    #Show character lists

    tit = None
    desc = None
    foot = None
    imgurl = None

    clist = []
    npclist = []

    targname = ""

    pcharsact = 0
    pcharsun = 0

    waitmess = await message.channel.send("We are processing your request now.")

    if not " " in message.content:
        message.content += " " + message.author.name

    if "help" in message.content.lower():
        message.content = "%help charlist"
        await helplist(message)
        return

    else:

        #Show other user's Characters

        pnames = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

        if "@" in message.content:

            targidpar = message.content.split("@")[1]

            targid = targidpar.replace("!","")
            targid = targid.replace("&","")
            targid = int(targid.replace(">",""))

            targname = await client.fetch_user(targid)

            targname = str(targname).split("#")[0]

        else: 

            targname = message.content.split(" ")[1]

        pindex = []

        for i in range(len(pnames)):
            if pnames[i][0].lower() == targname.lower():
                pindex.append(i)

        if pindex != []:
            charreg = sheet.values().get(spreadsheetId = CharSheet, range = "A1:AB" + str(pindex[-1]+1)).execute().get("values")
            for j in range(len(pindex)):

                #Get Char data
                cname = str(charreg[pindex[j]][5])
                cstat = str(charreg[pindex[j]][23])
                try:
                    cshort = str(charreg[pindex[j]][22])
                except IndexError:
                    cshort = None
                try:
                    npcplayers = str(charreg[pindex[j]][27])
                except IndexError:
                    npcplayers = None

                if cstat == "Active":
                    if cshort != None and cshort != "":
                        clist.append("**" + cname + "** - " + cshort)
                    else:
                        clist.append("**" + cname + "**")
                    pcharsact += 1
                elif cstat == "DMPC":
                    if npcplayers != None:
                        npclist.append("**" + cname + "** - " + cshort + " - DMPC\n   Also played by: " + npcplayers)
                    else:
                        npclist.append("**" + cname + "** - " + cshort + " - DMPC")
                else:
                    clist.append("~~" + cname + " (" + cstat + ")~~")
                    if cstat == "Unavailable":
                        pcharsun +=1

        if len(npclist) != 0:
            clist.append("-------------------------------------------------------------")
            for k in range(len(npclist)):
                clist.append(npclist[k])
        
        tit = targname + "'s Character List"

        if clist == []:
            desc = targname + " has no registered characters"
        else:
            desc = "\n\n".join(clist).strip("[]'")

    roles = str(str(message.author.roles))

    player_econ_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
    maxchars = startingslots + int(GlobalVars.economyData[player_econ_index + 2][1])


    emb = discord.Embed(title = tit, description = desc, colour = embcol)

    if str(message.author.name) == targname:
        if pcharsact == 1:
            if pcharsun == 0:
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active character, out of " + str(maxchars) + " slots." )
            elif pcharsun == 1:
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active character, and " + str(pcharsun) + " unavailable character (" + str(pcharsact + pcharsun) + " in total), out of " + str(maxchars) + " slots." )    
            else:
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active character, and " + str(pcharsun) + " unavailable characters (" + str(pcharsact + pcharsun) + " in total), out of " + str(maxchars) + " slots." )    
        else:
            if pcharsun == 0:        
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active characters, out of " + str(maxchars) + " slots." )
            elif pcharsun ==1:
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active characters, and " + str(pcharsun) + " unavailable character (" + str(pcharsact + pcharsun) + " in total), out of " + str(maxchars) + " slots." )    
            else:
                emb.set_footer(text = "-------------------------------------------------------------\n\n" + targname + " has " + str(pcharsact) + " active characters, and " + str(pcharsun) + " unavailable characters (" + str(pcharsact + pcharsun) + " in total), out of " + str(maxchars) + " slots." )    
    elif str(message.author.name) != targname:
        emb.set_footer(text = "-------------------------------------------------------------\n\nThis search was summoned by " + str(message.author.name))
    print(message.author.name + " summoned a charlist for " + targname)
    await message.channel.send(embed=emb)
    await message.delete()
    await waitmess.delete()

#Search Subroutine
async def charsearch(message, outputchannel):

    tit = None
    desc = None
    try:
        foot = "Searched for by " + message.author.name
        msgspl = message.content.split(" ")
    except AttributeError:
        foot = ""
        msgspl = message.split(" ")
    imgurl = ""
    imglen = 0

    cdata = ["\n"]

    charreg = sheet.values().get(spreadsheetId = CharSheet, range = "A1:AB4000", majorDimension='COLUMNS').execute().get("values")
    charreg2 = sheet.values().get(spreadsheetId = CharSheet, range = "A1:AB4000", majorDimension='ROWS').execute().get("values")
    cnames = charreg[5]
    pnames = charreg[1]
    cargs = sheet.values().get(spreadsheetId = CharSheet, range = "F1:AB4000" ).execute().get("values")

    searchedName = " ".join(msgspl[1:]).lower()

    if searchedName != None:  #Show only relevant shops if the searchedName was provided
        levenshtein_tuple_list = []
        index = 0
        for entry in charreg2:
            #Maybe do a combination of ratio and partial ratio here to favour stuff like collars appearing when "collar" is the search word?
            levenshtein_distance_partial = fuzz.partial_token_set_ratio(entry[5].lower(), searchedName.lower())
            levenshtein_distance_complete = fuzz.ratio(entry[5].lower(), searchedName.lower())
            levenshtein_distance = levenshtein_distance_complete * 0.5 + levenshtein_distance_partial * 0.5
            levenshtein_tuple_list.append([entry[5], levenshtein_distance, entry[1], index])
            index += 1

        sorted_list = sorted(levenshtein_tuple_list,key=lambda l:l[1], reverse=True)
        searchresults = [x[0::2] for x in sorted_list[:10]]

    count = 0
    multidata = []
    multindexes = []
    cindex = 0
    fieldappend = ""

    for f in str(searchedName.lower()):

        if ord(f) >= 97 and ord(f) <= 122 or f == " ":

            fieldappend += f
    
    searchedName = fieldappend
    optionsarray = []
    for c in range(len(searchresults)):
        optionsarray.append(f"{sorted_list[c][2]}'s {sorted_list[c][0]}")
    char_selection_view = EconomyV2.Dropdown_Select_View(message = message, timeout=30, optionamount=len(searchresults), maxselectionamount=1, namelist=optionsarray) #Only let them choose one item.
    charsel = []
    for c in range(len(searchresults)):
        charsel.append(f"`{str(c+1)}` - {searchresults[c][1]}'s {searchresults[c][0]}")
    emb = discord.Embed(title = "Which character would you like to see?", description = "Select the number of the one you want:\n" + "\n".join(charsel), colour = embcol)
    emb.set_footer(text = "This message will timeout in 30 seconds")
    await message.channel.send(embed = emb, view=char_selection_view)

    #Wait for reply
    if await char_selection_view.wait():
        await message.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
        return
    cindex = sorted_list[int(char_selection_view.button_response[0]) -1][3]

    for i in range(len(cnames)):
        if cindex > 0: #If index of character is known (from multiple selection, inputs it here)
            i = cindex
        elif cindex == -1: #If multiple selection failed, ends.
            break
        
        cname = str(cnames[i])
        tit = cname
        for j in range(len(headers)-1):
            try:
                carg = cargs[i][j]
            except IndexError:
                carg = ""
            if carg != "":
                if headers[j+1] == "Link":
                    pass
                elif headers[j+1] == "Approved":
                    cdata.append("Character sheet approved")
                elif headers[j+1] == "Players":
                    cdata.append("Also played by:" + carg)
                else:
                    cdata.append(headers[j+1] + ": " + carg)
            if headers[j+1] == "Image":
                if not "|" in carg:
                    imgurl = carg
                    imglen = 1
                else:
                    imgurl = carg.split("|")
                    imglen = carg.count("|") + 1
        try:
            foot = "---------------------------------------------------------\n\nOwned by " + str(pnames[i] + ". Searched for by " + message.author.name)
        except AttributeError:
            foot = ""
        break

    if cindex != -1:
        if cdata != None:
            desc = "\n".join(cdata)
        emb = discord.Embed(title = tit, description = desc, colour = embcol)
        if imgurl != "":
            if imglen == 1:
                emb.set_image(url=imgurl)
            else:
                emb.set_image(url=imgurl[0])
        if foot != None:
            emb.set_footer(text=foot)
        try:
            await outputchannel.send(embed=emb)
        except discord.errors.HTTPException:
            await outputchannel.send(embed=discord.Embed(title="Character couldn't be embedded",description="We refuse to write a whole library each time you search this character! (The character as a whole exceeds 4096 characters)\n\nIf this is not the case, it is likely that the image link has broken. Try editing the image, and if that doesn't work, contact the @bot gods.", colour = embcol))
            return
        if len(imgurl) > 1:
            for d in range(imglen-1):
                emb = discord.Embed(title = tit, description = "", colour = embcol)
                emb.set_image(url = imgurl[d+1])
                await outputchannel.send(embed=emb)
    try:
        await message.delete()
    except AttributeError:
        pass
    
#Retire Command
async def charretire(message):

    #Get Message Author Name

    auth = message.author.name

    autres = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

    pronounarg = sheet.values().get(spreadsheetId = CharSheet, range = "I1:I4000").execute().get("values")

    pnames = autres

    msgspl = message.content.split(" ")

    pchars = None

    charretired = 0

    tit = None
    desc = ""
    foot = None
    imgurl = None

    for i in range(len(pnames)):

        if auth == "C_allum" and "lalontra" in message.content.lower():

            await message.channel.send(embed = discord.Embed(title = "No, you do not.", description = "You're not allowed to do that.", colour = embcol))

            break

        elif auth in pnames[i] and charretired == 0:

            pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F" + str(i+1)).execute().get("values")[0][0]

            #Test for char name in Name string
            #Allows partial name matches, so can just type a first name to match the full thing.

            if msgspl[1].lower() in str(pchars).lower():

                sheet.values().update(spreadsheetId = CharSheet, range = str("X" + str(i+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Retired"]])).execute()

                await client.get_channel(logchannel).send(str(message.author) + " has retired " + pchars)

                tit = pchars + " has been retired"

                for a in range(len(headers)):

                    if headers[a] == "Pronouns":

                        if str(pronounarg[i]) != "[]":

                            if "/" in str(pronounarg[i][0]):
                                nouns = str(pronounarg[i][0]).split("/")
                                determiner = nouns[1].lower()
                                pronoun = nouns[0].lower()

                            else:
                                determiner = "them"
                                pronoun = "they"

                        else:
                            determiner = "them"
                            pronoun = "they"

                desc = pronoun.capitalize() + " will  be missed.\n\n----------------------------------\nTo undo this, speak to the moderator team"

                charretired = 1

            else:

                tit = "You don't have a character called " + msgspl[1]

        elif charretired == 0:

            tit = "You have no characters registered"

    emb = discord.Embed(title = tit, description=desc, colour = embcol)

    print(message.author.name + " retired a character")

    await message.channel.send(embed=emb)

    await message.delete()

#Activate Command
async def charactivate(message):

    #Get Message Author Name

    auth = message.author.name

    pnames = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

    msgspl = message.content.split(" ")

    tit = None
    desc = ""
    foot = None
    imgurl = None

    pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F1:F4000").execute().get("values")
    pstat = sheet.values().get(spreadsheetId = CharSheet, range = "X1:X4000").execute().get("values")

    charactivated = 0

    for i in range(len(pnames)):

        if auth in pnames[i] and charactivated == 0:

            #Test for char name in Name string
            #Allows partial name matches, so can just type a first name to match the full thing.

            if msgspl[1].lower() in str(pchars[i][0]).lower():

                charactivated = 1

                if pstat[i][0] == "Unavailable":

                    pcharsreg = 0

                    for g in range(len(pnames)):
                        if auth in pnames[g]:
                            if g <= len(pstat):
                                if "Active" in pstat[g]:
                                    pcharsreg += 1

                    roles = str(str(message.author.roles))

                    player_econ_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(message.author.id) in x][0])
                    maxchars = startingslots + int(GlobalVars.economyData[player_econ_index + 2][1])

                    if pcharsreg <= maxchars-1:

                        sheet.values().update(spreadsheetId = CharSheet, range = str("X" + str(i+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Active"]])).execute()

                        tit = pchars[i][0] + " has been set to active"

                        break

                    else:

                        tit = "You don't have enough slots to make " + pchars[i][0] + " active right now."

                        break

                elif pstat[i][0] == "Active":

                    tit = pchars[i][0] + " is already active"

                    break

                else:

                    tit = pchars[i][0] + " is retired. Speak to moderator if you want to bring them back in."

                    break

            else:

                tit = "You don't have a character called " + msgspl[1]

        elif charactivated == 0:

            tit = "You have no characters registered"

    emb = discord.Embed(title = tit, description=desc, colour = embcol)

    print(message.author.name + " activated a character")

    await message.channel.send(embed=emb)

    await message.delete()

#Deactivate Command
async def chardeactivate(message):

    #Get Message Author Name

    auth = message.author.name

    pnames = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

    msgspl = message.content.split(" ")

    tit = None
    desc = ""
    foot = None
    imgurl = None

    pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F1:F4000").execute().get("values")

    pstat = sheet.values().get(spreadsheetId = CharSheet, range = "X1:X4000").execute().get("values")

    chardeactivated = 0

    for i in range(len(pnames)):

        if auth in pnames[i] and chardeactivated == 0:

            #Test for char name in Name string
            #Allows partial name matches, so can just type a first name to match the full thing.

            if msgspl[1].lower() in str(pchars[i][0]).lower():

                chardeactivated = 1

                if pstat[i][0] == "Active":

                    sheet.values().update(spreadsheetId = CharSheet, range = str("X" + str(i+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Unavailable"]])).execute()

                    tit = pchars[i][0] + " has been set to unavailable"

                    break

                elif pstat[i][0] == "Unavailable":

                    tit = pchars[i][0] + " is already inactive"

                    break

                else:

                    tit = pchars[i][0] + " is retired. Speak to moderator if you want to bring them back in."

                    break

            else:

                tit = "You don't have a character called " + msgspl[1]

        elif chardeactivated == 0:

            tit = "You have no characters registered"

    emb = discord.Embed(title = tit, description=desc, colour = embcol)

    print(message.author.name + " deactivated a character")

    await message.channel.send(embed=emb)

    await message.delete()