from CommonDefinitions import *
import random
import CommonDefinitions
from TransactionsDatabaseInterface import updatePerson, printTransactions

async def staffVacation(message):
    #Toggle Lorekeeper chat Permissions
    perms = client.get_channel(LKVacationChannels[0]).overwrites_for(message.author)
    readMessages = perms.read_messages
    sendMessages = perms.send_messages
    author = message.author
    if "vacation" in str(message.author.roles).lower() and "lorekeeper" in str(message.author.roles).lower():
        if sendMessages == False and readMessages == False:
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            #await client.get_channel(LKChannel).category.set_permissions(message.author, overwrite=perms)
            #await client.get_channel(LKChannel).category.set_permissions(message.author, overwrite=None)
            for channel in LKVacationChannels:
                await client.get_channel(channel).set_permissions(message.author, overwrite=None)

        perms = client.get_channel(ModVacationChannels[0]).overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages
        if sendMessages == False and readMessages == False and "moderator" in str(message.author.roles).lower():
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            for channel in ModVacationChannels:
                await client.get_channel(channel).set_permissions(message.author, overwrite=None)
        role = discord.utils.get(author.guild.roles,name="Staff Vacation")
        await message.author.remove_roles(role)
        

    elif not("vacation" in str(message.author.roles).lower()) and "lorekeeper" in str(message.author.roles).lower():
        if sendMessages != True and readMessages != True:
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False

            #perms.send_messages = True
            #perms.read_messages = True
            #perms.view_channel = True
            for channel in LKVacationChannels:
                await client.get_channel(channel).set_permissions(message.author, overwrite=perms)

        perms = client.get_channel(ModVacationChannels[0]).category.overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages

        if sendMessages != False and readMessages != False and "moderator" in str(message.author.roles).lower():
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False
            for channel in ModVacationChannels:
                await client.get_channel(channel).set_permissions(message.author, overwrite=perms)



        
        role = discord.utils.get(author.guild.roles, name="Staff Vacation")
        print(role)
        await author.add_roles(role)

async def wildlust(message):
    if message.author.bot:
        auth = message.author.name
    elif message.author.nick:
        auth = message.author.nick
    else:
        auth = message.author.name
    lewdroll = random.randint(0,99)
    lewdtext = lewdtab[lewdroll]
    print(auth + " rolled on the lewd wild magic table")
    await message.delete()
    await message.channel.send(embed = discord.Embed(title= message.author.name + " rolled a " + str(lewdroll+1) + " on the Wild and Lustful Magic Table!", description= lewdtext, colour = embcol))

async def crunch(message):
    try:
        numbrolls = int(message.content.split(" ")[1])
    except IndexError:
        numbrolls = 1
    except TypeError:
        numbrolls = 1
    if numbrolls > 12:
        numbrolls = 12
    dezcost = numbrolls * 10
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ4000", majorDimension = 'ROWS').execute().get("values")
    authorindex = [row[0] for row in userinvs[::4]].index(message.author.name + "#" + message.author.discriminator)
    authorindex *= 4
    authorinv = userinvs[authorindex]
    if int(authorinv[1]) < dezcost:
        await message.channel.send(embed = discord.Embed(title= "You cannot afford this.", description= "It costs 10" + dezzieemj + " to find one of a suitable size to eat. You have only " + str(authorinv[1])))
    else:
        dezresults = []
        for a in range(numbrolls):
            rand = random.randint(0,9)
            if rand == 0:
                #Wildlust
                lustnum = random.randint(1,len(lewdtab))
                dezresults.append("You rolled a " + str(lustnum) + " on the wild magic table:\n" + lewdtab[lustnum])
            elif rand == 1:
                #Broken Tooth
                dezresults.append("You broke a tooth as you bit into the dezzie. " + random.choice(["These *are* rocks, after all.", "You may want to visit the clinic to fix that.", "The tooth fairy has been alerted to your position."]))
            elif rand == 2:
                #Mimic
                dezresults.append("The dezzie turns out to be a mimic. " + random.choice(["It bites back.", "It did not consent to voreplay.", "It seems to like being bitten.", "It tastes oddly metallic"]))
            elif rand == 3:
                #pass out
                dezresults.append(random.choice(["You awake 2 hours later, unaware of what transpired.", "You pass out for 2 hours", "You fall into a deep slumber, awakening about 2 hours later.", "The overwhelming sense of lust paralyses you for two hours."]))
            elif rand == 4:
                #Poisoned
                dezresults.append("Make a constitution save with a DC of 15. On a fail, you are poisoned for 6 hours.")
            elif rand == 5:
                #Change in senses
                dezresults.append(random.choice(["Everything appears slightly more purple.", "You can smell the odour of fresh sex.", "Everything tastes slightly saltier.", "Your egronious zones become more sensitive."]) + " This can only be undone by means of a greater restoration or wish spell")
            elif rand == 6:
                #Goblin transformation
                dezresults.append("Make an inhibition saving throw, with a DC of 14. On a failure, your skin turns pink and you are turned into a goblin for an hour.")
            elif rand == 7:
                #Nothing
                dezresults.append("Nothing seems to happen")
            elif rand == 8:
                #Orgy
                dezresults.append("You have the urge to start an orgy.")
            elif rand == 9:
                #Damage
                dezresults.append("You take 3d8 " + random.choice(["psychic", "bludgeoning", "poison", "piercing", "thunder"]) + random.choice([" damage.", " stimulation."]))
        await message.channel.send(embed = discord.Embed(title="You ate some dezzies!", description= "\n\n".join(dezresults), colour = embcol))
        sheet.values().update(spreadsheetId = EconSheet, range = "B" + str(authorindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[(int(authorinv[1]) - dezcost)]])).execute()
        await message.delete()

async def impTomeSpawn(message):
    tomeWeilder = await client.fetch_user(imptomeWielder)
    #await client.get_channel(logchannel).send(f"imp tome wielder {tomeWeilder.display_name} got notified that their tome got found.")
    outputchannel = await client.fetch_user(imptomeWielder)

    #This is a very good way of seeing how buttons work. You need to create a view class as you can see at the bottom of the code. 
    #In there we define our button, and behaviour of that button when clicked in the button_callback function. A message can carry a view
    view2 = ImpTomeView()
    sentmsg = await outputchannel.send(embed = discord.Embed(title = f"Hello {tomeWeilder.display_name}!", description = f"The imp tome possibly got found in the dungeon in channel {message.jump_url}. You have an hour to respond to this!", colour = embcol), view=view2)

    #This waits for either the button to be clicked, or for it to timeout (see impTomeView class.)
    await view2.wait()
    impTomeDescr = '''The air fills with the crackling of fire. A brimstone scent fills the air, and only a splitsecond later, a scarlet portal opens in the ceiling.
     Looking into it, there is an endless landscape of red rock, fires and towers made of bones here and there.
     You don't get a long look at it though, as a book falls out of the portal and hits the floor with a thump.
     It is a tome bound in leather, infernal symbols on it as well as lewd depictions of succubi, cambions and imps. What could possibly go wrong picking it up?'''
    #Check if the button was clicked, and the value therefore was set to true
    if view2.value == True:
        await message.channel.send(embed = discord.Embed(title = f"And infernal crackling appears...", description = impTomeDescr, colour = embcol))
    #If the button timed out, it will display this!
    else:
        await sentmsg.edit(embed = discord.Embed(title = f"Hello {tomeWeilder.display_name}", description = f"The imp tome possibly was found in the dungeon in channel {message.jump_url}. The timer expired and the scene probably moved on.", colour = embcol))
    
async def migrateAcc(message):

    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension = 'ROWS').execute().get("values")
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    charreg = sheet.values().get(spreadsheetId = CharSheet, range = "A2:AA2000", majorDimension='ROWS').execute().get("values")
    user = message.author
    newPlayerName = user.name
    try:
        if user.discriminator != "0" :
            await message.channel.send(embed = discord.Embed(title = f"{user.name}, you have to wait for your discord migration!", description = f"Your account is not been migrated to the new unique username system that discord introduced. Try again when you have your new username!"))
            return
    except:
        await message.channel.send(embed = discord.Embed(title = f"I can't access discriminators anymore. Contact Ken.", description = f"Something went wrong... Nothing critical, continuing"))

    if str(user.id) in str(kinkdata):
        playerIndex = [row[2] for row in kinkdata].index(str(user.id))
        oldPlayerName = kinkdata[playerIndex][1]
        oldPlayerNameSplit = oldPlayerName.split('#', 1)
        #Check if player is already migrated. If they are not, they will have a delimiter and the length of the split is 2
        if len(oldPlayerNameSplit) == 2:
            #replace the name in the kinklist. Nothing else needed here.
            kinkdata[playerIndex][1] = newPlayerName
            
            #Replace name in every character of the person
            for char in charreg:
                if str(char[0]) == str(oldPlayerNameSplit[0]):
                    char[0] = newPlayerName
                if str(char[1]) == str(oldPlayerNameSplit[0]):
                    char[1] = newPlayerName
            
            #merge the economy accounts
            oldEconomyIndex = -1
            for a in range(math.ceil((len(userinvs)-5)/4)):
                b = 4 * a + 5
                if str(oldPlayerName) == userinvs[b][0]:
                    oldEconomyIndex = b
                    break
            
            newEconomyIndex = -1
            for a in range(math.ceil((len(userinvs)-5)/4)):
                b = 4 * a + 5
                if str(newPlayerName + "#0") == userinvs[b][0]:
                    newEconomyIndex = b
                    break
            if oldEconomyIndex == -1 or newEconomyIndex == -1:
                await message.channel.send(embed = discord.Embed(title = "Not in Economy!", description = "Your new account name is not in the economy. Write something in OOC to get registered!"))
                return
            newBalance = int(userinvs[oldEconomyIndex][1]) + int(userinvs[newEconomyIndex][1])

            userinvs[oldEconomyIndex][1] = newBalance
            userinvs[oldEconomyIndex][0] = newPlayerName + "#0"
            del userinvs[newEconomyIndex:newEconomyIndex+4]
            
            #Fix the database
            updatePerson(oldPlayerName, newPlayerName)

            #write back the sheets
            rangeAll = 'A1:ZZ8000'
            body = {}
            sheet.values().clear(spreadsheetId = EconSheet, range = "Sheet2!"+rangeAll, body = body).execute()    #Delete the copy sheet
            sheet.values().update(spreadsheetId = EconSheet, range = "Sheet2!A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #save a copy
            
            sheet.values().clear(spreadsheetId = EconSheet, range = rangeAll, body = body).execute()    #Delete the sheet to rewrite if the copy is successful
            sheet.values().update(spreadsheetId = EconSheet, range = "A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute()
            sheet.values().update(spreadsheetId = kinksheet, range = "A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=kinkdata)).execute()
            sheet.values().update(spreadsheetId = CharSheet, range = "A2", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=charreg)).execute()
            await message.channel.send(embed = discord.Embed(title = f"{newPlayerName}: Migration completed!", description = "Your account is now migrated to the new Discord username system"))
        else:
            await message.channel.send(embed = discord.Embed(title = f"{newPlayerName} Migration not possible", description = f"Your account is probably already migrated. If that is not the case, please contact mods to resolve this."))
    else: 
        await message.channel.send(embed = discord.Embed(title = f"{newPlayerName} Migration not possible", description = f"You did not fill out your kinklist with us before changing to the new naming system. Please contact mods to resolve this."))

async def manualMigrateAcc(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension = 'ROWS').execute().get("values")
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    charreg = sheet.values().get(spreadsheetId = CharSheet, range = "A2:AA2000", majorDimension='ROWS').execute().get("values")
    newPlayerName = message.content.split()[1]
    oldPlayerName = message.content.split(" ", 2)[-1]

    localGuild = client.get_guild(828411760365142076)
    if localGuild != None:
        user = localGuild.get_member_named(newPlayerName)
    else: 
        user = client.get_guild(847968618167795782).get_member_named(newPlayerName)
    
    if oldPlayerName in str(userinvs):
        oldPlayerNameSplit = oldPlayerName.split('#', 1)
        skipkinklist = False
        try:
            playerIndex = [row[2] for row in kinkdata].index(str(user.id))
        except:
            await message.channel.send(embed = discord.Embed(title = "No Kinklist found", description = f"{oldPlayerName} doesn't have an entry in the kinklist - Skipping kinklist migration"))
            skipkinklist = True

        #Check if player is already migrated. If they are not, they will have a delimiter and the length of the split is 2
        if len(oldPlayerNameSplit) == 2:
            #replace the name in the kinklist. Nothing else needed here.
            if skipkinklist == False:
                kinkdata[playerIndex][1] = newPlayerName
            
            #Replace name in every character of the person
            for char in charreg:
                if str(char[0]) == str(oldPlayerNameSplit[0]):
                    char[0] = newPlayerName
                if str(char[1]) == str(oldPlayerNameSplit[0]):
                    char[1] = newPlayerName
            
            #merge the economy accounts
            oldEconomyIndex = -1
            for a in range(math.ceil((len(userinvs)-5)/4)):
                b = 4 * a + 5
                if str(oldPlayerName) == userinvs[b][0]:
                    oldEconomyIndex = b
                    break
            
            newEconomyIndex = -1
            for a in range(math.ceil((len(userinvs)-5)/4)):
                b = 4 * a + 5
                if str(newPlayerName + "#0") == userinvs[b][0]:
                    newEconomyIndex = b
                    break
            if oldEconomyIndex == -1 or newEconomyIndex == -1:
                await message.channel.send(embed = discord.Embed(title = "Not in Economy!", description = "Your new account name is not in the economy. Write something in OOC to get registered!"))
                return
            newBalance = int(userinvs[oldEconomyIndex][1]) + int(userinvs[newEconomyIndex][1])
            
            userinvs[oldEconomyIndex][1] = newBalance
            userinvs[oldEconomyIndex][0] = newPlayerName + "#0"
            sheetLen = math.ceil((len(userinvs)-5)/4) * 4 + 5
            del userinvs[newEconomyIndex:newEconomyIndex+4]
            
            #Fix the database
            updatePerson(oldPlayerName, newPlayerName)

            #write back the sheets - WE NEED TO COMPLETELY WIPE THE SHEET HERE BECAUSE LISTS ARE STUPID! IT HAS SOMETHING TO DO WITH DIFFERENT INVENTORY LENGTHS! ASK KEN IF SOMETHING COMES UP AND YOU AREN'T SURE
            rangeAll = 'A1:ZZ8000'
            body = {}
            sheet.values().clear(spreadsheetId = EconSheet, range = "Sheet2!"+rangeAll, body = body).execute()    #Delete the copy sheet
            sheet.values().update(spreadsheetId = EconSheet, range = "Sheet2!A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #save a copy
            
            sheet.values().clear(spreadsheetId = EconSheet, range = rangeAll, body = body).execute()    #Delete the sheet to rewrite if the copy is successful
            sheet.values().update(spreadsheetId = EconSheet, range = "A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #rewrite the econ sheet
            sheet.values().update(spreadsheetId = kinksheet, range = "A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=kinkdata)).execute()
            sheet.values().update(spreadsheetId = CharSheet, range = "A2", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=charreg)).execute()
            await message.channel.send(embed = discord.Embed(title = f"{newPlayerName}: Migration completed!", description = "Your account is now migrated to the new Discord username system"))
        else:
            await message.channel.send(embed = discord.Embed(title = f"{newPlayerName} Migration already completed", description = f"Your account is already migrated or {oldPlayerName} is not in the economy"))

async def regCommunityProject(message):
    #extract arguments
    split_message = message.content.split("-")
    name = split_message[1][:-1]
    description = split_message[2][:-1]
    amount_needed = split_message[3][:-1]
    fail_chance = split_message[4][:-1].replace("%", "")
    victory_message = split_message[5]

    #prepare data for the sheet
    projdata = sheet.values().get(spreadsheetId = Plotsheet, range = "AS1:AX200", majorDimension='ROWS').execute().get("values")
    new_proj = [name, amount_needed, fail_chance, 0, victory_message, ""]
    projdata.append(new_proj)
    

    #Create initial message and thread
    outputchannel = client.get_channel(communityProjectChannel)
    initial_message = await outputchannel.send(embed = discord.Embed(title = f"{name}", description = f"{description}", colour = embcol))
    await outputchannel.create_thread(name= name, message = initial_message)
    

    #Write into sheet and give feedback
    sheet.values().update(spreadsheetId = Plotsheet, range = "AS1:AX200", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=projdata)).execute()
    await message.channel.send(embed = discord.Embed(title = f"Success!", description = f"New community project generated", colour = embcol))



async def manualDezPoolReset(message):
    #Grab current date and time
    today = datetime.now()
    #Calculate new timestamp
    newResetDatetime = (today - timedelta(days=today.weekday()) + timedelta(days=7)).replace(hour=0, minute=0, second=0) #Takes todays date, subtracts the passed days of the week and adds 7, resulting in the date for next monday. Then replaces time component with 0
    newResetDateTimestamp = int(datetime.timestamp(newResetDatetime))

    #On reboot refresh dezzie pool of users
    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:A4000", majorDimension='ROWS').execute().get("values")

    for i in range(5, len(economydata)-1, 4):
        #Grab the name on the member
        try:
            name = economydata[i][0]
        except IndexError:
            print("Index error at: " + str(i) + ". Probably something broke in the economy sheet, and the registration of new people.")
        userStillOnServer = 1

        #Get Roles of the member. Attribute Error if they are not in the specified Guild (server)
        try:
            if len(name.split('#')[1]) == 4:
                roles = client.get_guild(828411760365142076).get_member_named(name).roles
            else:
                roles = client.get_guild(828411760365142076).get_member_named(name.split('#')[0]).roles
        except AttributeError:
            try:
                if len(name.split('#')[1]) == 4:
                    roles = client.get_guild(847968618167795782).get_member_named(name).roles
                else:
                    roles = client.get_guild(847968618167795782).get_member_named(name.split('#')[0]).roles
            except AttributeError:
                userStillOnServer = 0

            dezziePool = 0

        #If they aren't on the server anymore, we can just not refresh their dezzie pool.
        if userStillOnServer == 1:
            #Base values
            if "+3" in str(roles).lower():
                dezziePool = weeklyDezziePoolP3
            elif "+2" in str(roles).lower():
                dezziePool = weeklyDezziePoolP2
            elif "+1" in str(roles).lower():
                dezziePool = weeklyDezziePoolP1
            else:
                dezziePool = weeklyDezziePoolVerified
            #Bonus
            if "licensed fucksmith" in str(roles).lower():
                dezziePool += weeklyDezzieBonusFucksmith
            if "server booster" in str(roles).lower():
                dezziePool += weeklyDezzieBonusBoost
            if "server veteran" in str(roles).lower():
                dezziePool += weeklyDezzieBonusVeteran
            if "lorekeeper" in str(roles).lower() or "lorekeeper" in str(roles).lower() or "admin" in str(roles).lower():
                dezziePool = 100000
            if "patron tier 1" in str(roles).lower():
                dezziePool += weeklyDezzieBonusPatronT1
            if "patron tier 2" in str(roles).lower():
                dezziePool += weeklyDezzieBonusPatronT2
            if "patron tier 3" in str(roles).lower():
                dezziePool += weeklyDezzieBonusPatronT3
            if "cult of the mistress" in str(roles).lower():
                dezziePool += weeklyDezzieBonusPatronT3

        try:
            economydata[i+3][0] = dezziePool
        except IndexError:
            #Occurs when Dezzie pool is null. Initialize dezzie pool
            try:
                economydata[i+3] = [dezziePool]
            except IndexError:
                #Also triggers at the last person in the spreadsheet, as the cell is not just empty, but unreachable.
                pass


    #update dezzie pools
    sheet.values().update(spreadsheetId = EconSheet, range = "A1:A4000", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=economydata)).execute()

    print("Weekly Dezzie Award Pool Reset!")

#----------------View Classes----------------

#This is the view class for a simple accept button.
class ImpTomeView(discord.ui.View):
    #init initialises everything about the button. Here we give it a timeout, and a value so we know whether the button was pressed or not.
    def __init__(self):
        super().__init__(timeout=3600*2)
        self.value = None
    #This defines the button. The button_calback function defines what happened when we click it. We save the click in the variable to make sure
    # that we can later see if the button was actually pressed.´
    # The interaction.response is important as otherwise the interaction (button) will be seen as failed.
    # You can also silently acknowledge the interaction with interaction.response.defer()
    @discord.ui.button(label="Spawn Imp Tome!", style = discord.ButtonStyle.green)
    async def button_callback(self, interaction, item):
        await interaction.response.send_message("Imp tome spawning...")
        self.value = True
        self.stop()



#-----------------Helper functions-------------
async def uwutongue(message):
    chunks = message.content.split('"')
    result = []
    for a in range(len(chunks)):
        if (not chunks[a].startswith(" ")) and not chunks[a].endswith(" "):
            outputtext = []
            chunks[a] = chunks[a].lower()
            for b in range(len(chunks[a])):
                if chunks[a][b] == "l" or chunks[a][b] == "r":
                    outputtext.append("w")
                elif chunks[a][b] == "o" and (chunks[a][b-1] == "n" or chunks[a][b-1] == "m"):
                    outputtext.append("yo")
                elif random.randint(0,5) == 5 and chunks[a][b] == ".":
                    outputtext.append(random.choice([" owo", " uwu", " xD", " (*^.^*)", " 〜☆"]))
                else:
                    outputtext.append(chunks[a][b])
            result.append("".join(outputtext))
        else:
            result.append(chunks[a])
    return('"'.join(result))

async def beasttongue(message, animal):
    if animal.lower() == "dog":
        noises = ["woof", "ruf", "gruf", "yrif", "wruof"]
    elif animal.lower() == "cat":
        noises = ["meow", "mrrow", "mow", "nya", "mmeow", "rrrr", "grr", "mreeow"]
    elif animal.lower() == "horse":
        noises = ["neigh"]
    chunks = message.content.split('"')
    beastresult = []
    for a in range(len(chunks)):
        outputtex = []
        if (not chunks[a].startswith(" ")) and not chunks[a].endswith(" "):
            wordno = math.ceil(len(chunks[a])/6)
            for b in range(wordno):
                word = random.choice(noises)
                replacedword = ""
                for c in range(len(word)):
                    if random.randint(0,6) > 4:
                        for d in range(random.randint(1,4)):
                            replacedword += word[c]
                    else:
                        replacedword += word[c]
                newword = "".join(replacedword)
                outputtex.append("".join(newword).title())
            beastresult.append(" ".join(outputtex))
        else:
            beastresult.append(chunks[a])
    return('"'.join(beastresult))

async def getPlayerNameList():
    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension='ROWS').execute().get("values")
    playerList = []
    for a in range(math.floor(len(economydata)/4)):

        b = a * 4 + 5
        playerList.append(economydata[b][0])
    return playerList