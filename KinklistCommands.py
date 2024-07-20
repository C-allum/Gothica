#import readline
import CommonDefinitions
from CommonDefinitions import *
import discord
from discord import app_commands
from discord.app_commands import Choice
from typing import List
from thefuzz import fuzz

kinkOptions = ["Fave", "Kink", "Like", "It depends", "Willing to try", "No Strong Emotions", "Never heard of it", "Not my thing", "Soft Limit", "Hard Limit"]
participationOptions = ["Submissive", "Dominant", "Voyeur", "Switch", "Submissive and Voyeur", "Dominant and Voyeur", "Enthusiast (Role doesn't matter to me)", "None"]
categoriesWithoutAverage = ['General Preferences', 'Categories', 'Body Parts', 'Relationships', 'Additional Kinks and Limits']

#Displays the kinklist of the author, or another user if they are tagged.
#NOTE: IF WE EVER APPEND NEW KINKS TO THE KINKLIST, DON'T ADD THEM AT THE END OF A CATEGORY! THAT BREAKS LIST LENGTHS
@tree.command(name = "kinklist", description = "Checks the kinks of a user")
@app_commands.describe(user = "The owner of the kinklist to be checked")
@app_commands.checks.has_role("Verified")
async def kinklist(interaction, user: str = None):
    await interaction.response.defer(ephemeral=True, thinking=False)
    await kinklistA(user, interaction.channel, "Command", interaction)
    await interaction.followup.send("Kinklist summoned!")

async def kinklistA(user, outputchannel, trigger, interaction):
    if trigger == "Command":
        targ = await getKinkTarget(user, interaction)
        categories, kinksPerCategory, categoryIndex = await getCategoryData()
    else:
        targ = user
        categories, kinksPerCategory, categoryIndex = await getCategoryData()

    try:
        GlobalVars.kinkdatabase.index([x for x in GlobalVars.kinkdatabase if str(targ.name) in x][0])
    except IndexError:
        if targ.bot:
            if "Gothica" in targ.name:
                await outputchannel.send(embed = discord.Embed(title = "You have attempted to check our kinks?", description = "Your mind is overwhelmed with possibilities you can scarcely comprehend. Take " + str(random.randint(8, 42)) + " psychic damage.\n\n" + str(random.choice(["You have a sudden craving for waffles.", "You passed out for a moment. We have cleared your internet search history for you.", "You have the sudden to search the Gallery of Sin for kobold porn", "You're a furry now.", "You are incapacitated for " + str(random.randint(1,4)*6) + " seconds.", "You appear to have been drooling uncontrollably."])), colour = embcol))
            elif "Avrae" in targ.name:
                await outputchannel.send(embed = discord.Embed(title = "From what we know of Avrae", description = "They're into sadism and torture. Ask Fish in the River about it, he knows.", colour = embcol))
            else:
                await outputchannel.send(embed = discord.Embed(title = "You may not view the kinklist of the server bots.", description = "If the bot you were checking was a tupper, try the tupper's author instead.", colour = embcol))
        else:
            await outputchannel.send(embed = discord.Embed(title = "Could not find " + targ.display_name + "'s kink list", description = "Make sure that <@" + str(targ.id) + "> has completed the kink survey.", colour = embcol))
        return
    
    try:
        playerindex = [row[1] for row in GlobalVars.kinkdatabase].index(targ.name)
    except ValueError:
        playerindex = [row[1] for row in GlobalVars.kinkdatabase].index(targ.name + "#" + targ.discriminator)
    generalPrefs = [] #Contains the general preferences
    categoryAverages = [] #Contains category ratings
    currentKinkIndex = kinksPerCategory[0] #Begin at the first actual kink after the Player Info

    #Fill the category averages array
    for x in range (len(categories)): #Go over all categories

        categoryName = categories[x]
        categoryKinkCount = kinksPerCategory[x]
        categorySum = 0
        for y in range(categoryKinkCount): #Go over each kink in a category

            try:
                try:
                    categorySum += len(kinkOptions) - int(kinkOptions.index(GlobalVars.kinkdatabase[playerindex][currentKinkIndex]))     #Invert scale so fave = 10 and hardlimit = 1
                except IndexError:
                    pass
            except ValueError:
                categorySum += 5
            currentKinkIndex += 1
        try:
            categoryAverages.append(kinkOptions[len(kinkOptions) - round(categorySum/categoryKinkCount)].replace("Fave", "**Fave**").replace("Kink", "**Kink**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__").replace("Never heard of it", "No Strong Emotions"))
        
        except ZeroDivisionError:
            categoryAverages.append(kinkOptions[5])
        
    #Fill in general preferences array
    currentKinkIndex = 3 #Begin at the Pronouns
    for f in range(kinksPerCategory[categories.index("General Preferences")+1]):
        currentRating = GlobalVars.kinkdatabase[playerindex][currentKinkIndex].replace("Fave", "**Fave**").replace("Kink", "**Kink**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__")
        generalPrefs.append(f"{GlobalVars.kinkdatabase[1][currentKinkIndex]}: {currentRating}")
        currentKinkIndex += 1

    #Prepare general preferences for printing
    generalPrefString = ""
    for entry in generalPrefs:
        generalPrefString +=f"\n{entry}"

    #Remove Categories that shouldn't have an average in category arrays
    printCategoriesWithAvg = categories.copy()  #PrintCategoriesWithAvg contains those categories that possess an average.
    for entry in categoriesWithoutAverage:
        try:
            categoryAverages.pop(printCategoriesWithAvg.index(entry))
            printCategoriesWithAvg.pop(printCategoriesWithAvg.index(entry))
        except IndexError:
            pass
        
    #Prepare the category array for printing, containing all categories that need to be listed. Needed later for the category selection
    printCategories = categories.copy() #PrintCategories contains !ALL! categories that need to be printed, average or not

    printCategories.remove("General Preferences")
    printCategories.remove("Categories")

    #This constructs the string containing the categories, the user rating for them, and the averages where they apply.
    categoryEmbedString = printCategories.copy()
    categoryAvgIndex = 0    #This is the index for the printCategoriesWithAvg and printCategoriesWithAvg arrays. printCategoriesWithAvg and printCategoriesWithAvg are shorter than categoryEmbedString, hence it needs a different index
    try:
        for entryIndex in range(0, len(categoryEmbedString)):
            if categoryEmbedString[entryIndex] in printCategoriesWithAvg:
                tmp = categories.index("Categories")
                categoryEmbedString[entryIndex] = f"`{entryIndex + 1}`: {categoryEmbedString[entryIndex]} - " + GlobalVars.kinkdatabase[playerindex][categoryIndex[tmp] + categoryAvgIndex].replace("Fave", "**Fave**").replace("Kink", "**Kink**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__")  + f" ({categoryAverages[categoryAvgIndex]})"
                categoryAvgIndex += 1
            else:
                categoryEmbedString[entryIndex] = f"`{entryIndex + 1}`: {categoryEmbedString[entryIndex]}"
    except IndexError:
        pass

    #Send the embed. Discern between the sources of the request. If requested by command, send the embed to the channel where the command was called and only send the general preferences first with a selector.
    
    if trigger == "Command":

        kinkemb = discord.Embed(title = targ.display_name + "'s kink list:", description = "**General Preferences:**" +\
            generalPrefString +\
            "\n\n**Kink Overview:**\n" +\
            targ.name + "/ " + targ.display_name +\
            "'s general thoughts on each category of kink are shown below. We have then taken their average response in each category, and included that information in brackets.\n*As always, you should check with your rp partners regarding hard and soft limits for any particular scene.*\n\n*To see more detail on any of the below categories, type the corresponding number*\n\n" +\
            "\n".join(categoryEmbedString), colour = embcol).set_footer(text = f"-------------------------------------------------------------\n\nThis search was summoned by {interaction.user.name} / {interaction.user.display_name}")

        catAnswDrop = CommonDefinitions.Dropdown_Select_View(interaction = interaction, namelist = categoryEmbedString)
        msg = await interaction.channel.send(embed = kinkemb, view = catAnswDrop)

        if await catAnswDrop.wait():
            await interaction.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        sel = int(catAnswDrop.button_response[0])
        await msg.delete()
        foot = f"-------------------------------------------------------------\n\nThis search was summoned by {interaction.user.name} / {interaction.user.display_name}"
        try:
            #If the user answered with a number, display the subcategory of the kinksheet.
            await Kinklistdetail(categoryIndex, categories, printCategories, sel, playerindex, printCategoriesWithAvg, categoryAverages, tmp, targ.name, outputchannel, foot)
        except UnboundLocalError:
            return

    #If the kinklist was summoned by react, we want to send all categories to their DMs
    else:

        kinkemb = discord.Embed(title = targ.name + "'s kink list:", description = "**General Preferences:**" +\
            generalPrefString +\
            "\n\n**Kink Overview:**\n" +\
            targ.name + "/ " + targ.display_name +\
            "'s general thoughts on each category of kink are shown below. We have then taken their average response in each category, and included that information in brackets.\n*As always, you should check with your rp partners regarding hard and soft limits for any particular scene.*\n\n" +\
            "\n".join(categoryEmbedString), colour = embcol)

        await outputchannel.send(embed = kinkemb)

        for cat in range(len(categories)):
            await Kinklistdetail(categoryIndex, categories, printCategories, int(cat)+1, playerindex, printCategoriesWithAvg, categoryAverages, tmp, targ.name, outputchannel, "")

#Allows to edit the kinklist. Moderators can tag someone and edit someone elses kinks.
@tree.command(name = "kinkedit", description = "Edits one of your kinks")
@app_commands.describe(kink = "The kink to edit. Leave this blank to choose by category.")
@app_commands.describe(user = "The owner of the kinklist to modify (staff only)")
@app_commands.checks.has_role("Verified")
async def kinkedit(interaction, kink: str = None, user: str = None):
    await interaction.response.defer(ephemeral=True, thinking=False)

    targ = interaction.user
    if user != None:
        if not "Staff" in str(interaction.user.roles):
            await interaction.channel.send(embed = discord.Embed(title = "You can't do that", description = "Only Staff members can edit the kinks of another player. Editing your kink instead.", colour = embcol))
        else:
            targ = await getKinkTarget(user, interaction)
    try:
        index = GlobalVars.kinkdatabase.index([x for x in GlobalVars.kinkdatabase if str(targ.name) in x][0])
    except IndexError:
        await interaction.channel.send(embed = discord.Embed(title = "Could not find " + targ.name + "'s kink list", description = "Make sure that <@" + str(targ.id) + "> has completed the kink survey."))
        return    
    kinktoedit, kinkindex = await selkink(kink, interaction)

    if "role" in GlobalVars.kinkdatabase[1][kinkindex]:
        kinkOpts = participationOptions
    elif GlobalVars.kinkdatabase[1][kinkindex] == "Pronouns" or GlobalVars.kinkdatabase[1][kinkindex] == "Additional Kinks" or GlobalVars.kinkdatabase[1][kinkindex] == "Additional Limits":
        kinkOpts = None
    else:
        kinkOpts = kinkOptions
    embedstring = f"{interaction.user.name}, you currently have {kinktoedit} as: {GlobalVars.kinkdatabase[index][kinkindex]}. What would you like to change this to?\n\n"
    try:
        for z in range(0, len(kinkOpts)): #Add the answer options to the embed
            embedstring = embedstring + f"`{z+1}`: {kinkOpts[z]}\n"
    except TypeError:
        pass
    embedstring = embedstring + "\n\nThis message will timeout in 30 seconds."
    if kinkOpts == None: #Get text input
        await interaction.channel.send(embed = discord.Embed(title = "Editing " + kinktoedit, description = embedstring, colour = embcol))
        try:
            msg = await client.wait_for('message', timeout = 30, check = checkAuthor(interaction.user))
            newdata = msg.content
        except asyncio.TimeoutError:
            await interaction.channel.send("Message timed out")
            return
    else:
        kinkAnswDrop = CommonDefinitions.Dropdown_Select_View(interaction = interaction, namelist = kinkOpts)
        await interaction.channel.send(embed = discord.Embed(title = "Editing " + kinktoedit, description = embedstring, colour = embcol), view = kinkAnswDrop)
        if await kinkAnswDrop.wait():
            await interaction.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        
        i = int(kinkAnswDrop.button_response[0]) - 1
        if i >= 0 and i < len(kinkOpts):
            newdata = kinkOpts[i]
        else: 
            await interaction.channel.send(embed=discord.Embed(title=f"Number has to be between 1 and {len(kinkOpts)}", colour = embcol))
            return
        
    GlobalVars.kinkdatabase[index][kinkindex] = newdata
    gc.open_by_key(kinksheet).sheet1.update_cell(index+1, kinkindex+1, str(newdata))
    await interaction.channel.send(embed = discord.Embed(title = "Your changes have been made!", colour = embcol))
    await interaction.followup.send("Kinklist updated")

#Takes a kink as a second input and outputs people who like that kink.
@tree.command(name = "kinkplayers", description = "Displays the list of people with a certain kink. Use in #looking-for-new-roleplay to ping instead.")
@app_commands.describe(kink = "The kink to view. Leave this blank to choose by category.")
@app_commands.checks.has_role("Verified")
async def kinkplayers(interaction, kink: str = None):
    await interaction.response.defer(ephemeral=True, thinking=False)
    kinksel, kinkindex = await selkink(kink, interaction)

    if interaction.channel.id != 1009522511844749342:
        charlimit = 4096
    else:
        charlimit = 2000

    haskink = "The people with " + str(kinksel) + " listed as a kink are:\n"
    hasfave = "Additonally, those with this listed as a favourite are:\n"
    haslike = "Finally, the people with " + str(kinksel) + " listed as something they like are:\n"
    kinkmsgs = []
    favemsgs = []
    likemsgs = []
    for a in range(len(GlobalVars.kinkdatabase)):
        if GlobalVars.kinkdatabase[a][kinkindex] == "Kink":
            if len(str(haskink + "<@" + GlobalVars.kinkdatabase[a][2] + ">, ")) > charlimit:
                kinkmsgs.append(haskink)
                haskink = ""
            haskink += "<@" + GlobalVars.kinkdatabase[a][2] + ">, "
        elif GlobalVars.kinkdatabase[a][kinkindex] == "Fave":
            if len(str(hasfave + "<@" + GlobalVars.kinkdatabase[a][2] + ">, ")) > charlimit:
                favemsgs.append(hasfave)
                hasfave = ""
            hasfave += "<@" + GlobalVars.kinkdatabase[a][2] + ">, "
        elif GlobalVars.kinkdatabase[a][kinkindex] == "Like":
            if len(str(haslike + "<@" + GlobalVars.kinkdatabase[a][2] + ">, ")) > charlimit:
                likemsgs.append(haslike)
                haslike = ""
            haslike += "<@" + GlobalVars.kinkdatabase[a][2] + ">, "
    kinkmsgs.append(haskink)
    favemsgs.append(hasfave)
    likemsgs.append(haslike)

    for b in range(len(kinkmsgs)):
        if interaction.channel.id != 1009522511844749342:
            await interaction.channel.send(embed = discord.Embed(title = "People with " + kinksel + " as a kink:", description = kinkmsgs[b], colour = embcol).set_author(name = interaction.user.name + "/ " + interaction.user.display_name))
        else:
            await interaction.channel.send(kinkmsgs[b])
    for b in range(len(favemsgs)):
        if interaction.channel.id != 1009522511844749342:
            await interaction.channel.send(embed = discord.Embed(title = "People with " + kinksel + " as a favourite:", description = favemsgs[b], colour = embcol).set_author(name = interaction.user.name + "/ " + interaction.user.display_name))
        else:
            await interaction.channel.send(favemsgs[b])
    for b in range(len(likemsgs)):
        if interaction.channel.id != 1009522511844749342:
            await interaction.channel.send(embed = discord.Embed(title = "People with " + kinksel + " as something they like:", description = likemsgs[b], colour = embcol).set_author(name = interaction.user.name + "/ " + interaction.user.display_name))
        else:
            await interaction.channel.send(likemsgs[b])
    if interaction.channel.id != 1009522511844749342:
        await interaction.channel.send("This search was summoned by " + interaction.user.name + "/ " + interaction.user.display_name)

    await interaction.followup.send("Command complete.")

#Finds a room and an encounter for the specified person.
async def kinkencounter(message):
    if ("staff" in str(message.author.roles).lower() or message.author.name == "C_allum"):
        kinkdata, namestr, targname = await getKinkData(message)

        if not str(namestr) in str(kinkdata):

            await message.channel.send(embed = discord.Embed(title = "Could not find " + namestr.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the kink survey."))

        else:


            try:

                if "@" in message.content:

                    room = message.content.lower().split(" ", 2)[2]

                else:

                    room = message.content.lower().split(" ", 1)[1]

            except IndexError:

                room = "Room not found"

            encounters = sheet.values().get(spreadsheetId = encountersheet, range = "A1:R50", majorDimension='COLUMNS').execute().get("values")

            rooms = ["General Encounters", "Trapped Corridors", "Moaning Hallways", "Unlicensed Fights", "Sparring Pit", "Kobold Dens", "Wild Gardens", "Twilight Groves", "Sirens Grotto"]

            if not room.lower() in str(rooms).lower():

                room = "Room not found"

            else:

                for c in range(len(rooms)):

                    if room in rooms[c].lower():

                        colsel = 2 * c

                        rowsel = random.randint(1,len(encounters[2 * c]) - 1)

                        room = rooms[c]

                        break
                    
            #Check Kinks

            if room != "Room not found":

                try:

                    kinkneeded = encounters[colsel+1][rowsel]

                except IndexError:

                    kinkneeded = None

                if kinkneeded == "":

                    kinkneeded = None

                kinkinfo = "\n\nNo kinks are needed for this encounter"

                if kinkneeded != None:
                    playerIndex = [row[1] for row in kinkdata].index(namestr)

                    kinksreq = kinkneeded.split(", ")

                    kinkthoughts = []

                    for d in range(len(kinkdata[1])):

                        for e in range(len(kinksreq)):

                            if kinkdata[1][d] == kinksreq[e]:

                                kinkthoughts.append(kinkdata[1][d] + ": " + kinkdata[playerIndex][d])

                    kinkinfo = "\n\n" + str(targname) + "'s kinks for this encounter:\n\n" + "\n".join(kinkthoughts)

                encounter = encounters[colsel][rowsel].replace("{random race}", random.choice(["dragonborn", "dwarf", "elf", "gnome", "half-elf", "halfling", "half-orc", "human", "tiefling", "leonin", "satyr", "owlin", "aarakocra", "aasimar", "air genasi", "bugbear", "centaur", "changeling", "deep gnome", "duergar", "earth genasi", "eladrin", "fairy", "firbolg", "fire genasi", "githyanki", "githzerai", "goblin", "goliath", "harengon", "hobgoblin", "kenku", "kobold", "lizardfolk", "minotaur", "orc", "sea elf", "shadar-kai", "shifter", "tabaxi", "tortle", "triton", "water genasi", "yuan-ti", "kalashtar", "warforged", "astral elf", "autognome", "giff", "hadozee", "plasmoid", "loxodon", "simic hybrid", "vedalken", "verdan", "locathah", "grung", "babbage", "seedling", "chakara"])).replace("dwarfs", "dwarves").replace("elfs", "elves").replace("fairys", "fairies").replace("githyankis", "githyanki").replace("githzerais", "githzerai").replace("lizardfolks", "lizardfolk").replace("shadar-kais", "shadar-kai").replace("yuan-tis", "yuant-ti").replace("locathahs", "locathah").replace("grungs", "grung").replace("{1d4}", str(random.randint(1,4))).replace("{1d6}", str(random.randint(1,6))).replace("{1d8}", str(random.randint(1,8))).replace("{1d10}", str(random.randint(1,10))).replace("{1d12}", str(random.randint(1,12))).replace("{1d20}", str(random.randint(1,20))).replace("{2d4}", str(random.randint(2,8))).replace("{2d6}", str(random.randint(2,12))).replace("{3d4}", str(random.randint(3,12)))

                await message.channel.send(embed = discord.Embed(title = "Random Encounter for " + str(targname) + " in " + room, description = encounter + kinkinfo, colour = embcol))

            else:

                await message.channel.send("Room not found")

#Assist the author in generating their kinklist if they don't already have one.
@tree.command(name = "kinksurvey", description = "Runs a survey to establish what your kinks and limits are.")
@app_commands.checks.has_role("Verified")
async def kinksurvey(interaction):
    await interaction.response.defer(ephemeral=True, thinking=False)
    targ = await getKinkTarget("<@" + str(interaction.user.id) + ">", interaction)
    if interaction.channel.id != int(kinkcreatechannel):
        await interaction.channel.send(embed = discord.Embed(title = "This is not the place to talk about that.", description = f"We will gladly talk about your deepest desires, <@{targ.id}>. We prefer a bit of privacy for that however. Please use the <#{kinkcreatechannel}> channel to call this command.", colour = embcol))
        return
    
    #See if the user wants to retake the survey
    if any(targ.name in x for x in GlobalVars.kinkdatabase):
        retake, n = await CommonDefinitions.quicksel(interaction=interaction, options=["Yes", "No"], title = "We already know your deepest desires", description = f"Your kinklist is already registered with us, <@{targ.id}>.\n If you want to edit it a single kink, use %kinkedit.")
        if retake == None or retake == "No":
            return
        else:
            playerindex = GlobalVars.kinkdatabase.index([x for x in GlobalVars.kinkdatabase if str(targ.name) in x][0])
    else:
        playerindex = 0

    threadid = await interaction.channel.create_thread(name= "Kinklist Survey: " + targ.name)   
    await threadid.send(interaction.user.mention, embed = discord.Embed(title = "Kink Survey", description = f"Welcome to the kink survey! We will ask you to give us a rating on all sorts of kinks in just a moment. We will go through a couple of categories with plenty of kinks, and when we are done you can look at your kinklist with the /kinklist command, or edit it with the /kinkedit command. Furthermore you can search for users with a certain kink using the /kinkplayers [kink] command, or look at someone else's list with /kinklist [@username]. \n\n **Please note that we go to sleep around <t:1670025600:T> on the night from Tuesday to Wednesday every week. If you don't finish before that, your progress will be lost!** \n\n**Questions will timeout after 10 minutes. If one of the dropdown options doesn't respond or shows an error, try it again. ~~If the survey times out, you will be able to resume it with the /kinkresume command.~~** \n\n Okay, with the formalities out of the way, let us begin...", colour=embcol))

    #--------------Prepare variables---------------
    newKinklist = [str(datetime.now()), f"{targ.name}", f"{targ.id}"] #Contains kink data, will be written into the sheet.
    
    categories, kinksPerCategory, categoryIndex = await getCategoryData()

    #--------------Collect information from the user-------------
    #Request user's pronouns.
    try:
        await threadid.send(embed = discord.Embed(title = "Pronouns", description = "First of all: What are your preferred pronouns?", colour = embcol))
        messagefound = False
        while messagefound == False:
            msg = await client.wait_for('message',  check = checkAuthor(interaction.user))
            if msg.channel == threadid:
                messagefound = True
        newKinklist.append(msg.content)
    except asyncio.TimeoutError:
        await threadid.send("Message timed out")
        kinksel = "Fail"
        return

    except ValueError:
        await threadid.send("Something went wrong! ValueError.")
        kinksel = "Fail"
        await msg.delete()
        return
    
    await threadid.send(embed = discord.Embed(title = "Pronouns", description = f"Pronouns set as: {msg.content}", colour = embcol))
    
    #Now ask for the remaining things.
    kinkindex = kinksPerCategory[0] #Start at the first kink, not the player info.
    for x in range(len(categories)+1): #Go over all categories
        if x > 0:
            categoryName = categories[x-1]
            categoryKinkCount = kinksPerCategory[x]
            if categoryName == "Categories": #Check if this is the part of the survey about the categories. Need to list the involved kinks for those.
                categorySection = True
            else:
                categorySection = False

            for y in range(categoryKinkCount): #Go over each kink in a category
                kinkname = GlobalVars.kinkdatabase[1][kinkindex]

                #Ask the player about the kink
                if not "Role" in kinkname and not "Additional" in kinkname:   #Everything but the "If you are Role" questions
                    if (categorySection == False):  #Every category but "Categories"
                        embedstring = f"What are your feelings about {kinkname}?"                   
                        pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                    else:   #"Categories" category needs to list kinks in the message so users understand what is part of the category
                        categoryID = categories.index(categoryName)  #Find the index of the category we are asking about to get the amount of kinks in that category.
                        embedstring = f"What are your feelings about {categoryName}? \nThis includes things such as:\n"

                        for z in range(1, kinksPerCategory[categoryID]):    #Add the kinks of the category to the list in the embed.
                            embedstring = embedstring + f"- {GlobalVars.kinkdatabase[1][categoryIndex[categoryID] + z]}\n"

                        embedstring = embedstring + "You will be able to rate each kink individually later.\n\n"

                        for z in range(0, len(kinkOptions)):#Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                    
                        embedstring = f"What are your feelings about {kinkname}?"                   
                        pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                elif "Role" in kinkname:

                    splitName = kinkname.rsplit(" ", 1)[0]
                    embedstring = f"{interaction.user.name}, what is your preferred role in {splitName}?"                   
                    pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = participationOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                elif "Additional" in kinkname: #Additional kinks/limits section
                    try:
                        
                        await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}): \nQuestion {y+1}/{categoryKinkCount}: {kinkname}", description = f"Do you have any {kinkname} you want to add? List them here! If there aren't any, put \"none\".", colour = embcol))
                        messagefound = False
                        while messagefound == False:
                            msg2 = await client.wait_for('message',  check = checkAuthor(interaction.user))
                            if msg2.channel == threadid:
                                messagefound = True
                        pref = str(msg2.content)
                        if pref == "":
                            pref = "none"
                    except asyncio.TimeoutError:
                    
                        await threadid.channel.send("Message timed out")
                        kinksel = "Fail"
                        return

                    except ValueError:
                    
                        await threadid.channel.send("Something went wrong! ValueError.")
                        kinksel = "Fail"

                        try:
                            await msg2.delete()
                        except discord.errors.DiscordServerError:
                            await threadid.send(embed = discord.Embed(title = "Oops...", description = f"We experienced an internal error with the eldritch spaghetti monster called discord-api... Trying to continue. If we stop responding, please restart the survey.", colour = embcol))
                        return

                await threadid.send(embed = discord.Embed(description = f"Registered {kinkname} as {pref}.", colour = embcol))
                newKinklist.append(pref)

                #Increment kinkindex
                kinkindex += 1

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "That concludes the kink survey! Thank you for your time. If you change your mind on anything I just asked you about, you can request us to change it with /kinkedit.", colour = embcol))

    kinkws = gc.open_by_key(kinksheet).get_worksheet(0)
    if playerindex == 0:
        kinkws.append_row(values = newKinklist)
    else:
        krange = "A" + str(playerindex+1) + ":GZ" + str(playerindex+1)
        kinkws.update(krange, [newKinklist])
    GlobalVars.kinkdatabase = gc.open_by_key(kinksheet).sheet1.get_all_values()
    await interaction.followup.send("Survey complete.")
    return

@tree.command(name = "kinkresume", description = "Resumes a kink survey by reading the contents of the thread it is run in.")
@app_commands.checks.has_role("Verified")
async def kinkresume(interaction):
    await interaction.response.defer(ephemeral=True, thinking=False)
    targ = await getKinkTarget("<@" + str(interaction.user.id) + ">", interaction)
    
    #See if the user has already completed the survey
    if any(targ.name in x for x in GlobalVars.kinkdatabase):
        await interaction.channel.send(embed = discord.Embed(title = "We know your deepest secrets...", description= "We already have an entry for your kinklist. If you are looking to retake the survey, use /kinksurvey. Otherwise, if you are looking to fill any gaps in your survey, use /kinkfill. Finally, if you are just looking to edit a kink, use /kinkedit.", colour = embcol))
        return
    if not interaction.channel.name.startswith("Kinklist Survey:"):
        await interaction.channel.send(embed = discord.Embed(title = "This isn't the place for this!", description= "This command should be run in the incomplete thread of a /kinksurvey command.", colour = embcol))
  
    #--------------Prepare variables---------------
    newKinklist = [str(datetime.now()), f"{targ.name}", f"{targ.id}"] #Contains kink data, will be written into the sheet.
    
    categories, kinksPerCategory, categoryIndex = await getCategoryData()

    mess = [joinedMessages async for joinedMessages in interaction.channel.history(limit = None, oldest_first= True)]
    kinktitle = []
    oldpref = []
    for a in range(len(mess)):
        try:
            if (mess[a].embeds[0].description.startswith("Registered ") or mess[a].embeds[0].description.startswith("Pronouns ")) and mess[a].author == client.user:
                kinktitle.append(mess[a].embeds[0].description.replace(" as:", " as").split(" as ")[0].split(" ", 1)[1])
                oldpref.append(mess[a].embeds[0].description.replace(" as:", " as").split(" as ")[1].rstrip("."))
        except IndexError:
            pass
    
    #--------------Collect information from the user-------------
    #Request user's pronouns.
    try:
        newKinklist.append(oldpref[kinktitle.index("set")])
    except ValueError:
        try:
            await interaction.channel.send(embed = discord.Embed(title = "Pronouns", description = "First of all: What are your preferred pronouns?", colour = embcol))
            messagefound = False
            while messagefound == False:
                msg = await client.wait_for('message',  check = checkAuthor(interaction.user))
                if msg.channel == interaction.channel:
                    messagefound = True
            newKinklist.append(msg.content)
        except asyncio.TimeoutError:
            await interaction.channel.send("Message timed out")
            kinksel = "Fail"
            return

        except ValueError:
            await interaction.channel.send("Something went wrong! ValueError.")
            kinksel = "Fail"
            await msg.delete()
            return
        
        await interaction.channel.send(embed = discord.Embed(title = "Pronouns", description = f"Pronouns set as: {msg.content}", colour = embcol))
    
    #Now ask for the remaining things.
    kinkindex = kinksPerCategory[0] #Start at the first kink, not the player info.
    for x in range(len(categories)+1): #Go over all categories
        if x > 0:
            categoryName = categories[x-1]
            categoryKinkCount = kinksPerCategory[x]
            if categoryName == "Categories": #Check if this is the part of the survey about the categories. Need to list the involved kinks for those.
                categorySection = True
            else:
                categorySection = False

            for y in range(categoryKinkCount): #Go over each kink in a category
                kinkname = GlobalVars.kinkdatabase[1][kinkindex]

                try:
                    newKinklist.append(oldpref[kinktitle.index(kinkname)])
                except ValueError:

                    #Ask the player about the kink
                    if not "Role" in kinkname and not "Additional" in kinkname:   #Everything but the "If you are Role" questions
                        if (categorySection == False):  #Every category but "Categories"
                            embedstring = f"What are your feelings about {kinkname}?"                   
                            pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = interaction.channel)

                        else:   #"Categories" category needs to list kinks in the message so users understand what is part of the category
                            categoryID = categories.index(categoryName)  #Find the index of the category we are asking about to get the amount of kinks in that category.
                            embedstring = f"What are your feelings about {categoryName}? \nThis includes things such as:\n"

                            for z in range(1, kinksPerCategory[categoryID]):    #Add the kinks of the category to the list in the embed.
                                embedstring = embedstring + f"- {GlobalVars.kinkdatabase[1][categoryIndex[categoryID] + z]}\n"

                            embedstring = embedstring + "You will be able to rate each kink individually later.\n\n"

                            for z in range(0, len(kinkOptions)):#Add the answer options to the embed
                                embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                        
                            embedstring = f"What are your feelings about {kinkname}?"                   
                            pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = interaction.channel)

                    elif "Role" in kinkname:

                        splitName = kinkname.rsplit(" ", 1)[0]
                        embedstring = f"{interaction.user.name}, what is your preferred role in {splitName}?"                   
                        pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = participationOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = interaction.channel)

                    elif "Additional" in kinkname: #Additional kinks/limits section
                        try:
                            
                            await interaction.channel.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}): \nQuestion {y+1}/{categoryKinkCount}: {kinkname}", description = f"Do you have any {kinkname} you want to add? List them here! If there aren't any, put \"none\".", colour = embcol))
                            messagefound = False
                            while messagefound == False:
                                msg2 = await client.wait_for('message',  check = checkAuthor(interaction.user))
                                if msg2.channel == interaction.channel:
                                    messagefound = True
                            pref = str(msg2.content)
                            if pref == "":
                                pref = "none"
                        except asyncio.TimeoutError:
                        
                            await interaction.channel.send("Message timed out")
                            kinksel = "Fail"
                            return

                        except ValueError:
                        
                            await interaction.channel.send("Something went wrong! ValueError.")
                            kinksel = "Fail"

                            try:
                                await msg2.delete()
                            except discord.errors.DiscordServerError:
                                await interaction.send(embed = discord.Embed(title = "Oops...", description = f"We experienced an internal error with the eldritch spaghetti monster called discord-api... Trying to continue. If we stop responding, please restart the survey.", colour = embcol))
                            return

                    await interaction.channel.send(embed = discord.Embed(description = f"Registered {kinkname} as {pref}.", colour = embcol))
                    newKinklist.append(pref)

                #Increment kinkindex
                kinkindex += 1

    await interaction.channel.send(embed = discord.Embed(title = "Kink Survey", description = "That concludes the kink survey! Thank you for your time. If you change your mind on anything I just asked you about, you can request us to change it with /kinkedit.", colour = embcol))

    kinkws = gc.open_by_key(kinksheet).get_worksheet(0)
    kinkws.append_row(values = newKinklist)
    GlobalVars.kinkdatabase = gc.open_by_key(kinksheet).sheet1.get_all_values()
    await interaction.followup.send("Survey complete.")
    return

#Compares the kinklist of tagged persons
@tree.command(name = "kinkcompare", description = "Compares the kinks and limits of tagged users")
@app_commands.describe(players = "The players to compare. Tag them using @name and leave a space between each.")
@app_commands.checks.has_role("Verified")
async def kinkcompare(interaction, players: str):

    await interaction.response.defer(ephemeral=True, thinking=False)
    await comparekinks(players, interaction.channel, interaction.user.name + "/ " + interaction.user.display_name)
    await interaction.followup.send("Command complete.")

async def comparekinks(players, destinationchannel, user):

    #Fetch relevant data
    categories, kinksPerCategory, categoryIndex = await getCategoryData()
    playerIDsToCompare = [] #Contains the ID of the players whose kinklist should be compared
    commonKinks = []        #Contains common Like/Kink/Faves
    limits = []             #Contains common Limits
    maybeAvoid = []         #Contains kinks that should maybe be avoided
    KinkIDCol = gc.open_by_key(kinksheet).worksheet("Form Responses").col_values(3)
    playerIndices = []  #Contains player row indices in kinkdata
    playerNames = []    #Contains player names
    localGuild = client.get_guild(828411760365142076)

    if not "@" in players or not " " in players:
        await destinationchannel.send(embed = discord.Embed(title = "Kinklist Compare", description = f"Please tag everyone whose kinklist you want to compare, even yourself if you want to compare yours to someone elses!", colour = embcol))
        return
    else:   #If people were tagged, fetch the ID's of the players that need to be compared
        for a in range(len(players.split(" "))):
            playerIDsToCompare.append(int(players.split(" ")[a][2:-1]))
            try:
                playerIndices.append(KinkIDCol.index(str(playerIDsToCompare[a])))
                if localGuild != None:
                    currMember = localGuild.get_member(int(playerIDsToCompare[a]))
                else: 
                    currMember = client.get_guild(847968618167795782).get_member(int(playerIDsToCompare[a]))
                playerNames.append(currMember.name + "/" + currMember.display_name)
            except ValueError:
                await destinationchannel.send(embed = discord.Embed(title = "Could not find <@" + str(playerIDsToCompare[a]) + "> 's kink list", description = "Make sure that <@" + str(playerIDsToCompare[a]) + "> has completed the kink survey. Try again when they have.", colour = embcol))
                return

    #begin comparing... Mark out all common kinks that are at least a like, and every single soft or hard limit. Extra list for "Not my thing"
    for i in range(categoryIndex[categories.index("Body Parts")], len(GlobalVars.kinkdatabase[1])):
        likeOrMoreForAll = True #Stays true if this is a like or better for all people tagged
        softOrHardLimit = False
        uncertainElement = False
        for playern in playerIndices:
            if GlobalVars.kinkdatabase[playern][i] != kinkOptions[0] and GlobalVars.kinkdatabase[playern][i] != kinkOptions[1] and GlobalVars.kinkdatabase[playern][i] != kinkOptions[2]: #If entry is not Fave, Kink or Like, it is not among the common kinks
                likeOrMoreForAll = False

            if GlobalVars.kinkdatabase[playern][i] == kinkOptions[8] or GlobalVars.kinkdatabase[playern][i] == kinkOptions[9]:
                softOrHardLimit = True

            if GlobalVars.kinkdatabase[playern][i] == kinkOptions[7] or GlobalVars.kinkdatabase[playern][i] == kinkOptions[6]:
                uncertainElement = True

        #add the kink to the correct category
        if likeOrMoreForAll == True:
            commonKinks.append(GlobalVars.kinkdatabase[1][i])
        if softOrHardLimit == True:
            limits.append(GlobalVars.kinkdatabase[1][i])
        if uncertainElement == True:
            maybeAvoid.append(GlobalVars.kinkdatabase[1][i])
    
    #Send embeds
    output = []
    output.append(await destinationchannel.send(embed = discord.Embed(title = f"Common Faves/Kinks/Likes of " + ", ".join(playerNames), description = "\n".join(commonKinks), colour = embcol)))
    #await message.channel.send(embed = discord.Embed(title = f"Uncertain Elements shared by " + ", ".join(playerNames), description = "\n".join(maybeAvoid), colour = embcol))
    output.append(await destinationchannel.send(embed = discord.Embed(title = f"Accumulated Soft and Hard Limits of  " + ", ".join(playerNames), description = "\n".join(limits), colour = embcol).set_footer(text = f"-------------------------------------------------------------\n\nThis comparison was summoned by " + user)))
    output.append(await destinationchannel.send(embed = discord.Embed(title = f"Reminder!", description = "*Please remember that the kinklist is not a perfect guide. Just because someone has marked something positively or negatively, doesn't mean they have the same understanding of what that thing is as you do. It's important to discuss any element you plan to bring into a scene with your partner.*", colour = embcol)))
    return output

#Posts an embed with help on the commands.
async def kinkhelp(message):
    await message.channel.send(embed = discord.Embed(title = "Kinklist Help", description = f"*This is the %kinkhelp command! To start the kinklist survey, use the %kinksurvey command.\n If you have already filled out the survey, you can look at your kinklist with the %kinklist command, or edit it with the %kinkedit command. Furthermore you can search for users with a certain kink using the %kinkplayers [kink] command, or look at someone else's list with %kinklist [@username]. You can also compare kinklists of two or more people with the %kinkcompare [@username1] [@username2] [@username3 (OPTIONAL] command. You can compare 2 or more peoples kinklist with that to navigate scenes easier. Finally, the %lfg [hours of access] allows you access to the lfg channel for as many hours as you specify. There you can use %kinkplayers [kink] in a different way! We will not only tell you who likes the specified kink, but also tag the people that are also present in the channel, so you have an easier time looking for roleplays with a certain kink.*").set_footer(text = f"-------------------------------------------------------------\n\nThis search was summoned by {message.author.name} / {message.author.display_name}"))
    await message.delete()

@tree.command(name = "kinkfill", description = "Fills in any gaps in your kinksurvey.")
@app_commands.checks.has_role("Verified")
async def kinkfill(interaction):
    await interaction.response.defer(ephemeral=True, thinking=False)
    targ = await getKinkTarget("<@" + str(interaction.user.id) + ">", interaction)
    if interaction.channel.id != int(kinkcreatechannel):
        await interaction.channel.send(embed = discord.Embed(title = "This is not the place to talk about that.", description = f"We will gladly talk about your deepest desires, <@{targ.id}>. We prefer a bit of privacy for that however. Please use the <#{kinkcreatechannel}> channel to call this command.", colour = embcol))
        return
    
    try:
        playerindex = GlobalVars.kinkdatabase.index([x for x in GlobalVars.kinkdatabase if str(targ.name) in x][0])
    except IndexError:
        await interaction.channel.send(embed = discord.Embed(title = "We could not find you in the database.", description = "This command is for filling gaps in your kinklist, such as if kinks were added since you took it.\nUse /kinksurvey, rather than kinkfill.\n\nIf you have done so already, contact the bot gods.", colour = embcol))

    threadid = await interaction.channel.create_thread(name= "Kinklist Filling: " + targ.name)   
    await threadid.send(interaction.user.mention, embed = discord.Embed(title = "Kink Filling", description = f"Welcome back to the kink survey! We will ask you to give us a rating on all the kinks missing from your data. We will go through a couple of categories with plenty of kinks, and when we are done you can look at your kinklist with the /kinklist command, or edit it with the /kinkedit command. Furthermore you can search for users with a certain kink using the /kinkplayers [kink] command, or look at someone else's list with /kinklist [@username]. \n\n **Please note that we go to sleep around <t:1670025600:T> on the night from Tuesday to Wednesday every week. If you don't finish before that, your progress will be lost!** \n\n**Questions will timeout after 10 minutes. If one of the dropdown options doesn't respond or shows an error, try it again.** \n\n Okay, with the formalities out of the way, let us begin...", colour=embcol))

    #--------------Prepare variables---------------
    newKinklist = [str(datetime.now()), f"{targ.name}", f"{targ.id}"] #Contains kink data, will be written into the sheet.
    
    categories, kinksPerCategory, categoryIndex = await getCategoryData()

    #--------------Collect information from the user-------------
    #Request user's pronouns.
    if GlobalVars.kinkdatabase[playerindex][kinksPerCategory[0]-1] != "":
        newKinklist.append(GlobalVars.kinkdatabase[playerindex][kinksPerCategory[0]-1])
    else:
        try:
            await threadid.send(embed = discord.Embed(title = "Pronouns", description = "First of all: What are your preferred pronouns?", colour = embcol))
            messagefound = False
            while messagefound == False:
                msg = await client.wait_for('message',  check = checkAuthor(interaction.user))
                if msg.channel == threadid:
                    messagefound = True
            newKinklist.append(msg.content)
        except asyncio.TimeoutError:
            await threadid.channel.send("Message timed out")
            kinksel = "Fail"
            return

        except ValueError:
            await threadid.channel.send("Something went wrong! ValueError.")
            kinksel = "Fail"
            await msg.delete()
            return
        
        await threadid.send(embed = discord.Embed(title = "Pronouns", description = f"Pronouns set as: {msg.content}", colour = embcol))
    
    #Now ask for the remaining things.
    kinkindex = kinksPerCategory[0] #Start at the first kink, not the player info.
    for x in range(len(categories)+1): #Go over all categories
        if x > 0:
            categoryName = categories[x-1]
            categoryKinkCount = kinksPerCategory[x]
            if categoryName == "Categories": #Check if this is the part of the survey about the categories. Need to list the involved kinks for those.
                categorySection = True
            else:
                categorySection = False

            for y in range(categoryKinkCount): #Go over each kink in a category
                kinkname = GlobalVars.kinkdatabase[1][kinkindex]

                if GlobalVars.kinkdatabase[playerindex][kinkindex] != "":
                    newKinklist.append(GlobalVars.kinkdatabase[playerindex][kinkindex])
                else:

                    #Ask the player about the kink
                    if not "Role" in kinkname and not "Additional" in kinkname:   #Everything but the "If you are Role" questions
                        if (categorySection == False):  #Every category but "Categories"
                            embedstring = f"What are your feelings about {kinkname}?"                   
                            pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                        else:   #"Categories" category needs to list kinks in the message so users understand what is part of the category
                            categoryID = categories.index(categoryName)  #Find the index of the category we are asking about to get the amount of kinks in that category.
                            embedstring = f"What are your feelings about {categoryName}? \nThis includes things such as:\n"

                            for z in range(1, kinksPerCategory[categoryID]):    #Add the kinks of the category to the list in the embed.
                                embedstring = embedstring + f"- {GlobalVars.kinkdatabase[1][categoryIndex[categoryID] + z]}\n"

                            embedstring = embedstring + "You will be able to rate each kink individually later.\n\n"

                            for z in range(0, len(kinkOptions)):#Add the answer options to the embed
                                embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                        
                            embedstring = f"What are your feelings about {kinkname}?"                   
                            pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = kinkOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                    elif "Role" in kinkname:

                        splitName = kinkname.rsplit(" ", 1)[0]
                        embedstring = f"{interaction.user.name}, what is your preferred role in {splitName}?"                   
                        pref, n = await CommonDefinitions.quicksel(interaction=interaction, options = participationOptions, title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, dest = threadid)

                    elif "Additional" in kinkname: #Additional kinks/limits section
                        try:
                            
                            await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}): \nQuestion {y+1}/{categoryKinkCount}: {kinkname}", description = f"Do you have any {kinkname} you want to add? List them here! If there aren't any, put \"none\".", colour = embcol))
                            messagefound = False
                            while messagefound == False:
                                msg2 = await client.wait_for('message',  check = checkAuthor(interaction.user))
                                if msg2.channel == threadid:
                                    messagefound = True
                            pref = str(msg2.content)
                            if pref == "":
                                pref = "none"
                        except asyncio.TimeoutError:
                        
                            await threadid.channel.send("Message timed out")
                            kinksel = "Fail"
                            return

                        except ValueError:
                        
                            await threadid.channel.send("Something went wrong! ValueError.")
                            kinksel = "Fail"

                            try:
                                await msg2.delete()
                            except discord.errors.DiscordServerError:
                                await threadid.send(embed = discord.Embed(title = "Oops...", description = f"We experienced an internal error with the eldritch spaghetti monster called discord-api... Trying to continue. If we stop responding, please restart the survey.", colour = embcol))
                            return

                    await threadid.send(embed = discord.Embed(description = f"Registered {kinkname} as {pref}.", colour = embcol))
                    newKinklist.append(pref)

                #Increment kinkindex
                kinkindex += 1

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "That concludes the kink survey! Thank you for your time. If you change your mind on anything I just asked you about, you can request us to change it with /kinkedit.", colour = embcol))

    kinkws = gc.open_by_key(kinksheet).get_worksheet(0)
    krange = "A" + str(playerindex+1) + ":GZ" + str(playerindex+1)
    kinkws.update(krange, [newKinklist])
    GlobalVars.kinkdatabase = gc.open_by_key(kinksheet).sheet1.get_all_values()
    await interaction.followup.send("Command complete.")
    return

#Generates Random Loot, tailored to kinklist
async def randloot(message):
    kinkdata, namestr, targname = await getKinkData(message)
    playerIndex = [row[1] for row in kinkdata].index(namestr)
    playerKinkData = kinkdata[playerIndex]
    rarityletters = ["c", "u", "r", "v", "l", "a"]
    raritypercents = [1, commonpercent +1, uncommonpercent +1, rarepercent +1, veryrarepercent +1, 101]
    try:
        rarityroll = int(message.content.split(">")[1])
    except ValueError:
        try:
            raritext = message.content.split(">")[1].lstrip(" ")
            if not "-" in raritext:
                rarityroll = raritypercents[rarityletters.index(raritext[0].lower())] #Get index of first letter in terms of array, then check what value that represents as a percentage.
            else:
                rarityroll = random.randint(raritypercents[rarityletters.index(raritext.split("-")[0][0].lower())], raritypercents[rarityletters.index(raritext.split("-")[1][0].lower())])
        except IndexError:
            rarityroll = random.randint(1,100)
    except IndexError:
        rarityroll = random.randint(1,100)
    
    if rarityroll <= commonpercent:
        rarity = "Common"
        rarityrange = "A3:G100"
    elif rarityroll <= uncommonpercent:
        rarity = "Uncommon"
        rarityrange = "I3:O100"
    elif rarityroll <= rarepercent:
        rarity = "Rare"
        rarityrange = "Q3:W100"
    elif rarityroll <= veryrarepercent:
        rarity = "Very Rare"
        rarityrange = "Y3:AE100"
    elif rarityroll <= 100:
        rarity = "Legendary"
        rarityrange = "AG3:AM100"
    else:
        rarity = "Artifact"
        rarityrange = "AO3:AU100"
    randomloot = sheet.values().get(spreadsheetId = Randomlootsheet, range = rarityrange, majorDimension='ROWS').execute().get("values")
    #Loot Randomisation Functions
    randrace = random.choice(races)
    randcol = random.choice(colours)
    randtoy = random.choice(sextoys)
    randgag = random.choice(gags)
    randsize = random.choice(sizes)
    for a in range(limitloopmax): #Limit avoidance loop
        lootindex = random.randint(0,len(randomloot)-1)
        kinks = []
        try:
            reqkinks = randomloot[lootindex][6].split("|")
        except IndexError:
            reqkinks = ""
        #Additional kinks based on randomisation data
        if "[toy]" in str(randomloot[lootindex]):
            for c in range(len(sextoykinks[sextoys.index(randtoy)])):
                reqkinks.append(sextoykinks[sextoys.index(randtoy)][c])
        if "[gag]" in str(randomloot[lootindex]):
            for c in range(len(gagkinks[gags.index(randgag)])):
                reqkinks.append(gagkinks[gags.index(randgag)][c])
        for b in range(len(reqkinks)):
            kinks.append(reqkinks[b] + ": " + playerKinkData[kinkdata[1].index(reqkinks[b])])
        if (not "Limit" in "".join(kinks)) and (not "Not my Thing" in "".join(kinks)):
            break
    playerchar = ""
    playerrace = ""
    if "[player" in str(randomloot[lootindex]):
        chardata = sheet.values().get(spreadsheetId = CharSheet, range = "A1:Z1000" ).execute().get("values")
        playerrow = random.randint(2, len(chardata))
        try:
            playerchar = str(chardata[playerrow][5])
            playerrace = str(chardata[playerrow][6])
        except IndexError:
            playerchar = "Someone"
            playerrace = "person"
    lootTitle = await diceroll(str(randomloot[lootindex][0]).replace("[race]", randrace).replace("[playerchar]", playerchar).replace("[playercharrace]", playerrace).replace("[toy]", randtoy).replace("[gag]", randgag).replace("[size]", randsize).title().replace("'S", "'s"))
    lootDesc = await diceroll(str(randomloot[lootindex][3]).replace("[race]", randrace).replace("[colour]", randcol).replace("[playerchar]", playerchar).replace("[playercharrace]", playerrace).replace("[material]", random.choice(materials)).replace("[toy]", randtoy).replace("[gag]", randgag).replace("[size]", randsize))
    
    try:
        lootValue = int(randomloot[lootindex][4])
    except ValueError:
        try:
            if randomloot[lootindex][5] != "":
                typemod = 0.5
            else:
                typemod = 1.5
        except IndexError:
            typemod = 1.5
        if rarity == "Common":
            lootValue = int(((int(await diceroll("[1d6]")) + 1) * 1 * typemod) + int(await diceroll("[1d10]")) + 10)
        elif rarity == "Uncommon":
            lootValue = int((int(await diceroll("[1d6]")) * 10 * typemod) + int(await diceroll("[1d10]")) + 20)
        elif rarity == "Rare":
            lootValue = int((int(await diceroll("[2d10]")) * 100 * typemod) + int(await diceroll("[1d100]")) + 200)
        elif rarity == "Very Rare":
            lootValue = int(((int(await diceroll("[1d4]")) + 1) * 1000 * typemod) + int(await diceroll("[1d100]")) + 2000)
        elif rarity == "Legendary":
            lootValue = int((int(await diceroll("[2d6]")) * 2500 * typemod) + int(await diceroll("[1d100]")) + 10000)
    lootValue = str(lootValue)
    
    if ("Limit" in "".join(kinks)) or ("Not my Thing" in "".join(kinks)):
        await message.channel.send(embed = discord.Embed(title = "Random Loot Generation Failed", description = "We were unable to find a " + rarity + " item that was not a limit for " + namestr + ".\nTry again, specifying the rarity to a different value?\n\nCurrent rarity settings are:\n\nCommon: 1-" + str(commonpercent) + "\nUncommon: " + str(commonpercent+1) + "-" + str(uncommonpercent)+ "\nRare: " + str(uncommonpercent+1) + "-" + str(rarepercent)+ "\nVery Rare: " + str(rarepercent+1) + "-" + str(veryrarepercent)+ "\nLegendary: " + str(veryrarepercent+1) + "-100", colour = embcol))
        await message.delete()
        return
    elif reqkinks != "":
        await message.channel.send(embed = discord.Embed(title = "Random Loot Generation", description = "Random loot generated and compared to " + namestr + "'s kinks:\n\n**" + lootTitle + ":**\n*" + str(randomloot[lootindex][1]) + " - " + rarity + "*\n" + lootDesc + "\n\nIt is worth " + str(lootValue) + dezzieemj + "\n\n-------------------------------------------------------------------------------\n\nHere is how the associated kinks compares with " + namestr + "'s preferences:\n\n" + "\n".join(kinks) + "\n\nRolls: Rarity d100:" + str(rarityroll) + ", Item index: " + str(lootindex) + "\n\n-------------------------------------------------------------------------------\n\n" + str(message.author.name) + ", from here, you can:\n\n`1`: Add the item to " + namestr + "'s inventory\n`2`: Edit the item\n`3`: Cancel", colour = embcol))
    else:
        await message.channel.send(embed = discord.Embed(title = "Random Loot Generation", description = "Random loot generated and compared to " + namestr + "'s kinks:\n\n**" + lootTitle + ":**\n*" + str(randomloot[lootindex][1]) + " - " + rarity + "*\n" + lootDesc + "\n\nIt is worth " + str(lootValue) + dezzieemj + "\n\n-------------------------------------------------------------------------------\n\nThere are no kinks associated with this item" + "\n\nRolls: Rarity d100:" + str(rarityroll) + ", Item index: " + str(lootindex) + "\n\n-------------------------------------------------------------------------------\n\n" + str(message.author.name) + ", from here, you can:\n\n`1`: Add the item to " + namestr + "'s inventory\n`2`: Edit the item\n`3`: Cancel", colour = embcol))
    await message.delete()
    itemtype = str(randomloot[lootindex][1])
    shortdesc = str(randomloot[lootindex][2])
    while 1: #Editing loop
        try:
            msg = await client.wait_for('message', timeout = 60, check = check(message.author))
            try:
                lootindex = int(msg.content)
                await msg.delete()
            except TypeError or ValueError:
                await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                await msg.delete()
                return
        except asyncio.TimeoutError:
            await message.channel.send("Selection Timed Out")
            await message.delete()
            return
        if lootindex == 1:
            break
        elif lootindex == 2:
            await message.channel.send(embed = discord.Embed(title = "Editing Randomised Loot for " + namestr, description = "Here are the options you can edit:\n\n`1`: Name - *" + lootTitle + "*\n`2`: Item Type - *" + itemtype + "*\n`3`: Rarity - *" + rarity + "*\n`4`: Short Description - *" + shortdesc + "*\n`5`: Description" + lootDesc + "\n`6`: Value - *" + str(lootValue) + "*", colour = embcol))
            try:
                msg = await client.wait_for('message', timeout = 60, check = check(message.author))
                try:
                    editindex = int(msg.content)
                    await msg.delete()
                except TypeError or ValueError:
                    await message.channel.send(embed=discord.Embed(title="Selection Invalid",description="You must enter an integer", colour = embcol))
                    await msg.delete()
                    return
            except asyncio.TimeoutError:
                await message.channel.send("Selection Timed Out")
                await message.delete()
                return
            await message.channel.send(embed = discord.Embed(title = "Editing", description = "Please input the new value now.\n\nThis message has a longer timeout than most, so will timeout in two minutes.", colour = embcol))
            try:
                msg2 = await client.wait_for('message', timeout = 120, check = checkstr(message.author))
                if editindex == 1:
                    lootTitle = msg2.content
                elif editindex == 2:
                    itemtype = msg2.content
                elif editindex == 3:
                    rarity = msg2.content
                elif editindex == 4: 
                    lootDesc = msg2.content
                elif editindex == 5:
                    shortdesc = msg2.content
                elif editindex == 6:
                    lootValue = msg2.content
                await message.channel.send(embed = discord.Embed(title = lootTitle, description = "*" + itemtype + "* - " + rarity + "\n\n" + lootDesc + "\n\n" + str(lootValue) + dezzieemj  + "\n\n-------------------------------------------------------------------------------\n\n" + str(message.author.name) + ", from here, you can:\n\n`1`: Add the item to " + namestr + "'s inventory\n`2`: Edit the item\n`3`: Cancel", colour = embcol))
            except asyncio.TimeoutError:
                await message.channel.send("Selection Timed Out")
        else:
            return
    try:
        await message.channel.send(embed = discord.Embed(title = "Choose Destination Channel", description = "Type the link to the channel you want the item to be sent to. You can also type DM to have it sent to the player via direct messages instead.", colour = embcol))
        msg3 = await client.wait_for('message', timeout = 30, check = checkstr(message.author))
    except asyncio.TimeoutError:
        await message.channel.send("Selection Timed Out")
        return
    if msg3.content.lower() == "dm":
        destchannel = await client.fetch_user(int(targname.id))
    else:
        try:
            channelid = int(msg3.content.split("#")[1].split(">")[0])
            destchannel = client.get_channel(channelid)
        except IndexError:
            await message.channel.send("That is not a valid channel?")
    await destchannel.send(embed = discord.Embed(title = namestr + ", you have found an item!", description = "**" + lootTitle + "**\n\n*" + itemtype + " - " + rarity + "*\n" + lootDesc + "\n\nIt is worth " + str(lootValue) + dezzieemj + "\n\nIt has not yet been added to your inventory, but *soon*...", colour = embcol))
    await message.channel.send("Sent Loot")
    #Update inventory
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ8000", majorDimension = 'ROWS').execute().get("values")
    targetindex = [row[0] for row in userinvs[::4]].index(namestr)
    targetindex *= 4
    targetinv = userinvs[targetindex]
    if lootTitle.replace("'","").replace("’","").lower() in str(userinvs[targetindex]).replace("'","").replace("’","").lower():
        for itno in range(len(userinvs[targetindex+5])):
            
            #If item is existing
            if lootTitle.replace("'","").replace("’","").lower() in userinvs[r][itno].replace("'","").replace("’","").lower():
                newquant = int(userinvs[targetindex][itno].split("|")[1]) + 1
                collet = await getColumnLetter(itno)
                lootarray = [lootTitle + "|" + str(newquant), shortdesc, lootDesc, str(lootValue)]
                sheet.values().update(spreadsheetId = EconSheet, range = collet + str(targetindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[lootarray])).execute()
                break

    else:
        #If item is new
        itno = len(userinvs[targetindex])
        lootarray = [lootTitle + "|" + str(1), shortdesc, lootDesc, str(lootValue)]
        collet = await getColumnLetter(itno)
        sheet.values().update(spreadsheetId = EconSheet, range = str(collet) + str(targetindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[lootarray])).execute()


#---------------------------Helper Functions---------------------------------

#Fetches name and ID of author, and loads the kinkdata from the sheet.
async def getKinkTarget(target, interaction):
    if target != None:
        try:
            targid = int(target[2:-1])
        except ValueError:
            await interaction.channel.send(embed = discord.Embed(title = "Error!", description = "Make sure that the user you tagged is valid.", colour = embcol))
            return
        targname = await client.fetch_user(targid)
    else:
        targname = interaction.user
    return targname

async def getKinkData(message):
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    if "@" in message.content:
        try:
            targid = int(str(message.content.split("@")[1]).split(" ")[0].replace("!","").replace("&","").replace(">",""))
        except ValueError:
            await message.channel.send(embed = discord.Embed(title = "Error!", description = "Make sure that the user you tagged is valid.", colour = embcol))
            return
        targname = await client.fetch_user(targid)
    else:
        targname = message.author
    if message.author.discriminator == "0" or message.author.discriminator == None:
        namestr = str(targname.name)
    else:
        namestr = str(targname.name + "#" + targname.discriminator)
    return kinkdata, namestr, targname

#Returns the secondary embed of Kinklist
async def Kinklistdetail(categoryIndex, categories, printCategories, sel, playerindex, printCategoriesWithAvg, categoryAverages, tmp, namestr, outputchannel, foot):

    #Prepare the string containing the kinks and their ratings
    try:
        try:
            kinkrange = [categoryIndex[categories.index(printCategories[sel])], categoryIndex[categories.index(printCategories[sel]) + 1]]
        except IndexError:
            kinkrange = [categoryIndex[-1], categoryIndex[-1] + 2]
        kinkratingString = ""
        for index in range(kinkrange[0], kinkrange[1]):
            rating = GlobalVars.kinkdatabase[playerindex][index].replace("Fave", "**Fave**").replace("Kink", "**Kink**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__")
            kinkratingString += f"\n{GlobalVars.kinkdatabase[1][index]}: {rating}"

        try:

            #Perpare the index for the part of the string with the averages.
            if printCategories[sel-1] in printCategoriesWithAvg:
                #Fetch the average and user set rating for this category.
                avgRating = categoryAverages[printCategoriesWithAvg.index(printCategories[sel-1])]
                userRating = GlobalVars.kinkdatabase[playerindex][categoryIndex[tmp] + (sel) - 1]    #-2 is a magic number and symbolises the amount of categories that (except for Gen Pref and Categories) do not have an average before the first that does. 
                #At the time of wrinting this, categories are "General Preferences"[0], "Categories"[1], "Bodyparts"[2], "Relationships"[3], "Physical Dominance"[4]. Gen Pref and Categories are not in our array, so "Bodyparts" and "Relationships" are the 2 categories that need to be skipped.

                kinkemb2 = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = f"**{printCategories[sel-1]}:**\n\n {kinkratingString} \n\nOverall, " + namestr.split("#")[0] + str(" rates this category as " + str(userRating.replace("Fave", "**Fave**").replace("Kink", "**Kink**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__").replace("as Likes", "as something they generally like"))), colour = embcol).set_footer(text = foot)
            
            else:
                kinkemb2 = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = f"**{printCategories[sel-1]}:**\n\n {kinkratingString}", colour = embcol).set_footer(text = foot)

        except IndexError:
            return
        await outputchannel.send(embed = kinkemb2)
    except IndexError:
        pass

#Returns valuable information about the kinklist itself like categories, kinks per category, the index of each category in the overall kinks and the amount of player information entries.
async def getCategoryData():

    categories = list(filter(None, GlobalVars.kinkdatabase[0])) #Categories for embed titles. The filter removes blank entries
    kinksPerCategory = []
    categoryIndex = []
    for a in range(len(categories)):
        categoryIndex.append(GlobalVars.kinkdatabase[0].index(categories[a]))
        try:
            kinksPerCategory.append(GlobalVars.kinkdatabase[0].index(categories[a+1]) - GlobalVars.kinkdatabase[0].index(categories[a]))
        except IndexError:
            kinksPerCategory.append(2)
    try:
        categories.remove("Player Information")
    except ValueError:
        pass
 
    return categories, kinksPerCategory, categoryIndex

#Returns the column letter
async def getColumnLetter(columnindex):
    collet = ""
    if columnindex > 25:
        collet = chr(64 + math.floor(columnindex / 26))
    else:
        collet = ""                        
    collet += chr(65 + (int(columnindex % 26)))
    return collet

#Returns the limits of the member as a string
async def getLimits(player):

    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    playerIndex = [row[1] for row in kinkdata].index(player)
    limits = []

    for a in range(len(kinkdata[1])):
        if "limit" in kinkdata[playerIndex][a].lower() or "not my thing" in kinkdata[playerIndex][a].lower():
            limits.append(kinkdata[1][a])
    return limits

#Returns a user selected kink:
async def selkink(kink, interaction):

    kinkindex = None
    if kink != None: #Fuzz match typed kink
        kinksel = await CommonDefinitions.selectItem(interaction, kink, 10, GlobalVars.kinkdatabase[1])
        try:
            kinkindex = GlobalVars.kinkdatabase[1].index(kinksel[0])
        except TypeError:
            return
    else: #Search by category
        categories, kinksPerCategory, categoryIndex = await getCategoryData()
        catlis = []
        for a in range(len(categories)):
            catlis.append("`" + str(a+1) + "`: " + categories[a])
        dropsel = CommonDefinitions.Dropdown_Select_View(interaction = interaction, timeout=30, optionamount=len(categories), maxselectionamount=1, namelist=categories)
        msg = await interaction.channel.send(embed = discord.Embed(title = "Choose the category of kink from this list", description = "\n".join(catlis), colour= embcol), view = dropsel)
        #Wait for reply
        if await dropsel.wait():
            await interaction.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
            return
        catindex = int(dropsel.button_response[0])
        await msg.delete()
        
        kinklis = []   
        kinkarr = []
        try:
            kinkrange = [categoryIndex[catindex], categoryIndex[catindex + 1] - 1]
        except IndexError:
            kinkrange = [categoryIndex[catindex], categoryIndex[catindex] + 2]
        for a in range(len(GlobalVars.kinkdatabase[1])):
            if a < 4 or a < kinkrange[0] or a > kinkrange[1]:
                pass
            else:
                try:
                    kinklis.append("`" + str(len(kinklis)+1) + "`: " + str(GlobalVars.kinkdatabase[1][a]))
                except TypeError:
                    kinklis.append("`1`: " + str(GlobalVars.kinkdatabase[1][a]))
                kinkarr.append(GlobalVars.kinkdatabase[1][a])

        indexoffset = 0
        kinkcopy = list.copy(kinkarr)
        while 1:
            if len(kinkcopy) > 25:
                kinkreduced = list.copy(kinkcopy)
                kinkreduced = kinkreduced[:24]
                kinkreduced.append("See more")
                kinkcopy = kinkcopy[25:]
            else:
                kinkreduced = kinkcopy
            dropsel2 = CommonDefinitions.Dropdown_Select_View(interaction = interaction, timeout=30, optionamount=len(kinkreduced), maxselectionamount=1, namelist=kinkreduced)
            msg = await interaction.channel.send(embed = discord.Embed(title = "Choose the kink from this list", description = "\n".join(kinklis), colour= embcol), view = dropsel2)
            #Wait for reply
            if await dropsel2.wait():
                await interaction.channel.send(embed=discord.Embed(title="Selection Timed Out", colour = embcol))
                return
            
            if kinkreduced[int(dropsel2.button_response[0])-1] == "See more":
                indexoffset += 25
            else:
                kinkindex = GlobalVars.kinkdatabase[1].index(kinkarr[int(dropsel2.button_response[0]) - 1 + indexoffset])
                break
    try:
        kinkname = GlobalVars.kinkdatabase[1][kinkindex]
    except IndexError:
        await interaction.channel.send(content = "@<&1055536891606351983>", embed = discord.Embed(title = "Your kink could not be found", description = "We're not actually sure how you managed this. The bot gods have been alerted to your location. ~~Run~~.", colour= embcol))
        return
    return kinkname, kinkindex