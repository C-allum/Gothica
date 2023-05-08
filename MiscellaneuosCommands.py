from CommonDefinitions import *
import random
import CommonDefinitions

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
