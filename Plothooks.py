from CommonDefinitions import sheet as SheetsService, CharSheet, plothooks, random, embcol, fracture, Plotsheet, datetime, discord

async def create(message):
    delay = await message.channel.send("We are processing your request now")

    if " " in message.content:

        tempname = message.content.split(" ",1)[1]

    else:

        tempname = None

    #get player chars

    auth = message.author.name

    pnames = SheetsService.values().get(spreadsheetId = CharSheet, range = "B1:B1000").execute().get("values")

    msgspl = message.content.split(" ")

    tit = None
    desc = ""
    foot = None
    imgurl = None

    pchars = SheetsService.values().get(spreadsheetId = CharSheet, range = "F1:F1000").execute().get("values")
    pstat = SheetsService.values().get(spreadsheetId = CharSheet, range = "X1:X1000").execute().get("values")
    ppron = SheetsService.values().get(spreadsheetId = CharSheet, range = "I1:I1000").execute().get("values")

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

        return


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

    prevlist = SheetsService.values().get(spreadsheetId = Plotsheet, range = "W2:AM100", majorDimension='ROWS').execute().get("values")

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

                room = SheetsService.values().get(spreadsheetId = Plotsheet, range = "A1:O1", majorDimension='COLUMNS').execute().get("values")

                selroom = room[j][0]

                prevlist[pind][j+1] = "".join(roomstring)

                prevlist[pind][-1] = str(datetime.now())

                SheetsService.values().update(spreadsheetId = Plotsheet, range = str("W" + str(pind+2)), valueInputOption = "RAW", body = dict(majorDimension='ROWS', values=[prevlist[pind]])).execute()

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

async def showLeaderboard(message):
    delay = await message.channel.send("We are processing your request now")

    prevlist = SheetsService.values().get(spreadsheetId = Plotsheet, range = "R2:AC100", majorDimension='ROWS').execute().get("values")

    formlist = []

    for n in range(len(prevlist)):

        seenno = 0

        for sn in range(len(plothooks)):
            try:
                seenno += prevlist[n][sn+1].count("1")
            except:
                return

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

