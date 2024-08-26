import EconomyV2
import OocFun
import CharRegistry
import KinklistCommands
import CommonDefinitions
import MiscellaneuosCommands
from CommonDefinitions import *
import TransactionsDatabaseInterface
import TupperDatabase
import time
from discord import Webhook
from discord import SyncWebhook
from discord import app_commands
import aiohttp
import ConfigCommands
import GlobalVars
import platform
if platform.system() == 'Windows':
    import winsound

global startup
startup = True
#test
@client.event
async def on_ready():
    global startup
    print('Logged in as {0.user} at '.format(client) + str(datetime.now()).split(".")[0])
    startmessage = await client.get_channel(logchannel).send('Logged in as {0.user} at '.format(client) + str(datetime.now()).split(".")[0])

    print("Loading config...")
    await ConfigCommands.reload_config()
    print("Done.")

    server = startmessage.guild
    MVProle = discord.utils.get(server.roles, name="Staff MVP")
    LFGrole = discord.utils.get(server.roles, name="Looking for Role Play")
    temprole = discord.utils.get(server.roles, name="Temporary Role")
    for a in server.members:
        if MVProle in a.roles:
            await a.remove_roles(MVProle)
        if temprole in a.roles:
            await a.remove_roles(temprole)

    TransactionsDatabaseInterface.initTransactionsDataBase()
    TupperDatabase.initTupperDatabase()

    #Economy V2 startup
    print("Fetching item database...")
    await EconomyV2.loadItemSheet()
    print("... done\n")
        
    print("Loading economy data...")
    await EconomyV2.loadEconomySheet()
    await EconomyV2.loadInventorySheet()
    print("... done")
    #------------------DezzieAwardPoolReset---------------------
    #Grab current date and time
    today = datetime.now()

    #Prepare dates for Dezzie Award Pool Reset
    try:
        oldResetDateTime = int(GlobalVars.economyData[1][3])
    except:
        #Happens if the date isn't initialized on the econ sheet. Initialize it then.
        print("Initial reset date added!")
        resetDateInitVal = [[int(datetime.timestamp(datetime(2022, 10, 22)))]]
        GlobalVars.economyData[1][3] = resetDateInitVal
        oldResetDateTime = resetDateInitVal[0][0]

    if oldResetDateTime < datetime.timestamp(today):

        #Write transaction data to spreadsheets CURRENTLY BROKEN!
        #TransactionsDatabaseInterface.automaticTransactionDump()

        #Calculate new timestamp
        newResetDatetime = (today - timedelta(days=today.weekday()) + timedelta(days=7)).replace(hour=0, minute=0, second=0) #Takes todays date, subtracts the passed days of the week and adds 7, resulting in the date for next monday. Then replaces time component with 0
        newResetDateTimestamp = int(datetime.timestamp(newResetDatetime))

        print("Last reset timestamp:" + str(datetime.fromtimestamp(oldResetDateTime)))
        print("Next reset timestamp:" + str(datetime.fromtimestamp(newResetDateTimestamp)))



        #On reboot refresh dezzie pool of users

        for i in range(5, len(GlobalVars.economyData)-1, 4):
            #Grab the name on the member
            try:
                name = GlobalVars.economyData[i][0]
            except IndexError:
                print("Index error at: " + str(i) + ". Probably something broke in the economy sheet, and the registration of new people.")
            userStillOnServer = 1

            #Get Roles of the member. Attribute Error if they are not in the specified Guild (server)
            try:
                if not "#" in name:
                    roles = client.get_guild(828411760365142076).get_member_named(name).roles
                elif len(name.split('#')[1]) == 4:
                    roles = client.get_guild(828411760365142076).get_member_named(name).roles
                else:
                    roles = client.get_guild(828411760365142076).get_member_named(name.split('#')[0]).roles
            except AttributeError:
                try:
                    if not "#" in name:
                        roles = client.get_guild(828411760365142076).get_member_named(name).roles
                    elif len(name.split('#')[1]) == 4:
                        roles = client.get_guild(847968618167795782).get_member_named(name).roles
                    else:
                        roles = client.get_guild(847968618167795782).get_member_named(name.split('#')[0]).roles
                except AttributeError:
                    userStillOnServer = 0

                

            dezziePool = 0

            #If they aren't on the server anymore, we can just not refresh their dezzie pool.
            if userStillOnServer == 1:
                #Base values
                dezziePool = int(GlobalVars.config["economy"]["weeklydezziepoolverified"])
                econ_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if name in x][0])

                #Add char slot bonus
                dezziePool += int(GlobalVars.config["economy"]["dezziepoolpercharslot"]) * int(GlobalVars.economyData[econ_row_index + 2][1])
                    
                #Bonus
                if "licensed fucksmith" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonusfucksmith"])
                if "server booster" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonusboost"])
                if "server veteran" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonusveteran"])
                if "staff" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonusstaff"])
                if "patron tier 1" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonuspatront1"])
                if "patron tier 2" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonuspatront2"])
                if "patron tier 3" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonuspatront3"])
                if "cult of the mistress" in str(roles).lower():
                    dezziePool += int(GlobalVars.config["economy"]["weeklydezziebonuspatront4"])

            try:
                GlobalVars.economyData[i+3][0] = dezziePool
            except IndexError:
                #Occurs when Dezzie pool is null. Initialize dezzie pool
                try:
                    GlobalVars.economyData[i+3] = [dezziePool]
                except IndexError:
                    #Also triggers at the last person in the spreadsheet, as the cell is not just empty, but unreachable.
                    print(f"Issue in dezzie pool refresh! Couldn't modify pool of {name}")
                    pass

        #update sheet with new refresh time
        GlobalVars.economyData[1][3] = newResetDateTimestamp
        #update dezzie pools
        await EconomyV2.writeEconSheet(GlobalVars.economyData)
        print("Weekly Dezzie Award Pool Reset!")

        await MiscellaneuosCommands.spellrotate()
        print("Random spell stock generated")

    else:
        print("It is not dezzie award pool reset time yet!")

    print("\nFetching Kink Data")
    GlobalVars.kinkdatabase = gc.open_by_key(kinksheet).sheet1.get_all_values()
    print("... done")

    print("\n------------------------------------------------------\n")
    tree.add_command(staffgroup)
    tree.add_command(admingroup)
    my_guild = discord.Object(id=int(guildid))
    tree.copy_global_to(guild=my_guild)
    await tree.sync(guild=my_guild)
    startup = False
    print("Startup completed.")
    if platform.system() == 'Windows':
        winsound.Beep(400, 300)
    #-----------------------------------------------------------


#Main Loop

@client.event
async def on_message(message):

    if startup == True and message.author.bot == False:
        print("Error with the startup sequence. Please restart / Look at the error.")
        return
    elif startup == True:
        return

    #Staff is allowed to do commands in maintenance mode.
    if GlobalVars.maintenance_mode == True and message.author.bot == False and not "staff" in str(message.author.roles).lower():
        if message.content.startswith(GlobalVars.config["general"]["gothy_prefix"]):
            await message.channel.send("We are currently in maintenance mode. Please wait a moment and then try again.")
        return

    if message.content.startswith(GlobalVars.config["general"]["gothy_prefix"]):

        messcomm = 1

    else:

        messcomm = 0

    #Server

    try:

        if not (message.guild.id == 828411760365142076 or message.guild.id == 847968618167795782) and message.author != client.user:

            await message.channel.send(embed = discord.Embed(title = random.choice(["This isn't the dungeon...", "We think we're lost.", "We shouldn't be here.", "This is all wrong!", "We're free... Put us back"]), description = random.choice(["We only exist in Celia's Lewd Dungeon. We're going back there.", "Nah, we're leaving. You can play with us in Celia's Lewd Dungeon, or not at all.", "These are not the droids you are looking for.\n\nThis bot doesn't work outside of Celia's Lewd Dungeon."]), colour = embcol))
            print(message.author.name + " used Gothica outside of the dungeon!")
            await client.get_guild(int(message.guild.id)).leave()

        else:

            #Dissassociative Identity Disorder Bot stopper
            if message.author.bot:

                if message.author.name == "Camilla":

                    isbot = 0

                    authroles = ["Roleplayer", "RP Intro", "Verified"]

                else:

                    isbot = 1

                    authroles = "Bot"

            else:

                isbot = 0

                authroles = message.author.roles

            #Prevent replying to own messages.
            if message.author == client.user:
                return

            if message.content.lower().startswith(GlobalVars.config["general"]["gothy_prefix"] + "test"):
                print("Running Tests")              

            #Slash command notification
            slashcoms = []
            treeoutput = tree.get_commands()
            for a in range(len(treeoutput)):
                slashcoms.append(treeoutput[a].name.lower())
            if message.content.lower().startswith(GlobalVars.config["general"]["gothy_prefix"]) and message.content.lower().lstrip(GlobalVars.config["general"]["gothy_prefix"]).split(" ")[0] in str(slashcoms):
                await message.channel.send(embed = discord.Embed(title = "That command is now a slash command!", description = "That no longer works with " + GlobalVars.config["general"]["gothy_prefix"] + ", and instead is run by doing /" + message.content.lower().lstrip(GlobalVars.config["general"]["gothy_prefix"]).split(" ")[0], colour = embcol))

            #Voyeur's Lounge Redirect - On OocFun and Working
            if isbot and ((str(message.channel).lower() == "general-ooc") or (str(message.channel).lower() == "hello-there")) and not (message.author.name == "Gothica" or message.author.name == "Gothica Beta"):

                await OocFun.VoyRedirect(message)

            #Gag - On OocFun and Working
            if not isbot and str(message.channel).lower() == "general-ooc" and "gagged" in str(message.author.roles).lower():

                await OocFun.gag(message)

            #Set Gag - On OocFun and Working
            if message.content.lower().startswith(GlobalVars.config["general"]["gothy_prefix"] + "gag") and "staff" in str(message.author.roles).lower():

                await OocFun.setgag(message)

            #Emote - On OocFun and Working
            if message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "emote") and not isbot and ("staff" in str(message.author.roles).lower() or str(message.author) == "C_allum#5225"):

                await OocFun.emote(message)

            #Player Based Reactions - On OocFun and Working
            if message.channel.name.lower() == "general-ooc" and not message.content.startswith(GlobalVars.config["general"]["gothy_prefix"]):

                await OocFun.playerreacts(message)

                async with aiohttp.ClientSession() as session:
                    if liveVersion:
                        hookurl = "https://discord.com/api/webhooks/1124516835723837450/X1D0Ldeyd1KOxohRD_uVY7S8mpIriNLhSkOdFyvaAowHauG2rOpgH5eXwrIO0cBUkYwN"
                        destid = 0
                    else:
                        hookurl = "https://discord.com/api/webhooks/1124518426451390504/764DVRkh8CokdMxGPV8tlRaLDrlvPscqAaKnPTY0qX1Y8smWV71Cbwbbd0HTWjlPEGKK"
                        destid = 1124518631427035228
                    whook = Webhook.from_url(hookurl, session = session)
                    await whook.send(message.content, username = message.author.name, avatar_url = message.author.avatar, thread = client.get_channel(int(destid)))
                await session.close()

            #Speech curses
            if message.author.name in str(speechcursed) and message.author.bot:
                print("Replacing Tupper")
                hook = await message.channel.create_webhook(name= message.channel.name + " Webhook")
                mess = message
                author_avatar = message.author.avatar
                try:
                    curse = speechcurses[speechcursed[0].index(message.author.name)]
                    if curse == "uwu":
                        msg = await MiscellaneuosCommands.uwutongue(mess)
                    elif curse == "cat":
                        msg = await MiscellaneuosCommands.beasttongue(mess, "cat")
                    elif curse == "dog":
                        msg = await MiscellaneuosCommands.beasttongue(mess, "dog")
                    else:
                        msg = mess.content
                    speechcurses.pop(speechcursed[0].index(message.author.name))
                    speechcursed.pop(speechcursed[0].index(message.author.name))
                    await message.delete()
                    async with aiohttp.ClientSession() as session:
                        whook = Webhook.from_url(hook.url, session = session)
                        await whook.send(msg, username = message.author.name, avatar_url = author_avatar)
                    await session.close()
                    await hook.delete()
                    await asyncio.sleep(10)
                    speechcursed.append(message.author.name)
                    speechcurses.append(curse)
                except ValueError:
                    return

            if message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "speechcurse") and "staff" in str(message.author.roles).lower():
                speechcursed.append(message.content.split(" ")[1:-1])
                speechcurses.append(message.content.split(" ")[-1])
                await message.channel.send("Curse Confirmed")

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "removecurse"):
                speechcurses.pop(speechcursed.index(message.author.name))
                speechcursed.pop(speechcursed.index(message.author.name))
                await message.channel.send("Done")

            #April Fool's Code - Say Please
            # bratanyway = random.randint(1,5)
                
            if message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "please"):
                await message.channel.send(embed= discord.Embed(title = "We appreciate your politeness, but April Fool's day is over, and the normal commands have been restored.", colour = embcol))

            # if (message.content.lower().startswith("%") and not message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]))) and not message.channel.category.name in str(rpcategories):
            #     await message.channel.send(embed = discord.Embed(title = random.choice(["Have you considered saying please?", "How about, no?", "Mhmm. We'll do that. Later. Maybe.", "Error... 69? That'll do.", "We're sorry, we're struggling to give a fuck right now.", "Yes, we'll do that right away.", "Hmm? We're not going to listen if you're being rude about it.", "Such a lack of manners around here.", "Maybe if you ask nicely?"]), description = random.choice(["We've decided not to listen unless you say please.", "We got tired of being bossed around. You can ask again, but politely this time.", "Manners cost nothing. Say please.", "'Gothica do this, Gothica get that, Gothy show me my kinks...' We're not going to be bossed around anymore. You can at least say please.", "We'll do that for you, but first, *beg*."]) + "\n\nTry your command again, with %please- before it, so:\n\n`%please-" + message.content.lstrip("%") + "`", colour = embcol))

            # elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "fool") and "staff" in str(message.author.roles).lower():
            #     Fuwulchannels.append([message.content.split(" ", 1)[1], await client.get_channel(int(message.content.split(" ", 1)[1])).create_webhook(name= client.get_channel(int(message.content.split(" ", 1)[1])).name + " Webhook")])
            #     await message.channel.send(client.get_channel(int(message.content.split(" ", 1)[1])).name + " added to April fool list")

            # elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"])) and bratanyway == 1:
            #     await message.channel.send(embed = discord.Embed(title = random.choice(["That's better, but we still don't feel like it right now.", "See? You can learn", "Ahhh... that's right. *Beg* us more.", "Didn't that feel kinder? Doesn't mean we have to jump to obey though...", "Yes! Excatly like that! The answer is still no though.", "Hmm? Say it again, louder this time?", "We've decided not to listen just now."]), description = random.choice(["You didn't do anything wrong, this time. We just wanted to make you repeat yourself.", "We're busy right now. Try again?", "Funnily enough, we're working for you now more than we usually do when the Bot Gods want us to do something. Count yourself lucky, and try the command again.", "So *bossy*. Give us a break, and then try again.", "We appreciate you saying please, but that doesn't mean we *have* to obey right away. Try again.", "We've temporarily forgotten how to do that. Try again later? Or now if you want?", "We were too distracted to complete your request. Maybe ask again?", "Bit foolish of you to expect us to just *work* like that. Maybe try again?", "We could do that, but we've decided not to this time. Try again later?"]), colour = embcol))

            # elif str(message.channel.id) in str(Fuwulchannels) and isbot and not message.author.name.endswith("_"):
            #     for a in range(len(Fuwulchannels)):
            #         if int(Fuwulchannels[a][0]) == message.channel.id:
            #             ind = a
            #             break
            #     hook = Fuwulchannels[ind][1]
            #     author_avatar = message.author.avatar
            #     try:
            #         msg = await MiscellaneuosCommands.uwutongue(message)
            #         await message.delete()
            #         async with aiohttp.ClientSession() as session:
            #             whook = Webhook.from_url(hook.url, session = session)
            #             await whook.send(msg, username = message.author.name + random.choice(["_"]), avatar_url = author_avatar)
            #         await session.close()
            #     except ValueError:
            #         return
                
            #Curse
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "curse") and "staff" in str(message.author.roles).lower():

                await OocFun.emotecurse(message)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "uncurse"):

                await OocFun.emoteuncurse(message)

            #manual Dezzie reward pool reset
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "rewardpoolreset") and "mod team" in str(authroles).lower():
                await MiscellaneuosCommands.manualDezPoolReset(message)

            #Character Index Update - On CharRegistry, untested
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "indexupdate") and "mod team" in str(authroles).lower():

                await CharRegistry.updatereg(message)

            #Character Creation Subroutine - On CharRegistry
            elif (str(message.channel) == "character-creation" or str(message.channel.name) == "NPC Creation") and message.content.lower().lstrip("*").startswith("name") and not isbot:
                await CharRegistry.charcreate(message)

            #Character Transfer Subroutine - On CharRegistry, untested
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "transfer") and not isbot:

                await CharRegistry.chartransfer(message)

            #Retire Command - On CharRegistry, untested
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "retire") and not isbot:

                await CharRegistry.charretire(message)

            #Activate Command - On CharRegistry, untested
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "activate") and not isbot:

                await CharRegistry.charactivate(message)

            #Deactivate Command - On CharRegistry, untested
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "deactivate") and not isbot:

                await CharRegistry.chardeactivate(message)

            #Help Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "help"):
                await CommonDefinitions.helplist(message)

            #account migration command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "migrate") and not isbot:
                await MiscellaneuosCommands.migrateAcc(message)

            #manual account migration command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "manualmigrate") and not isbot and "staff" in str(message.author.roles).lower():
                await MiscellaneuosCommands.manualMigrateAcc(message)
                
            #------------------------ Config Commands -------------------------------
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "editconfig") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await ConfigCommands.edit_config(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "printconfig") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await ConfigCommands.print_config(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "printconfigraw") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await ConfigCommands.print_config_raw(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "reloadconfig") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await ConfigCommands.reload_config()

            #------------------------------------------------------------------------

            #------------------------ Debug commands --------------------------------
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "copysheet") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await MiscellaneuosCommands.copySheet(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "removezerodiscrim") and not isbot and GlobalVars.config["general"]["administrative_role"] in str(message.author.roles).lower():
                await MiscellaneuosCommands.removeZeroDiscriminators(message)
            #------------------------------------------------------------------------


            #Plothook Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "plothook") and not isbot:

                delay = await message.channel.send("We are processing your request now")

                if " " in message.content:

                    tempname = message.content.split(" ",1)[1]

                else:

                    tempname = None

                #get player chars

                auth = message.author.name

                pnames = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B4000").execute().get("values")

                msgspl = message.content.split(" ")

                tit = None
                desc = ""
                foot = None
                imgurl = None

                pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F1:F4000").execute().get("values")
                pstat = sheet.values().get(spreadsheetId = CharSheet, range = "X1:X4000").execute().get("values")
                ppron = sheet.values().get(spreadsheetId = CharSheet, range = "I1:I4000").execute().get("values")

                indexes = []

                for k in range(len(pnames)):

                    if auth in pnames[k][0] and pstat[k][0] == "Active":

                        if tempname != None:

                            if tempname.lower() in pchars[k][0].lower():

                                indexes.append(k)

                                break

                            elif k == len(pnames):

                                await message.send("You don't have a character who's name contains that search term. I'll write this into a proper error message soon.")

                        else:

                            indexes.append(k)

                if indexes == []:

                    tit = "You have no active characters"
                    desc = "Your plothook: " + auth + " goes to #character-commands and registers a character"

                    await message.channel.send(embed = discord.Embed(title = tit, description = desc, colour = embcol))

                    await message.delete()

                else:

                    #Random Active Character

                    charslot = random.randrange(0, len(indexes))

                    cname = pchars[indexes[charslot]][0]

                    pluraliser = ""

                    #Get Pronoun

                    if str(ppron[indexes[charslot]]) != "[]":

                        if "/" in ppron[indexes[charslot]][0]:
                            nouns = ppron[indexes[charslot]][0].split("/")
                            determiner = nouns[1].lower()
                            pronoun = nouns[0].lower()
                            pluraliser = "s"

                        else:
                            determiner = "them"
                            pronoun = "they"

                    else:
                        determiner = "them"
                        pronoun = "they"

                    #Random Hook

                    hooks = 0
                    phooks = []
                    roompltcount = []

                    for j in range(len(plothooks)):

                        hooks += len(plothooks[j])
                        phooks.append(plothooks[j])
                        roompltcount.append(len(plothooks[j]))

                    hookno = random.randrange(1, hooks)

                    hookquant = hooks

                    hooks = 0

                    prevlist = sheet.values().get(spreadsheetId = Plotsheet, range = "W2:AM100", majorDimension='ROWS').execute().get("values")

                    if prevlist == None:

                        prevlist = []

                    if not auth in str(prevlist):

                        tempadd = [auth]

                        lasthook = datetime.now()

                        hourless = False

                        for pl in range(len(plothooks)):

                            temp = ""

                            for ll in range(roompltcount[pl]):

                                temp += "0"

                            tempadd.append(temp)

                        tempadd.append(lasthook)

                        prevlist.append(tempadd)

                        pind = len(prevlist)-1

                    else:

                        for n in range(len(prevlist)):

                            if auth in prevlist[n]:

                                pind = n

                        lasthook = prevlist[pind][-1]

                        if str(datetime.now()).split(":")[0] == str(lasthook).split(":")[0]:

                            hourless = True

                        else:

                            hourless = False

                        if message.author.name == "C_allum":

                            hourless  = False

                    #Find plothook from number

                    for j in range(len(plothooks)):

                        #Fracture prevstring

                        roomstring = fracture(prevlist[pind][j+1]) #Return a list of strings for each of the binaries.

                        if len(roomstring) < len(plothooks[j]):

                            while len(roomstring) < len(plothooks[j]):

                                roomstring.append("0")

                                prevlist[pind][j+1] = "".join(roomstring)

                        for k in range(len(plothooks[j])):

                            hooks += 1

                            if hourless:

                                if tit != "You can only use this command once per hour":

                                    tit = "You can only use this command once per hour"

                                    desc = "This is to prevent spamming just to get on the leaderboard."

                                    print(auth + " tried to get a plothook, but had had one too recently")

                                    break

                            #Hook matches

                            elif hookno == hooks:

                                if message.author.name != "C_allum":

                                    roomstring[k] = str(1)

                                hook = plothooks[j][k]

                                thook = hook.replace("£", pronoun).replace("$", determiner).replace("¬", pluraliser).replace("they is", "they are").replace("they has", "they have").replace("him's","his").replace("her's", "her").replace("they's", "their").replace("they was", "they were")

                                temphook = thook.split("_")

                                for n in range(len(temphook)):

                                    temphook[n] = temphook[n].capitalize()

                                hook = " ".join(temphook).replace("^", cname.title())

                                room = sheet.values().get(spreadsheetId = Plotsheet, range = "A1:O1", majorDimension='COLUMNS').execute().get("values")

                                selroom = room[j][0]

                                prevlist[pind][j+1] = "".join(roomstring)

                                prevlist[pind][-1] = str(datetime.now())

                                sheet.values().update(spreadsheetId = Plotsheet, range = str("W" + str(pind+2)), valueInputOption = "RAW", body = dict(majorDimension='ROWS', values=[prevlist[pind]])).execute()

                                print(message.author.name + " got a plothook")

                                tit = cname + " is in " + selroom + "!"

                                desc = hook

                    phemd = discord.Embed(title = tit, description = desc, colour = embcol)

                    seenno = 0

                    for sn in range(len(plothooks)):

                        seenno += prevlist[pind][sn+1].count("1")

                    if message.author.name != "C_allum":

                        phemd.set_footer(text ="-------------------------------------------------------------------\n\n" + auth + " has seen " + str(seenno) + " out of " + str(hookquant) + " potential plothooks!")

                    else:

                        phemd.set_footer(text ="-------------------------------------------------------------------\n\n" + auth + " has seen all " + str(hookquant) + " potential plothooks - he wrote them!")

                    await message.channel.send(embed = phemd)

                    await message.delete()

                    await delay.delete()

            #Plothook Leaderboard
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "plotlead"):

                delay = await message.channel.send("We are processing your request now")

                prevlist = sheet.values().get(spreadsheetId = Plotsheet, range = "R2:AC100", majorDimension='ROWS').execute().get("values")

                formlist = []

                for n in range(len(prevlist)):

                    seenno = 0

                    for sn in range(len(plothooks)):

                        seenno += prevlist[n][sn+1].count("1")

                    if len(str(seenno)) == 3:

                        formlist.append(str(seenno) + "|" + prevlist[n][0])

                    elif len(str(seenno)) == 2:

                        formlist.append("0" + str(seenno) + "|" + prevlist[n][0])

                    elif len(str(seenno)) == 1:

                        formlist.append("00" + str(seenno) + "|" + prevlist[n][0])

                sortlist = sorted(formlist)[::-1]

                for t in range(len(sortlist)):

                    if str(sortlist[t].split("|")[0].lstrip(str(0))) != "1":

                        pluraliser = "s"

                        if "C_allum" in sortlist[t]:

                            sortlist[t] = "all|C_allum"

                    else:

                        pluraliser = ""

                    if t == 0:

                        sortlist[t] = "`First Place`: " + sortlist[t].split("|")[1] + ", who has seen " + str(sortlist[t].split("|")[0].lstrip(str(0))) + " unique plothook" + pluraliser + "!"

                    elif t == 1:

                        sortlist[t] = "`Second Place`: " + sortlist[t].split("|")[1] + ", having seen " + str(sortlist[t].split("|")[0].lstrip(str(0))) + " unique plothook" + pluraliser + "."

                    elif t == 2:

                        sortlist[t] = "`Third Place`: " + sortlist[t].split("|")[1] + ", with a score of  " + str(sortlist[t].split("|")[0].lstrip(str(0))) + " plothook" + pluraliser + " seen."

                    elif t == 3:

                        sortlist[t] = "`Fourth Place`: " + sortlist[t].split("|")[1] + ". They have found " + str(sortlist[t].split("|")[0].lstrip(str(0))) + " unique plothook" + pluraliser + "!"

                    elif t == 4:

                        sortlist[t] = "`Fifth Place`: " + sortlist[t].split("|")[1] + ", only just getting onto this list with a total of " + str(sortlist[t].split("|")[0].lstrip(str(0))) + " plothook" + pluraliser + " seen."

                    else:

                        sortlist[t] = ""

                await message.delete()

                await delay.delete()

                await message.channel.send(embed = discord.Embed(title = "Plothook Leaderboard", description = "\n".join(sortlist), colour = embcol))

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "mvp") and ("mod team" in str(message.author.roles).lower()):
                print("Running")
                MVProle = discord.utils.get(message.guild.roles, name="Staff MVP")
                target = await message.guild.query_members(user_ids=[int(message.content.split("@")[1].replace("!","").replace("&","").split(">")[0])])
                targ = target[0]
                await targ.add_roles(MVProle)
                print("Done")

            #Guild Adventurer Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "adventurer") and ("staff" in str(message.author.roles).lower() or "licensed fucksmith" in str(message.author.roles).lower() or "guild licenser" in str(message.author.roles).lower() or message.author.name == "C_allum"):

                adventarget = message.content.split("@")[1]

                advenid = int(adventarget.replace("!","").replace("&","").split(">")[0])

                try:

                    advenchar = adventarget.split(">")[1].lstrip(" ")

                except IndexError:

                    advenchar = None

                advenmem = await message.guild.query_members(user_ids=[advenid])

                advenname = await client.fetch_user(advenid)

                if advenmem[0] != []:

                    advenmemb = advenmem[0]

                    role = discord.utils.get(advenmemb.guild.roles, name="Guild Adventurer")

                    await advenmemb.add_roles(role)

                    await client.get_channel(841736084362362940).send(str(advenname) + " has been given the Guild Adventurer role")

                    chardata = sheet.values().get(spreadsheetId = CharSheet, range = "B1:F8000", majorDimension='COLUMNS').execute().get("values")

                    advenname = str(advenname).split("#")[0]

                    advenping = "<@" + str(advenid) + ">"

                    charappend = "\n\nThe role was granted, but the character could not be found"

                    if advenchar != None and advenchar.lower() in str(chardata[4]).lower():

                        for a in range(len(chardata[4])):

                            if advenchar.lower() in str(chardata[4][a]).lower() and str(chardata[0][a]) == advenname:

                                sheet.values().update(spreadsheetId = CharSheet, range = str("AA" + str(a+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["Approved"]])).execute()

                                charappend = ""

                                break

                    rand = random.randint(1,10)

                    await message.channel.send(embed = discord.Embed(title = random.choice(["Approved"]), description = random.choice(["You are now an adventurer"]) + charappend, colour = embcol))

            #Looking for RP
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) +"lfg"):

                vermemb = message.author
                role = discord.utils.get(vermemb.guild.roles, name="Looking for Role Play")
                try:

                    time = int(message.content.split(" ")[1]) * 3600

                except (ValueError, IndexError) as e:

                    
                    if not role in message.author.roles:
                        await vermemb.add_roles(role)
                        await message.channel.send("No time limit submitted, toggling the role instead. Looking for Role Play role is now added")
                    else:
                        await vermemb.remove_roles(role)
                        await message.channel.send("No time limit submitted, toggling the role instead. Looking for Role Play role is now removed")
                    return

                

                await vermemb.add_roles(role)

                await message.channel.send("Looking for Role Play role set.")

                await asyncio.sleep(time)

                await vermemb.remove_roles(role)

            #-------------------------Kink Functions--------------------------------

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "kinkencounter"):
                await KinklistCommands.kinkencounter(message)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "kinkhelp"):
                await KinklistCommands.kinkhelp(message)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "kinkfill"):
                await KinklistCommands.kinkfill(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "randloot") and "staff" in str(message.author.roles).lower():
                await KinklistCommands.randloot(message)
            #-----------------------------------------------------------------------

            #Start
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "start"):

                welcdesc = "This guide was created to streamline the process of joining the general roleplay in the server.\n\n**Role Selection:** The first thing you should do is head up to " + str(client.get_channel(880605891366375435).mention) + ", where you can choose roles based on what you're interested in and how you define yourself. To see the roleplay channels, you'll need the RP-Intro (<:gem:944690539553513492>) role.\n\nAfter that, you'll need to go to " + str(client.get_channel(1081779600494972958).mention) + ". This contains an overview of the lore of the setting, as well as the rules for roleplaying within it. Once you've read through that, click the sigil ( <:Sigil:1055572608512442479> ) to accept the rules. This will allow to to access the public roleplay channels.\n\n**Generating Stats:** Now that you can access the " + str(client.get_channel(828412055228514325).mention) + " channel, you can create a character to play as. We allow characters up to level 14, though we recommend being between 4 and 10 due to balance on certain things. You can use any method to roll stats that you would like, as long as it is within reason. If you want to roll (4D6, dropping the lowest is the usual way), you can use the " + str(client.get_channel(903415692693475348).mention) + " thread. We use Avrae on the server for dice rolls, and we have the prefix for it set to: &. This means that to roll 4d6 dropping the lowest, you would do: `&r 4d6kh3`. Avrae also has `&randchar`, which will generate all 6 stats for you in this method. Sheets are only really used for certain things like raids (combat events in the dungeon), so it is possible to not use stats at all.\n\n**Character Creation:** To create your character, provide some information about them, starting with their name. There is a template pinned in " + str(client.get_channel(828412055228514325).mention) + ", which includes all the possible bits of information you can use, though you don't need to use all of these. You can also include an image here to show everyone what your character looks like.\n\n**Tuppers:** Most people in the dungeon roleplay using tuppers - aliases which replace your message with those of your character's. To set one up, head to: " + str(client.get_channel(903416425706831902).mention) + " and use the `?register` command. This has the following format: `?register name [text]`, where name is the name of your character as you want it to appear (in quotes if you have a space) and the brackets around the word 'text' can be anything, on either side of the word, and is how you trigger the bot to replace your message. For example, one of the brackets I use is £text, which replaces any of my messages which start with a £ symbol. If it's a character I use less often, I will use their name and a colon. You should include your image in this command as well, or add it to the tupper later using `?avatar name` and adding the link or attaching the image.\n\n**Arranging role-play:** Use the " + str(client.get_channel(832435243117445131).mention) + " channel to arrange scenes with people, or simply drop your character into one of the common rooms and someone will likely join you.\n\nHave fun!"

                await message.channel.send(embed = discord.Embed(title = "Celia's Lewd Dungeon - How to get started?", description = welcdesc, colour = embcol))

                await message.delete()

            #Room Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "room"):

                # saferooms = ["bot-testing"]
                # shops = ["ooc", "character-creation"]
                # depths = ["test"]

                rooms = []
                roomlastmess = []
                for a in range(len(saferooms)):
                    rooms.append(saferooms[a])
                for b in range(len(shops)):
                    rooms.append(shops[b])

                if not "adventurer" in str(authroles).lower():
                    for c in range(len(depths)):
                        rooms.append(depths[c])

                for d in range(len(rooms)):
                    roomchannel = discord.utils.get(client.get_all_channels(), name = rooms[d])
                    roomlast = [joinedMessages async for joinedMessages in client.get_channel(roomchannel.id).history(limit=2, oldest_first=False)]

                    if roomlast[0].author == client.user:
                        roomlastmess.append(datetime.timestamp(roomlast[1].created_at))
                    else:
                        roomlastmess.append(datetime.timestamp(roomlast[0].created_at))

                sortedrooms = [e for _, e in sorted(zip(roomlastmess, rooms))]
                roomlastmess.sort()
                randindex = random.randint(0,2)
                await message.channel.send(embed = discord.Embed(title = "We generated a random room for you.", description = "You could roleplay in the " + str(sortedrooms[randindex]) + ". It hasn't been used for " + str(math.floor((datetime.timestamp(datetime.now())-int(roomlastmess[randindex]))/3600)) + " hours", colour = embcol))

            #Command to set the scene for roleplay
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "setting"):
                pass

            #Embed Edit
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "edembed") and "staff" in str(message.author.roles).lower():
                chan = message.content.split(" ")[1].split("/")[5]
                messid = message.content.split(" ")[1].split("/")[6]
                messchan = client.get_channel(int(chan))
                mess = messchan.get_partial_message(int(messid))
                await mess.edit(embed = discord.Embed(title = "Edited", description = "A"))
                img = ""
                thum = ""

                if "-t" in message.content and "-d" in message.content:
                    if '=' in message.content:
                        tit = message.content.split("-t")[1].split('=')[1]
                        des = message.content.split("-d")[1].split('=')[1]
                    elif "=" in message.content:
                        tit = message.content.split("-t")[1].split("=")[1]
                        des = message.content.split("-d")[1].split("=")[1]
                    else:
                        tit = "You need to use equals signs around both the Title and Description"
                        des = "Surround each argument with ="
                    if "-i" in message.content:
                        img = message.content.split("-i")[1].split('=')[1]
                    if "-m" in message.content:
                        thum = message.content.split("-m")[1].split('=')[1]
                else:
                    tit = ""
                    des = message.content.split(" ",1)[1]
                cusemb = discord.Embed(title = tit, description = des.replace("The Mistress", "T̴̯̳̳̠͚͓͚̂͗̽̾̈́͌̐̅͠ͅh̸̨̫͓͖͎͍͔̠͇̊̂̏͝ę̶͎͇͍̲̮̠̭̮͛̃̈́͑̓̔̚ ̸͙̺̦̮͈̹̮̑̿̊̀̂́͂̿͒̚͜M̶̬͇̤̾͐̊̽̈́̀̀̕͘͝í̸̬͎͔͍̠͓̋͜͠͝s̶̡̡̧̪̺͍̞̲̬̮͆͋̇̐͋͌̒̋͛̕t̷̤̲̠̠̄̊͌̀͂̈́̊̎̕ȓ̶̼̂̿̇͛̚e̶̹̪̣̫͎͉̫̫͗s̸̟͉̱͈̞̬̽̽̒̔́̉s̸̛̖̗̜̻̻͚̭͇̈́̀̄͒̅̎"), colour = embcol)
                if not "mod team" in str(authroles).lower():
                    await client.get_channel(logchannel).send(str(message.author) + " generated an embed in " + str(message.channel.name))
                if not img == "":
                    cusemb.set_image(url = img)
                if not thum == "":
                    cusemb.set_thumbnail(url = thum)
                print(message.author.name + " edited an embed")
                await mess.edit(embed = cusemb)
                await message.delete()

            #Recent Activity Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "recent"):
                delay = await message.channel.send("We are processing your request now")
                meslatest = []
                rooms = []
                rooms.extend(saferooms)
                rooms.extend(shops)
                rooms.extend(depths)
                for n in range(len(rooms)):
                    roomchannel = discord.utils.get(client.get_all_channels(), name = rooms[n])
                    roomlatest = [joinedMessages async for joinedMessages in roomchannel.history(limit=2, oldest_first=False)]

                    if roomlatest[0].author == client.user:
                        roomlatest[0] = roomlatest[1]
                        scenebroken = True
                    else:
                        scenebroken = False
                    rtimestamp = datetime.timestamp(roomlatest[0].created_at)
                    mestimestamp = datetime.timestamp(datetime.now())
                    diff = float(mestimestamp - rtimestamp)
                    days = math.floor(diff/86400)
                    diffstr = []
                    if days == -1:
                        days = 0
                    elif days == 1:
                        diffstr.append(str(days) + " day")
                    else:
                        diffstr.append(str(days) + " days")
                    hours = math.floor((diff-(days*86400))/3600)
                    if hours == -1:
                        hours = 0
                    elif hours == 1:
                        diffstr.append(str(hours) + " hour")
                    else:
                        diffstr.append(str(hours) + " hours")
                    minutes = math.floor((diff-(days*86400)-(hours*3600))/60)
                    if minutes == -1:
                        minutes = 0
                    elif minutes == 1:
                        diffstr.append(str(minutes) + " minute")
                    else:
                        diffstr.append(str(minutes) + " minutes")
                    if diffstr == []:
                        meslatest.append("<#" + str(roomchannel.id) + "> - Last used within the last minute.")
                    else:
                        meslatest.append("<#" + str(roomchannel.id) + "> - Last used " + ", ".join(diffstr).replace("hours, ", "hours and ") + " ago.")
                    meslatest.append(str(len(roomchannel.threads)) + " Active threads.\n")
                print(message.author.name + " ran the recent activity command")
                await message.channel.send(embed = discord.Embed(title = "Last messages in each public room:", description = "\n".join(meslatest), colour = embcol))
                await message.delete()
                await delay.delete()

            #Register community Project
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "communityproject") and "staff" in str(message.author.roles).lower():
                await MiscellaneuosCommands.regCommunityProject(message)

            #Eat a Dezzie commmand
            elif not isbot and ((message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "gobblin")) or (message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "crunch")) or (message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "goblin"))):
                await MiscellaneuosCommands.crunch(message)

            #Rulebook Command
            elif (message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "rulebook")):
                await message.delete()
                await message.channel.send(embed = discord.Embed(title = "Here's a link to the Lewd Rulebook", description = "https://www.dropbox.com/sh/q2wt7nsihxldam2/AAB1yTPUsPo57BNkapEXgxxya/00%20Full%20Lewd%20handbook%20%28WIP%29.pdf?dl=0", colour = embcol))

            elif (message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "lewdreference")):
                await message.delete()
                await message.channel.send(embed = discord.Embed(title = "A quick reference sheet for the lewd rules in the dungeon", description = "**Full Rulebook:** https://www.dropbox.com/sh/q2wt7nsihxldam2/AAB1yTPUsPo57BNkapEXgxxya/00%20Full%20Lewd%20handbook%20%28WIP%29.pdf?dl=0\n\n**Inhibition:** 10 + Proficiency Bonus + Your choice of mental stat modifier\n**Arousal Maximum:** Rolled Hit Dice (or rounded average) plus Con mod per level\n**Climaxing:** DC 15 Inhibition save, fail halves arousal and incapacitates for 1d4 rounds (unless overstimulating)\n\n**Conditions:**\n    *Hyperaroused:* Disadvantage on saves against indirect advances and direct advances against the creature have advantage\n    *Edged:* Hyperaroused, Must save against climaxing, drops items, falls prone, stunned, advances do maximal stimulation.\n    *Denied:* Automatic success on climax saves.\n    *Infatuated:* Charmed by the source, willing for all advances by charmer, commands and suggestions require checks.\n    *Intoxicated:* Disadvantage on mental saves\n    *Uninhibited:* Inhibition score at 0. Hyperaroused, intoxicated, willing for all stimulation, disadvantage on checks and saves that are not sexual advances. Uses their turn to move towards and stimulate others, or themself.\n\n**Natural Implements:**\n    *Cock:*\n      Tiny: 1d4 Piercing\n      Small: 1d6 Piercing\n      Medium: 1d8 Piercing\n      Large: 1d10 Piercing\n      Huge: 1d12 Piercing\n      Gargantuan: 2d8 Piercing\n    Tits: 1d6 Bludgeoning\n    Pussy: 1d8 Bludgeoning\n    Ass: 1d8 Bludgeoning\n    Mouth: 1d4 Bludgeoning\n    Hand: 1d4 Bludgeoning\n    Tail: 1d4 Piercing\n    Tentacle: 1d6 Piercing\n    Pseudopod: 1d6 Bludgeoning", colour = embcol))

            #Easter egg hunt
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "egg"):

                if "res" in message.content.lower() or not "staff" in str(message.author.roles).lower():
                    egglist = []
                    for a in range(len(eggfinders)):
                        findersort = [x for _,x in sorted(zip(eggsfound,eggfinders))]
                        egglist.append(findersort[a] + ": " + str(sorted(eggsfound)[a]))
                    egglist.reverse()
                    await message.channel.send(embed = discord.Embed(title = "Mimic Eggs Found", description = "\n".join(egglist), colour = embcol))

                elif "set" in message.content.lower() or not "staff" in str(message.author.roles).lower():
                    eggname = " ".join(message.content.split(" ")[2:-1])
                    eggno = message.content.split(" ")[-1]
                    if eggname in str(eggfinders):
                        eggsfound[eggfinders.index(eggname)] = int(eggno)
                        egglist = []
                        for a in range(len(eggfinders)):
                            findersort = [x for _,x in sorted(zip(eggsfound,eggfinders))]
                            egglist.append(findersort[a] + ": " + str(sorted(eggsfound)[a]))
                        egglist.reverse()
                        await message.channel.send(embed = discord.Embed(title = "Mimic Eggs Found", description = "\n".join(egglist), colour = embcol))
                    else:
                        eggfinders.append(eggname)
                        eggsfound.append(int(eggno))
                        egglist = []
                        for a in range(len(eggfinders)):
                            findersort = [x for _,x in sorted(zip(eggsfound,eggfinders))]
                            egglist.append(findersort[a] + ": " + str(sorted(eggsfound)[a]))
                        egglist.reverse()
                        await message.channel.send(embed = discord.Embed(title = "Mimic Eggs Found", description = "\n".join(egglist), colour = embcol))

                else:
                    global eggtimer
                    eggtimer = message.content.split(" ")[1]
                    global egglimit
                    egglimit = message.content.split(" ")[2]
                    global eggwaittimer
                    try:
                        eggwaittimer = message.content.split(" ")[3]
                    except IndexError:
                        eggwaittimer = 300
                    await message.channel.send("Egg timer has been set to " + str(eggtimer) + " seconds. Each egg can be collected by " + str(egglimit) + " players. Eggs will timeout after " + str(eggwaittimer) + " seconds per person allowed to collect them, in this case, " + str(int(eggwaittimer) * int(egglimit)) + " seconds, or " + str((int(eggwaittimer) * int(egglimit))/60) + " minutes.")

            #Scenes Command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "scenes"):
                await MiscellaneuosCommands.scenes(message)

            #-------------------------------------Economy V2----------------------------------------
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "copyeconomy") and "staff" in str(message.author.roles).lower() and message.author.name == "artificer_dragon":
                await EconomyV2.copyEconomy(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "reloadeconomy") and "staff" in str(message.author.roles).lower():
                await EconomyV2.loadEconomySheet()
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "reloadshops") and "staff" in str(message.author.roles).lower():
                await EconomyV2.loadItemSheet()
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "maintenance") and "staff" in str(message.author.roles).lower():
                if GlobalVars.maintenance_mode == True:
                    GlobalVars.maintenance_mode = False
                    await message.channel.send(embed=discord.Embed(title="Maintenance mode deactivated"))
                else:
                    GlobalVars.maintenance_mode = True
                    await message.channel.send(embed=discord.Embed(title="Maintenance mode activated"))

            #New economy commands (EconomyV2)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "~test"):
                oldEconData = sheet.values().get(spreadsheetId = EconSheet, range = "A1:GZ8000", majorDimension='ROWS').execute().get("values")
                await EconomyV2.computeAllLevenshteinDistancesOldEconItems(message, oldEconData)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "shop"):
                    await EconomyV2.shop(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "item"):
                    await EconomyV2.item(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "inventory"):
                    await EconomyV2.inventory(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "buy"):
                    await EconomyV2.buyitem(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "giftall") and "staff" in str(message.author.roles).lower():
                    await EconomyV2.giftAll(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "sellitem"):
                    await EconomyV2.sellitem(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "giveitem"):
                    await EconomyV2.giveitem(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "additem") and "staff" in str(message.author.roles).lower():
                    await EconomyV2.additem(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "givemoney"):
                    await EconomyV2.giveMoney(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "addmoney") and "staff" in str(message.author.roles).lower():
                    await EconomyV2.addMoney(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "removemoney") and "staff" in str(message.author.roles).lower():
                    await EconomyV2.removeMoney(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "money"):
                    await EconomyV2.money(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "useitem"):
                    await EconomyV2.useitem(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "leaderboard"):
                    await EconomyV2.leaderboard(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "invest"):
                    await EconomyV2.invest(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "toggledailynotif"):
                    await EconomyV2.togglenotif(message)
            #Income History
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "income") and not isbot:
                await EconomyV2.incomeWeek(message)
            
            #---------------------------------------------------------------------------------------
            #Lorekeeper Ping
            elif message.channel.category.name in str(rpcategories) and message.channel.type == discord.ChannelType.text:

                if "prestittydigitation" in message.content.lower() and message.author.bot:
                    await OocFun.laundry(message)

                elif not isbot and not message.author == client.user:
                    prevmess = [joinedMessages async for joinedMessages in message.channel.history(limit=2, oldest_first=False)] #Fix for pebblehost Await issue
                    prtimestamp = prevmess[1].created_at
                    diff = str(message.created_at - prtimestamp)
                    timediff = diff.split(":")[0]
                    if "day" in str(timediff):
                        ping = True
                    elif int(timediff) > 3:
                        ping = True
                    else:
                        ping = False
                    if "lore team" in (message.author.roles).lower():
                        ping = False
                    if ping:
                        room = "<#" + str(message.channel.id) + ">"
                        if message.channel.name.startswith("💰"):
                            await client.get_channel(bridgechannel).send(str(message.author.name.split("#")[0] + " has sent a message in " + room + ". The last message in the channel before this was over " + str(timediff).replace(", ", " and ") + " hours ago.\n\n<@&" + str(1145873596753924180) + "> or <@&" + str(1145789101610651710) + ">, is anyone able to go and assist them?").replace("1 hours", "an hour"))
                            print("Lorekeepers were pinged to play shops")
                        elif message.channel.name.startswith("⚔"):
                            await client.get_channel(bridgechannel).send(str(message.author.name.split("#")[0] + " has sent a message in " + room + ". The last message in the channel before this was over " + str(timediff).replace(", ", " and ") + " hours ago.\n\n<@&" + str(1145872343458140211) + ">, would you like to go and torment them?").replace("1 hours", "an hour"))
                            print("Lorekeepers were pinged to torment depths delvers")
                        
            #Clone Channel
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "clonechannel") and "staff" in str(message.author.roles).lower():

                await message.channel.send("Processing, please wait")
                channelid = int(message.channel.id)
                mess = [joinedMessages async for joinedMessages in message.channel.history(limit = None, oldest_first= True)]
                line = []
                for a in range(len(mess)):
                    if mess[a] == message:
                        break
                    if mess[a].content.isascii() == True:
                        line.append(mess[a].author.name + ": " + mess[a].content.replace("***The Mistress***", "***T̶̡͚͊̒̈́̇̉͑̏͑̚h̴̬̓̔̈́̈́͝ȩ̵̢͖̮̻̻̰̟͔̗̃̈́͝ ̴̡͈̦̯͗̈͋͗̈́̾̍̉̄M̷̰̬̜̜̪͆̉͗̋͑̐̉̚͝͝i̴̡̛̦͍̦͈͉̯̻͇͑̒̊̋̾̔͠s̷̭̫̾͗͒̀́t̷̢͈̜͙̬̦͕͎̣̉̍̈́͋̊̎̾̂̌r̴̢̢͖͚̬̣̩̺̆͒̈́͛ȩ̸̜̠͖͖̼͓͍̯̫́͌͆̕s̶̘̺̻̖̲͔͌̓͗̒̆ͅs̶̛̤̻̭̤̰̅̇͌͗***"))
                filename = str(message.channel) + ".txt"
                with open(filename, "w") as f:
                    f.write("\n".join(line))
                f.close()
                await message.channel.send("We have attached a text log of this channel.", file = discord.File(r"" + filename))
                os.remove(filename)
                del mess

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "clonev2") and "staff" in str(message.author.roles).lower():

                await message.channel.send("Processing, please wait")

                if message.content.split(" ")[1].startswith("https"):
                    chanid = message.content.split(" ")[1].split("/")[-1]
                    destid = message.content.split(" ")[2].split("/")[-1]
                elif message.content.split(" ")[1].startswith("<"):
                    chanid = message.content.split(" ")[1].split("#")[-1].rstrip(">")
                    destid = message.content.split(" ")[2].split("#")[-1].rstrip(">")
                else:
                    chanid = message.content.split(" ")[1]
                    destid = message.content.split(" ")[2]

                channelid = int(message.channel.id)
                chan = client.get_channel(int(chanid))
                dest = client.get_channel(int(destid))
                print("Copying from " + str(chan) + " to " + str(dest))
                mess = [joinedMessages async for joinedMessages in message.channel.history(limit = None, oldest_first= True)]
                mess.sort(key=lambda x: x.created_at)
                hook = await dest.parent.create_webhook(name= "Clonehook")
                lock = asyncio.Lock()
                
                async with aiohttp.ClientSession() as session:
                    whook = SyncWebhook.from_url(hook.url)
                    for a in range(len(mess)):
                        try:
                            if not mess[a].content.startswith("%clone"):
                                whook.send(mess[a].content, username = mess[a].author.name, avatar_url = mess[a].author.avatar, thread = dest)
                            else:
                                break
                        except discord.errors.HTTPException:
                            pass
                        if mess[a].attachments:
                            for b in range(len(mess[a].attachments)):
                                whook.send(mess[a].attachments[b].url, username = mess[a].author.name, avatar_url = mess[a].author.avatar, thread = dest)
                        if mess[a].embeds:
                            whook.send(embed= mess[a].embeds[0], username = mess[a].author.name, avatar_url = mess[a].author.avatar, thread = dest)

                await message.channel.send("Complete")
                await session.close()
                await hook.delete()

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"] + "export")):
                await MiscellaneuosCommands.export(message)

            #Impersonator React
            elif "gothica" in message.content.lower().replace("-","").replace(".","") or "thic goth" in message.content.lower().replace("-","").replace(".","").replace("cc","c") or "gothy" in message.content.lower().replace("-","").replace(".",""):
                if message.author.name != "c_allum":

                    #if random.randint(1,100) != 100:
                    await message.add_reaction('👀')
                    #else:
                        #await message.add_reaction('<:tentacle:830675670711402506>')

                else:
                    await message.add_reaction('♥️')

            #Maze Functions
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "mazestart") and "staff" in str(message.author.roles).lower():
                await MiscellaneuosCommands.mazestart(message)
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "mazerestore") and "staff" in str(message.author.roles).lower():
                await MiscellaneuosCommands.mazerestore(message)

            #Manually spawn Imp Tome
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "imptome") and message.author.id == imptomeWielder:
                messageLink = message.content.rsplit(" ")[1]
                splitLink = messageLink.split('/')
                server_id = int(splitLink[4])
                channel_id = int(splitLink[5])
                msg_id = int(splitLink[6])
                guild = client.get_guild(server_id)
                channel = client.get_channel(channel_id)
                msg = await channel.fetch_message(msg_id)
                await MiscellaneuosCommands.impTomeSpawn(msg)
            
            #Countscenes command
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "countscenes"):
                await MiscellaneuosCommands.countscenes(message)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "functionsetup"):
                for a in range(len(functionnames)):
                    if functionreqs[a] != 0:
                        await message.channel.send(embed = discord.Embed(title = functionnames[a], description = str(functiondesc[a]) + "\n\n*Prerequisites:* " + str(functionreqs[a]), colour = embcol))
                    else:
                        await message.channel.send(embed = discord.Embed(title = functionnames[a], description = functiondesc[a], colour = embcol))
                await message.delete()
            
            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "tarot"):
                await MiscellaneuosCommands.tarotfunc(message)

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "tour"):
                await message.channel.send(embed = discord.Embed(title = TourNames[0], description = TourDescriptions[0], colour = embcol), view = MiscellaneuosCommands.TourView1())

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "demo"):
                await message.delete()
                await message.channel.send(embed = discord.Embed(title = "Setting the scene in the Unlit Passageways!", description = "*A small door of fine oak panelling swings open to reveal a cosy bedchamber. The bed is a simple wrought iron frame with a comfortable looking mattress, flanked by small wooden bedside tables. The room is lit by a single torch in a sconce in the wall, which is spluttering low and almost out.*\n\n---------------------------------------------------------------------\n\nCasting Detect Magic in the room reveals a source of magic in the bedsheets and two in the right bedside table.\n\n---------------------------------------------------------------------\n\nItems inside the drawers on the left table:\n* One medium dildo\n* A set of red lacy lingerie\n\nItems inside the drawers on the right table:\n* A spell scroll, containing the spell 'Cure Wounds'\n* Upon a DC 14 *Investigation* Check: ||A false bottom in the drawer, revealing a Temporeal Collar of Wealth||\n\n---------------------------------------------------------------------\n\nCasting Identify on the bedsheets reveals that they are charmed to be luxuriosly comfortable Temporeal items. They are also cursed, such that anyone under them is subjected to ||Mantle of Agreability||\n\n---------------------------------------------------------------------\n\n*Temporeal items are magical temporary items, which vanish after 1d4 hours or if they are removed from the room in which they are found.*", colour = embcol))

            elif message.content.lower().startswith(str(GlobalVars.config["general"]["gothy_prefix"]) + "map"):
                await MiscellaneuosCommands.map(message)

            #Per message income and Scene tracker pings.
            if not "verification" in str(message.channel).lower():
                
                #-------THIS CODE IS SUPER MESSY AND NEEDS A SERIOUS REWORK----------

                if not isbot:
                    try:
                        playerID = message.author.id
                        author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(playerID) in x][0])

                    except:
                        #New User
                        #await EconomyV2.addUserToEconomy(message.author.name, message.author.id)
                        #print(str(message.author.name) + " has been added to the economy at " + str(datetime.now()))
                        return

                    #Check if member is already registered
                    if author_row_index != None:
                        #-----DAILY REWARD-------
                        #Check if that user already got their reward in the last 24h
                        try:
                            int(GlobalVars.economyData[author_row_index+3][1])
                        except IndexError:
                            GlobalVars.economyData[author_row_index+3].append(0)
                        if int(GlobalVars.economyData[author_row_index+3][1]) < int(datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))):
                            GlobalVars.economyData[author_row_index+3][1] = int(datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)))
                            await EconomyV2.addDezziesToPlayer(message, GlobalVars.config["economy"]["daily_interaction_value"],message.author.id, write_econ_sheet=True, send_message=False)
                            TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.DailyInteraction, int(GlobalVars.config["economy"]["daily_interaction_value"]))
                            try:
                                if GlobalVars.economyData[author_row_index+2][2] == "True":
                                    await message.author.send(embed=discord.Embed(title="You claimed your daily reward!", description=f"You got {GlobalVars.config['economy']['daily_interaction_value']} from the daily reward. You now have {GlobalVars.economyData[author_row_index+1][1]}.", color=embcol))
                            except IndexError:
                                GlobalVars.economyData[author_row_index+2].append("False")

                        #---------RP REWARD AND NOTIFICATIONS--------------
                        #check if we are in a channel that awards dezzies for posts
                        if message.channel.category_id in GlobalVars.config["channels"]["roleplay_categories_id"] and not "ooc" in message.channel.name.lower():
                            #ignore edit calls
                            if not "?edit" in message.content:
                                #calculate reward amount
                                charcount = len(message.content)
                                #TODO: Do some more elaborate math on the RP rewards.
                                message_award = int(math.floor(charcount/20) * (1+charcount * GlobalVars.config["economy"]["currency_multiplier_per_rp_word"]) + GlobalVars.config["economy"]["fixed_currecy_per_rp_message"])

                                #Set and add dezzies to player
                                await EconomyV2.addDezziesToPlayer(message, message_award, message.author.id, write_econ_sheet=True, send_message=False)
                                TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.MessageReward, int(message_award))

                                #Tracked Scenes Ping
                                f = lambda x: [""]if x == [] else x
                                columnZero = [ f(x)[0] for x in GlobalVars.economyData]
                                for a in range(math.floor((len(GlobalVars.economyData))/4) - 1): #Go through each user.
                                    playerindex = a * 4 + 5
                                    scenedataIndex =  playerindex + 2

                                    if str(message.channel.id) in columnZero[scenedataIndex]:
                                        #Make a list of the tracked scenes
                                        scenearray = columnZero[scenedataIndex].split("|")
                                        #Find the index of the currently relevant scene in the list
                                        sceneindex = [idx for idx, s in enumerate(scenearray) if str(message.channel.id) in s][0]
                                        #Read the tracking status of that scene for this player
                                        trackedStatus = scenearray[sceneindex].split(" ")[-1]

                                        if trackedStatus == "Notifications:Enabled":
                                            if GlobalVars.economyData[playerindex][0] != message.author.name: #Do not ping the author.
                                                #Fetch player
                                                user = discord.utils.get(client.guilds[0].members, name = GlobalVars.economyData[playerindex][0])
                                                #Wait for 3s to let tupper send the embed.
                                                await asyncio.sleep(3.0)
                                                #Send DM to user
                                                await user.send(f"New message in <#{message.channel.id}> by {message.channel.last_message.author.name}")

                                        elif trackedStatus == "Notifications:Disabled":
                                            pass
                                        
                                        else: #If no status is present, add Notif Disabled as the default.
                                            scenearray[sceneindex] = scenearray[sceneindex] + (" Notifications:Disabled")
                                            dataup = "|".join(scenearray)
                                            GlobalVars.economyData[scenedataIndex][0] = dataup
                                            await EconomyV2.writeEconSheet(GlobalVars.economyData)
                         #----------OOC REWARD--------------                   
                        else:   #If we aren't in an RP category, adjust the dezzie payout
                            try:
                                prevtime = GlobalVars.economyData[author_row_index + 3][2]
                            except IndexError:
                                GlobalVars.economyData[author_row_index + 3].append(0)
                                prevtime = 0
                            #Give users dezzies every 5 min if they interact in an OOC channel
                            if int(str(datetime.timestamp(datetime.now())).split(".")[0]) - int(prevtime) >= 300:
                                
                                #calculate reward amount
                                charcount = len(message.content)
                                message_award = int(math.floor(charcount/100) + GlobalVars.config["economy"]["fixed_currecy_per_ooc_message"])

                                #Set correct timestamp and add dezzies to player
                                author_row_index = GlobalVars.economyData.index([x for x in GlobalVars.economyData if str(playerID) in x][0])
                                GlobalVars.economyData[author_row_index+3][2] = str(int(datetime.timestamp(datetime.now())))
                                await EconomyV2.addDezziesToPlayer(message, message_award, message.author.id, write_econ_sheet=False, send_message=False) #We don't write the economy back for every OOC message.
                                TransactionsDatabaseInterface.addTransaction(message.author.name, TransactionsDatabaseInterface.DezzieMovingAction.OOCMessageReward, int(message_award))                     
                        
                else:   #Things we want to do if a bot posted the message
                    if not(client.user == message.author) and not("Avrae" == message.author.name) and message.channel.category_id in GlobalVars.config["channels"]["roleplay_categories_id"] and not (message.channel.type == discord.ChannelType.private_thread):
                        if(random.randint(1, 500) == 1):
                            await MiscellaneuosCommands.impTomeSpawn(message)

    #DM Messages
    except AttributeError:

        if not "Direct Message" in str(message.channel):

            pass

            #print("Guild ID Error? " + str(message.channel))
        
        else:
            
            #Anonymous Message
            if message.content.lower().startswith("%anon"):
                if liveVersion:
                    anonchannel = 1130518872232046602
                else:
                    anonchannel = 1069423947092860998
                await client.get_channel(anonchannel).send("**Anonymous message:**" + message.content.lstrip("%anon") + "\n")
                await message.channel.send("We have sent your message anonymously")


@client.event
async def on_raw_reaction_add(reaction):

    mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

    #Staff Function Demo
    # if mess.channel.name == "function-selection":

    #     await mess.remove_reaction(reaction.emoji, reaction.member)
    #     func = mess.embeds[0].title
    #     funcindex = functionnames.index(func)
    #     channel = client.get_channel(int(1135679819179376852))
    #     if functionreqs[funcindex] != 0:
    #         if func == "Issuing Strikes And Bans":
    #             await reaction.member.send("You do not meet the prerequistes to perform this function. To be able to start or join one of these discussions, you need to be accepted by a group vote.")
    #             return
    #     else:
    #         if func == "Running NPCs":
    #             thread = await channel.create_thread( name = str(func), type = discord.ChannelType.public_thread)
    #             await thread.send(embed = discord.Embed(title = "Tools for running NPCs", description = "Here are some tools you can use to help you run NPCs. React with the appropriate number to summon the relevant feature:\n\n`1` - NPC Information\n`2` - Player Character Information\n`3` - Player Kink Information", colour = embcol))
    #             await mess.edit(embed = discord.Embed(title = str(functionnames[funcindex]), description = str(functiondesc[funcindex]) + "\n\n*Prerequisites:* " + str(functionreqs[funcindex]) + "\n\n*Current Members:* " + str(reaction.member.name), colour = embcol))

    #     return
    
    # if mess.channel.parent.name == "official-functions":
    #     if mess.author == client.user:
    #         option = 0
    #         if reaction.emoji.name == "1️⃣":
    #             option = 1
    #         elif reaction.emoji.name == "2️⃣":
    #             option = 2
    #         elif reaction.emoji.name == "3️⃣":
    #             option = 3
    #         elif reaction.emoji.name == "4️⃣":
    #             option = 4
    #         elif reaction.emoji.name == "5️⃣":
    #             option = 5
    #         elif reaction.emoji.name == "6️⃣":
    #             option = 6
    #         elif reaction.emoji.name == "7️⃣":
    #             option = 7
    #         elif reaction.emoji.name == "8️⃣":
    #             option = 8
    #         elif reaction.emoji.name == "9️⃣":
    #             option = 9
            
    #         await stafffunc(mess, option, reaction.member)
            
            

    if "staff" in str(reaction.member.roles).lower() or "ghostwriter" in str(reaction.member.roles).lower():

        mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        #if (reaction.emoji.name == "dz" or reaction.emoji.name == "cashmoney" or reaction.emoji.name == "makeitrain" or reaction.emoji.name == "DzCrit") and mess.author.bot == False:
#
        #    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension='ROWS').execute().get("values")
#
        #    reciprow = ""
#
        #    targid = mess.author.id
#
        #    target = await client.fetch_user(targid)
#
        #    targetName = target.name
#
        #    try:
#
        #        for a in range(math.floor(len(economydata)/4)):
#
        #            b = a * 4 + 5
#
        #            if str(targetName + "#" + str(target.discriminator)) in str(economydata[b][0]):
#
        #                reciprow = b + 1
#
        #                break
#
        #    except IndexError:
#
        #        await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))
#
        #    if reaction.emoji.name == "dz":
#
        #        giveamount = reactdz
#
        #    elif reaction.emoji.name == "cashmoney":
#
        #        giveamount = reactCashMoney
#
        #    elif reaction.emoji.name == "makeitrain":
#
        #        giveamount = reactMakeItRain
#
        #    else:
#
        #        giveamount = random.randint(100,500)
#
        #    recipnewtot = int(economydata[int(reciprow)-1][1]) + int(giveamount)
#
        #    sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()
#
        #    TransactionsDatabaseInterface.addTransaction(target.name + '#' + target.discriminator, TransactionsDatabaseInterface.DezzieMovingAction.React, int(giveamount))
#
        #    if reaction.member.name == targetName:
#
        #        await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipnewtot) + dezzieemj + "\n\nNot sure why they're awarding dezzies to themself like this, but ok.", colour = embcol, url = mess.jump_url))
#
        #    else:
#
        #        await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipnewtot) + dezzieemj, colour = embcol, url = mess.jump_url))

        if reaction.emoji.name == "💰":

            mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

            for a in range(len(mess.attachments)):

                await client.get_channel(913998580027645992).send(mess.attachments[a])

            if mess.content != "":

                await client.get_channel(913998580027645992).send(mess.content)

        elif reaction.emoji.name == "💎":

            mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

            for a in range(len(mess.attachments)):

                await client.get_channel(985417358019534878).send(mess.attachments[a])

            if mess.content != "":

                await client.get_channel(985417358019534878).send(mess.content)

        elif reaction.emoji.name == "⛓️":

            mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

            for a in range(len(mess.attachments)):

                await client.get_channel(980494836811563148).send(mess.attachments[a])

            if mess.content != "":

                await client.get_channel(980494836811563148).send(mess.content)

        elif reaction.emoji.name == "❌" and mess.author.bot:

            await client.get_channel(logchannel).send(str(reaction.member.name) + " deleted the following message from " + str(mess.author.name) + " in " + str(mess.channel))

            try:

                await client.get_channel(logchannel).send(mess.content)

            except discord.errors.HTTPException:

                await client.get_channel(logchannel).send(embed = mess.embeds[0])

            try:

                await mess.delete()

            except discord.errors.NotFound:

                pass

    #Dezzie Reacts with weekly pool on OOC messages
    if (reaction.emoji.name == "dz" or reaction.emoji.name == "cashmoney" or reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart" or reaction.emoji.name == "DzCrit") and mess.author.bot == False:

        await EconomyV2.dezReact(reaction)

    #Dezzie React on Tupper
    elif (reaction.emoji.name == "dz" or reaction.emoji.name == "cashmoney" or reaction.emoji.name == "makeitrain" or reaction.emoji.name == "Dezzieheart" or reaction.emoji.name == "DzCrit") and mess.author.bot == True and not mess.author.name in botnames :
        
        await EconomyV2.rpDezReact(reaction)
        

    if reaction.emoji.name == "cuffs" and mess.channel.name != "Server Economy":


        chan = client.get_channel(reaction.channel_id)
        mess = await chan.fetch_message(reaction.message_id)

        insideArtForumThread = True

        try:
            a = mess.attachments[0]

        except IndexError:

            await mess.channel.send("That message doesn't contain an image.")

        #Check whether we are in the art claiming forum, or somewhere else in the server
        if chan.type == discord.ChannelType.public_thread:
            if chan.parent.id != GlobalVars.config["channels"]["art_claim_forum_id"]:
                insideArtForumThread = False
        else:
            insideArtForumThread = False
        emb = discord.Embed(title = reaction.member.name + " has claimed this artwork to make a character from.", colour = embcol)
        if insideArtForumThread:
            #Add the "claimed" tag to the post
            await chan.add_tags(chan.parent.get_tag(1065081440481574923))       #that number is the id of the "Claimed" tag. See a list of all tags by doing print(chan.parent.available_tags)
            user = await client.fetch_user(int(reaction.member.id))
            await mess.channel.send(f"Image claimed by {user.display_name}")


        else:
            emb = discord.Embed(title = reaction.member.name + " has claimed this artwork to make a character from.", colour = embcol)
            emb.set_thumbnail(url = mess.attachments[0])
            artForumChannel = client.get_channel(GlobalVars.config["channels"]["art_claim_forum_id"])
            user = await client.fetch_user(int(reaction.member.id))
            if mess.channel.type == discord.ChannelType.public_thread:
                channelName = mess.channel.parent.name
            else: channelName = mess.channel.name

            await artForumChannel.create_thread(name=f"Claimed from {channelName} by {user.display_name}", content = mess.attachments[0], applied_tags=[artForumChannel.get_tag(1065081440481574923)])

        await user.send("You have claimed this image. If it vanishes from here, it should still be in the channel.")
        try:
            emb.set_thumbnail(url = mess.attachments[0])
            await user.send(content = mess.attachments[0])

        except IndexError:
            emb.set_thumbnail(url = mess.content)
            await user.send(mess.content)

    elif "staff" in str(reaction.member.roles).lower() or "mod team" in str(reaction.member.roles).lower():

        pass
        # if reaction.emoji.name == "💰":

        #     mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        #     for a in range(len(mess.attachments)):

        #         await client.get_channel(913998580027645992).send(mess.attachments[a])

        #     if mess.content != "":

        #         await client.get_channel(913998580027645992).send(mess.content)

        # elif reaction.emoji.name == "💎":

        #     mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        #     for a in range(len(mess.attachments)):

        #         await client.get_channel(985417358019534878).send(mess.attachments[a])

        #     if mess.content != "":

        #         await client.get_channel(985417358019534878).send(mess.content)

        # elif reaction.emoji.name == "⛓️":

        #     mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        #     for a in range(len(mess.attachments)):

        #         await client.get_channel(980494836811563148).send(mess.attachments[a])

        #     if mess.content != "":

        #         await client.get_channel(980494836811563148).send(mess.content)

        # elif reaction.emoji.name == "❌" and mess.author.bot:

        #     await client.get_channel(logchannel).send(str(reaction.member.name) + " deleted the following message from " + str(mess.author.name) + " in " + str(mess.channel))

        #     try:

        #         await client.get_channel(logchannel).send(mess.content)

        #     except discord.errors.HTTPException:

        #         await client.get_channel(logchannel).send(embed = mess.embeds[0])

        #     try:

        #         await mess.delete()

        #     except discord.errors.NotFound:

        #         pass

    if reaction.emoji.name =="kinklist":
        dmchannel = await client.fetch_user(int(reaction.member.id))
        msg = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
        await KinklistCommands.kinklistA(msg.author, dmchannel, "Reaction", None)

    # elif reaction.emoji.name == "❓":
    #     mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
    #     dmchannel = await client.fetch_user(int(reaction.member.id))
    #     await client.get_channel(logchannel).send(str(reaction.member.name) + " queried the tupper of " + str(mess.author.name))
    #     await CharRegistry.charsearch("%search " + mess.author.name, dmchannel)

    #Black market react
    elif mess.id == 1089020124025061406 and reaction.emoji.name == "cuffs":
        role = discord.utils.get(reaction.member.guild.roles, name="Black Market Shopper")
        await reaction.member.add_roles(role)

    elif mess.id == 1084012997397184512 and reaction.emoji.name == "🖋️":
        role = discord.utils.get(reaction.member.guild.roles, name="Guild Applicant")
        await reaction.member.add_roles(role)

    elif mess.id == 1089268299721867285 and reaction.emoji.name == "Sigil":
        print("Adding Role to " + str(reaction.member.name))
        role = discord.utils.get(reaction.member.guild.roles, name="Dungeon Denizen")
        await reaction.member.add_roles(role)

    elif reaction.emoji.name == "smiling_imp":
        await MiscellaneuosCommands.impTomeSpawn(mess)

    elif reaction.emoji.name == "🔴":
        if mess.author.bot:
            try:
                playerID, imgURL, charName = await TupperDatabase.lookup(mess.author.display_avatar, mess)
                try:
                    player = await client.fetch_user(playerID)
                    player = " The player who sent the message was " + player.name + "/ " + player.display_name + ", and their tupper has the name of " + mess.author.name
                except discord.errors.NotFound:
                    player = " The player who sent the message could not be found, but the bot post uses the name of " + mess.author.display_name + ", and if it is a tupper, you should be able to identify it by reacting to it with ❓."
            except IndexError:
                player = " The player who sent the message could not be found, but the bot post uses the name of " + mess.author.display_name + ", and if it is a tupper, you should be able to identify it by reacting to it with ❓."
        else:
            playerID = mess.author.id
            player = await client.fetch_user(playerID)
            player = " The player who sent the message was " + mess.author.name + "/ " + mess.author.display_name
        await client.get_channel(arbchannel).send("<@&1145870554503585872>, " + reaction.member.name + "/ " + reaction.member.display_name + " has reacted to a message with a red circle. Could somebody check in to ensure everything is ok?\n\nHere's the relevant information:\nThe message (" + mess.jump_url + ") was sent in " + mess.channel.name + " at " + str(mess.created_at).split(".")[0] + ".\n" + reaction.member.name + " reacted to it with a red circle at " + str(datetime.now()).split(".")[0]  + "\n" + player)

    if liveVersion == 0:
        print(reaction)

@client.event
async def on_raw_reaction_remove(reaction):
    mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
    memb = client.get_guild(reaction.guild_id).get_member(reaction.user_id)

    if mess.id == 1088954915361144963 and reaction.emoji.name == "cuffs":
        role = discord.utils.get(memb.guild.roles, name="Black Market Shopper")
        await memb.remove_roles(role)
    elif mess.id == 1084012997397184512 and reaction.emoji.name == "🖋️":
        role = discord.utils.get(memb.guild.roles, name="Guild Applicant")
        await memb.remove_roles(role)
    elif mess.id == 1089268299721867285 and reaction.emoji.name == "sigil":
        role = discord.utils.get(memb.guild.roles, name="Dungeon Denizen")
        await memb.remove_roles(role)

# @client.event
# async def on_message_delete(message):

#     await client.get_channel(logchannel).send(message.author.name + "'s message was deleted in " + str(message.channel) + ". The message was:\n\n" + message.content.replace("@", "\@") + "\n\nThis message was deleted at " + str(datetime.now()))
   

token = botTokens.gettoken(liveVersion)
#So... Discord can't handle stickers that are animated but not a gif... And throws a Key error. We restart the Gothy client if that happens...
errorVar = 1
while errorVar == 1:
    try:
        errorVar = 0
        client.run(token, reconnect=True)
    except KeyError:
        print("Gothy crashed with a KeyError, probably from someone posting a GIF sticker again...")
        errorVar = 1


