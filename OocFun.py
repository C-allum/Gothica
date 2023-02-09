from CommonDefinitions import *

#Voyeur's Lounge Redirect
async def VoyRedirect(message):

    if message.author.name != "Avrae":

        if not message.content.startswith("TEST"):

            if random.randint(1,30) != 1:

                await message.channel.send(random.choice(["Shouldn't you be in the <#975624986603692052>?","I believe <#975624986603692052> is that way.", "<#975624986603692052>, for all your in character comments!", "That belongs in <#975624986603692052>", "You know, I *could* just delete comments that should be in <#975624986603692052>...", message.author.name + ", You know where <#975624986603692052> is.", "<#975624986603692052>. <#975624986603692052>. <#975624986603692052>. Does saying it thrice send " + message.author.name + " there?"]))

                if "sorry" in message.content.lower() or "goth" in message.content.lower():

                    meslist = ["BAD","HOWDARE", "NAUGHTY", "RUDE"]

                    reacts = meslist[random.randint(0,len(meslist)-1)]

                    reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

                    for n in range(len(reacts)):

                        await message.add_reaction(reacts[n])

            else:

                await message.delete()

                await message.channel.send(random.choice(["You asked for it. I deleted " + message.author.name + "'s message and moved them to <#975624986603692052>", "Goodbye, poorly located message from " + message.author.name + ". We have decided to put you in <#975624986603692052> instead.", "We've been threatening it for a while. Now we have actually deleted a message that should be in <#975624986603692052>!"]))

                voyemb = discord.Embed(title = message.author.name + "'s message, moved here from ooc:", description = message.content, colour = embcol)

                voyemb.set_thumbnail(url = message.author.avatar)

                await client.get_channel(975624986603692052).send(embed = voyemb)

#Gag
async def gag(message):

    await message.delete()

    print(message.author.name + " sent a gagged message:\n" + message.content)

    messpoint = random.randint(0, math.floor(len(message.content)*2/3))

    msgmmms = []

    for a in range(len(message.content)):

        if a < messpoint:

            msgmmms.append(message.content[a])

        elif message.content[a].isalpha():

            msgmmms.append(random.choice(["M", "m", "m", "N", "n", " *m*", "-**m**", "h-"]))

    mutemess = random.choice(["Fine. They said:\n\n", "We think their message was:\n\n", "They probably tried to say:\n\n"]) + "".join(msgmmms)

    if message.author.nick != None:

        await message.channel.send(embed = discord.Embed(title = str(message.author.nick).replace("Spiteful", "Strawberry") + " tried to send a message, but couldn't, as they've been gagged.", description = mutemess, colour = embcol))

    else:

        await message.channel.send(embed = discord.Embed(title = str(message.author.name).replace("Spiteful", "Strawberry") + " tried to send a message, but couldn't, as they've been gagged.", description = mutemess, colour = embcol))

#Set Gag
async def setgag(message):

    gagtarget = message.content.split("@")[1]

    gagid = int(gagtarget.replace("!","").replace("&","").replace(">",""))

    gagmem = await message.guild.query_members(user_ids=[gagid])

    if gagmem[0].nick != None:

        gagname = str(gagmem[0].nick)

    else:

        gagname = str(gagmem[0].name)

    if message.author.nick != None:

        lkname = str(message.author.nick)

    else:

        lkname = str(message.author.name)

    await message.channel.send(embed = discord.Embed(title = gagname + " has been gagged!", description = lkname + " has gagged " + gagname + " for 69 seconds", colour = embcol))

    await client.get_channel(logchannel).send(str(gagmem[0]) + " has been gagged by " + message.author.name)

    role = discord.utils.get(message.author.guild.roles, name="Gagged")

    await gagmem[0].add_roles(role)

    print(message.author.name + " has gagged " + str(gagname).split("#")[0])

    await asyncio.sleep(69)

    await gagmem[0].remove_roles(role)

#Emote
async def emote(message):

    chan = message.content.split(" ")[1].split("/")[5]

    messid = message.content.split(" ")[1].split("/")[6]

    messchan = client.get_channel(int(chan))
    
    mess = messchan.get_partial_message(int(messid))

    meslist = message.content.split(" ")[2].upper()

    reacts = reactletters(meslist)

    for n in range(len(reacts)):

        await mess.add_reaction(reacts[n])

    await message.channel.send("Reactions sent")

    if not "moderator" in str(message.author.roles).lower():

        await client.get_channel(logchannel).send(message.author.name + " reacted to a message in " + messchan.name + " with " + meslist)

    print(message.author.name + " reacted to a message in " + messchan.name + " with " + meslist)

#Player Based Reactions
async def playerreacts(message):

    if "sweet dreams" in message.content.lower() and message.author.name == "Jessalyn":

        await message.add_reaction("<:asexual:861679481525501962>")

    if random.randint(1,20) == 20 and str(message.channel).lower() == "ooc" and " 69" in message.content and not message.content.bot:

        reacts = reactletters("NICE")

        for n in range(len(reacts)):

            await message.add_reaction(reacts[n])

    if (message.author.name == "Mailin") and random.randint(1,5) == 5 and str(message.channel).lower() == "ooc":
    
        meslist = ["CUTE","CUTIE", "ADORBS", "DELIGHT", "BRAT", "SEXY"]

        reacts = meslist[random.randint(0,len(meslist)-1)]

        reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

        for n in range(len(reacts)):

            await message.add_reaction(reacts[n])

    if (message.author.name == "Junebug99") and "valid" in message.content.lower() and str(message.channel).lower() == "ooc":
    
        meslist = ["VALID"]

        reacts = meslist[random.randint(0,len(meslist)-1)]

        reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

        for n in range(len(reacts)):

            await message.add_reaction(reacts[n])

    if message.author.name == "Spiteful Chaos" and str(message.channel).lower() == "ooc" and random.randint(1,50) == 50:

        meslist = ["STRAWB", "STRAWB", "STRAWB", "ROPEBAT"]

        reacts = meslist[random.randint(0,len(meslist)-1)]

        reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

        for n in range(len(reacts)):

            await message.add_reaction(reacts[n])

    if message.author.name == "Rozaria" and str(message.channel).lower() == "ooc" and random.randint(1,50) == 50:
        meslist = ["CAT", "MEOW", "🐈"]
        reacts = meslist[random.randint(0,len(meslist)-1)]
        reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

        for n in range(len(reacts)):
            await message.add_reaction(reacts[n])


    if message.author.name == "C_allum" and str(message.author) != "C_allum#5225":

        meslist = ["FAKE", "LIAR", "FALSE", "NOTREAL", "EVIL", "NOTCAL", "LIES", "NO", "STOPMIXED"]

        reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])

        for n in range(len(reacts)):

            await message.add_reaction(reacts[n])

    if ("sleep well " in (message.content).lower() or "sleep tight " in (message.content).lower() or"gute nacht " in (message.content).lower() or "nini " in (message.content).lower() or "goodnight" in (message.content).lower() or "good night" in (message.content).lower() or "night" in (message.content).lower() or "gn " in (message.content).lower()) and " ken" in message.content.lower() and str(message.channel).lower() == "ooc":
        await message.add_reaction("❤️")