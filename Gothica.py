import EconomyCommands
import OocFun
import CharRegistry
import KinklistCommands
import CommonDefinitions
from CommonDefinitions import *
@client.event
async def on_ready():
    print('Logged in as {0.user} at '.format(client) + str(datetime.now()).split(".")[0])
    

    #------------------DezzieAwardPoolReset--------------------


    #Read old dezzie award reset date
    economyResetDate = sheet.values().get(spreadsheetId = EconSheet, range = "D2", majorDimension='ROWS').execute().get("values")

    #Grab current date and time
    today = datetime.now()
 
    #Prepare dates for Dezzie Award Pool Reset
    try:
        oldResetDateTime = int(economyResetDate[0][0])
    except: 
        #Happens if the date isn't initialized on the econ sheet. Initialize it then.
        print("Initial reset date added!")
        resetDateInitVal = [[int(datetime.timestamp(datetime(2022, 10, 22)))]]
        sheet.values().update(spreadsheetId = EconSheet, range = "D2", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=resetDateInitVal)).execute()
        oldResetDateTime = resetDateInitVal[0][0]
        
    if oldResetDateTime < datetime.timestamp(today):

        #Calculate new timestamp
        newResetDatetime = (today - timedelta(days=today.weekday()) + timedelta(days=7)).replace(hour=0, minute=0, second=0) #Takes todays date, subtracts the passed days of the week and adds 7, resulting in the date for next monday. Then replaces time component with 0
        newResetDateTimestamp = int(datetime.timestamp(newResetDatetime))

        #Set timestamp in data
        newResetValue = [[newResetDateTimestamp]]



        print("Last reset timestamp:" + str(datetime.fromtimestamp(oldResetDateTime)))
        print("Next reset timestamp:" + str(datetime.fromtimestamp(newResetDateTimestamp)))

       
        
        #On reboot refresh dezzie pool of users
        economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:A2000", majorDimension='ROWS').execute().get("values")

        for i in range(5, len(economydata)-1, 4):            
            #Grab the name on the member
            try:
                name = economydata[i][0]
            except IndexError:
                print("Index error at: " + str(i) + ". Probably something broke in the economy sheet, and the registration of new people.")
            userStillOnServer = 1

            #Get Roles of the member. Attribute Error if they are not in the specified Guild (server)
            try:
                roles = client.get_guild(828411760365142076).get_member_named(name).roles
            except AttributeError:
                try:
                    roles = client.get_guild(847968618167795782).get_member_named(name).roles
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
        sheet.values().update(spreadsheetId = EconSheet, range = "A1:A2000", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=economydata)).execute()

        #update sheet with new refresh time
        sheet.values().update(spreadsheetId = EconSheet, range = "D2", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=newResetValue)).execute()
        print("Weekly Dezzie Award Pool Reset!")
    else:
        print("It is not dezzie award pool reset time yet!")
    #----------------------------------------------------------


    


#Main Loop

@client.event
async def on_message(message):

    if message.content.startswith("%"):

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
                
                pass

            #Voyeur's Lounge Redirect - On OocFun and Working
            if isbot and (str(message.channel).lower() == "ooc") and not (message.author.name == "Gothica" or message.author.name == "Gothica Beta"):

                await OocFun.VoyRedirect(message)
            
            #Gag - On OocFun and Working
            if not isbot and str(message.channel).lower() == "ooc" and "gagged" in str(message.author.roles).lower():

                await OocFun.gag(message)
                
            #Set Gag - On OocFun and Working
            if message.content.lower().startswith(myprefix + "gag") and "lorekeeper" in str(message.author.roles).lower():

                await OocFun.setgag(message)

            #Emote - On OocFun and Working
            if message.content.lower().startswith(str(myprefix) + "emote") and not isbot and ("lorekeeper" in str(message.author.roles).lower() or str(message.author) == "C_allum#5225"):

                await OocFun.emote(message)

            #Player Based Reactions - On OocFun and Working
            if message.channel.name.lower() == "ooc":

                await OocFun.playerreacts(message)
            
            #Character Index Update - On CharRegistry, untested
            elif message.content.lower().startswith(str(myprefix) + "indexupdate") and "moderator" in str(authroles):

                await CharRegistry.updatereg(message)

            #Character Creation Subroutine - On CharRegistry, untested
            elif str(message.channel) == "character-creation" and message.content.lower().lstrip("*").startswith("name") and not isbot:

                await CharRegistry.charcreate(message)

            #Character Edit Subroutine - On CharRegistry, untested
            elif message.content.lower().startswith(str(myprefix) + "edit") and not isbot:

                await CharRegistry.charedit(message)

            #Character Transfer Subroutine - On CharRegistry, untested            
            elif message.content.lower().startswith(str(myprefix) + "transfer") and not isbot:

                await CharRegistry.chartransfer(message)
                
            #Character List Subroutine - On CharRegistry, untested            
            elif (message.content.lower().startswith(str(myprefix) + "charlist") or message.content.lower().startswith(str(myprefix) + "list")) and not isbot:

                await CharRegistry.charlist(message)

            #Search Subroutine - On CharRegistry, untested            
            elif (message.content.lower().startswith(str(myprefix) + "search") or message.content.lower().startswith(str(myprefix) + "char")or message.content.lower().startswith(str(myprefix) + "show")) and not isbot:

                await CharRegistry.charsearch(message)

            #Retire Command - On CharRegistry, untested         
            elif message.content.lower().startswith(str(myprefix) + "retire") and not isbot:

                await CharRegistry.charretire(message)

            #Activate Command - On CharRegistry, untested            
            elif message.content.lower().startswith(str(myprefix) + "activate") and not isbot:

                await CharRegistry.charactivate(message)

            #Deactivate Command - On CharRegistry, untested             
            elif message.content.lower().startswith(str(myprefix) + "deactivate") and not isbot:

                await CharRegistry.chardeactivate(message)

            #Help Command
            
            elif message.content.lower().startswith(str(myprefix) + "help"):

                await CommonDefinitions.helplist(message)

                # msgarg = message.content.lower()

                # tit = "Gothica Help"

                # if "reg" in msgarg:

                #     desc = helptextreg

                # elif "edit" in msgarg:

                #     desc = helptextedit

                # elif "tran" in msgarg:

                #     desc = helptexttrans

                # elif "list" in msgarg:

                #     desc = helptextlist

                # elif "search" in msgarg:

                #     desc = helptextsearch

                # elif "retire" in msgarg:

                #     desc = helptextretire

                # elif "activ" in msgarg:

                #     desc = helptextactivate

                # elif "plot" in msgarg:

                #     desc = helptextplothook

                # elif "room" in msgarg:

                #     desc = helptextrooms

                # elif "wildlust" in msgarg:

                #     desc = helptextwild

                # elif "recent" in msgarg:

                #     if message.channel.id == 828519271466008586:

                #         desc = helptextrecentsmoderator

                #     else:

                #         desc = helptextrecents

                # elif "shop" in msgarg:

                #     desc = helptextshop

                # elif "veri" in msgarg and "moderator" in str(authroles).lower():

                #     desc = helptextverify

                # elif "log" in msgarg and "moderator" in str(authroles).lower():

                #     desc = helptextlogs

                # elif "lott" in msgarg and "moderator" in str(authroles).lower():

                #     desc = helptextlottery

                # elif "raid" in msgarg:

                #     desc = helptextraid

                # elif "embed" in msgarg:

                #     desc = helptextembed

                # elif "moderator" in str(authroles).lower() and message.channel.id == 828519271466008586:

                #     desc = helptext_moderator

                # else:

                #     desc = helptext

                # emb = discord.Embed(title=tit, description=desc, colour = embcol)

                # print(message.author.name + " ran a help command")

                # await message.channel.send(embed=emb)

                # await message.delete()

            #Plothook Command

            elif message.content.lower().startswith(str(myprefix) + "plothook") and not isbot:

                delay = await message.channel.send("We are processing your request now")

                if " " in message.content:

                    tempname = message.content.split(" ",1)[1]

                else:

                    tempname = None

                #get player chars

                auth = message.author.name

                pnames = sheet.values().get(spreadsheetId = CharSheet, range = "B1:B1000").execute().get("values")

                msgspl = message.content.split(" ")

                tit = None
                desc = ""
                foot = None
                imgurl = None

                pchars = sheet.values().get(spreadsheetId = CharSheet, range = "F1:F1000").execute().get("values")
                pstat = sheet.values().get(spreadsheetId = CharSheet, range = "X1:X1000").execute().get("values")
                ppron = sheet.values().get(spreadsheetId = CharSheet, range = "I1:I1000").execute().get("values")

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

                    prevlist = sheet.values().get(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = "W2:AM100", majorDimension='ROWS').execute().get("values")

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
                                
                                room = sheet.values().get(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = "A1:O1", majorDimension='COLUMNS').execute().get("values")

                                selroom = room[j][0]

                                prevlist[pind][j+1] = "".join(roomstring)

                                prevlist[pind][-1] = str(datetime.now())

                                sheet.values().update(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = str("W" + str(pind+2)), valueInputOption = "RAW", body = dict(majorDimension='ROWS', values=[prevlist[pind]])).execute()

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

            elif message.content.lower().startswith(str(myprefix) + "plotlead"):

                delay = await message.channel.send("We are processing your request now")

                prevlist = sheet.values().get(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = "R2:AC100", majorDimension='ROWS').execute().get("values")

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

            #Verify Command

            elif message.content.lower().startswith(str(myprefix) + "verify") and ("moderator" in str(message.author.roles).lower() or message.author.name == "C_allum"):

                vertarget = message.content.split("@")[1]

                verid = int(vertarget.replace("!","").replace("&","").replace(">",""))

                vermem = await message.guild.query_members(user_ids=[verid])

                vername = await client.fetch_user(verid)

                if vermem[0] != []:

                    vermemb = vermem[0]

                    role = discord.utils.get(vermemb.guild.roles, name="Verified")

                    await vermemb.add_roles(role)

                    await message.channel.send(embed = discord.Embed(title = "**Please read this before closing this ticket**", description = ":one: Go to role-selection to choose your roles. Make sure that you at least select the channels you want to have access to.\n(You can change your role and the channels you want to see anytime by un-clicking your reaction.)\n\n:two: Press on the :lock:-icon on the first message to close the ticket.\n\nYou are good to go now, enter the server and have fun :slight_smile:", colour = embcol))

                    await client.get_channel(841736084362362940).send(str(vername) + " is now verified")

                    vername = str(vername).split("#")[0]

                    verping = "<@" + vertarget

                    rand = random.randint(1,10)

                    titles = ["Say hello to " + str(vername) + "!", "Look - we found someone new - " + str(vername) + "!", "Can someone look after " + str(vername) + "?", str(vername) + " just turned up!", "We caught " + str(vername) + " trying to sneak in!", str(vername) + " just dropped in!", str(vername) + " could use some help", str(vername) + " has discovered a portal into the Dungeon!", "Helpfully discovering a hole in our ceiling, here's " + str(vername), str(vername) + " has swung in!"]

                    welcomes = ["Hello everyone! We were taking detailed notes about the xio colony in the lower halls and found a new visitor! Please say hello to " + str(verping) + "!\nNow if you'll excuse us, we must go back to find out precisely how quickly those broodmothers spawn.", "Pardon me. We were helping Sophie care for a sick tentacle, and it spat up a person! Would one of you please take care of " + str(verping) + " while We help Sophie clean up the excess slime?", str(verping) + ", here, got caught trying to look under Our skirts. Apparently, they have never heard what happens when you stare into the Abyss because they seem to be stunned by what was down there. We're sure a hot meal will do the trick though.", "We were mucking out the Cathedral's prison cells and found " + str(verping) + " tied to a post, promising to be good. Come say hello to the newest lewd convert!", str(verping) + " thought they could get in without us noticing. Everybody, make sure they feel welcome!", "This poor soul fell through a portal onto a pile of lightly used mattresses while We were changing, and seemed unable to handle the psychic stress of our unfiltered form. They've passed out from shock for now, would someone make sure they still remember their name when they wake up? I believe it's " + str(verping) + ".", str(verping) + " seems to have had a recent encounter with some of the dungeon slimes. Could someone get them some clothes, and see to it that they are taken care of?", "Oh Dear," + str(verping) + "appears to have been transported here from their native plane of existence! Could someone help them get settled into their new home?", "It's odd, We thought we had fixed that hole already? Could someone check if " + str(verping) + " is alright while we go see to the repairs again?", "We think " + str(verping) + " must have had a run in with one of the amnesia blooms in the garden. They dont seem to remember where they are! Could someone help them get settled back in while We do some weeding?"]

                    await client.get_channel(828411760847356005).send(embed = discord.Embed(title = titles[rand], description = welcomes[rand], colour = embcol))

            #Guild Adventurer Command

            elif message.content.lower().startswith(str(myprefix) + "adventurer") and ("lorekeeper" in str(message.author.roles).lower() or message.author.name == "C_allum"):

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

                    chardata = sheet.values().get(spreadsheetId = CharSheet, range = "B1:F1000", majorDimension='COLUMNS').execute().get("values")

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

            elif message.content.lower().startswith("%lfg"):

                vermemb = message.author

                try:

                    time = int(message.content.split(" ")[1]) * 3600

                except ValueError:

                    await message.channel.send("Not a valid integer, set to 1 hour.")

                    time = 3600

                except IndexError:

                    time = 3600

                role = discord.utils.get(vermemb.guild.roles, name="Looking for Role Play")

                await vermemb.add_roles(role)

                await message.channel.send("Looking for Role Play role set.")

                await asyncio.sleep(time)

                await vermemb.remove_roles(role)

            #Kink Functions
            elif message.content.lower().startswith(str(myprefix) + "kinklist"):
                await KinklistCommands.kinklist(message)
            elif message.content.lower().startswith(str(myprefix) + "kinkedit"):
                await KinklistCommands.kinkedit(message)
            elif message.content.lower().startswith(str(myprefix) + "kinkplayers"):
                await KinklistCommands.kinkplayers(message)
            elif message.content.lower().startswith(str(myprefix) + "kinkencounter"):
                await KinklistCommands.kinkencounter(message)
            elif message.content.lower().startswith(str(myprefix) + "kinksurvey"):
                await KinklistCommands.kinksurvey(message)
            elif message.content.lower().startswith(str(myprefix) + "kinkhelp"):
                await KinklistCommands.kinkhelp(message)
            elif message.content.lower().startswith(str(myprefix) + "kinkcompare"):
                await KinklistCommands.kinkcompare(message)

            #Start
            
            elif message.content.lower().startswith(str(myprefix) + "start"):

                welcdesc = "This guide was created to streamline the process of joining the general roleplay in the server.\n\n**Role Selection:** The first thing you should do is head up to " + str(client.get_channel(880605891366375435).mention) + ", where you can choose roles based on what you're interested in and how you define yourself. To see the roleplay channels, you'll need the RP-Intro (<:gem:944690539553513492>) role.\n\nAfter that, you'll need to go to " + str(client.get_channel(895531096350011442).mention) + ". This contains an overview of the lore of the setting, as well as the rules for roleplaying within it. Once you've read through that, click the D20 (" + critemj + ") to accept the rules. This will allow to to access the public roleplay channels.\n\n**Generating Stats:** Now that you can access the " + str(client.get_channel(828412055228514325).mention) + " channel, you can create a character to play as. We allow characters up to level 14, though we recommend being between 4 and 10 due to balance on certain things. You can use any method to roll stats that you would like, as long as it is within reason. If you want to roll (4D6, dropping the lowest is the usual way), you can use the " + str(client.get_channel(903415692693475348).mention) + " thread. We use Avrae on the server for dice rolls, and we have the prefix for it set to: &. This means that to roll 4d6 dropping the lowest, you would do: `&r 4d6kh3`. Avrae also has `&randchar`, which will generate all 6 stats for you in this method. Sheets are only really used for certain things like raids (combat events in the dungeon), so it is possible to not use stats at all.\n\n**Character Creation:** To create your character, provide some information about them, starting with their name. There is a template pinned in " + str(client.get_channel(828412055228514325).mention) + ", which includes all the possible bits of information you can use, though you don't need to use all of these. You can also include an image here to show everyone what your character looks like.\n\n**Tuppers:** Most people in the dungeon roleplay using tuppers - aliases which replace your message with those of your character's. To set one up, head to: " + str(client.get_channel(903416425706831902).mention) + " and use the `?register` command. This has the following format: `?register name [text]`, where name is the name of your character as you want it to appear (in quotes if you have a space) and the brackets around the word 'text' can be anything, on either side of the word, and is how you trigger the bot to replace your message. For example, one of the brackets I use is £text, which replaces any of my messages which start with a £ symbol. If it's a character I use less often, I will use their name and a colon. You should include your image in this command as well, or add it to the tupper later using `?avatar name` and adding the link or attaching the image.\n\n**Arranging role-play:** Use the " + str(client.get_channel(832435243117445131).mention) + " channel to arrange scenes with people, or simply drop your character into one of the common rooms and someone will likely join you.\n\nHave fun!" 

                await message.channel.send(embed = discord.Embed(title = "Celia's Lewd Dungeon - How to get started?", description = welcdesc, colour = embcol))

                await message.delete()

            #Room Command

            elif message.content.lower().startswith(str(myprefix) + "room"):

                rooms = ["unlit-passageways", "trapped-corridors", "moaning-hallways", "salamander-hot-springs", "monster-girl-cantina", "the-ole-burlesque", "backstage-burlesque", "library-of-carnal-knowledge", "the-cathedral", "sparring-pit", "spectators-stands", "unlicensed-fights", "💎the-gobblin-bazaar💎", "🏺the-golden-jackal🏺", "🐍venom-ink🐍", "🧵widows-boutique🧵", "🍄sophies-garden🍄", "📜menagerie-magiks📜", "🔔the-polished-knob🔔"]

                if not "explorer" in str(authroles).lower():

                    rooms.remove("sparring-pit")
                    rooms.remove("spectators-stands")
                    rooms.remove("unlicensed-fights")

                while 1:

                    roll = random.choice(rooms)

                    roomchannel = discord.utils.get(client.get_all_channels(), name = roll)

                    roomlatest = [joinedMessages async for joinedMessages in client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()] #Fix for pebblehost Await issue
                    #roomlatest = await client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()

                    if roomlatest[0].author == client.user:

                        roomlatest[0] = roomlatest[1]

                        scenebroken = True

                    else:

                        scenebroken = False

                    rtimestamp = roomlatest[0].created_at

                    mestimestamp = message.created_at

                    diff = str(mestimestamp - rtimestamp)

                    if "day" in diff:

                        tit = str("You could roleplay in the " + roll.replace("-", " ").title()).replace("the the", "the")

                        if "days" in diff:

                            diffplu = str(diff.split(" day")[0]) +  " days."
                        
                        else:

                            diffplu = "a day."

                        desc = "It has been inactive for over " + diffplu

                        if not scenebroken:

                            await client.get_channel(roomchannel.id).send("```\u200b```")

                        break

                    else:

                        hours = int(diff.split(":")[0])

                        if hours >= 3:

                            tit = str("You could roleplay in the " + roll.replace("-", " ").title()).replace("the the", "the")

                            desc = "It has been inactive for over " + str(hours) + " hours."

                            if not scenebroken:

                                await client.get_channel(roomchannel.id).send("```\u200b```")

                            break

                        else:

                            rooms.remove(roll)

                            if len(rooms) == 0:

                                tit = "All public rooms have been used within the last few hours. Check if any have recently moved to threads, ask if you can join an active scene, or go straight to a private thread?"

                                desc = "We hadn't expected to need this message.."

                                break

                roomemb = discord.Embed(title = tit, description = desc, colour = embcol)

                roomemb.set_footer(text = "----------------------------------------------------------\n\nThis suggestion was made in response to a command from " + message.author.name)

                print(message.author.name + " used the room command, getting: " + roll)

                await message.channel.send(embed = roomemb)

                await message.delete()

            #Scene Break Command

            elif message.content.lower().startswith(str(myprefix) + "br"):

                if isbot:

                    await message.delete()

                else:

                    await message.delete()

                    await message.channel.send("```\u200b```")

                    print(message.author.name + " created a scene division")

            #Embed Command

            elif message.content.lower().startswith(str(myprefix) + "embed") and not isbot:

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

                if not "moderator" in str(authroles).lower():

                    await client.get_channel(logchannel).send(str(message.author) + " generated an embed in " + str(message.channel.name))

                    if not "lore" in str(authroles).lower():

                        cusemb.set_footer(text = "----------------------------------------------------\n\nThis embed was generated by " + message.author.name)

                if not img == "":

                    cusemb.set_image(url = img)

                if not thum == "":

                    cusemb.set_thumbnail(url = thum)

                print(message.author.name + " generated an embed")

                await message.channel.send(embed = cusemb)

                await message.delete()

            elif message.content.lower().startswith(str(myprefix) + "oocembed") and "lorekeeper" in str(message.author.roles).lower():

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

                if not "moderator" in str(authroles).lower():

                    await client.get_channel(logchannel).send(str(message.author) + " generated an embed in " + str(message.channel.name))

                    if not "lore" in str(authroles).lower():

                        cusemb.set_footer(text = "----------------------------------------------------\n\nThis embed was generated by " + message.author.name)

                if not img == "":

                    cusemb.set_image(url = img)

                if not thum == "":

                    cusemb.set_thumbnail(url = thum)

                print(message.author.name + " generated an embed")

                await client.get_channel(832435243117445131).send(embed = cusemb)

                await message.channel.send("Embed sent to ooc.")

            elif message.content.lower().startswith(str(myprefix) + "oocmsg") and ("lorekeeper" in str(message.author.roles).lower() or str(message.author) == "C_allum#5225"):

                await client.get_channel(832435243117445131).send(message.content.split(" ", 1)[1].replace("The Mistress", "T̴̯̳̳̠͚͓͚̂͗̽̾̈́͌̐̅͠ͅh̸̨̫͓͖͎͍͔̠͇̊̂̏͝ę̶͎͇͍̲̮̠̭̮͛̃̈́͑̓̔̚ ̸͙̺̦̮͈̹̮̑̿̊̀̂́͂̿͒̚͜M̶̬͇̤̾͐̊̽̈́̀̀̕͘͝í̸̬͎͔͍̠͓̋͜͠͝s̶̡̡̧̪̺͍̞̲̬̮͆͋̇̐͋͌̒̋͛̕t̷̤̲̠̠̄̊͌̀͂̈́̊̎̕ȓ̶̼̂̿̇͛̚e̶̹̪̣̫͎͉̫̫͗s̸̟͉̱͈̞̬̽̽̒̔́̉s̸̛̖̗̜̻̻͚̭͇̈́̀̄͒̅̎"))

                await message.channel.send("Message sent to ooc")

            #Recent Activity Command

            elif message.content.lower().startswith(str(myprefix) + "recent"):

                delay = await message.channel.send("We are processing your request now")

                if "break" in message.content.lower() and "moderator" in authroles.lower():

                    rbreak = True

                else:

                    rbreak = False

                rooms = ["💎the-gobblin-bazaar💎", "🏺the-golden-jackal🏺", "🐍venom-ink🐍", "🧵widows-boutique🧵", "🍄sophies-garden🍄", "📜menagerie-magiks📜", "🔔the-polished-knob🔔", "💰-adventurers-guild-💰", "unlit-passageways", "salamander-hot-springs", "monster-girl-cantina", "the-ole-burlesque", "backstage-burlesque", "library-of-carnal-knowledge", "the-cathedral", "spectators-stands", "trapped-corridors", "moaning-hallways",  "unlicensed-fights", "sparring-pit", "kobold-dens", "wild-gardens", "twilight-groves", "sirens-grotto"]

                meslatest = []

                for n in range(len(rooms)):
                    
                    roomchannel = discord.utils.get(client.get_all_channels(), name = rooms[n])

                    #roomlatest = await client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()
                    roomlatest = [joinedMessages async for joinedMessages in client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()] #Fix for pebblehost Await issue

                    if roomlatest[0].author == client.user:

                        roomlatest[0] = roomlatest[1]

                        scenebroken = True

                    else:

                        scenebroken = False

                    rtimestamp = roomlatest[0].created_at

                    mestimestamp = message.created_at

                    diff = str(mestimestamp - rtimestamp)

                    meslatest.append(rooms[n] + " - Last used " + diff.split(":")[0] + " hours and " + diff.split(":")[1] + " minutes ago.")

                    if not "day" in diff:

                        hours = int(diff.split(":")[0])

                        if hours >= 3 and not scenebroken and rbreak:

                            await client.get_channel(roomchannel.id).send("```\u200b```")

                    elif not scenebroken and rbreak:

                        await client.get_channel(roomchannel.id).send("```\u200b```")

                print(message.author.name + " ran the recent activity command")

                await message.channel.send(embed = discord.Embed(title = "Last messages in each public room:", description = "\n".join(meslatest), colour = embcol))

                await message.delete()

                await delay.delete()

            #Invest Command

            elif message.content.lower().startswith(str(myprefix) + "invest"):

                devdata = sheet.values().get(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = "AS1:AX200", majorDimension='COLUMNS').execute().get("values")

                if str(message.channel).lower() in str(devdata[0]).lower():

                    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                    reciprow = ""

                    target = message.author

                    targname = target.name

                    for a in range(math.floor(len(economydata)/4)):

                        b = a * 4 + 5

                        if str(targname + "#" + str(target.discriminator)) in str(economydata[b][0]):

                            reciprow = b + 1

                            break

                    try:
                        
                        giveamount = int(message.content.split(" ")[1].strip("-"))

                    except ValueError:

                        giveamount = int(message.content.split(" ")[2].strip("-"))
                    
                    if giveamount >= float(int(devdata[1][row])/4):

                        giveamount = math.floor(int(devdata[1][row])/4)

                        await message.channel.send(embed = discord.Embed(title = "You cannot donate that much!", description = "You cannot donate more than 1/4 of the project cost by yourself. We appreciate your generosity, and have set your donation to the maximum of " + str(math.floor(int(devdata[1][row])/4))))

                    if giveamount > int(economydata[reciprow-1][1]):

                        await message.channel.send(embed=discord.Embed(title = "You don't have enough money to do that.", description = "You only have " + str((economydata[reciprow-1][1]) + dezzieemj), colour = embcol))

                    else:

                        recipnewtot = int(economydata[reciprow-1][1]) - int(giveamount)

                        if not (str(message.author) == "C_allum#5225" and "-" in message.content):

                            sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

                        if str(message.channel).lower() in str(devdata).lower():

                            for a in range(len(devdata[0])):

                                if (message.channel.name).lower() in str(devdata[0][a]).lower():

                                    row = a

                            #Contributors

                            try:

                                devconts = devdata[5][row].split("|")

                            except IndexError:

                                devconts = ""

                                print(devdata)
                             
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
                                
                                imglist = ["https://i.ibb.co/TPRKffZ/loading-dezzie0001.png","https://i.ibb.co/1m60NWV/loading-dezzie0002.png","https://i.ibb.co/FnfHtf3/loading-dezzie0003.png","https://i.ibb.co/28h1xK4/loading-dezzie0004.png","https://i.ibb.co/pnv2RSL/loading-dezzie0005.png","https://i.ibb.co/7nyXP9t/loading-dezzie0006.png","https://i.ibb.co/HPtc5QW/loading-dezzie0007.png","https://i.ibb.co/H7SG2rV/loading-dezzie0008.png","https://i.ibb.co/NTDGY9b/loading-dezzie0009.png","https://i.ibb.co/tqQLm7L/loading-dezzie0010.png","https://i.ibb.co/nzgJR1M/loading-dezzie0011.png","https://i.ibb.co/nD7jHjT/loading-dezzie0012.png","https://i.ibb.co/T2jVx0h/loading-dezzie0013.png","https://i.ibb.co/s3bb0Gt/loading-dezzie0014.png","https://i.ibb.co/RjCXnY8/loading-dezzie0015.png","https://i.ibb.co/3mKY69j/loading-dezzie0016.png","https://i.ibb.co/f4Xjg63/loading-dezzie0017.png","https://i.ibb.co/7Qh98cb/loading-dezzie0018.png","https://i.ibb.co/k0mW2hZ/loading-dezzie0019.png","https://i.ibb.co/wRxCQVM/loading-dezzie0020.png","https://i.ibb.co/tz7fFFg/loading-dezzie0021.png","https://i.ibb.co/pxkBpP5/loading-dezzie0022.png","https://i.ibb.co/SNLbxt1/loading-dezzie0023.png","https://i.ibb.co/HGV26LQ/loading-dezzie0024.png","https://i.ibb.co/FzxGXX1/loading-dezzie0025.png","https://i.ibb.co/4KkZcqh/loading-dezzie0026.png","https://i.ibb.co/p4mkH4x/loading-dezzie0027.png","https://i.ibb.co/z6LZgCs/loading-dezzie0028.png","https://i.ibb.co/GnQKHGS/loading-dezzie0029.png","https://i.ibb.co/rbbjzNP/loading-dezzie0030.png","https://i.ibb.co/m8D5YqF/loading-dezzie0031.png","https://i.ibb.co/nfysj4L/loading-dezzie0032.png","https://i.ibb.co/1T4f7YQ/loading-dezzie0033.png","https://i.ibb.co/tLp7RK2/loading-dezzie0034.png","https://i.ibb.co/t8Ygm5C/loading-dezzie0035.png","https://i.ibb.co/1zB0yPV/loading-dezzie0036.png","https://i.ibb.co/SBB5d6f/loading-dezzie0037.png","https://i.ibb.co/4mPvSdy/loading-dezzie0038.png","https://i.ibb.co/3S9Dhrt/loading-dezzie0039.png","https://i.ibb.co/M1XKkYB/loading-dezzie0040.png","https://i.ibb.co/b5VzVYz/loading-dezzie0041.png","https://i.ibb.co/5rwTJQj/loading-dezzie0042.png","https://i.ibb.co/cK9y4t6/loading-dezzie0043.png","https://i.ibb.co/qDYBfFs/loading-dezzie0044.png","https://i.ibb.co/grW8NsN/loading-dezzie0045.png","https://i.ibb.co/Vj84zY4/loading-dezzie0046.png","https://i.ibb.co/mX7FMBY/loading-dezzie0047.png","https://i.ibb.co/MZBmZqR/loading-dezzie0048.png","https://i.ibb.co/zSxQsbM/loading-dezzie0049.png","https://i.ibb.co/7pSkMxj/loading-dezzie0050.png","https://i.ibb.co/DG2KqYG/loading-dezzie0051.png","https://i.ibb.co/84bngKX/loading-dezzie0052.png","https://i.ibb.co/S5scHyC/loading-dezzie0053.png","https://i.ibb.co/kQsmr9q/loading-dezzie0054.png","https://i.ibb.co/r5PTVPj/loading-dezzie0055.png","https://i.ibb.co/j9KcKsf/loading-dezzie0056.png","https://i.ibb.co/3NVMCNG/loading-dezzie0057.png","https://i.ibb.co/9rfyp5h/loading-dezzie0058.png","https://i.ibb.co/7KCSQ90/loading-dezzie0059.png","https://i.ibb.co/vQVJQRp/loading-dezzie0060.png","https://i.ibb.co/HPRxwJ8/loading-dezzie0061.png","https://i.ibb.co/pbBTqS8/loading-dezzie0062.png","https://i.ibb.co/563ZBfN/loading-dezzie0063.png","https://i.ibb.co/FY065ty/loading-dezzie0064.png","https://i.ibb.co/qxCzJR3/loading-dezzie0065.png","https://i.ibb.co/T8PBnJN/loading-dezzie0066.png","https://i.ibb.co/fFm92D0/loading-dezzie0067.png","https://i.ibb.co/mcJ47qj/loading-dezzie0068.png","https://i.ibb.co/4VyvV9G/loading-dezzie0069.png","https://i.ibb.co/Y2qFHN1/loading-dezzie0070.png","https://i.ibb.co/593DGqF/loading-dezzie0071.png","https://i.ibb.co/v30RgH4/loading-dezzie0072.png","https://i.ibb.co/b351RF0/loading-dezzie0073.png","https://i.ibb.co/x3rv11r/loading-dezzie0074.png","https://i.ibb.co/ySNh943/loading-dezzie0075.png","https://i.ibb.co/BjPSpDZ/loading-dezzie0076.png","https://i.ibb.co/NNwSpKy/loading-dezzie0077.png","https://i.ibb.co/mN8mdt9/loading-dezzie0078.png","https://i.ibb.co/TK3jtVx/loading-dezzie0079.png","https://i.ibb.co/WgjtBZ5/loading-dezzie0080.png","https://i.ibb.co/BKxybMV/loading-dezzie0081.png","https://i.ibb.co/kBRxqZk/loading-dezzie0082.png","https://i.ibb.co/CzmTPbK/loading-dezzie0083.png","https://i.ibb.co/sQr72KL/loading-dezzie0084.png","https://i.ibb.co/4j3fdf0/loading-dezzie0085.png","https://i.ibb.co/x1jGjxM/loading-dezzie0086.png","https://i.ibb.co/jD4NVCY/loading-dezzie0087.png","https://i.ibb.co/S6yKQYb/loading-dezzie0088.png","https://i.ibb.co/bNkrGSn/loading-dezzie0089.png","https://i.ibb.co/d0NXt5z/loading-dezzie0090.png","https://i.ibb.co/smfYLDV/loading-dezzie0091.png","https://i.ibb.co/XS1c3x6/loading-dezzie0092.png","https://i.ibb.co/1vJtBtS/loading-dezzie0093.png","https://i.ibb.co/98BCvYt/loading-dezzie0094.png","https://i.ibb.co/cYctMPp/loading-dezzie0095.png","https://i.ibb.co/pP6SQvd/loading-dezzie0096.png","https://i.ibb.co/gSSqZGp/loading-dezzie0097.png","https://i.ibb.co/hLP8k2R/loading-dezzie0098.png","https://i.ibb.co/XyLFCn3/loading-dezzie0099.png"]
                                
                                imlink = imglist[percent]

                                investemb.set_image(url = imlink)

                            await message.channel.send(embed = investemb)

                            sheet.values().update(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = str("AV" + str(row+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newtotal]])).execute()

                            sheet.values().update(spreadsheetId = "17ZTklwFnnrVk1qeZLOnEK6YacNQusRljUxaSXTvPDWU", range = str("AX" + str(row+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[contributors]])).execute()

                else:

                    await message.delete()

                    await message.channel.send(embed = discord.Embed(title = "This channel isn't set up to receive donations", description = "If you believe this to be in error, contact the moderator team", colour = embcol))

            #Poker Setup Command

            elif message.content.lower().startswith(str(myprefix) + "poker"):
                
                gamedata = sheet.values().get(spreadsheetId = gamesheet, range = "A1:E1000").execute().get("values")

                gamevalue = len(gamedata)

                threadid = await message.create_thread(name= "Poker Game: " + str(gamevalue))

                cardtemp = cardnames

                random.shuffle(cardtemp)

                cardtemp.append(str(0))
                
                gameinit = [gamevalue, "Poker", 0, "", "", "|".join(cardtemp)]

                sheet.values().append(spreadsheetId = gamesheet, range = "A2", valueInputOption = "USER_ENTERED", body = {'values':[gameinit]}).execute()

                await threadid.send(embed = discord.Embed(title = "Gothica's Gambling Games! - Texas Hold'em Poker", description = "To be done: Add summary of rules\nTo be dealt into this hand, send a message in this thread containing the name of the character you are playing. When everyone is in, type `Ready`"))

            #In Poker Thread

            elif str(message.channel).startswith("Poker Game"):

                tit = "Lucky Hare Casino's Texas Hold'em Poker"
                
                #Poker Game

                gamedata = sheet.values().get(spreadsheetId = gamesheet, range = "A1:F1000").execute().get("values")

                econdata =  sheet.values().get(spreadsheetId = EconSheet, range = "A6:B2000", majorDimension = 'ROWS').execute().get("values")

                for n in range(math.ceil(len(econdata)/4)):

                    r = 4 * n 

                    if str(message.author) in econdata[r][0]:

                        #Check Balance!

                        currentbal = int(econdata[r][1])

                        econrow = r

                        break

                #Get Game Value

                for gv in range(len(gamedata)):

                    if gv != 0:

                        if str(message.channel) == "Poker Game " + str(gv):

                            #Get Game Position

                            state = int(gamedata[gv][2])

                            if state == 0: # Getting Players and Dealing Hands

                                #Get Players

                                if message.content.lower() != "ready":

                                    if not message.author.name in gamedata[gv][3] and not isbot:

                                        if currentbal < int(bigblind):

                                            await message.channel.send(embed=discord.Embed(title = tit, description = message.author.name + ", you do not have enough dezzies to play this game. The starting bid is set at " + str(bigblind) + dezzieemj + ". \n\nYou can earn more by running the `%work` or `%slut` commands.", colour = embcol))

                                        else:

                                            if len(gamedata[gv][3]) == 0:

                                                players = message.author.name + "'s " + message.content.title().replace("|", "")

                                                playerids = str(econrow) + "-" + str(message.author.id)

                                            else:

                                                players = gamedata[gv][3] + "|" + message.author.name + "'s " + message.content.title().replace("|", "")

                                                playerids = str(gamedata[gv][4]) + "|" + str(econrow) + "-" + str(message.author.id)

                                            await message.channel.send(embed=discord.Embed(title = tit, description = message.author.name + "'s " + message.content.title() + " has joined the game\n\nType 'Ready' to begin.", colour = embcol))

                                            #Add Player to Sheet

                                            sheet.values().update(spreadsheetId = gamesheet, range = "D" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[[players]]}).execute()

                                            sheet.values().update(spreadsheetId = gamesheet, range = "E" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[[playerids]]}).execute()

                                    else:

                                        await message.channel.send(embed=discord.Embed(title = tit, description = message.author.name + ", you already have a character in this game!", colour = embcol))

                                elif len(gamedata[gv][3].split("|")) < 2:

                                    await message.channel.send(embed=discord.Embed(title = tit, description = "You need at least two players to play this game!\n\nWe're working on adding NPCs, so this might change in future.", colour = embcol))

                                else:

                                    #DM Cards to each player

                                    playerids = str(gamedata[gv][4]).split("|")

                                    smallblindtaken = 0

                                    for p in range(len(playerids)):

                                        playerrow = int(playerids[p].split("-")[0])

                                        playerid = str(playerids[p].split("-")[1])

                                        pcards = gamedata[gv][5].split("|")

                                        dmchannel = await client.fetch_user(int(playerid))
                                        
                                        await dmchannel.send(embed = discord.Embed(title = "Lucky Hare Poker Game " + str(gv), description = str(pcards[p*2] + " and " + pcards[p*2+1]), colour = embcol))

                                        try:

                                            if p == 1:

                                                currentbal = int(econdata[playerrow][1]) - bigblind

                                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(playerrow + 6)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[currentbal]])).execute()

                                            elif (p == 2):

                                                currentbal = int(econdata[playerrow][1]) - smallblind

                                                smallblindtaken = 1

                                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(playerrow + 6)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[currentbal]])).execute()

                                        except IndexError:

                                            playerrow = int(playerids[0].split("|")[0].split("-")[0])

                                            currentbal = int(econdata[playerrow][1]) - smallblind

                                            print(econdata[playerrow-6][0])

                                            sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(playerrow + 6)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[currentbal]])).execute() 

                                    if not smallblindtaken:

                                        playerrow = int(playerids[0].split("|")[0].split("-")[0])

                                        currentbal = int(econdata[playerrow][1]) - smallblind

                                        print(econdata[playerrow-6][0])

                                        sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(playerrow + 6)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[currentbal]])).execute() 

                                    pname = str(gamedata[gv][3]).split("|")

                                    cname = []

                                    for i in range(len(pname)):
            
                                        cname.append(pname[i].split(" ",1)[1])

                                    playerspl = gamedata[gv][3].split("|")

                                    if len(cname) == 2:

                                        await message.channel.send(embed=discord.Embed(title = tit, description = "Playing with:\n\n" + "\n".join(gamedata[gv][3].split("|")) + "\n\nYou have each been sent your hand via direct message. The small blind is " + str(smallblind) + dezzieemj + ", paid by " + cname[0] + ", while " + cname[1] + " is paying the big blind of " + str(bigblind) + dezzieemj +  ". " + cname[0] + ", will you call, raise, or fold?", colour = embcol))
                                        
                                        playerspl[0] = playerspl[0] = ">" + str(smallblind) + "£" + playerspl[0]

                                        playerspl[1] = "<" + str(bigblind) + "£" + playerspl[1]

                                    else:

                                        await message.channel.send(embed=discord.Embed(title = tit, description = "Playing with:\n\n" + "\n".join(gamedata[gv][3].split("|")) + "\n\nYou have each been sent your hand via direct message. The small blind is " + str(smallblind) + dezzieemj + ", paid by " + cname[0] + ", while " + cname[1] + " is paying the big blind of " + str(bigblind) + dezzieemj +  ". " + cname[2] + ", will you call, raise, or fold?", colour = embcol))

                                        playerspl[0] = str(smallblind) + "£" + playerspl[0]
                                        
                                        playerspl[1] = "<" + str(bigblind) + "£" + playerspl[1]

                                        playerspl[2] = ">" + playerspl[2]

                                    playersjoined = "|".join(playerspl)  

                                    sheet.values().update(spreadsheetId = gamesheet, range = "D" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[[playersjoined]]}).execute()

                                    #Update State

                                    sheet.values().update(spreadsheetId = gamesheet, range = "C" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[[1]]}).execute()

                            elif state == 1: # Getting initial bids

                                if message.author.name in gamedata[gv][3]:

                                    players = gamedata[gv][3].split("|")

                                    playersfull = players

                                    for m in range(len(players)):

                                        if "¬" in players[m]:

                                            players.remove("¬")

                                    for i in range(len(players)):

                                        if message.author.name in players[i] and ">" in players[i]:

                                            #Find highest bid this round

                                            currentbid = max([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")])

                                            if "raise" in message.content.lower():

                                                if not ("call" in message.content.lower() or "fold" in message.content.lower()):

                                                    #Check amount to be raised by

                                                    raiseval = [int(s) for s in re.findall(string=str(message.content), pattern="[0-9]+")]

                                                    #Get new pot

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")]) + int(raiseval[0]) + currentbid - sum([int(n) for n in re.findall(string=str(players[i]), pattern="[0-9]+")])

                                                    #Get new total bid

                                                    newbid = int(currentbid) + int(raiseval[0])

                                                    #Get next player in list

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    #Send bid update to players, prompt next player.

                                                    await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " raised by " + str(raiseval[0]) + " dezzies!\n\nThe bid is now " + str(newbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold.", colour = embcol)))

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            if "£" in players[i]:

                                                                rejoin.append("<" + str(newbid) + "£" + players[i].split("£")[1])
                                                    
                                                            else:

                                                                rejoin.append("<" + str(newbid) + "£" + players[i])

                                                        else:

                                                            rejoin.append(playersfull[n].replace("<",""))

                                                    gamedata[gv][3] = "|".join(rejoin)

                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

                                            elif "call" in message.content.lower():

                                                if not ("raise" in message.content.lower() or "fold" in message.content.lower()):

                                                    #Get new pot

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")]) + int(currentbid) - sum([int(n) for n in re.findall(string=str(players[1]), pattern="[0-9]+")])

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    if (not "<" in next and not "<" in players[i]) or gamedata[gv][3].count(str(currentbid)) != len(players):

                                                        if not "NPC" in next:

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold.", colour = embcol)))

                                                        else:

                                                            #To do: Add logic to determine if the NPC should raise.

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + "called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + " is an NPC, and needs to actually be taught how to play...", colour = embcol)))

                                                    else:

                                                        await message.channel.send(embed=discord.Embed(title=tit, description="Everyone has matched the bid! The flop is:\n\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+1]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+2]), colour = embcol))

                                                        #Update the state.

                                                        gamedata[gv][2] = 2

                                                        if len(players) >= 3:

                                                            players[2] = "><" + players[2]

                                                        else:

                                                            players[0] = "><" + players[0]

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            if "£" in players[i]:

                                                                rejoin.append(str(currentbid) + "£" + players[i].split("£")[1])
                                                    
                                                            else:

                                                                rejoin.append(str(currentbid) + "£" + players[i])

                                                        else:

                                                            rejoin.append(playersfull[n])

                                                    gamedata[gv][3] = "|".join(rejoin)
                                                    
                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

                                            elif "fold" in message.content.lower():

                                                if not ("raise" in message.content.lower() or "call" in message.content.lower()):

                                                    for t in range(len(playersfull)):

                                                        if players[i].split(" ",1)[1] in playersfull[t]:

                                                            playersfull[t] = "¬" + playersfull[t]

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")])

                                                    if len(players) -1 == 1:

                                                        foldamount = []
                                                        payout = []
                                                        winner = ""

                                                        for b in range(len(playersfull)):

                                                            if "<" in playersfull[b]:

                                                                winner = playersfull[b].split("£")[1]

                                                        for b in range(len(playersfull)):

                                                            foldamount.append(sum([int(n) for n in re.findall(string=str(playersfull[b]), pattern="[0-9]+")]))

                                                            if "¬" in playersfull[b]:

                                                                payout.append(playersfull[b].split("£")[1] + " loses " + str(foldamount[b]) + ":dz:. Please give them to " + winner.split(" ",1)[1] + ", using the command: `$give-money @" + winner.split("'",1)[0] + " " + str(foldamount[b]) + "`")

                                                            else:

                                                                payout.append("")

                                                        await message.channel.send(embed=discord.Embed(title=tit, description=str(winner.split(" ",1)[1] + " has won the hand!\n\n" + "\n".join(payout) + "\n\nIncluding " + winner.split(" ",1)[1] + "'s own bid of " + str(currentbid) + ", that equals the pot of " + str(pot) + "\n\nWould you like to play another hand?", colour = embcol)))
                                                        break

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    if (not "<" in next and not "<" in players[i]) or gamedata[gv][3].count(str(currentbid)) != len(players):

                                                        if not "NPC" in next:

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " folded!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold."), colour = embcol))

                                                        else:

                                                            #To do: Add logic to determine if the NPC should raise.

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + "called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + " is an NPC, and needs to actually be taught how to play..."), colour = embcol))

                                                    else:

                                                        await message.channel.send(embed=discord.Embed(title=tit, description="Everyone has matched the bid or folded! The flop is:\n\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+1]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+2]), colour = embcol))

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            rejoin.append(str("¬" + players[i]))

                                                        else:

                                                            rejoin.append(playersfull[n])

                                                    gamedata[gv][3] = "|".join(rejoin)

                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

                                        else:

                                            if not message.author.name in players:

                                                await message.channel.send(embed = discord.Embed(title = "Lucky Hare Casino's Texas Hold'em Poker", description = message.author.name + ", you are not in this game. You need to join before the hand is dealt.\n\nIt is " + players[i] + "'s turn"))

                                            else:

                                                await message.channel.send(embed = discord.Embed(title = "Lucky Hare Casino's Texas Hold'em Poker", description = message.author.name + ", it is not currently your turn.\n\nWe are waiting on " + players[i], colour = embcol))

                            elif state == 2: # After the flop

                                if message.author.name in gamedata[gv][3]:

                                    players = gamedata[gv][3].split("|")

                                    playersfull = players

                                    for m in range(len(players)):

                                        if "¬" in players[m]:

                                            players.remove("¬")

                                    for i in range(len(players)):

                                        if message.author.name in players[i] and ">" in players[i]:

                                            #Find highest bid this round

                                            currentbid = max([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")])

                                            if "raise" in message.content.lower():

                                                if not ("call" in message.content.lower() or "fold" in message.content.lower()):

                                                    #Check amount to be raised by

                                                    raiseval = [int(s) for s in re.findall(string=str(message.content), pattern="[0-9]+")]

                                                    #Get new pot

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")]) + int(raiseval[0]) + currentbid - sum([int(n) for n in re.findall(string=str(players[i]), pattern="[0-9]+")])

                                                    #Get new total bid

                                                    newbid = int(currentbid) + int(raiseval[0])

                                                    #Get next player in list

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    #Send bid update to players, prompt next player.

                                                    if not "NPC" in next:

                                                        await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " raised by " + str(raiseval[0]) + " dezzies!\n\nThe bid is now " + str(newbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold."), colour = embcol))

                                                    else:

                                                        #To do: Add logic to determine if the NPC should raise.

                                                        await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " raised by " + str(raiseval[0]) + " dezzies!\n\nThe bid is now " + str(newbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + " is an NPC, and needs to actually be taught how to play..."), colour = embcol))

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            rejoin.append("<" + str(newbid) + "£" + players[i].split("£")[1])

                                                        else:

                                                            rejoin.append(playersfull[n].replace("<",""))

                                                    gamedata[gv][3] = "|".join(rejoin)

                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

                                            elif "call" in message.content.lower():

                                                if not ("raise" in message.content.lower() or "fold" in message.content.lower()):

                                                    #Get new pot

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")]) + int(currentbid) - sum([int(n) for n in re.findall(string=str(players[1]), pattern="[0-9]+")])

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    if (not "<" in next and not "<" in players[i]) or gamedata[gv][3].count(str(currentbid)) != len(players):

                                                        if not "NPC" in next:

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold."), colour = embcol))

                                                        else:

                                                            #To do: Add logic to determine if the NPC should raise.

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + "called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + " is an NPC, and needs to actually be taught how to play..."), colour = embcol))

                                                    else:

                                                        await message.channel.send(embed=discord.Embed(title=tit, description="Everyone has matched the bid! The flop is:\n\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+1]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+2]), colour = embcol))

                                                        #Update the state.

                                                        gamedata[gv][2] = 2

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            if "£" in players[i]:

                                                                rejoin.append(str(currentbid) + "£" + players[i].split("£")[1])
                                                    
                                                            else:

                                                                rejoin.append(str(currentbid) + "£" + players[i])

                                                        else:

                                                            rejoin.append(playersfull[n])

                                                    gamedata[gv][3] = "|".join(rejoin)
                                                    
                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

                                            elif "fold" in message.content.lower():

                                                if not ("raise" in message.content.lower() or "call" in message.content.lower()):

                                                    for t in range(len(playersfull)):

                                                        if players[i].split(" ",1)[1] in playersfull[t]:

                                                            playersfull[t] = "¬" + playersfull[t]

                                                    pot = sum([int(n) for n in re.findall(string=str(gamedata[gv][3]), pattern="[0-9]+")])

                                                    if len(players) -1 == 1:

                                                        foldamount = []
                                                        payout = []
                                                        winner = ""

                                                        for b in range(len(playersfull)):

                                                            if "<" in playersfull[b]:

                                                                winner = playersfull[b].split("£")[1]

                                                        for b in range(len(playersfull)):

                                                            foldamount.append(sum([int(n) for n in re.findall(string=str(playersfull[b]), pattern="[0-9]+")]))

                                                            if "¬" in playersfull[b]:

                                                                payout.append(playersfull[b].split("£")[1] + " loses " + str(foldamount[b]) + ":dz:. Please give them to " + winner.split(" ",1)[1] + ", using the command: `$give-money @" + winner.split("'",1)[0] + " " + str(foldamount[b]) + "`")

                                                            else:

                                                                payout.append("")

                                                        await message.channel.send(embed=discord.Embed(title=tit, description=str(winner.split(" ",1)[1] + " has won the hand!\n\n" + "\n".join(payout) + "\n\nIncluding " + winner.split(" ",1)[1] + "'s own bid of " + str(currentbid) + ", that equals the pot of " + str(pot) + "\n\nWould you like to play another hand?")))
                                                        break

                                                    if i+1 == len(players):

                                                        next = players[0]
                                                        
                                                        players[0] = ">" + players[0]

                                                    else:

                                                        next = players[i+1]

                                                        players[i+1] = ">" + players[i+1]

                                                    if (not "<" in next and not "<" in players[i]) or gamedata[gv][3].count(str(currentbid)) != len(players):

                                                        if not "NPC" in next:

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + " folded!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + ", will you match this bid? You can call, raise, or fold."), colour = embcol))

                                                        else:

                                                            #To do: Add logic to determine if the NPC should raise.

                                                            await message.channel.send(embed=discord.Embed(title=tit, description=str(players[i].split(" ",1)[1] + "called!\n\nThe bid is still " + str(currentbid) + ", and the total pot is at " + str(pot) + "\n\n" + next.split(" ",1)[1] + " is an NPC, and needs to actually be taught how to play..."), colour = embcol))

                                                    else:

                                                        await message.channel.send(embed=discord.Embed(title=tit, description="Everyone has matched the bid or folded! The flop is:\n\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+1]) + "\n" + str(gamedata[gv][5].split("|")[len(gamedata[gv][3].split("|")*2)+2]), colour = embcol))

                                                    #Store the pot

                                                    gamedata[gv][5] = "|".join(gamedata[gv][5].split("|")[:-1])

                                                    gamedata[gv][5] = gamedata[gv][5] + "|" + str(pot)

                                                    #Update the sheet

                                                    players[i].strip(">")

                                                    rejoin = []

                                                    for n in range(len(playersfull)):

                                                        if str(players[i].split(" ",1)[1]) in playersfull[n]:

                                                            rejoin.append(str("¬" + players[i]))

                                                        else:

                                                            rejoin.append(playersfull[n])

                                                    gamedata[gv][3] = "|".join(rejoin)

                                                    sheet.values().update(spreadsheetId = gamesheet, range = "A" + str(gv+1) + ":F" + str(gv+1), valueInputOption = "USER_ENTERED", body = {'values':[gamedata[gv]]}).execute()

            #Wild and Lustful Magic Table

            elif (message.content.lower().startswith(str(myprefix) + "wildlust")):

                if isbot:
                    
                    auth = message.author.name

                elif message.author.nick:

                    auth = message.author.nick

                else:

                    auth = message.author.name

                lewdtab = "Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls|Your arousal increases to its maximum value and you immediately begin making climax saving throws.|Your clothes and armor disappear until you complete a long rest. You are unaware of this fact, and utterly deny any suggestions to the contrary, or attempts to make you wear clothes.|Your body begins to compulsively masturbate. For the next minute, you must succeed on a DC 15 strength check at the start of each of your turns, or spend the turn pleasuring yourself to the best of your ability.|You cast Enlarge/Reduce on your genitals or other sexual traits. Roll 1d6: on a roll of 1-3, you enlarge these parts of your body; on a roll of 4-6 you reduce these parts of your body.|For the next hour whenever you open your mouth to speak, you experience the sensation and of a phantom cock in your mouth.|The last creature you had sexual intercourse with immediately climaxes, and is aware of the source of their climax.|You are petrified for 1d6 hours. While petrified in this way, your erogenous zones remain soft and fleshy, and you experience stimulation as normal.|You immediately grow a 12 inch cock if you do not already have one. If you already have a cock, ignore this result and roll again. This effect lasts until you climax.|For the next 1d6 hours, you can see the genitals and sexual characteristics of other creatures through their clothes.|For the next hour, anytime you climax, all other creatures within 30 ft must also make a climax saving throw, regardless of their current arousal.|You gain a powerful fetish for a random body part. For the next 24 hours, sexual acts or advances using that body part are made against you with advantage.|You lose any and all sexual characteristics, including genitals, until you complete a long rest. While transformed in this way, you may gain arousal, but automatically succeed on climax saving throws|Your pubic hair grows to a length of 12 inches, and is silky soft. It cannot be cut until you complete a long rest, after which it falls out and returns to its natural state.|Your erogenous zones become fully and almost painfully erect for the next 4 hours.|You are infatuated by the next creature you see for 1 hour, or until you climax.|A tiny fey appears on your shoulder and proceeds to kink-shame you for the next 24 hours.|A tiny imp appears on your shoulder and verbally encourages your most perverted sexual appetites for the next 24 hours.|Your breasts increase in size by one size category and begin lactating at high volume and pressure for the next 1d4 hours.|For next 1d4 hours, an ethereal squirrel proceeds to whisper your darkest sexual fantasies into the ear of any creature within 20 ft of you. If the squirrel is killed, 2 more take its place.|For the next 24 hours, you find yourself aroused by the silliest of things. Each time you hear a joke, pun, or other comedic retort, you gain 1d4 psychic arousal.|An illusionary copy of you appears within 5 ft of your current position, and lasts for 1d8 hours. The duplicate shares your appearance, but none of your ingame statistics, and is only interested in helping you get laid.|1d12 spectres appear at random locations within 20 ft of you. They move with you, and perform no actions other than watching you and pleasuring themselves.|For the next hour, the only words you can speak or write in any language are “Fuck Me”|For the next 24 hours, each time you climax, each creature within a 10ft cone must succeed on a dexterity saving throw or be covered in cum and gain 2d6 acid stimulation.|You smell strongly of sex for the next 24 hours. Any attempt to clean or remove this smell instead makes it stronger.|A magical seal appears above your genitals. For the next 1d6 days, you automatically succeed on climax saving throws.|You climax immediately, and the sound and image of your climax is magically broadcast to every creature of age within 1 mile.|A powerful fey appears at a point within 20 ft of you and demands to be brought to climax. If you fail to fulfil their request, they cast bestow curse upon you. If you succeed, they may grant you some form of boon or aid.|Your clothes magically transform to resemble a sexy maid’s outfit. For the next 24 hours, you feel the magical compulsion to cook and clean, after which your clothes return to normal|You cast Arcane Eye. The magical sensor appears within 10 ft a creature currently engaged in sexual intercourse, regardless of range, and projects it’s observations 5 ft in front of you for all to see.|The lower half of your clothes fall to the ground or are otherwise doffed, leaving your naked from the waist down.|If you have a cock, it is transformed into an enormous limp noodle for the next 1d6 hours. If you do not have a cock, ignore this result and roll again.|For the next hour, each of your fingers becomes tipped with a tiny cock|For the next 24 hours, any container you open contains an erect disembodied cock, in addition to any other contents.|A small rainstorm of flexible dildos falls on you, striking you for 1d4 bludgeoning damage. The dildos disappear shortly after falling to the ground.|You cast Grease, centred on yourself|If you have balls, they burst into harmless magical flame. For the next 24 hours, you produce powerful alcoholic drink in place of semen, after which your balls return to normal. If you do not have balls, ignore this result and roll again.|If you have tits, they become covered in a thin layer of frost, and feel cool to the touch. For the next 24 hours, squeezing them causes you to lactate ice-cream, after which your tits return to normal if you do not have tits, ignore this result and roll again.|Your senses are magically altered. For the next minute, you treat damage done to you as stimulation, and stimulation done to you as damage.|You gain the cock of a dragon or similarly sized monster, chosen by the DM. This lasts for 1 hour.|For the next 24 hours, each time you succeed on a knowledge check, you must make a climax saving throw, regardless of your current arousal.|Each creature within 20 ft of you must succeed on a wisdom saving throw or become hyperaroused for 1d4 rounds.|Even the lightest touch thrills your mind with mental pleasure. You gain an extra 1d6 psychic stimulation whenever you gain stimulation from a physical source.|Your hair transforms into 1d4 tentacles for the next hour. These tentacles act on your initiative each round. If you do not command them, they make a sexual act against the nearest creature, or you, if there are no other targets.|You and a random creature within 30 ft swap genitals for the next hour. Stimulation and other sensations affect the original owner of the genitals, rather than the current owner|Your genitals detach from your body and become a tiny creature with the statistics of a homunculus. They reattach or reappear after 24 hours, or if reduced to 0 hit points|For the next 24 hours, your skin flashes through vibrant colors to display your emotions and arousal. Insight checks against you are made at advantage.|For the next 1d6 days, each time you climax, your cum animates into a small elemental sprite with the statistics of a water mephit.|For the next 24 hours, when you climax, your genitals release a small cloud of colourful confetti and the sound of a birthday cheer in place of cum. |You and all creatures within 30 ft of you must succeed on a constitution saving throw or become intoxicated for the next minute|You Cast Evards Black Tentacles centered on yourself. The tentacles deal stimulation instead of damage.|Your Cast the Light Spell targeted on your erogenous zones.|Your Clothes Animate and begin pleasuring you. You gain 1d6 bludgeoning stimulation at the start of each of your turns. This effect lasts until you remove your clothes by succeeding on a strength saving throw.|You Grow Animal Ears and a tail. For the next 24 hours, your speech is magically altered to include cute animal noises and puns, after which the tail and ears disappear.|You transform into a gargantuan dildo for one minute.|For the next minute, if you move more than 5 ft on your turn, your ass cheeks cast the thundeclap cantrip as a free action.|A pair of phallic horns appear on your head, crowned with a halo of flames. These horns remain for one hour, after which they disappear|14 werewolves appear at random points within 30 ft of you. They are fully erect and violently horny.|You cast charm person, targeting a random creature within range.|It all goes to your hips. For the next minute, your size category increases by one, and your intelligence score becomes 8|A large, phallic mushroom bursts from the ground at a point within 5 ft of you. If touched, it moans loudly.|For the next hour, you can only speak or vocalize in animal noises. This does not impact your ability to cast spells with verbal components Wild and Lustful Magic|You cast entangle, centered on yourself. Creatures that end their turn within the spell’s area take 1d4 bludgeoning stimulation.|Your undergarments teleport to the top of your head. If you are not wearing undergarments, someone else’s undergarments teleport to the top of your head.|Error 404, your sex is missing|A succubus appears at a point within 20 ft of you, and makes it their personal mission to seduce you into lecherous acts.|You regain your virginity. You lose proficiency with all sexual implements (including your natural implements) until you cause another creature to climax.|For the next 24 hours, faint and seductive music can be heard playing by any creature within 30 ft of you. Nice.|Your tongue grows to a length of 2 ft, and counts as a +1 sexual implement for the next hour.|You cast Time Stop. Sexual acts you perform while under the effects of this spell do not cause the spell to end.|A wolf or other large canine appears at a point within 5 ft of you and immediately attempts to hump your leg|A random object within 30 ft of you becomes a mimic.|You cast prestidigitation, soiling the pants of the nearest creature other than yourself that is wearing pants.|A market stall full of bread appears within 30 ft of you. Everyone is uncomfortable.|A Ghost appears at a point within 5 ft of you and proceeds to perform oral sex on you for the next minute, or until you climax.|You are showered with the loose pages of a large journal. Each page contains a beautifully rendered images of feet|Sexually degrading writing appears all over your body. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.|You cast Enthral, targeting all creatures within range.|2d6 poisonous snakes appear within 20 ft of you. They have a fly speed of 30 ft, and their bite attacks deal stimulation instead of damage.|A strange nun appears, spanking you for 1d8 bludgeoning damage before disappearing|You cast suggestion on yourself and your nearest ally. The suggestion is to kiss|You are showered in coins and tips. Gain 2cp for every sexual act or advance you have made in the past 24 hours|A bullywug appears from the nearest body of water, and attempts to persuade you into kissing it. The bullywug claims to be royalty of some sort.|You cast haste on yourself. Your skin turns blue for the duration of the spell.|Your genitals are swarmed by an array of tiny harmless lizards for the next 24 hours. The lizards spread to any creature you have sexual intercourse with.| I disembodied voice calls from the distance, encouraging you to “do it for the exposure” each creature that can hear the voice must make a performance check, and lose a number of CP equal to the result.|A for the next minute, an ethereal greatclub hovers over you, attacking any creature you can see that performs a sexual act or advance. The club uses your spell attack modifier when making attacks|If you have a pussy, it transforms into a fragrant flower for the next 1d6 hours. If you do not have a pussy, ignore this result and roll again.|An incredibly attractive goblin appears at a point within 5 ft of you, wearing leather pants and singing words of power. He claims to be a king, and will not leave until you agree to marry him.|You begin drooling uncontrollably, and are unable to close your mouth.|A random barmaid appears, slapping you for 1d4 bludgeoning damage before calling you a pig or a whore and then disappears|If you have tits, you magically grow an additional single breast|A talking squirrel appears at a point within 5 ft of you, and drunkenly accosts you for money before asking if you know where he lives. He seems to be having a very bad day.|For the next minute, any food you touch magically transforms into dick-shaped candies.|A portal to your genitals appears on a random surface within 1000 miles. The portal lasts for 24 hours, and can be used to perform sexual acts.|You cast Hypnotic pattern, centered on your nipples.|If you have a cock, it magically splits into two duplicates of itself for the next 24 hours.|A scarlet “A” appears on your left breast, and is visible through your clothing. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.|You violently climax in a burst of magical energy, regaining all expended spell slots."

                lewdroll = random.randint(0,99)

                lewdtext = lewdtab.split("|")[lewdroll]

                # if message.author.name == "C_allum":

                #     lewdroll = 59

                #     lewdtext = "14 werewolves appear at random points within 30 ft of you. They are fully erect and violently horny"

                print(auth + " rolled on the lewd wild magic table")

                await message.delete()

                await message.channel.send(embed = discord.Embed(title= message.author.name + " rolled a " + str(lewdroll+1) + " on the Wild and Lustful Magic Table!", description= lewdtext, colour = embcol))

            #Rulebook Command

            elif (message.content.lower().startswith(str(myprefix) + "rulebook")):

                await message.delete()

                await message.channel.send(embed = discord.Embed(title = "Here's a link to the Lewd Rulebook", description = "https://www.dropbox.com/s/cl1w7a55onzjpnk/00%20Full%20Lewd%20handbook%20%28WIP%29.pdf?dl=0", colour = embcol))

            #Bid Command

            elif (message.content.lower().startswith(str(myprefix) + "bid")):

                if isbot:

                    await message.delete()

                else:

                    bidchannel = 1010566688326045797

                    #bidlatest = await client.get_channel(bidchannel).history(limit=1, oldest_first=True).flatten()
                    bidlatest = [joinedMessages async for joinedMessages in client.get_channel(bidchannel).history(limit=1, oldest_first=True).flatten()] #Fix for pebblehost Await issue

                    bids = bidlatest[0].content.split("\n")

                    prevbids = []

                    for a in range(len(bids)):

                        if str(message.content.split(" ")[1]) in bids[a]:

                            try:
                                
                                if int(message.content.split(" ")[2]) > int(bids[a].split(" | ")[2]):

                                    bids[a] = str(bids[a].split(" | ")[0]) + " | " + str(message.author.name) + " | " + str(message.content.split(" ")[2])

                                    await message.channel.send(message.author.name + " has bid " + str(message.content.split(" ")[2]) + dezzieemj + " on " + str(message.channel))

                                else:

                                    await message.channel.send("Your bid is too low, the current bid is: " + str(bids[a].split(" | ")[2]) + dezzieemj)

                            except IndexError:

                                await message.channel.send("Incorrect format. Use %bid name amount.")

                            except ValueError:

                                await message.channel.send(message.content.split(" ")[2] + " is not an integer. Use %bid name amount.")

                        if not "setup" in bids[a]:

                            prevbids.append(bids[a])

                    if ("lorekeeper" in str(message.author.roles).lower() or message.author.name == "C_allum") and "set" in message.content:

                        prevbids.append(str((message.content.split(" ")[1]) + " | No Bids Yet | " + "0"))

                        await message.delete()

                    try:
                        
                        await bidlatest[0].edit("\n".join(prevbids))

                    except discord.errors.Forbidden:

                        await bidlatest[0].delete()

                        await client.get_channel(bidchannel).send("\n".join(prevbids))            

            #Easter egg hunt

            elif not 1:# (message.content.lower().startswith(str(myprefix) + "egg") and "lorekeeper" in str(message.author.roles).lower()):

                # room = random.choice([845498061459554334, 845498746870693898, 861688038928023583, 838821621913223229, 955144068386664479, 951666605568458752, 951666822636273674, 831906482408259604, 832770478942060574, 832842032073670676, 837112469356019742, 837114447758884885, 887184341875183626, 904403930505678879, 861686321659248640])

                # await message.channel.send(embed = discord.Embed(description = message.author.name + " hid an egg!", colour = embcol))     

                # time = random.randint(30, 300)

                # eggemb = discord.Embed(title = random.choice(["An Egg has appeared!", "You have found an egg!", "The Easter Bunny appears to have been here!", "Is that... an egg?", "An egg!", "You found an egg!"]), description = "Our bunny seems to have left an egg here for you! Click the reaction to find it before this message disappears in " + str(time) + " seconds! That's <t:" + str(int(datetime.timestamp(message.created_at)) + int(time)) + ":R>!", colour = embcol)

                # eggemb.set_thumbnail(url = "https://cdn.discordapp.com/attachments/832435243117445131/964197891935731833/0be8e65e-b68e-49d1-a2e5-c316e86c9b18.gif")

                # eggmess = await client.get_channel(room).send(embed = eggemb)

                # await message.delete()

                # await eggmess.add_reaction("<:EasterEgg:964636527432978482>")

                # reacters = []

                # while True:

                #     if int(datetime.timestamp(datetime.now())) > (int(datetime.timestamp(message.created_at)) + int(time)):

                #         break

                #     try:

                #         reaction, user = await client.wait_for("reaction_add", timeout = 5)

                #         if str(reaction.emoji) == "<:EasterEgg:964636527432978482>":

                #             reacters.append(str(user.name))

                #     except asyncio.exceptions.TimeoutError:

                #         pass

                # await eggmess.delete()

                # await client.get_channel(logchannel).send(message.author.name + " sent an egg. It was found by:\n\n" + "\n".join(reacters))

                pass

            #Scenes Command

            elif message.content.lower().startswith(str(myprefix) + "scenes"):

                await message.delete()

                waitmess = await message.channel.send("We are processing your request now.")

                econdata = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ2000", majorDimension = 'ROWS').execute().get("values")

                row = 0

                for n in range(math.ceil(len(econdata)/4)):

                    r = 4 * n 

                    if str(message.author) in econdata[r][0]:

                        if not econdata[r+2][0] == "":
                            
                            if len(econdata[r+2][0]) == 1:

                                prevscenes = [econdata[r+2][0]]

                            else:

                                prevscenes = econdata[r+2][0].split("|")

                        else:

                            prevscenes = ""

                            await message.channel.send(embed = discord.Embed(title = "You have no scenes tracked.", description = "Add one using:\n\n`%scenes add Brief Scene Description #Channel Name`\n\nFor example, to watch the a particular scene in the cantina, you might type:\n\n`%scenes add Dinner Date #<832842032073670676>`", colour = embcol))

                        if message.content.lower().startswith(str(myprefix) + "scenes add"):

                            scenestr = message.content.split(" ", 2)[2]

                            if scenestr.replace(" ", "") == "":

                                await message.channel.send("Add help here")

                            else:

                                if prevscenes != "":

                                    scenelist = "|".join(prevscenes) + "|" + scenestr

                                else:

                                    scenelist = scenestr

                                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(r+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[scenelist]])).execute()

                            await message.channel.send(embed = discord.Embed(title = "Added to your scenes", description = "We have added '" + scenestr + "' to your tracked scenes.", colour = embcol))

                        else:

                            if "|" in prevscenes:

                                prevs = prevscenes.split("|")

                            else:

                                prevs = prevscenes

                            if prevs != "":

                                prevlist = []

                                prevscenelist = []

                                for a in range(len(prevs)):

                                    if "#" in prevs[a]:

                                        try:

                                            sceneno = int(prevs[a].split("#")[1].strip(">"))

                                            if not "remove" in message.content:

                                                try:
                                                    
                                                    #last = await client.get_channel(sceneno).history(limit=1, oldest_first=False).flatten()
                                                    last = [joinedMessages async for joinedMessages in client.get_channel(sceneno).history(limit=1, oldest_first=False).flatten()] #Fix for pebblehost Await issue
                                                    prevlist.append(str("`" + str(a+1) + "` " + str(prevs[a]) + " - Last message by: " + last[0].author.name))

                                                except AttributeError:

                                                    prevname = "" 

                                                    prevlist.append(str("`" + str(a+1) + "` " + str(prevs[a]) + " - Thread archived or channel deleted."))

                                            else:

                                                prevlist.append(str("`" + str(a+1) + "` " + str(prevs[a])))

                                                prevscenelist.append(str(prevs[a]))

                                        except ValueError:

                                            prevlist.append(str("`" + str(a+1) + "` " + str(prevs[a])))

                                    else:

                                        prevlist.append(str("`" + str(a+1) + "` " + str(prevs[a])))

                                if "remove" in message.content:

                                    scenetemp = await message.channel.send(embed = discord.Embed(title = "Type the number of the scene to stop tracking", description= "\n".join(prevlist), colour = embcol))

                                    try: 
                                        
                                        scenerechoice = await client.wait_for('message', timeout = 30, check = check(message.author))

                                        await scenerechoice.delete()

                                        # if scenerechoice.content.lower() == "all":

                                        #     sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(n+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[""]])).execute()

                                        #     await message.channel.send(embed = discord.Embed(title = "Scenes removed", description = "Your tracked scenes have been wiped.", colour = embcol))

                                        # elif scenerechoice.content.lower() == "clean":

                                        #     sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(n+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[scenelist]])).execute()

                                        #     await message.channel.send(embed = discord.Embed(title = "Scenes removed", description = "Your tracked scenes have been wiped.", colour = embcol))

                                        try:

                                            scenenum = int(scenerechoice.content)

                                            prevscenelist = prevscenelist[:scenenum-1] + prevscenelist[scenenum:]

                                            await message.channel.send(embed = discord.Embed(title = "Scene removed", description = "The requested scene has been removed from your tracked scene list.", colour = embcol))

                                            if len(prevscenelist) > 1:

                                                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(4*n+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[["|".join(prevscenelist)]])).execute()

                                            elif len(prevscenelist) == 0:

                                                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(4*n+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[""]])).execute()

                                            else:

                                                sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(4*n+8)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[prevscenelist[0]]])).execute()

                                        except TypeError:

                                            await message.channel.send("Value not recognised")

                                    except TimeoutError:

                                        await message.channel.send("Selection Timed Out")

                                else:

                                    await message.channel.send(embed = discord.Embed(title = message.author.name + "'s tracked scenes", description= "\n".join(prevlist), colour = embcol))

                        break

                await waitmess.delete()

            #The Economy

            #Buy Item

            elif message.content.lower().startswith(str(myprefix) + "buy") or message.content.lower().startswith("$buy"):
                
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
                        print("error")
                        buyquant = 1  
                    except TypeError:
                        print("error typerror")
                        buyquant = 1  
                except IndexError:
                    searchterm = "11111111111111" #Something irrelevant cause the search was empty
                
                itindex = ""

                
                print(searchterm)
                print(buyquant)
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


            #Use Item

            elif message.content.lower().startswith(str(myprefix) + "use") or message.content.lower().startswith("$use"):

                userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ2000", majorDimension = 'ROWS').execute().get("values")

                shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")

                itnames = []

                itshorts = []

                itlongs = []

                itprices = []

                row = 0

                for n in range(math.ceil(len(userinvs)/4)):

                    r = 4 * n 

                    if str(message.author) in userinvs[r][0]:

                        if message.content.split(" ",1)[1].replace("'","").replace("’","").lower() in str(userinvs[r]).replace("'","").replace("’","").lower():

                            for itno in range(len(userinvs[r])):

                                if message.content.split(" ",1)[1].replace("'","").replace("’","").lower() in userinvs[r][itno].replace("'","").replace("’","").lower():

                                    if userinvs[r][itno].split("|")[0][1:] in str(shopdata):

                                        for a in range(len(shopdata[1])):

                                            if userinvs[r][itno].split("|")[0][1:] in shopdata[1][a]:

                                                if shopdata[7][a] == "This item was not supposed to be used this way.":

                                                    usequant = 0

                                                else:

                                                    usequant = 1

                                                    row = a

                                                break
                                            
                                            else:

                                                usequant = 0

                                    #Set new quantity

                                    newquant = int(userinvs[r][itno].split("|")[1]) - usequant

                                    if newquant > 0:

                                        itnames.append(str(userinvs[r][itno].split("|")[0]) + "|" + str(newquant))

                                        try:

                                            if userinvs[r+1][itno] != "" or userinvs[r+1][itno] != " ":

                                                itshorts.append(str(userinvs[r+1][itno]))

                                        except IndexError:

                                            itshorts.append(" ")

                                        itlongs.append(userinvs[r+2][itno])

                                        itprices.append(userinvs[r+3][itno])

                                else:

                                    itnames.append(userinvs[r][itno])

                                    try:

                                        if userinvs[r+1][itno] != "" or userinvs[r+1][itno] != " ":

                                            itshorts.append(str(userinvs[r+1][itno]))

                                    except IndexError:

                                        itshorts.append(" ")

                                        pass

                                    itlongs.append(userinvs[r+2][itno])

                                    itprices.append(userinvs[r+3][itno])

                            itnames.append("")

                            try:

                                if userinvs[r+1][itno] != "":

                                    itshorts.append("")

                            except IndexError:

                                pass

                            itlongs.append("")

                            itprices.append("")

                            sheet.values().update(spreadsheetId = EconSheet, range = "A" + str(r+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[itnames])).execute()

                            sheet.values().update(spreadsheetId = EconSheet, range = "A" + str(r+7), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[itshorts])).execute()

                            sheet.values().update(spreadsheetId = EconSheet, range = "A" + str(r+8), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[itlongs])).execute()

                            sheet.values().update(spreadsheetId = EconSheet, range = "A" + str(r+9), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[itprices])).execute()

                            if usequant == 0:

                                await message.channel.send(embed = discord.Embed(title = "Nothing happened", description = "This item is not a consumable. It cannot be used in this way.", colour = embcol))

                            else:

                                await message.channel.send(embed = discord.Embed(title = "You used an " + shopdata[1][row], description = shopdata[7][row].replace("{user.mention}", message.author.name), colour = embcol))

                        break

            #Work Command

            elif message.content.lower().startswith(str(myprefix) + "work") or message.content.lower().startswith("$work"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    workreward = random.randint(20,250)

                    try:

                        if str(message.author) in str(economydata[b][0]):

                            try:
                                
                                workdiff = int(datetime.timestamp(datetime.now())) - int(economydata[b+1][1])

                            except IndexError:

                                workdiff = 86401

                            except ValueError:

                                workdiff = 86401

                            if int(workdiff) > 84600:

                                row = b + 1

                                newtot = int(economydata[b][1]) + int(workreward)

                                workresptemp = str(random.choice(workhooks[0]))

                                workresp = workresptemp.replace("[amount]", str(workreward) + dezzieemj)

                                roles = str(authroles).lower()

                                pay = 0

                                payroles = []

                                if "admin" in roles:

                                    pay += 100

                                    payroles.append("Admin")

                                if "mvp" in roles:

                                    pay += 150

                                    payroles.append("MVP")

                                if "moderator" in roles:

                                    pay += 100

                                    payroles.append("Dungeon moderator")

                                if "lorekeeper" in roles:

                                    pay += 200

                                    payroles.append("Lorekeeper")
                            
                                if "pet" in roles:

                                    pay += 50

                                    payroles.append("Dungeon Pet")

                                if "fucksmith" in roles:

                                    pay += 25

                                    payroles.append("Licensed Fucksmith")

                                if pay == 0:

                                    paymess = ""

                                else:

                                    if len(payroles) == 1:

                                        paylist = str(payroles[0])

                                    else:

                                        paylist = ", ".join(payroles[:-1]) + " and " + payroles[-1]

                                    if str(workdiff) == "day" or not "days" in str(workdiff):

                                        paymess = "\n\nYou also collect your role-based income for today, from your work as " + paylist + ": " + str(pay)+ dezzieemj

                                        newtot += pay
                                    
                                    else:

                                        if int(str(workdiff).split(" day")[0]) > 4:

                                            days = 4

                                            paymess = "\n\nYou also collect your role-based income since you last worked (over 4 days ago), from your work as " + paylist + ": " + str(pay * int(days)) + dezzieemj

                                            newtot += pay * 4

                                        else:

                                            days = str(str(workdiff).split(" day")[0])

                                            paymess = "\n\nYou also collect your role-based income since you last worked (" + days + " days ago), from your work as " + paylist + ": " + str(pay * int(days)) + dezzieemj

                                            newtot += pay * int(str(workdiff).split(" day")[0])

                                crit = random.randint(1,20)

                                if crit == 1:

                                    critresp = "\n\nBut you rolled a critical failure for this work, so the amount is halved to " + str(math.floor(workreward / 2)) + "!"

                                    newtot = newtot - math.ceil(workreward / 2)

                                elif crit == 20:

                                    critresp = "\n\nAnd you rolled a natural 20 for the work, doubling the amount to " + str(workreward * 2) + "!"

                                    newtot = newtot + workreward

                                else:

                                    critresp = "\n\nYou rolled a " + str(crit) + ", which doesn't do anything special."

                                if workdiff < 172800:

                                    try:

                                        streakmess = "\n\nYou now have a " + str(int(economydata[b+3][1]) + 1) + " day streak!"

                                        if (int(economydata[b+3][1]) + 1) % 7 == 0:

                                            if (int(economydata[b+3][1]) + 1) / 7 >= 4:

                                                streakbonus = 200

                                            else:

                                                streakbonus = ((int(economydata[b+3][1]) + 1) / 7) * 50

                                            if ((int(economydata[b+3][1]) + 1) / 7) == 1:

                                                streakmess += " That's a full week without missing a day! Keep it up! Here's an extra 50" + dezzieemj + "!"

                                            else:

                                                streakmess += " That's " + str(int(math.floor((int(economydata[b+3][1]) + 1) / 7))) + " full weeks! You've earned an extra " + str(streakbonus) + dezzieemj + "!"

                                            newtot += int(streakbonus)

                                        elif (int(economydata[b+3][1]) + 1) == 69:

                                            streakmess += " ***Nice***. You've earned an extra 69" + dezzieemj

                                            newtot += 69

                                        streakdays = str(int(economydata[b+3][1]) + 1)

                                    except ValueError:

                                        streakmess = "\n\nWork every day to build a streak!"

                                        streakdays = 1

                                    except IndexError:

                                        streakmess = "\n\nWork every day to build a streak!"

                                        streakdays = 1

                                else:

                                    streakmess = "\n\nWork every day to build a streak!"

                                    streakdays = 1

                                randbal = str(random.choice([message.author.display_name + " now has " + str(newtot) + dezzieemj, "According to our records, " + message.author.display_name + " now has " + str(newtot) + dezzieemj, str(newtot) + dezzieemj + ". " + message.author.display_name + " has " + str(newtot) + dezzieemj + ".", "This work brings " + message.author.display_name + "'s balance to.. " + str(newtot) + dezzieemj + ".", message.author.display_name + " should really go and visit the Gobblin Bazzar. They have " + str(newtot) + dezzieemj + " to spend."]))

                                balresp = "\n\n---------------------------------------------------------\n\n" + randbal

                                worktit = random.choice([message.author.display_name + " earned some dezzies with the work command!", message.author.display_name + " has been hard at work!", "Working hard, or hardly working, " + message.author.display_name + "?", "You guys are getting paid? Well, " + message.author.display_name + " is, anyway.", message.author.display_name + " did some work.", message.author.display_name + " decided to do some work. It's about time they pitched in."])

                                if (message.author.name == "Mailin" or message.author.name == "ELeif") and workreward < 100 and crit != 1 and crit != 20:

                                    if random.randint(1,20) == 1:

                                        wrong = await message.channel.send(embed = discord.Embed(title = worktit, description = workresptemp.replace("[amount]", str(604) + dezzieemj) + critresp + paymess + streakmess + "\n\n---------------------------------------------------------\n\n" +  message.author.display_name + " now has " + str(int(economydata[b][1]) + 604 + pay) + dezzieemj, colour = embcol))

                                        time.sleep(4)

                                        await message.channel.send(embed = discord.Embed(title = "Wait.. that's not right.", description = "That should have only been " + str(workreward) + "... Let me try that again for my records.", colour = embcol))

                                        await wrong.edit(embed = discord.Embed(title = "~~" + worktit + "~~", description = "~~" + workresptemp.replace("[amount]", str(604) + dezzieemj) + "~~" + critresp + paymess + streakmess + "\n\n---------------------------------------------------------\n\n~~" +  message.author.display_name + " now has " + str(int(economydata[b][1]) + 604 + pay) + dezzieemj + "~~", colour = embcol))

                                await message.channel.send(embed = discord.Embed(title = worktit, description = workresp + critresp + paymess + streakmess + balresp, colour = embcol))

                                await message.delete()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[streakdays]])).execute()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newtot]])).execute()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[str(datetime.timestamp(datetime.now()))]])).execute()

                            else:

                                await message.channel.send(embed = discord.Embed(title = message.author.name + " cannot work at this time!", description = "You last worked at <t:" + str(economydata[b+1][1]) + ">.\n The work command can only be used once per day.\n\n Try again " + "<t:" + str(int(economydata[b+1][1]) + 84600) + ":R>", colour = embcol))

                                await message.delete()

                    except IndexError:

                        pass

            #Slut Command

            elif message.content.lower().startswith(str(myprefix) + "slut") or message.content.lower().startswith("$slut"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    slutreward = random.randint(100,250)

                    slutfine = random.randint(math.floor((int(economydata[b][1]))/100),math.floor((int(economydata[b][1]))/20))

                    if str(message.author) in str(economydata[b][0]):

                        try:
                            
                            slutdiff = int(datetime.timestamp(datetime.now())) - int(economydata[b+2][1])

                        except ValueError:

                            try:

                                slutdiff = int(str(datetime.timestamp(datetime.now())).split(".")[0]) - int(economydata[b+2][1])

                            except ValueError:

                                slutdiff = 21600

                        except IndexError:

                            slutdiff = 21600

                        if int(slutdiff) >= 21600:

                            if random.randint(1,100) > 20:

                                row = b + 1

                                newtot = int(economydata[b][1]) + int(slutreward)

                                slutresp = str(random.choice(sluthooks[0])).replace("[amount]", str(slutreward) + dezzieemj)

                                balresp = "\n\n---------------------------------------------------------\n\n" + message.author.name + " now has " + str(newtot) + dezzieemj 

                                await message.channel.send(embed = discord.Embed(title = message.author.name + " slutted!", description = slutresp + balresp, colour = embcol))

                                await message.delete()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newtot]])).execute()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[str(datetime.timestamp(datetime.now())).split(".")[0]]])).execute()

                            else:

                                row = b + 1

                                newtot = int(economydata[b][1]) - slutfine

                                slutresp = str(random.choice(sluthooks[1])).replace("[amount]", str(slutfine) + dezzieemj)

                                balresp = "\n\n---------------------------------------------------------\n\n" + message.author.name + " now has " + str(newtot) + dezzieemj 

                                await message.channel.send(embed = discord.Embed(title = message.author.name + " slutted!", description = slutresp + balresp, colour = embcol))

                                await message.delete()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newtot]])).execute()

                                sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(row+2)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[str(datetime.timestamp(datetime.now())).split(".")[0]]])).execute()

                        else:
                                
                            await message.channel.send(embed = discord.Embed(title = message.author.name + " cannot slut at this time!", description = "You last slutted at <t:" + str(economydata[b+2][1]) + ">.\n The slut command can only be used once every six hours.\n\n Try again " + "<t:" + str(int(economydata[b+2][1]) + 21600) + ":R>", colour = embcol))

                            await message.delete()

                        break

            #Slit

            elif message.content.lower().startswith(str(myprefix) + "slit"):

                await message.channel.send(embed = discord.Embed(title = "You found a slit.", description = "Don't feel bad, it's a common typo. Try %slut instead?", colour = embcol))

            #Slur

            elif message.content.lower().startswith(str(myprefix) + "slur"):

                await message.channel.send(embed = discord.Embed(title = "Oh-kay, we're sluhrin' ouhr wohrds...", description = "Mahybe try %slut instead?", colour = embcol))              

            #Money Command

            elif message.content.lower().startswith(str(myprefix) + "money") or message.content.lower().startswith("$money") or message.content.lower().startswith(str(myprefix) + "wallet") or message.content.lower().startswith("$wallet"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                balances = []

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    try:

                        balances.append(int(economydata[b][1]))

                    except IndexError:

                        pass

                balances = sorted(balances)

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    if str(message.author) in str(economydata[b][0]):

                        for c in range(len(balances)):

                            if int(economydata[b][1]) == balances[-c]:

                                position = c

                                if position == 1:

                                    position = "1st"

                                elif position == 2:

                                    position = "2nd"

                                elif position == 3:

                                    position = "3rd"

                                else:

                                    position = str(position) + "th"

                        await message.channel.send(embed = discord.Embed(title = str(message.author) + " has " + str(economydata[b][1]) + dezzieemj + ".", description = "Leaderboard Rank: " + position, colour = embcol))

                        await message.delete()

                        break

            #Leaderboard Command

            elif message.content.lower().startswith(str(myprefix) + "leaderboard") or message.content.lower().startswith("$leaderboard"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                balancesobj = []

                for a in range(math.floor(len(economydata)/4)):

                    b = (int(a) * 4) + 5

                    try:

                        balancesobj.append([str(economydata[b][0]),int(economydata[b][1])])

                    except IndexError:

                        pass

                balances = list(reversed(sorted(balancesobj, key=lambda balance: balance[1])))

                richlist = []

                authisrich = 0

                leademb = discord.Embed(title = "The richest people in the dungeon:", description = "The 10 people with the most dezzies in the dungeon are:\n", colour = embcol)

                for c in range(10):

                    if str(message.author) == balances[c][0]:

                        balances[c][0] = "**" + balances[c][0] + "**"

                        authisrich = 1

                    leademb.add_field(name = "`" + str(c+1) + ":` " + balances[c][0], value = str(balances[c][1]) + dezzieemj, inline = False)

                if not authisrich:

                    for d in range(len(balances)):

                        if str(message.author) == balances[d][0]:

                            userbalpos = d

                    leademb.set_footer(text = "----------------------------------------------------------------------\n\n" + str(balances[userbalpos][0]) + " is in " + str(userbalpos + 1) + "th place, with " + str(balances[userbalpos][1]) + " dezzies.")

                await message.channel.send(embed = leademb)

                await message.delete()

            #Deposit Command

            elif message.content.lower().startswith(str(myprefix) + "deposit") or message.content.lower().startswith("$deposit"):

                await message.delete()

                await message.channel.send(embed = discord.Embed(title = random.choice(["We don't want that sort of deposit!", "You don't know how to use a gloryhole, do you?", "No tips needed!"]), description = "We don't use a bank on this server, so there's nowhere to deposit dezzies to. They've all been returned to you.", colour = embcol))

            #Give Money (player to player)

            elif message.content.lower().startswith(str(myprefix) + "give-money") or message.content.lower().startswith(str(myprefix) + "give-dezzies") or message.content.lower().startswith("$give-money"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                reciprow = ""

                giverrow = ""

                targid = int((message.content.split(" ")[1]).replace("@","").replace("&","").replace(">","").replace("<","").replace("!",""))

                target = await client.fetch_user(targid)

                targname = target.name

                if targname == "C_allum":

                    await message.channel.send(embed = discord.Embed(title = "Callum doesn't need your money!", description = "You should keep it, he has enough already.", colour = embcol))

                else:
                    
                    try:
                        
                        giveamount = int(message.content.split(" ")[2])

                    except ValueError:

                        giveamount = int(message.content.split(" ")[3])

                    except IndexError:

                        giveamount = 0

                    for a in range(math.floor(len(economydata)/4)):

                        b = a * 4 + 5

                        if str(message.author) in str(economydata[b][0]):

                            giverrow = b + 1

                        if str(targname + "#" + str(target.discriminator)) in str(economydata[b][0]):

                            reciprow = b + 1

                        if giverrow != "" and reciprow != "":

                            break

                    if reciprow == "":

                        await message.channel.send(embed=discord.Embed(title = "Could not find anyone by the name: " + targname, description = "Are you sure you've spelled it correctly?", colour = embcol))

                        await message.delete()

                    elif giveamount <= 0:

                        await message.channel.send(embed=discord.Embed(title = "You need to specify an amount!", description = "You need to specify a positive amount to give. The format should be:\n\n`" + myprefix + "give-money @name amount`", colour = embcol))

                        await message.delete()

                    else:

                        if int(economydata[giverrow-1][1]) < int(giveamount):

                            await message.channel.send(embed=discord.Embed(title = "You don't have enough money to do that.", description = "You only have " + str(economydata[giverrow-1][1]) + dezzieemj, colour = embcol))

                            await message.delete()

                        elif giverrow == reciprow:

                            await message.channel.send(embed=discord.Embed(title = "You can't give yourself money.", description = "What *exactly* are you trying to do here?", colour = embcol))

                            await message.delete()

                        else:

                            givernewtot = int(economydata[giverrow-1][1]) - int(giveamount)

                            recipnewtot = int(economydata[reciprow-1][1]) + int(giveamount)

                            sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

                            sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(giverrow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[givernewtot]])).execute()

                            await message.channel.send(embed=discord.Embed(title = message.author.name + " has given " + str(giveamount) + dezzieemj + " to " + targname, description = message.author.name + " has " + str(givernewtot) + dezzieemj + "\n\n" + targname + " has " + str(recipnewtot) + dezzieemj, colour = embcol))

                            await message.delete()

            #Add Money (moderator to player)

            elif (message.content.lower().startswith(str(myprefix) + "add-money") or message.content.lower().startswith(str(myprefix) + "add-dezzies") or message.content.lower().startswith("$add-money")) and not isbot:

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                reciprow = ""

                targid = int((message.content.split(" ")[1]).replace("@","").replace("&","").replace(">","").replace("<","").replace("!",""))

                target = await client.fetch_user(targid)

                targname = target.name

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    if str(targname + "#" + str(target.discriminator)) in str(economydata[b][0]):

                        reciprow = b + 1

                        break

                if not "moderator" in str(authroles).lower() and not "lorekeeper" in str(authroles).lower():

                    await message.channel.send(embed=discord.Embed(title = "You cannot use this", description = "Our records show that you are neither moderator, nor a lorekeeper here. It does look like they're taking applications for lorekeepers though?", colour = embcol))

                    await message.delete()

                elif reciprow == "":

                    await message.channel.send(embed=discord.Embed(title = "Could not find anyone by the name: " + targname, description = "Are you sure you've spelled it correctly?", colour = embcol))

                    await message.delete()

                else:

                    try:
                        
                        giveamount = int(message.content.split(" ")[2])

                    except ValueError:

                        giveamount = int(message.content.split(" ")[3])

                    recipnewtot = int(economydata[reciprow-1][1]) + int(giveamount)

                    sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

                    await message.channel.send(embed=discord.Embed(title = str(giveamount) + dezzieemj + " has been given to " + targname, description = targname + " now has " + str(recipnewtot) + dezzieemj, colour = embcol))

                    await message.delete()            

            #Remove Money (moderator to player or self)

            elif (message.content.lower().startswith(str(myprefix) + "remove-money") or message.content.lower().startswith(str(myprefix) + "remove-dezzies") or message.content.lower().startswith(str(myprefix) + "take-money") or message.content.lower().startswith(str(myprefix) + "take-dezzies") or message.content.lower().startswith(str(myprefix) + "spend") or message.content.lower().startswith("$add-money")) and not isbot:

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                reciprow = ""

                try:

                    targid = int((message.content.split(" ")[1]).replace("@","").replace("&","").replace(">","").replace("<","").replace("!",""))

                    if targid < 0:

                        targid = 0 - targid

                    target = await client.fetch_user(targid)

                except discord.errors.NotFound:

                    target = message.author

                targname = target.name

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    if str(targname + "#" + str(target.discriminator)) in str(economydata[b][0]):

                        reciprow = b + 1

                        break

                if (not "moderator" in str(authroles).lower() and not "lorekeeper" in str(authroles).lower()) or not "@" in message.content:

                    try:
                        
                        giveamount = int(message.content.split(" ")[1].strip("-"))

                    except ValueError:

                        try:
                            
                            giveamount = int(message.content.split(" ")[2].strip("-"))

                        except ValueError:

                            giveamount = int(message.content.split(" ")[3].strip("-"))

                    if giveamount > int(economydata[reciprow-1][1]):

                        await message.channel.send(embed=discord.Embed(title = "You don't have enough money to do that.", description = "You only have " + str((economydata[reciprow-1][1]) + dezzieemj), colour = embcol))

                    else:

                        recipnewtot = int(economydata[reciprow-1][1]) - int(giveamount)

                        sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

                        await message.channel.send(embed=discord.Embed(title = str(giveamount) + dezzieemj + " has been taken from " + message.author.name, description = message.author.name + " now has " + str(recipnewtot) + dezzieemj, colour = embcol))

                    await message.delete()

                elif reciprow == "":

                    await message.channel.send(embed=discord.Embed(title = "Could not find anyone by the name: " + targname, description = "Are you sure you've spelled it correctly?", colour = embcol))

                    await message.delete()

                else:

                    try:
                        
                        giveamount = int(message.content.split(" ")[2])

                    except ValueError:

                        giveamount = int(message.content.split(" ")[3])

                    recipnewtot = int(economydata[reciprow-1][1]) - int(giveamount)

                    if recipnewtot < 0:

                        await message.channel.send(embed=discord.Embed(title = targname + " does not have enough money to do that!", description = targname + " only has " + str(economydata[reciprow-1][1]) + dezzieemj, colour = embcol))

                    else:

                        sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

                        await message.channel.send(embed=discord.Embed(title = str(giveamount) + dezzieemj + " has been taken from " + targname, description = targname + " now has " + str(recipnewtot) + dezzieemj, colour = embcol))

                    await message.delete()

            #Item Info

            elif message.content.lower().startswith(str(myprefix) + "item") or message.content.lower().startswith(str(myprefix) + "info") or message.content.lower().startswith("$item"):

                shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")

                searchterm = "SearchFailed"

                if message.content.split(" ")[1].lower() in str(shopdata[1]).lower():
        
                    itcount = str(shopdata[1]).lower().count(message.content.split(" ", 1)[1].lower())

                    if itcount == 1:

                        itfound = 1

                        searchterm = message.content.split(" ", 1)[1].lower()

                    else:

                        itfound = itcount

                        matchnames = []

                        searchnames = []

                        matchno = 0

                        for n in range(len(shopdata[0])):

                            if message.content.split(" ", 1)[1].lower() in str(shopdata[1][n]).lower():

                                matchno += 1

                                matchnames.append("`" + str(matchno) + "` " + shopdata[0][n] + shopdata[1][n] + ", sold at" + shopdata[3][n].replace("#", " ").replace("-", " ").title())

                                searchnames.append(shopdata[1][n])

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

                else:

                    itfound = 0

                for n in range(len(shopdata[0])):

                    if searchterm.replace("'","").replace("’","").lower() in shopdata[1][n].replace("'","").replace("’","").lower():

                        tit = "Item Info for " + shopdata[1][n]

                        itnpc = shopdata[5][n]

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

                        price = str(shopdata[2][n]) + dezzieemj

                        itemb = discord.Embed(title = tit, description = "\n\n" + shopdata[4][n], colour = npccol)

                        itemb.add_field(name = "Sold by:", value = str(shopdata[5][n] + " at " + shopdata[3][n].replace("-", " ").lstrip("#").title()).replace("Generic at ", ""), inline = True)

                        itemb.add_field(name = "Price:", value = price, inline = True)

                        itemb.set_thumbnail(url = npcthumb)

                        try:

                            if shopdata[8][n] != "":

                                itemb.add_field(name = "Stock Remaining:", value = shopdata[8][n], inline = True)

                        except IndexError:

                            pass

                        await message.channel.send(embed = itemb)

                        await message.delete()

                        itfound = 1

                        break

                if not itfound:

                    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                    if message.content.split(" ")[1].lower() in str(economydata).lower():

                        for a in range(len(economydata)):

                            if itfound:

                                break

                            elif message.content.split(" ")[1].lower() in str(economydata[a]).lower():

                                for b in range(len(economydata[a])):

                                    if message.content.split(" ")[1].lower() in str(economydata[a][b]).lower():

                                        itemb = discord.Embed(title = "Item Info for " + str(economydata[a][b]).split("|")[0] + str(economydata[a][b])[0], description = str(economydata[a+2][b]), colour = embcol)

                                        itemb.add_field(name = "Price:", value = economydata[a+3][b], inline = True)

                                        await message.channel.send(embed = itemb)

                                        itfound = 1

                                        break                        

                    else:                    

                        await message.channel.send(embed = discord.Embed(title = "Could not find an item matching that name.", description= "Check your spelling, and browse `" + myprefix + "shop <shopname>` to ensure it is there.", colour = embcol))

                    await message.delete()

            #Inventory

            elif message.content.lower().startswith(str(myprefix) + "inventory") or message.content.lower().startswith("$inventory"):

                economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ4000", majorDimension = 'ROWS').execute().get("values")

                shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")

                reciprow = ""

                if not " " in message.content:

                    target = message.author

                    targname = message.author.name

                else:

                    targid = int((message.content.split(" ")[1]).replace("@","").replace("&","").replace(">","").replace("<","").replace("!",""))

                    target = await client.fetch_user(targid)

                    targname = target.name

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    if str(targname + "#" + str(target.discriminator)) in str(economydata[b][0]):

                        targrow = b

                        break

                if targrow + 1 == "":

                    await message.channel.send(embed = discord.Embed(title = "User not found", description = "Try again", colour = embcol))

                else:

                    invlist = []

                    for b in range(len(economydata[targrow])):

                        if b >= 2:

                            try:

                                if str(economydata[targrow + 1][b]) != "":

                                    invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "` - " + str(economydata[targrow + 1][b]))

                                elif str(economydata[targrow + 1][b]) == "" or str(economydata[targrow + 1][b]) == " ":

                                    itemrow = ""

                                    for c in range(len(shopdata[0])):

                                        if shopdata[1][c] in str(economydata[targrow][b]):

                                            itemrow = int(c)

                                            break
                                        
                                    if itemrow == "":

                                        invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "`")

                                    else:

                                        invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "` - " + str(shopdata[9][itemrow]))

                            except IndexError:

                                for c in range(len(shopdata[0])):

                                    if shopdata[1][c] in str(economydata[targrow][b]):

                                        itemrow = c

                                        break
                                        
                                if itemrow == "":

                                    invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "`")

                                else:

                                    try:

                                        invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "` - " + str(shopdata[9][itemrow]))

                                    except IndexError:

                                        invlist.append(str(economydata[targrow][b].split("|")[1]) + "x `" + str(economydata[targrow][b].split("|")[0]) + "`")

                    invmesslen = 0

                    invmessage = ""

                    for d in range(len(invlist)):

                        if len(invlist[0]) + invmesslen < 4000:

                            invmessage += invlist[0] + "\n\n"

                            invmesslen = len(invmessage)

                            invlist.remove(invlist[0])

                        else:

                            await message.channel.send(embed = discord.Embed(title = targname + "'s inventory", description = invmessage, colour = embcol))

                            invmessage = invlist[0] + "\n\n"

                            invmesslen = len(invmessage)

                            invlist.remove(invlist[0])

                    await message.channel.send(embed = discord.Embed(title = targname + "'s inventory", description = invmessage, colour = embcol))

                    await message.delete()           
                
            #Shop Listing

            elif message.content.lower().startswith(str(myprefix) + "shop"):

                if isbot:

                    await message.delete()

                else:

                    #Get Channel

                    shopdata = sheet.values().get(spreadsheetId = shopsheet, range = "A1:J1000", majorDimension = 'COLUMNS').execute().get("values")

                    itlist = []

                    shopchan = "No shop selected"

                    if " " in message.content:

                        shopnames = ["the-golden-jackal", "venom-ink", "widows-boutique", "sophies-garden", "menagerie-magiks", "the-polished-knob", "moo-mellon-auction", "purrfect-petshop"]

                        for a in range(len(shopnames)):

                            if message.content.split(" ")[1].lower() in shopnames[a]:

                                shopchan = shopnames[a]

                                break

                            else:

                                shopchan = "No shop selected"

                    else:

                        shopchan = str(message.channel)

                    npc = ""

                    for n in range(len(shopdata[0])):

                        if shopchan in shopdata[3][n]:

                            if shopdata[5][n] != "Generic" and shopdata[5][n] != "Amelia":

                                npc = shopdata[5][n]

                            if "The" in shopdata[1][n]:

                                itlist.append(shopdata[0][n] + "  **" + shopdata[1][n].lstrip("The ").replace("ome of Imps", "Tome of Imps") + "**\n*" + str(shopdata[2][n]) + "*<:dz:844365871350808606>")

                            else:
                            
                                itlist.append(shopdata[0][n] + "  **" + shopdata[1][n] + "**\n*" + str(shopdata[2][n]) + "*<:dz:844365871350808606>")

                            shoptit = shopdata[3][n].strip("#").replace("-", " ").title()

                        if npc == "Nubia":

                            shopintro = "Hey, how's it going. You've been to The Jackal before. You know how it goes, you break it, I break you.\n------------------------------------------------------------"
                            shopcolour = 0xded233
                            npcthumb = "https://cdn.discordapp.com/attachments/912879579260125184/917863713514590228/Nubia-icon.png"

                        elif npc == "Nessa":

                            shopintro = "Alright there? Don't mind the snakes, they won't bite. I might, but that's another matter\n------------------------------------------------------------"
                            shopcolour = 0x18cdd3
                            npcthumb = "https://cdn.discordapp.com/attachments/912882341091876915/917863626151456818/Nessa.png"

                        elif npc == "Madame Webb":

                            shopintro = "Welcome to the Widow's Boutique. Mind your manners, and feel free to look at the displays for something you like.\n------------------------------------------------------------"
                            shopcolour = 0x222222
                            npcthumb = "https://cdn.discordapp.com/attachments/917870118342647808/917878405473656862/webb_avatar.png"

                        elif npc == "Sophie":

                            shopintro = "Oh hello, dear. Welcome to my own little garden, Sophie's Garden, might we find you a friend today?\n------------------------------------------------------------"
                            shopcolour = 0xaed318
                            npcthumb = "https://cdn.discordapp.com/attachments/918575985669062727/919379824986976356/sophie_avatar.png"

                        elif npc == "Runar":

                            shopintro = "Huh, oh, right Sophie told me what to say, one moment. Ahem. Welcome to Menagerie Magiks, I am Runar and may I interest you in something?\n------------------------------------------------------------"
                            shopcolour = 0x4a97df
                            npcthumb = "https://cdn.discordapp.com/attachments/912759640008298577/926340769344798730/RunarToken.png"
                        
                        elif npc == "Voivode":

                            shopintro = "Good day. Feel free to browse. Don't touch, ask first.\n------------------------------------------------------------"
                            shopcolour = 0x96470c
                            npcthumb = "https://cdn.discordapp.com/attachments/912758732142837761/921654371903750144/D-9576iWwAAPgcP.jpeg"

                        elif npc == "Amelia":

                            shopintro = "Oh hello, dear. Welcome to my own little garden, Sophie's Garden, might we find you a friend today?\n------------------------------------------------------------"
                            shopcolour = 0x9ac7fc
                            npcthumb = ""

                        else:

                            shopintro = ""
                            shopcolour = 0x000000
                            npcthumb = ""

                    print(message.author.name + " summoned a shop")

                    if len(itlist) != 0:

                        shoptext = shopintro + "\n" + "\n".join(sorted(itlist)).replace("Bimbonomicon", "The Bimbonomicon").replace("Doctor", "The Doctor").replace("Widow", "The Widow").replace("Tome of Imps", "The Tome of Imps")

                        shopemb = discord.Embed(title = shoptit, description = shoptext, colour = shopcolour)

                        shopemb.set_footer(text = "------------------------------------------------------------\nBuy an item with the `%buy <name>` command.\nFor more information on an item use the `%item <name>` command.")

                        shopemb.set_thumbnail(url = npcthumb)

                        await message.delete()

                        await message.channel.send(embed = shopemb)

                    else:

                        await message.channel.send(embed = discord.Embed(title = "Request Failed", description = "We can't find a shop with the name containing " + message.content.split(" ",1)[1], colour = embcol))

                        await message.delete()

            #Runar's Inventory

            elif message.content.lower().startswith(str(myprefix) + "spellrotation") and "lorekeeper" in str(message.author.roles).lower():

                cantrips = ["Acid Splash (Conjuration)","Chill Touch (Necromancy)","Dancing Lights (Evocation)","Druidcraft (Transmutation)","Eldritch Blast (Evocation)","Fire Bolt (Evocation)","Guidance (Divination)","Light (Evocation)","Mage Hand (Conjuration)","Mending (Transmutation)","Message (Transmutation)","Minor Illusion (Illusion)","Poison Spray (Conjuration)","Prestidigitation (Transmutation)","Produce Flame (Conjuration)","Ray of Frost (Evocation)","Resistance (Abjuration)","Sacred Flame (Evocation)","Shillelagh (Transmutation)","Shocking Grasp (Evocation)","Spare the Dying (Necromancy)","Thaumaturgy (Transmutation)","True Strike (Divination)","Vicious Mockery (Enchantment)"]

                spell1s = ["Alarm (Abjuration (Ritual))","Animal Friendship (Enchantment)","Bane (Enchantment)","Bless (Enchantment)","Burning Hands (Evocation)","Charm Person (Enchantment)","Color Spray (Illusion)","Command (Enchantment)","Comprehend Languages (Divination (Ritual))","Create or Destroy Water (Transmutation)","Cure Wounds (Evocation)","Detect Evil and Good (Divination)","Detect Magic (Divination (Ritual))","Detect Poison and Disease (Divination (Ritual))","Disguise Self (Illusion)","Divine Favor (Evocation)","Entangle (Conjuration)","Expeditious Retreat (Transmutation)","Faerie Fire (Evocation)","False Life (Necromancy)","Feather Fall (Transmutation)","Find Familiar (Conjuration (Ritual))","Floating Disk (Conjuration (Ritual))","Fog Cloud (Conjuration)","Goodberry (Transmutation)","Grease (Conjuration)","Guiding Bolt (Evocation)","Healing Word (Evocation)","Hellish Rebuke (Evocation)","Heroism (Enchantment)","Hideous Laughter (Enchantment)","Hunter’s Mark (Divination)","Identify (Divination (Ritual))","Illusory Script (Illusion (Ritual))","Inflict Wounds (Necromancy)","Jump (Transmutation)","Longstrider (Transmutation)","Mage Armor (Abjuration)","Magic Missile (Evocation)","Protection from Evil and Good (Abjuration)","Purify Food and Drink (Transmutation (Ritual))","Sanctuary (Abjuration)","Shield (Abjuration)","Shield of Faith (Abjuration)","Silent Image (Illusion)","Sleep (Enchantment)","Speak with Animals (Divination (Ritual))","Thunderwave (Evocation)","Unseen Servant (Conjuration (Ritual))"]

                spell2s = ["Acid Arrow (Evocation)","Aid (Abjuration)","Alter Self (Transmutation)","Animal Messenger (Enchantment (Ritual))","Arcane Lock (Abjuration)","Arcanist’s Magic Aura (Illusion)","Augury (Divination (Ritual))","Barkskin (Transmutation)","Blindness/Deafness (Necromancy)","Blur (Illusion)","Branding Smite (Evocation)","Calm Emotions (Enchantment)","Continual Flame (Evocation)","Darkness (Evocation)","Darkvision (Transmutation)","Detect Thoughts (Divination)","Enhance Ability (Transmutation)","Enlarge/Reduce (Transmutation)","Enthrall (Enchantment)","Find Steed (Conjuration)","Find Traps (Divination)","Flame Blade (Evocation)","Flaming Sphere (Conjuration)","Gentle Repose (Necromancy (Ritual))","Gust of Wind (Evocation)","Heat Metal (Transmutation)","Hold Person (Enchantment)","Invisibility (Illusion)","Knock (Transmutation)","Lesser Restoration (Abjuration)","Levitate (Transmutation)","Locate Animals or Plants (Divination (Ritual))","Locate Object (Divination)","Magic Mouth (Illusion (Ritual))","Magic Weapon (Transmutation)","Mirror Image (Illusion)","Misty Step (Conjuration)","Moonbeam (Evocation)","Pass without Trace (Abjuration)","Prayer of Healing (Evocation)","Protection from Poison (Abjuration)","Ray of Enfeeblement (Necromancy)","Rope Trick (Transmutation)","Scorching Ray (Evocation)","See Invisibility (Divination)","Shatter (Evocation)","Silence (Illusion)","Spider Climb (Transmutation)","Spike Growth (Transmutation)","Spiritual Weapon (Evocation (Ritual))","Suggestion (Enchantment)","Warding Bond (Abjuration)","Web (Conjuration)","Zone of Truth (Enchantment)"]

                spell3s = ["Animate Dead (Necromancy)","Beacon of Hope (Abjuration)","Bestow Curse (Necromancy)","Blink (Transmutation)","Call Lightning (Conjuration)","Clairvoyance (Divination)","Conjure Animals (Conjuration)","Counterspell (Abjuration)","Create Food and Water (Conjuration)","Daylight (Evocation)","Dispel Magic (Abjuration)","Fear (Illusion)","Fireball (Evocation)","Fly (Transmutation)","Gaseous Form (Transmutation)","Glyph of Warding (Abjuration)","Haste (Transmutation)","Hypnotic Pattern (Illusion)","Lightning Bolt (Evocation)","Magic Circle (Abjuration)","Major Image (Illusion)","Mass Healing Word (Evocation)","Meld into Stone (Transmutation (Ritual))","Nondetection (Abjuration)","Phantom Steed (Illusion (Ritual))","Plant Growth (Transmutation)","Protection from Energy (Abjuration)","Remove Curse (Abjuration)","Revivify (Necromancy)","Sending (Evocation)","Sleet Storm (Conjuration)","Slow (Transmutation)","Speak with Dead (Necromancy)","Speak with Plants (Transmutation)","Spirit Guardians (Conjuration)","Stinking Cloud (Conjuration)","Tiny Hut (Evocation (Ritual))","Tongues (Divination)","Vampiric Touch (Necromancy)","Water Breathing (Transmutation (Ritual))","Water Walk (Transmutation (Ritual))","Wind Wall (Evocation)"]

                spell4s = ["Arcane Eye (Divination)","Banishment (Abjuration)","Black Tentacles (Conjuration)","Blight (Necromancy)","Compulsion (Enchantment)","Confusion (Enchantment)","Conjure Minor Elementals (Conjuration)","Conjure Woodland Beings (Conjuration)","Control Water (Transmutation)","Death Ward (Abjuration)","Dimension Door (Conjuration)","Divination (Divination (Ritual))","Dominate Beast (Enchantment)","Fabricate (Transmutation)","Faithful Hound (Conjuration)","Fire Shield (Evocation)","Freedom of Movement (Abjuration)","Giant Insect (Transmutation)","Greater Invisibility (Illusion)","Guardian of Faith (Conjuration)","Hallucinatory Terrain (Illusion)","Ice Storm (Evocation)","Locate Creature (Divination)","Phantasmal Killer (Illusion)","Polymorph (Transmutation)","Private Sanctum (Abjuration)","Resilient Sphere (Evocation)","Secret Chest (Conjuration)","Stone Shape (Transmutation)","Stoneskin (Abjuration)","Wall of Fire (Evocation)"]

                spell5s = ["Animate Objects (Transmutation)","Antilife Shell (Abjuration)","Arcane Hand (Evocation)","Awaken (Transmutation)","Cloudkill (Conjuration)","Commune (Divination (Ritual))","Commune with Nature (Divination (Ritual))","Cone of Cold (Evocation)","Conjure Elemental (Conjuration)","Contact Other Plane (Divination (Ritual))","Contagion (Necromancy)","Creation (Illusion)","Dispel Evil and Good (Abjuration)","Dominate Person (Enchantment)","Dream (Illusion)","Flame Strike (Evocation)","Geas (Enchantment)","Greater Restoration (Abjuration)","Hallow (Evocation)","Hold Monster (Enchantment)","Insect Plague (Conjuration)","Legend Lore (Divination)","Mass Cure Wounds (Evocation)","Mislead (Illusion)","Modify Memory (Enchantment)","Passwall (Transmutation)","Planar Binding (Abjuration)","Raise Dead (Necromancy)","Reincarnate (Transmutation)","Scrying (Divination)","Seeming (Illusion)","Telekinesis (Transmutation)","Telepathic Bond (Divination (Ritual))","Teleportation Circle (Conjuration)","Tree Stride (Conjuration)","Wall of Force (Evocation)","Wall of Stone (Evocation)"]

                spell6s = ["Blade Barrier (Evocation)","Chain Lightning (Evocation)","Circle of Death (Necromancy)","Conjure Fey (Conjuration)","Contingency (Evocation)","Create Undead (Necromancy)","Disintegrate (Transmutation)","Eyebite (Necromancy)","Find the Path (Divination)","Flesh to Stone (Transmutation)","Forbiddance (Abjuration (Ritual))","Freezing Sphere (Evocation)","Globe of Invulnerability (Abjuration)","Guards and Wards (Abjuration)","Harm (Necromancy)","Heal (Evocation)","Heroes’ Feast (Conjuration)","Instant Summons (Conjuration (Ritual))","Irresistible Dance (Enchantment)","Magic Jar (Necromancy)","Mass Suggestion (Enchantment)","Move Earth (Transmutation)","Planar Ally (Conjuration)","Programmed Illusion (Illusion)","Sunbeam (Evocation)","Transport via Plants (Conjuration)","True Seeing (Divination)","Wall of Ice (Evocation)","Wall of Thorns (Conjuration)","Wind Walk (Transmutation)","Word of Recall (Conjuration)"]

                spell7s = ["Arcane Sword (Evocation)","Conjure Celestial (Conjuration)","Delayed Blast Fireball (Evocation)","Divine Word (Evocation)","Etherealness (Transmutation)","Finger of Death (Necromancy)","Fire Storm (Evocation)","Forcecage (Evocation)","Magnificent Mansion (Conjuration)","Mirage Arcane (Illusion)","Prismatic Spray (Evocation)","Project Image (Illusion)","Regenerate (Transmutation)","Resurrection (Necromancy)","Reverse Gravity (Transmutation)","Sequester (Transmutation)","Simulacrum (Illusion)","Symbol (Abjuration)","Teleport (Conjuration)"]

                cantsin = random.randint(2,8)

                spell1sin = random.randint(2,8)

                spell2sin = random.randint(1,8)

                spell3sin = random.randint(1,10)

                spell4sin = random.randint(2,8)

                spell5sin = random.randint(0,7)

                spell6sin = random.randint(0,5)

                spell7sin = random.randint(0,3)

                spellsin = ["**Cantrips**"]

                cantrips = sample(cantrips, cantsin)

                spell1s = sample(spell1s, spell1sin)

                spell2s = sample(spell2s, spell2sin)

                spell3s = sample(spell3s, spell3sin)

                spell4s = sample(spell4s, spell4sin)

                spell5s = sample(spell5s, spell5sin)

                spell6s = sample(spell6s, spell6sin)

                spell7s = sample(spell7s, spell7sin)

                for a in range(len(cantrips)):

                    spellsin.append(str(cantrips[a]) + str(" " + str(int(random.randint(2,7)/2 + random.randint(11,21))) + dezzieemj))

                spellsin.append("\n**First Level Spells**")

                for a in range(len(spell1s)):

                    spellsin.append(str(spell1s[a]) + str(" " + str(int(random.randint(1,6)*5 + random.randint(21,121))) + dezzieemj))

                spellsin.append("\n**Second Level Spells**")

                for a in range(len(spell2s)):

                    spellsin.append(str(spell2s[a]) + str(" " + str(int(random.randint(2,20)*50 + random.randint(21,121))) + dezzieemj))
                    
                spellsin.append("\n**Third Level Spells**")

                for a in range(len(spell3s)):

                    spellsin.append(str(spell3s[a]) + str(" " + str(int(random.randint(1,6)*50 + random.randint(201,301))) + dezzieemj))

                spellsin.append("\n**Fouth Level Spells**")

                for a in range(len(spell4s)):

                    spellsin.append(str(spell4s[a]) + str(" " + str(int(random.randint(1,6)*50 + random.randint(201,301))) + dezzieemj))

                spellsin.append("\n**Fifth Level Spells**")

                for a in range(len(spell5s)):

                    spellsin.append(str(spell5s[a]) + str(" " + str(int(random.randint(1,6)*50 + random.randint(201,301))) + dezzieemj))

                spellsin.append("\n**Sixth Level Spells**")

                for a in range(len(spell6s)):

                    spellsin.append(str(spell6s[a]) + str(" " + str(int(random.randint(2,5)*500 + random.randint(2001,2101))) + dezzieemj))

                spellsin.append("\n**Seventh Level Spells**")

                for a in range(len(spell7s)):

                    spellsin.append(str(spell7s[a]) + str(" " + str(int(random.randint(2,5)*500 + random.randint(2001,2101))) + dezzieemj))
                
                spelllist = "Runar has the following spellscrolls available right now:\n\n" + "\n".join(spellsin) + "\n\nCustom scribed scrolls can also be requested, at the following prices:\n\nCantrips: 24 " + dezzieemj + ", 1 day to make\n1st Levels: 423" + dezzieemj + ", 1 day to make\n2nd Levels: 445" + dezzieemj + ", 3 days to make\n3rd Levels: 1350" + dezzieemj + ", 1 week to make\n4th Levels: 1550" + dezzieemj + ", 2 weeks to make\n5th Levels: 1800"  + dezzieemj + ", 4 weeks to make\n6th Levels: 6100" + dezzieemj + ", 8 weeks to make\n7th Levels: 7100" + dezzieemj + ", 16 weeks to make."

                await message.channel.send(embed = discord.Embed(title = "Spells", description = spelllist, colour = embcol))

            #Lorekeeper Ping

            elif message.channel.id == 917235652947488808 or message.channel.id == 917235695398039583 or message.channel.id == 917236137234399233 or message.channel.id == 917236902921388042 or message.channel.id == 917239168969621515 or message.channel.id == 917565100553031732:

                if not isbot and not message.content.startswith("%") and not message.content.startswith("$"):

                    prevmess = [joinedMessages async for joinedMessages in message.channel.history(limit=2, oldest_first=False)] #Fix for pebblehost Await issue

                    #prevmess = await message.channel.history(limit=2, oldest_first=False).flatten()

                    shopids = [917235652947488808, 917235695398039583, 917236137234399233, 917236902921388042, 917239168969621515, 917565100553031732]

                    shopnames = ["🏺the-golden-jackal🏺", "🐍venom-ink🐍", "🧵widows-boutique🧵", "🍄sophies-garden🍄", "📜menagerie-magiks📜", "🔔the-polished-knob🔔"]

                    prtimestamp = prevmess[1].created_at

                    mestimestamp = message.created_at

                    diff = str(mestimestamp - prtimestamp)

                    timediff = diff.split(":")[0]

                    if "day" in str(timediff):

                        ping = True

                    elif int(timediff) > 3:

                        ping = True

                    else:

                        ping = False

                    if "lorekeeper" in str(authroles).lower():

                        ping = False

                    if ping:

                        for n in range(len(shopnames)):

                            if message.channel.id == shopids[n]:

                                roomname = "#" + shopnames[n]

                                room = "<#" + str(message.channel.id) + ">"

                        await client.get_channel(996826636358000780).send(str(message.author.name.split("#")[0] + " has sent a message in " + room + ". The last message in the channel before this was over " + str(timediff).replace(", ", " and ") + " hours ago.\n\n<@&" + str(912552597041340416) + ">, is anyone able to go and assist them?").replace("1 hours", "an hour"))

                        print("Lorekeepers were pinged to play shops")

            elif message.channel.id == 845498061459554334 or message.channel.id == 845498746870693898 or message.channel.id == 861688038928023583 or message.channel.id == 838821621913223229 or message.channel.id == 955144068386664479 or message.channel.id == 951666605568458752 or message.channel.id == 951666822636273674 or message.channel.id == 951666912272732270:

                if not isbot and not message.content.startswith("%") and not message.content.startswith("$"):

                    if random.randint(1,200) == 1:

                        ping = True

                    else:

                        ping = False

                    if "lorekeeper" in str(authroles).lower():

                        ping = False

                    if ping:

                        room = "<#" + str(message.channel.id) + ">"

                        await client.get_channel(996826636358000780).send(str(message.author.name.split("#")[0] + " has sent a message in " + room + ". We think a <@&912552597041340416> should go and torment them.\n\nWe suggest... Um, tentacles? That's all we've got at the moment, but this will be expanded as room specific things are added. Also need to check kinks. There are some *weirdos* out there *not* into tentacles?\n\nThis has a one in 200 chance of appearing on any given message. Let Callum know if you think that's too much or too little?"))

                        print("Lorekeepers were pinged to run traps")

            elif message.content.lower().startswith(str(myprefix) + "rembed"):

                #mess = await client.get_channel(1008422338548736060).history(limit=500, oldest_first=True).flatten()
                mess = [joinedMessages async for joinedMessages in client.get_channel(1008422338548736060).history(limit=500, oldest_first=True).flatten()] #Pebblehost msg history fix
                for n in range(len(mess)):

                    if mess[n].content != "":

                        messn = mess[n].content.replace("***The Mistress***", "***T̶̡͚͊̒̈́̇̉͑̏͑̚h̴̬̓̔̈́̈́͝ȩ̵̢͖̮̻̻̰̟͔̗̃̈́͝ ̴̡͈̦̯͗̈͋͗̈́̾̍̉̄M̷̰̬̜̜̪͆̉͗̋͑̐̉̚͝͝i̴̡̛̦͍̦͈͉̯̻͇͑̒̊̋̾̔͠s̷̭̫̾͗͒̀́t̷̢͈̜͙̬̦͕͎̣̉̍̈́͋̊̎̾̂̌r̴̢̢͖͚̬̣̩̺̆͒̈́͛ȩ̸̜̠͖͖̼͓͍̯̫́͌͆̕s̶̘̺̻̖̲͔͌̓͗̒̆ͅs̶̛̤̻̭̤̰̅̇͌͗***")

                        if len(messn) >= 2000:

                            messns = messn.split(".")

                            currmess = []

                            for i in range(len(messns)):

                                currmess.append(messns[i])

                                try:

                                    if len(".".join(currmess)) + len(messns[i+1]) > 2000:

                                        rembed = discord.Embed(title = mess[n].author.name, description = ".".join(currmess), colour = embcol)

                                        rembed.set_thumbnail(url = mess[n].author._avatar)

                                        await message.channel.send(embed = rembed)

                                        currmess = []

                                except IndexError:

                                    rembed = discord.Embed(title = mess[n].author.name, description = ".".join(currmess), colour = embcol)

                                    rembed.set_thumbnail(url = mess[n].author._avatar)

                                    await message.channel.send(embed = rembed)

                                    currmess = []

                        else:

                            await message.channel.send(mess[n].author.name + ": " + messn)

            #Impersonator React

            elif "gothica" in message.content.lower().replace("-","").replace(".","") or "thic goth" in message.content.lower().replace("-","").replace(".","").replace("cc","c") or "gothy" in message.content.lower().replace("-","").replace(".",""):

                if message.author.name != "C_allum":

                    await message.add_reaction('\N{EYES}')

            #Dating Game

            elif (str(message.channel).startswith("Dating Game") and not isbot):

                if not message.content.startswith("TEST"):

                    contestantno = str(message.channel).split("-")[1]

                    if contestantno == str(message.channel).split("-")[1] == "1":

                        mysterembed = discord.Embed(title = "Mystery Contestant 1", description = message.content, colour = 0x46D311)

                        mysterembed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/927298209183830066/989179789371928677/token_2_2.png")

                    elif contestantno == str(message.channel).split("-")[1] == "2":

                        mysterembed = discord.Embed(title = "Mystery Contestant 2", description = message.content, colour = 0x115AD3)

                        mysterembed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/927298209183830066/989179797643096144/token_3_2.png")

                    elif contestantno == str(message.channel).split("-")[1] == "3":

                        mysterembed = discord.Embed(title = "Mystery Contestant 3", description = message.content, colour = 0x6F11D3)

                        mysterembed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/927298209183830066/989179806555971594/token_4_1.png")

                    elif contestantno == str(message.channel).split("-")[1] == "4":

                        mysterembed = discord.Embed(title = "Mystery Contestant 4", description = message.content, colour = 0xB8B8B8)

                        mysterembed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/927298209183830066/989179813627568128/token_5_1.png")

                    await client.get_channel(990265174126645298).send(embed = mysterembed)

            #Timestamp Message

            elif message.content.lower().startswith(str(myprefix) + "timestamp"):

                print("A")

                try:

                    timezone = message.content.split(" ")[2]

                except IndexError:

                    timezone = "GMT"

                print(timezone)

                try:

                    time = datetime.time(message.content.split(" ")[7])

                except IndexError:

                    time = str(datetime.timestamp(datetime.now())).split(".")[0]

                print(time)

                await message.channel.send(embed = discord.Embed(title = "Timestamp Converter", description = "<t:" + str(time) + ":T>" , colour = embcol))

            #Shop Break Command

            else:

                messcomm = 0

                rooms = ["🏺the-golden-jackal🏺", "🐍venom-ink🐍", "🧵widows-boutique🧵", "🍄sophies-garden🍄", "📜menagerie-magiks📜", "🔔the-polished-knob🔔"]

                for n in range(len(rooms)):

                    roomcur = rooms[n]

                    roomchannel = discord.utils.get(client.get_all_channels(), name = roomcur)

                    if message.channel != roomchannel and message.channel.name != "alias-bot":

                        #roomlatest = await client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()
                        roomlatest = [joinedMessages async for joinedMessages in client.get_channel(roomchannel.id).history(limit=2, oldest_first=False).flatten()] #Fix for pebblehost Await issue

                        if roomlatest[0].author == client.user:

                            roomlatest[0] = roomlatest[1]

                            scenebroken = True

                        else:

                            scenebroken = False

                        rtimestamp = roomlatest[0].created_at

                        mestimestamp = message.created_at

                        diff = str(mestimestamp - rtimestamp)

                        if int(str(rtimestamp).split(":")[0].split(" ")[1]) >= 3:

                            if "day" in diff and not "-" in diff:

                                if not scenebroken:

                                    await client.get_channel(roomchannel.id).send("```\u200b```")

                                    print("Automatically created a scene break in " + roomcur + ". The time difference was: " + diff + ", which Gothica read as " + str(diff.split(":")[0]) + " hours.")

                            elif "-" in diff:

                                pass

                            elif int(diff.split(":")[0]) == 0:

                                pass

                            elif int(diff.split(":")[0]) >= 3:

                                if not scenebroken:

                                    await client.get_channel(roomchannel.id).send("```\u200b```")

                                    print("Automatically created a scene break in " + roomcur + ". The time difference was: " + diff + ", which Gothica read as " + str(diff.split(":")[0]) + " hours.")

            #Per message income
            if not "verification" in str(message.channel).lower():
                
                if not isbot:
                    
                    row = 0

                    newtot = 0

                    economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

                    #Existing Member

                    if str(message.author) in str(economydata):

                        for a in range(math.floor(len(economydata)/4)):

                            b = a * 4 + 5

                            if "safe passages" in str(message.channel.category).lower() or "the market" in str(message.channel.category).lower() or "keyholder" in str(message.channel.category).lower() or "dangerous depths" in str(message.channel.category).lower() or "outside adventures" in str(message.channel.category).lower() or "quests" in str(message.channel.category).lower():

                                mult = 1

                            else:

                                mult = 0

                            charcount = len(message.content)

                            randaward = (math.floor(charcount/100) + random.randint(1,4)) * mult

                            if str(message.author) in str(economydata[b][0]):

                                row = b + 1

                                newtot = int(economydata[b][1]) + int(randaward)

                                break

                    #New member

                    else:

                        newtot = 0

                        print(str(message.author) + " has been added to the economy at " + str(datetime.now()))

                        if (int(len(economydata) - 1) / 4).is_integer():

                            row = len(economydata) + 1

                        else:
                            row = ((int(int(len(economydata) - 1) / 4) + 1) * 4) + 2 #Calculates the next line on the sheet that is divisible by 4. This is a bit of a magic formula. 
                            #len econdata-1 / 4 gives us the player number of the current last player. that + 1 and * 4 gives us the cell that is one before the last one of that player (because we did -1 earlier). 
                            #+1 gives us the last line of the currently last registered player, meaning +2 gives us the line the new player's entry needs to start at.
                    
                    try:

                        prevtime = int(str(economydata[row][0]))

                    except IndexError:

                        prevtime = 0

                    except ValueError:

                        prevtime = 0

                    dataup = [str(message.author), str(newtot)]

                    if int(str(datetime.timestamp(datetime.now())).split(".")[0]) - int(prevtime) >= 300 and row != 0:

                        sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(row + 1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[datetime.timestamp(datetime.now())]])).execute()

                        sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(row)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[dataup])).execute()
    
    except AttributeError:

        if not "Direct Message" in str(message.channel):

            pass

            #print("Guild ID Error? " + str(message.channel))

@client.event
async def on_raw_reaction_add(reaction):

    if "lorekeeper" in str(reaction.member.roles).lower() or "ghostwriter" in str(reaction.member.roles).lower():

        mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        if reaction.emoji.name == "dz" or reaction.emoji.name == "cashmoney" or reaction.emoji.name == "makeitrain" or reaction.emoji.name == "DzCrit":

            economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

            reciprow = ""

            targid = mess.author.id

            target = await client.fetch_user(targid)

            targetName = target.name

            try:

                for a in range(math.floor(len(economydata)/4)):

                    b = a * 4 + 5

                    if str(targetName + "#" + str(target.discriminator)) in str(economydata[b][0]):

                        reciprow = b + 1

                        break

            except IndexError:

                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))

            if reaction.emoji.name == "dz":
                
                giveamount = reactdz

            elif reaction.emoji.name == "cashmoney":
                
                giveamount = reactCashMoney

            elif reaction.emoji.name == "makeitrain":
                
                giveamount = reactMakeItRain

            else:

                giveamount = random.randint(100,500)

            recipnewtot = int(economydata[reciprow-1][1]) + int(giveamount)

            sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipnewtot]])).execute()

            if reaction.member.name == targetName:

                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipnewtot) + dezzieemj + "\n\nNot sure why they're awarding dezzies to themself like this, but ok.", colour = embcol, url = mess.jump_url))    

            else:

                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipnewtot) + dezzieemj, colour = embcol, url = mess.jump_url))
        
        elif reaction.emoji.name == "💰":

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

    #Dezzie Reacts with weekly pool
    elif reaction.emoji.name == "dz" or reaction.emoji.name == "cashmoney" or reaction.emoji.name == "makeitrain" or reaction.emoji.name == "DzCrit":

        mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        economydata = sheet.values().get(spreadsheetId = EconSheet, range = "A1:ZZ2000", majorDimension='ROWS').execute().get("values")

        reciprow = ""

        targid = mess.author.id

        target = await client.fetch_user(targid)

        targetName = target.name

        giverow = ""

        giveid = reaction.member.id

        giver = await client.fetch_user(giveid)

        givename = giver.name

        try:

            for a in range(math.floor(len(economydata)/4)):

                b = a * 4 + 5

                if str(targetName + "#" + str(target.discriminator)) in str(economydata[b][0]):

                    reciprow = b + 1

                    break

            for a in range(math.floor(len(economydata)/4)):

                b = a * 4 + 5

                if str(givename + "#" + str(giver.discriminator)) in str(economydata[b][0]):

                    giverow = b + 1

                    break

        except IndexError:

            if not mess.author.bot:

                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = str(mess.author) + " is not in the economy.", description = "If this should not be the case, speak to Callum", colour = embcol))



        #Determine gift amount - Values in CommonDefinitions.py
        if reaction.emoji.name == "dz":
                
            giveamount = reactdz

        elif reaction.emoji.name == "cashmoney":
                
            giveamount = reactCashMoney

        elif reaction.emoji.name == "makeitrain":
                
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


        #Check if given amount is smaller than the pool of dezzies left for the user
        if reaction.channel_id != 828545311898468352: #Disable Noticeboard Reacts

            if reaction.member.name == targetName:

                await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = "No.", description = targetName + ", you can't just award dezzzies to yourself.", colour = embcol))    

                await client.get_channel(918257057428279326).send(targetName + " tried to award dezzies to themself.")

            else:
                #Enough dezzies left in users dezzie pool:
                if giveamount <= prevDezziePool:

                    recipNewTot = int(economydata[reciprow-1][1]) + int(giveamount)
                 
                    newDezziePool = prevDezziePool - giveamount

                    sheet.values().update(spreadsheetId = EconSheet, range = str("B" + str(reciprow)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[recipNewTot]])).execute()

                    sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(giverow+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()

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

                    sheet.values().update(spreadsheetId = EconSheet, range = str("A" + str(giverow+3)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[newDezziePool]])).execute()

                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + " has awarded " + str(giveamount) + dezzieemj + " to " + targetName, description = targetName + " now has " + str(recipNewTot) + dezzieemj + "\n\n" + givename + " has used up their dezzie award pool for the week!", colour = embcol, url = mess.jump_url))

                    await client.get_channel(918257057428279326).send(givename + " awarded Dezzies to " + targetName)
                
                #User dezzie pool is empty:
                else:
                    await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = reaction.member.name + "'s dezzie award pool for the week is empty!" , description = "You will receive a fresh pool of dezzies to award to others at the start of next week!", colour = embcol, url = mess.jump_url))



        else:

            await client.get_channel(reaction.channel_id).send(embed=discord.Embed(title = "You can't use this at the here.", colour = embcol, url = mess.jump_url))




    if reaction.emoji.name == "cuffs":

        chan = client.get_channel(reaction.channel_id)

        mess = await chan.fetch_message(reaction.message_id)

        if reaction.channel_id == 994340109962973204:

            emb = discord.Embed(title = reaction.member.name + " has claimed this artwork to make a character from.", colour = embcol)

            user = await client.fetch_user(int(reaction.member.id))

            await user.send("You have claimed this image. If it vanishes from here, it should still be in the channel.")

            try:

                emb.set_thumbnail(url = mess.attachments[0])

                await user.send(mess.attachments[0])

            except IndexError:

                emb.set_thumbnail(url = mess.content)

                await user.send(mess.content)

            meslist = ["CLAIMED"]

            reacts = meslist[random.randint(0,len(meslist)-1)]

            reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

            for n in range(len(reacts)):

                await mess.add_reaction(reacts[n])

        else:

            try:

                a = mess.attachments[0]

                await client.get_channel(994340109962973204).send(reaction.member.name)

                await client.get_channel(994340109962973204).send(mess.attachments[0].url)

            except IndexError:

                await mess.channel.send("That message doesn't contain an image.")

    elif reaction.emoji.name == "❓":

        mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        await client.get_channel(918257057428279326).send(str(reaction.member.name) + " queried the tupper of " + str(mess.author))


    
    if "lorekeeper" in str(reaction.member.roles).lower() or "moderator" in str(reaction.member.roles).lower():   

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

    if reaction.emoji.name == "cuffs":

        chan = client.get_channel(reaction.channel_id)

        mess = await chan.fetch_message(reaction.message_id)

        if reaction.channel_id == 994340109962973204:

            emb = discord.Embed(title = reaction.member.name + " has claimed this artwork to make a character from.", colour = embcol)

            user = await client.fetch_user(int(reaction.member.id))

            await user.send("You have claimed this image. If it vanishes from here, it should still be in the channel.")

            try:

                emb.set_thumbnail(url = mess.attachments[0])

                await user.send(mess.attachments[0])

            except IndexError:

                emb.set_thumbnail(url = mess.content)

                await user.send(mess.content)

            meslist = ["CLAIMED"]

            reacts = meslist[random.randint(0,len(meslist)-1)]

            reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

            for n in range(len(reacts)):

                await mess.add_reaction(reacts[n])

        else:

            try:

                a = mess.attachments[0]

                await client.get_channel(994340109962973204).send(reaction.member.name)

                await client.get_channel(994340109962973204).send(mess.attachments[0].url)

            except IndexError:

                await mess.channel.send("That message doesn't contain an image.")

    elif reaction.emoji.name == "❓":

        mess = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        await client.get_channel(918257057428279326).send(str(reaction.member.name) + " queried the tupper of " + str(mess.author))

    # else:

    #     print(reaction.emoji.name)

@client.event
async def on_message_delete(message):

    if "@" in message.content and not message.content.startswith("%") and not " " in message.content:

        await client.get_channel(logchannel).send(message.author.name + "'s message was deleted in " + str(message.channel) + ". The message was:\n\n" + message.content.replace("@", "\@") + "\n\nThis message was deleted at " + str(datetime.now()))

client.run(token, reconnect=True)
