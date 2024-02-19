from CommonDefinitions import *
import random
import CommonDefinitions
from TransactionsDatabaseInterface import updatePerson, printTransactions
from discord import Webhook
from discord import SyncWebhook
import aiohttp

async def staffVacation(message):
    #Toggle Lorekeeper chat Permissions
    perms = client.get_channel(GlobalVars.config["channels"]["staff_vacation_channels"][0]).overwrites_for(message.author)
    readMessages = perms.read_messages
    sendMessages = perms.send_messages
    author = message.author
    if "vacation" in str(message.author.roles).lower() and "staff" in str(message.author.roles).lower():
        if sendMessages == False and readMessages == False:
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            #await client.get_channel(LKChannel).category.set_permissions(message.author, overwrite=perms)
            #await client.get_channel(LKChannel).category.set_permissions(message.author, overwrite=None)
            for channel in GlobalVars.config["channels"]["staff_vacation_channels"]:
                await client.get_channel(channel).set_permissions(message.author, overwrite=None)

        perms = client.get_channel(GlobalVars.config["channels"]["mod_vacation_channels"][0]).overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages
        if sendMessages == False and readMessages == False and "mod team" in str(message.author.roles).lower():
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            for channel in GlobalVars.config["channels"]["mod_vacation_channels"]:
                await client.get_channel(channel).set_permissions(message.author, overwrite=None)
        role = discord.utils.get(author.guild.roles,name="Staff Vacation")
        await message.author.remove_roles(role)
        

    elif not("vacation" in str(message.author.roles).lower()) and "staff" in str(message.author.roles).lower():
        if sendMessages != True and readMessages != True:
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False

            #perms.send_messages = True
            #perms.read_messages = True
            #perms.view_channel = True
            for channel in GlobalVars.config["channels"]["staff_vacation_channels"]:
                await client.get_channel(channel).set_permissions(message.author, overwrite=perms)

        perms = client.get_channel(GlobalVars.config["channels"]["mod_vacation_channels"][0]).category.overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages

        if sendMessages != False and readMessages != False and "mod team" in str(message.author.roles).lower():
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False
            for channel in GlobalVars.config["channels"]["mod_vacation_channels"]:
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
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ8000", majorDimension = 'ROWS').execute().get("values")
    authorindex = [row[0] for row in userinvs[::4]].index(message.author.name)
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
    if imptomeWielder == -1: #If we currently don't have anyone that wants to use this function
        return
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

    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ8000", majorDimension='ROWS').execute().get("values")
    charreg = sheet.values().get(spreadsheetId = CharSheet, range = "A2:AA8000", majorDimension='ROWS').execute().get("values")
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
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")
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
    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:A8000", majorDimension='ROWS').execute().get("values")

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
                dezziePool = GlobalVars.config["economy"]["weeklydezziepoolplus3"]
            elif "+2" in str(roles).lower():
                dezziePool = GlobalVars.config["economy"]["weeklydezziepoolplus2"]
            elif "+1" in str(roles).lower():
                dezziePool = GlobalVars.config["economy"]["weeklydezziepoolplus1"]
            else:
                dezziePool = GlobalVars.config["economy"]["weeklydezziepoolverified"]
            #Bonus
            if "licensed fucksmith" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonusfucksmith"]
            if "server booster" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonusboost"]
            if "server veteran" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonusveteran"]
            if "staff" in str(roles).lower() or "mod team" in str(roles).lower() or "admin" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonusstaff"]
            if "patron tier 1" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonuspatront1"]
            if "patron tier 2" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonuspatront2"]
            if "patron tier 3" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonuspatront3"]
            if "cult of the mistress" in str(roles).lower():
                dezziePool += GlobalVars.config["economy"]["weeklydezziebonuspatront4"]

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
    sheet.values().update(spreadsheetId = EconSheet, range = "A1:A8000", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=economydata)).execute()

    print("Weekly Dezzie Award Pool Reset!")

async def copySheet(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")
    rangeAll = 'A1:ZZ8000'
    body = {}
    sheet.values().clear(spreadsheetId = EconSheet, range = "copysheet!"+rangeAll, body = body).execute()    #Delete the copy sheet
    sheet.values().update(spreadsheetId = EconSheet, range = "copysheet!A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #save a copy

async def removeZeroDiscriminators(message):
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension = 'ROWS').execute().get("values")
    rangeAll = 'A1:ZZ8000'
    body = {}
    sheet.values().clear(spreadsheetId = EconSheet, range = "copysheetZeroDiscrim!"+rangeAll, body = body).execute()    #Delete the copy sheet
    sheet.values().update(spreadsheetId = EconSheet, range = "copysheetZeroDiscrim!A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #save a copy

    #Remove #0 discriminators
    i = 5
    while i < len(userinvs):
        if userinvs[i][0].endswith('#0'):
            userinvs[i][0] = userinvs[i][0][:-2] #Cut last 2 characters, which are # and 0
        i+=4

    sheet.values().update(spreadsheetId = EconSheet, range = "Sheet1!A1", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=userinvs)).execute() #save a copy

#Dating Game
async def datingjoin(message):
    if not "private_thread" in str(message.channel.type):
        await message.channel.send("This is not a private thread.")
        return
    for source in datingprivatethreads:
        if str(message.channel.id) == str(source):
            await message.channel.send("This thread is already in the game. You may make another to use another of your characters.")
            return
    else:
        try:
            if not ((str(message.author) in str(datingplayers)) and  (str(message.content.split(" ", 1)[1]) in str(datingchars))):
                datingplayers.append(str(message.author))
                datingchars.append(str(message.content.split(" ", 1)[1]))
                datingprivatethreads.append(str(message.channel.id))
                await datingmatch(message)
            else:
                await message.channel.send(embed = discord.Embed(title = "This character is already in the game!", description= "You may start a thread for one of your other characters, or wait for a date to start", colour= embcol))

        except IndexError:
            await message.channel.send(embed = discord.Embed(title= "You need to enter by typing `%datingjoin` followed by your character's name.", description= "For example:\n\n`%datingjoin Lalontra`", colour = embcol))

async def datingrelay(message):

    if message.content.startswith("%"):
        return

    if str(message.channel) in str(datingsources):
        for a in range(len(datingsources)):
            if datingsources[a] == message.channel: #Find last source thread.
                b = a
        index = b

        if index % 2 == 0: #Get partner thread
            blindthread = datingsources[index+1]
            datcol = 0xfcb603
            person = random.choice(["Blind dater number 1", "Person 1", "Dater number 1", "Someone wearing blindfold 1"])
        else:
            blindthread = datingsources[index-1]
            datcol = 0x036bfc
            person = random.choice(["Blind dater number 2", "Person 2", "Dater number 2", "Someone wearing blindfold 2"])
        index = math.floor(index/2)
        if datingcounts[index] < datingmax:
            sendthreads = [datingdests[index], blindthread]

            dattit = random.choice([person + " sent a message!", "Message from " + person + "!", person + " says:"])
            await sendthreads[0].send(embed = discord.Embed(title = random.choice(["Your date sent a message!", "Message from your date!", "Your blind date says:"]), description= message.content + "\n\n*You have " + str(int(datingmax) - int(datingcounts[index]) - 1) + " messages left in this date.*", colour = datcol))
            await sendthreads[1].send(embed = discord.Embed(title = dattit, description= message.content + "\n\n*You have " + str(int(datingmax) - int(datingcounts[index]) - 1) + " messages left in this date.*", colour = datcol))
            datingcounts[index] += 1
            if datingcounts[index] == datingmax:
                await message.channel.send(embed = discord.Embed(title = "The date has now ended!", description= "You need to leave a rating for the date. Type an integer between 0 and 10.", colour  = embcol))
                await blindthread.send(embed = discord.Embed(title = "The date has now ended!", description= "You need to leave a rating for the date. Type an integer between 0 and 10.", colour  = embcol))
                await datingdests[index].send(embed = discord.Embed(title = random.choice(["Annnd... change!", "Next table, please!", "Time's up, onto the next one!", "That's all this date has time for!"]), description= "This date has now ended.", colour = embcol))
            await datingbackup()

        else:
            if datingscores[b] == -1: #Get score
                try:
                    datingscores[b] += int(message.content) + 1
                    if int(datingscores[b]) > 10 or int(datingscores[b]) < 0:
                        await message.channel.send(embed = discord.Embed(title = "You must type an integer between 1 and 10", description= "We're pretty sure that " + str(datingscores[b]) + " is not between 1 and 10. Try again.", colour = embcol))
                        datingscores[b] -= int(message.content) + 1
                    else:
                        await message.channel.send(embed = discord.Embed(title = "Thanks!", description= "These will be passed to the host, who will pair up the best matches at the end!", colour = embcol))
                        await datingmatch(message)
                    await datingbackup()
                except ValueError:
                    await message.channel.send(embed = discord.Embed(title = "You must type an integer between 1 and 10", colour = embcol))

async def datingmatch(message):
    if datingstate > 0:
        if random.randint(1,20) == 20:
            random.shuffle(datingwaiting)
        hasdated = 0
        for a in range(len(datingsources)):
            if datingsources[a] == message.channel:
                if a % 2 == 0 or a == 0:
                    b = a + 1
                else:
                    b = a - 1
                try:
                    if datingwaiting[0] == datingsources[b]:
                        hasdated = 1
                except IndexError:
                    pass
        if len(datingwaiting) == 0 or hasdated:
            await message.channel.send(embed = discord.Embed(title= "You have been added to the waiting list.", description= "We will notify you when a date becomes available.", colour = embcol))
            datingwaiting.append(message.channel)
            await datingbackup()
        else:
            datingsources.append(datingwaiting.pop(0))
            datingsources.append(message.channel)
            tabno = str(len(datingdests)+1)
            await datingbackup()
            dest = await client.get_channel(datingchannel).create_thread(name = "Date " + tabno, type = discord.ChannelType.public_thread)
            await dest.send(embed = discord.Embed(title=random.choice(["This is table " + tabno + "! It's reserved", "You can't sit here - they're on a *date*!", "This table - number " + tabno + " is reserved for our blindfolded dates", "Here we are, table " + tabno + ", ready for your blind date. How romantic!", "Let me guide you to your seats - oh, not there, that's your date's lap!", "Blindfolded dating. Such a good idea until you have to seat people. You're on table " + tabno + ". See if you can find it. No peeking!", "Such a cute couple. Shame we're the only ones that can see them."]), description= "This thread is only to be used for blind dating. Feel free to join the thread to view the messages, but we ask that you don't message here.\n\n To our contestants, messaging in your private thread will relay the message here. After 24 messages, the date will end and you will move on to the next one.", colour = embcol))
            datingdests.append(dest)
            datingcounts.append(0)
            datingscores.append(-1)
            datingscores.append(-1)
            for a in range(2):
                await datingsources[-(a+1)].send(embed = discord.Embed(title= "We have set up a date for you!", description= "Your blind date awaits on table " + str(len(datingdests)) + ".\n\nHere's a link to the thread. We don't advise joining it unless many people are as that could give away who you are.\n\n" + str(dest.jump_url) + "\n\nFrom now on, anything you type into this thread will be relayed to that thread, and we will post your blind date's replies here as well for you. Don't use a tupper, *especially* if your tupper includes the name of your character! Keep your messages brief to keep the game moving, but try to give your date enough to reply to!", colour = embcol))
            await datingbackup()

async def datingsetup(message):
    await message.channel.send(embed = discord.Embed(title = "Valentine's Day Blind Dating!", description= "Welcome to 2024's Valentine's day event: Blind dating! To join in, create a *private* thread in this channel, and type `%datingjoin` followed by your character's name. For example:\n\n`%datingjoin Lalontra`\n\nFeel free to follow any of the threads we open here, but don't message in them. At the end of the night, our host will reveal who matched best with who! Happy dating!", colour = embcol))
    await message.delete()

async def datingbackup():
    string = "|".join(datingplayers) + "\n\n"
    string += "|".join(datingchars) + "\n\n"
    for a in range(len(datingsources)):
        string += str(datingsources[a].id) + "|"
    string = string.lstrip("|") + "\n\n"
    for a in range(len(datingdests)):
        string += str(datingdests[a].id) + "|"
    string = string.lstrip("|") + "\n\n"
    if len(datingwaiting) == 0:
        string += "-"
    else:
        for a in range(len(datingwaiting)):
            string += str(datingwaiting[a].id) + "|"
    string = string.lstrip("|") + "\n\n"
    for a in range(len(datingscores)):
        string += str(datingscores[a]) + "|"
    string = string.lstrip("|") + "\n\n"
    for a in range(len(datingcounts)):
        string += str(datingcounts[a]) + "|"
    string = string.lstrip("|")     

    sheet.values().update(spreadsheetId = Plotsheet, range = str("AZ1"), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[string]])).execute()

async def datingrestorefromfile(message):
    with open('datingrecovery.txt') as f:
        string = f.read()
    f.close

    parts = string.split("\n\n")
    for a in range(len(parts[0].split("|"))):
        datingplayers.append(parts[0].split("|")[a])

    for a in range(len(parts[1].split("|"))):
        datingchars.append(parts[1].split("|")[a])

    for a in range(len(parts[2].split("|"))):
        datingsources.append(client.get_channel(datingchannel).get_thread(int(parts[2].split("|")[a])))

    for a in range(len(parts[3].split("|"))):
        datingdests.append(client.get_channel(datingchannel).get_thread(int(parts[3].split("|")[a])))

    if parts[4] != "-":
        for a in range(len(parts[4].split("|"))):
            datingwaiting.append(client.get_channel(datingchannel).get_thread(int(parts[4].split("|")[a])))
    else:
        datingwaiting = []

    for a in range(len(parts[5].split("|"))):
        datingscores.append(int(parts[5].split("|")[a]))

    for a in range(len(parts[6].split("|"))):
        datingcounts.append(int(parts[6].split("|")[a]))

    await message.channel.send(embed = discord.Embed(title = "Restore successful.", colour = embcol))

async def datingrestore(message):

    parts = message.content.split("\n\n")

    for a in range(len(parts[0].split("|"))):
        datingplayers.append(parts[0].split("|")[a])

    for a in range(len(parts[1].split("|"))):
        datingchars.append(parts[1].split("|")[a])

    for a in range(len(parts[2].split("|"))):
        datingsources.append(client.get_channel(datingchannel).get_thread(int(parts[2].split("|")[a])))

    for a in range(len(parts[3].split("|"))):
        datingdests.append(client.get_channel(datingchannel).get_thread(int(parts[3].split("|")[a])))

    if parts[4] != "-":
        for a in range(len(parts[4].split("|"))):
            datingwaiting.append(client.get_channel(datingchannel).get_thread(int(parts[4].split("|")[a])))
    else:
        datingwaiting = []

    for a in range(len(parts[5].split("|"))):
        datingscores.append(int(parts[5].split("|")[a]))

    for a in range(len(parts[6].split("|"))):
        datingcounts.append(int(parts[6].split("|")[a]))

    await message.channel.send(embed = discord.Embed(title = "Restore successful.", colour = embcol))

async def datingend(message):
    results = []
    for a in range(len(datingdests)):
        ind1 = datingsources.index(datingsources[a])
        ind2 = datingsources.index(datingsources[a+1])
        results.append("**" + str(datingchars[ind1]) + "** *and* **" + str(datingchars[ind2]) + "**: " + str(datingscores[ind1] + datingscores[ind2]))
        a += 1
    await message.channel.send(embed = discord.Embed(title = "The results are in, here are the final scores of the dating game!", description = "We advise just writing up the results and pairing off the highest scoring ones.\n\n" + "\n".join(results), colour = embcol))
    datingstate -= 1

async def datingmanual(message):
    threads = client.get_channel(datingchannel).threads
    threaddata = []
    await message.channel.send("Running. This will take a while.")

    ref = 0
    for a in range(len(threads)):
        if not "Gothica" in str(threads[a].owner):
            mess = [joinedMessages async for joinedMessages in threads[a].history(limit = None, oldest_first= True)]
            mess.sort(key=lambda x: x.created_at)
            dateno = []

            for b in range(len(mess)):
                if mess[b].content.lower().startswith("%datingjoin"):
                    char = mess[b].content.split(" ", 1)[1]
                if len(mess[b].embeds) == 1:
                    if mess[b].embeds[0].title == "Thanks!":
                        c = 0
                        embtit = mess[b-c].embeds[0].title
                        while embtit != "We have set up a date for you!":
                            c += 1
                            try:
                                embtit = mess[b-c].embeds[0].title
                            except IndexError:
                                pass
                        try:
                            dateno.append(str(mess[b-c].embeds[0].description.split(".")[0].split(" ")[-1]) + ": " + str(mess[b-c].embeds[0].description.split("are.")[1].split(" ")[0].rstrip("From")).lstrip().rstrip() + ", Rated: " + str(mess[b-1].content))
                        except IndexError:
                            dateno.append("N/A")

            threaddata.append(str(threads[a].owner) + ": **" + str(char) + "**\n\nDate Numbers:\n\n" + str("\n".join(dateno)) + "\n\nThread: " + str(threads[a].jump_url))
            await message.channel.send(threaddata[ref])
            ref += 1
    
            
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
    # You can also silently acknowledge the interaction with interaction.response.defer() - This makes the bot think it properly responded with "" for full invisibility.
    @discord.ui.button(label="Spawn Imp Tome!", style = discord.ButtonStyle.green)
    async def button_callback(self, interaction, item):
        await interaction.response.send_message("Imp tome spawning...")
        self.value = True
        self.stop()

#----------------Tour View Buttons----------------

class TourView0(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[0], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        print(self)
        print(component)
        print(btn)
        #await Tourparser(btn.user, 0, TourView1())

class TourView1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[1], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        print(self)
        print(component)
        print(btn)
        #await Tourparser(btn.user, 1, TourView2())

class TourView2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[2], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        await Tourparser(btn.user, 2, TourView3())

class TourView3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[3], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        await Tourparser(btn.user, 3, TourView4())

class TourView4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[4], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        await Tourparser(btn.user, 4, TourView5())

class TourView5(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label=Tourbuttontext[5], style = discord.ButtonStyle.green, custom_id = "TourButton")
    async def tourbutton_callback(self, component, btn):
        await Tourparser(btn.user, 5, None)

async def Tourparser(presser, stage, tourview):
    await client.get_channel(TourLocations[stage]).send("<@" + str(presser.id) + ">")
    if tourview != None:
        await client.get_channel(TourLocations[stage]).send(embed = discord.Embed(title = TourNames[stage], description = str(TourDescriptions[stage]) + "\n<#" + str(TourLocations[stage+1]) + ">", colour = embcol), view = tourview)
    else:
        await client.get_channel(TourLocations[stage]).send(embed = discord.Embed(title = TourNames[stage], description = TourDescriptions[stage], colour = embcol))

#Yes, it's unbearably clunky. If I could have an array of classes, that would make this system amazing.

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
    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ8000", majorDimension='ROWS').execute().get("values")
    playerList = []
    for a in range(math.floor(len(economydata)/4) -1):

        b = a * 4 + 5
        playerList.append(economydata[b][0])
    return playerList

async def export(message):

    if message.author.bot:
        return

    dest = message.content.split(" ")[1]
    processing = await message.channel.send(embed = discord.Embed(title="Processing", description= "This may take some time, depending on the length of the channel.", colour=embcol))

    try:
        int(dest)
        dest = "<#" + str(dest) + ">"
    except ValueError:
        pass

    if "doc" in dest.lower() or "sheet" in dest.lower():
        desttype = "Spreadsheet"
        try:
            if "docs.google.com/spreadsheets" in dest.lower():
                dest = gc.open_by_url(dest)
            elif "staff" in str(message.author.roles).lower() and "@" in message.content.split(" ")[2]:
                dest = gc.create(message.channel.name)
                recip = message.content.split(" ")[2]
            else:
                await message.channel.send(embed = discord.Embed(title = "You need to provide the link to an editable document.", description= "", colour = embcol))
                return
        except IndexError:
            await message.channel.send(embed = discord.Embed(title = "You need to provide an email address to add to the spreadsheet.", description= "The API doesn't support setting it to public, so we need to share the sheet with you via email.", colour = embcol))
            return
        
    elif dest.lower().startswith("https://discord.com/channels") or dest.startswith("<#"):

        dest = client.get_channel(int(str(message.content.split(" ")[1].split("/")[-1]).rstrip(">").lstrip("<#")))

        if "thread" in str(dest.type) and ("staff" in str(message.author.roles).lower() or str(dest.owner) == str(message.author)):
            desttype = "Thread"
            hook = await dest.parent.create_webhook(name= "Exporthook")
        elif "staff" in str(message.author.roles).lower():
            desttype = "Channel"
            hook = await dest.create_webhook(name= "Exporthook")
        else:
            await message.channel.send(embed = discord.Embed(title = "You cannot write to that thread.", description= "Only Staff members can write to threads that they did not create", colour= embcol))
            return
        
    elif dest.lower() == "file":
        dest = "File"
        desttype = "File"

    else:
        await message.channel.send(embed = discord.Embed(title = "Output format not recognised.", description = "Options to output to are:\n\nGoogle Sheet; providing a link to an editable spreadsheet.\n\nDiscord Threads; providing the link, #-link or ID of the thread to write to. Unless you are staff, this must be a thread you have created.\n\nA text file, in which case you would use `%export file`.", colour = embcol))
        return

    await message.delete()

    mess = [joinedMessages async for joinedMessages in message.channel.history(limit = None, oldest_first= True)]
    mess.sort(key=lambda x: x.created_at)

    sheetarray = [["Author", "Content", "Avatar Link", "Timestamp", "Character Count", "Wordcount"]]
    textarray = []
    charcount = []
    wordcount = []

    if desttype == "Spreadsheet" or desttype == "File":
        for a in range(len(mess)):

            if mess[a] == message or mess[a] == processing:
                break

            if len(mess[a].content) != 0:
                #Sheet Layout:
                sheetarray.append([str(mess[a].author).split("#")[0], str(mess[a].content), str(mess[a].author.avatar), str(mess[a].created_at).split(".")[0], str(len(mess[a].content)), str(len(mess[a].content.split(" ")))])
                #Text file Layout:
                textarray.append(str(mess[a].author).split("#")[0] + ": " + str(mess[a].content))
            else:
                if mess[a].embeds != 0:
                    #Sheet Layout:
                    sheetarray.append([str(mess[a].author).split("#")[0], (str(mess[a].embeds[0].title) + "\n\n" + str(mess[a].embeds[0].description)), str(mess[a].author.avatar), str(mess[a].created_at).split(".")[0], str(len(mess[a].content)), str(len(mess[a].content.split(" ")))])
                    #Text file Layout:
                    textarray.append(str(mess[a].author).split("#")[0] + ": " + (str(mess[a].embeds[0].title) + "\n\n" + str(mess[a].embeds[0].description)))
            charcount.append(len(mess[a].content))
            wordcount.append(len(mess[a].content.split(" ")))

        if desttype == "Spreadsheet":
            sheetarray.append(["Total", "", "", str(mess[-3].created_at-mess[0].created_at).split(".")[0], sum(charcount), sum(wordcount)])
            sheetarray.append(["Average", "", "", "", sum(charcount)/(len(mess)), sum(wordcount)/(len(mess))])
            ws = dest.get_worksheet(0)
            ws.update("A1:F" + str(len(mess)+3), sheetarray)
            await message.channel.send(embed = discord.Embed(title = "Channel written to Spreadsheet.", description = "The contents of this channel have been cloned to a spreadsheet, available at:\n\nhttps://docs.google.com/spreadsheets/d/" + str(dest.id), colour = embcol))
            dest.share(recip, perm_type = "user", role = "writer")
        else:
            filename = str(message.channel) + ".txt"
            with open(filename, "w") as f:
                f.write("\n\n".join(textarray))
            f.close()
            await message.channel.send("We have attached a text log of this channel.", file = discord.File(r"" + filename))
            os.remove(filename)

    else:
        lock = asyncio.Lock()
        async with aiohttp.ClientSession() as session:
            whook = SyncWebhook.from_url(hook.url)

            for b in range(len(mess)):
                if mess[b] == message or mess[b] == processing:
                    break
                else:
                    try:
                        whook.send(mess[b].content, username = mess[b].author.name, avatar_url = mess[b].author.avatar, thread = dest)
                    except discord.errors.HTTPException:
                        whook.send(mess[b].content, username = mess[b].author.name, avatar_url = mess[b].author.avatar)

                    if mess[b].attachments:
                        for c in range(len(mess[b].attachments)):
                            try:
                                whook.send(mess[b].attachments[c].url, username = mess[b].author.name, avatar_url = mess[b].author.avatar, thread = dest)
                            except discord.errors.HTTPException:
                                whook.send(mess[b].attachments[c].url, username = mess[b].author.name, avatar_url = mess[b].author.avatar)
                                
                    if mess[b].embeds:
                        try:
                            whook.send(embed= mess[b].embeds[0], username = mess[b].author.name, avatar_url = mess[b].author.avatar, thread = dest)
                        except discord.errors.HTTPException:
                            whook.send(embed= mess[b].embeds[0], username = mess[b].author.name, avatar_url = mess[b].author.avatar)

        await hook.delete()
    await processing.delete()

