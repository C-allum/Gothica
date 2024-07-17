from CommonDefinitions import *
from discord import app_commands

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

@staffgroup.command(name = "emote", description = "Sends a string of letters as emotes to any message.")
@app_commands.describe(emotes = "The word or words to send. It works best when there are no duplicate letters.", message = "The link to the message to react to. Uses the last message in this channel if not specified.")
@app_commands.checks.has_role("Staff")
@app_commands.default_permissions(manage_messages=True)
async def emote(interaction, emotes: str, message: str = None):
    await interaction.response.defer(ephemeral=True, thinking=False)
    if message != None:
        chan = message.split("/")[5]
        messid = message.split("/")[6]
        messchan = client.get_channel(int(chan))
        mess = messchan.get_partial_message(int(messid))
    else:
        mess = [joinedMessages async for joinedMessages in interaction.channel.history(oldest_first=False, limit = 1)][0]
    meslist = emotes.upper()
    reacts = reactletters(meslist)
    for n in range(len(reacts)):
        try:
            await mess.add_reaction(reacts[n])
        except discord.errors.HTTPException:
            pass
    await client.get_channel(logchannel).send(interaction.user.name + " reacted to a message in " + mess.channel.name + " with " + meslist + " - " + mess.jump_url)
    await interaction.followup.send("Reactions sent")

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

    if str(message.author) in emoteCursed:
        curseindex = emoteCursed.index(str(message.author))
        if random.randint(1,100) <= emoteCursechance[curseindex]:
            meslist = emoteCurses[curseindex].split("|")
            reacts = reactletters(meslist[random.randint(0,len(meslist)-1)])
            for n in range(len(reacts)):
                await message.add_reaction(reacts[n])
    
    if ("sleep well " in (message.content).lower() or "sleep tight " in (message.content).lower() or"gute nacht " in (message.content).lower() or "nini " in (message.content).lower() or "goodnight" in (message.content).lower() or "good night" in (message.content).lower() or "night" in (message.content).lower() or "gn " in (message.content).lower()) and " ken" in message.content.lower() and str(message.channel).lower() == "ooc":
        await message.add_reaction("❤️")

async def emotecurse(message):
    curseparts = message.content.split(" ")[1:]
    cursememb = client.get_guild(message.channel.guild.id).get_member(int(curseparts[0].lstrip("<@").rstrip(">")))
    cursechance = int(curseparts[1])
    curselist = curseparts[2].upper()
    global emoteCursed
    global emoteCursechance
    global emoteCurses
    emoteCursed.append(str(cursememb))
    emoteCursechance.append(cursechance)
    emoteCurses.append(curselist)
    await message.channel.send(embed = discord.Embed(title = "You have cursed " + str(cursememb), description = "Those cursed this week are:\n\n" + "\n".join(emoteCursed), colour= embcol))
    await message.delete()

async def emoteuncurse(message):
    if not " " in message.content:
        targ = message.author.name
    elif "staff" in str(message.author.roles).lower():
        target = client.get_guild(message.channel.guild.id).get_member(int(message.content.split(" ")[1].lstrip("<@").rstrip(">")))
        targ = target.name
    global emoteCursed
    global emoteCursechance
    global emoteCurses
    curseindex = emoteCursed.index(targ)
    emoteCursed.pop(curseindex)
    emoteCursechance.pop(curseindex)
    emoteCurses.pop(curseindex)
    await message.channel.send("Curse removed. Current Cursed People are:\n\n" + "\n".join(emoteCursed))


async def laundry(message):
    if not "goblin" in message.content.lower():
        roll = random.randint(1,19)
        if roll == 1:
            res = "Oh no! The mimic washer got a little hungry and decided to grab you instead! It might have been worth considering purchasing one of our presto scrolls instead, at a *discounted* price? But don't worry! Step-Goblin can get you out, right? Right?"
        elif roll < 11:
            res = "The mimic washer seems to have wanted to eat the clothes instead of clean them! Moblin Dry Cleaning apologizes for the inconvenience, and would be happy to offer you a totally legitimate (it isn't) coupon to the Widow's Boutique for their lost clothing!"
        elif roll < 20:
            res = "Oh what's that? Not only did the clothes come out amazing, but you also found some rather special article of clothing (1 Uncommon Clothing Item) stashed in load too! Lucky you! Wonder who that came from..."
        res = res.replace("you ", message.author.name + " ")
        await message.channel.send(embed = discord.Embed(title = "Washing Cycle Started!", description = random.choice(["Upon hearing the command word, the nearest mimic washer begins churning and stretching.", "A rumble of wet, sloshing sounds emanate from the nearest mimic.", "Water begins seeping onto the floor from the nearest washer, which slurps it back up."]) + "\n\nYou rolled a " + str(roll) + ".\n" + res, colour = embcol))