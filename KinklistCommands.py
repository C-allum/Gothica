from CommonDefinitions import *


kinkOptions = ["Fave", "Kink", "Like", "It depends", "Willing to try", "No Strong Emotions", "Never heard of it", "Not my thing", "Soft Limit", "Hard Limit"]
participationOptions = ["Submissive", "Dominant", "Voyeur", "Switch", "Submissive and Voyeur", "Dominant and Voyeur", "Enthusiast (Role doesn't matter to me)"]
#Displays the kinklist of the author, or another user if they are tagged.
async def kinklist(message):
    kinkdata, namestr, targname = await getKinkData(message)

    categories, kinksPerCategory, categoryIndex, playerInformationEntries = await getCategoryData(kinkdata)

    if not str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

    else:

        #Show all kinks
        kinksec = -1

        kinks = []

        kinklist = []

        kinksegment = []

        kinktot = 0

        kinksum = 0

        segid = -2

        allCategoriesTotal = 4

        kinkres = []

        namestr = str(targname.name + "#" + targname.discriminator)

        playerindex = [row[1] for row in kinkdata].index(namestr)

        print(playerindex)
        print(namestr)

        for c in range(len(categories)):

            kinksum = 0

            for d in range(kinksPerCategory[c]):

                try:

                    kinkdatanumb = len(kinkOptions) - int(kinkOptions.index(kinkdata[playerindex][allCategoriesTotal]))

                except ValueError:

                    kinkdatanumb = 5

                allCategoriesTotal += 1

                kinksum += kinkdatanumb

            try:
                
                kinkres.append(kinkOptions[len(kinkOptions) - round(kinksum/kinksPerCategory[c])])

            except ZeroDivisionError:

                kinkres.append(kinkOptions[5])

            

        for b in range(len(categories)):

            try:
                if kinkdata[0][b] != "":

                    kinklist.append("\n".join(kinks))

                    kinks = ""

                    kinks = []

                    if kinktot == 0:

                        kinkres = kinkOptions[5]

                    else:

                        try:

                            kinkres = kinkOptions[round(kinksum/kinktot)]

                        except ZeroDivisionError:

                            kinkres = kinkOptions[5]

                    kinktot = 0

                    kinksum = 0

                    kinksec += 1

                    if segid > 2 and segid != 11:

                        kinksegment.append("`" + str(segid) + "`: " + str(kinkdata[0][b] + " - " + str(kinkdata[a][segid+9].replace("Fave", "**Fave**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__"))))

                        if segid > 3:

                            kinksegment[int(segid)-2] = kinksegment[int(segid)-2] + " (" + kinkres + ")"


                    elif segid > 0:

                        kinksegment.append("`" + str(segid) + "`: " + str(kinkdata[0][b]))


                    segid += 1

            except IndexError:

                print("IndexError")

                pass

            try:
                
                kinksum += int(kinkdatanumb)

                kinktot = b

            except ValueError:

                print("ValueError")

                pass

            kinks.append("*" + kinkdata[1][b] + ":* " + str(kinkdata[a][b]).replace("Fave", "**Fave**").replace("Soft Limit", "__Soft Limit__").replace("Hard Limit", "__Hard Limit__"))

        if kinktot == 0:

            kinkres = kinkOptions[5]

        else:

            try:

                kinkres = kinkOptions[round(kinksum/kinktot)]

            except ZeroDivisionError:

                kinkres = kinkOptions[5]

            kinksegment[-2] = kinksegment[-2] + " (" + kinkres + ")"

        kinklist.append("\n".join(kinks))
        print(f"Kinklist: {kinklist}")
        kinkemb = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = "**General Preferences:**\n\n" + str(kinklist[2]) + "\n\n**Kink Overview:**\n" + namestr.split("#")[0] + "'s general thoughts on each category of kink are shown below. We have then taken their average response in each category, and included that information in brackets.\n*As always, you should check with your rp partners regarding hard and soft limits for any particular scene.*\n\n*To see more detail on any of the below categories, type the corresponding number*\n\n" + "\n".join(kinksegment), colour = embcol)

        await message.channel.send(embed = kinkemb)

        await message.delete()

        try:

            msg = await client.wait_for('message', timeout = 30, check = check(message.author))

        except asyncio.exceptions.TimeoutError:

            await message.channel.send("Message Timed Out")

            pass

        try:

            sel = int(msg.content)

            await msg.delete()

            try:

                if sel == 11:

                    kinkemb2 = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = "**" + str(kinksegment[sel-1].split(":")[1]) + ":**\n\n" + str(kinklist[sel+3]), colour = embcol)

                elif sel < 3:

                    kinkemb2 = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = "**" + str(kinksegment[sel-1].split(":")[1]) + ":**\n\n" + str(kinklist[sel+3]), colour = embcol)

                else:

                    kinkemb2 = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = "**" + str(kinksegment[sel-1].split(":")[1].split(" - ")[0]) + ":**\n\n" + str(kinklist[sel+3]) + "\n\nOverall, " + namestr.split("#")[0] + str(" rates this category as " + str(kinksegment[sel-1].split(":")[1].split(" - ")[1].split(" (")[0])).replace("as Likes", "as something they generally like") + ". On average, these answers sit at " + str(kinksegment[sel-1].split(":")[1].split(" - ")[1].split("(")[1].replace(")","")), colour = embcol)

            except IndexError:

                kinkemb2 = discord.Embed(title = "That is not a number of a category to view.", description = "The categories range from 1 to 11.", colour = embcol)

            await message.channel.send(embed = kinkemb2)

        except ValueError:

            pass

        except TimeoutError:

            pass


#Allows to edit the kinklist. Moderators can tag someone and edit someone elses kinks.
async def kinkedit(message):

    kinkdata, namestr, targname = await getKinkData(message)

    if not str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

    else:
        #Get player info
        playerIndex = [row[1] for row in kinkdata].index(namestr)
        playerKinkData = kinkdata[playerIndex]

        if targname != message.author and not "moderator" in str(message.author.roles).lower():

            await message.channel.send(embed = discord.Embed(title = "You can't edit someone else's kinks.", description = "", colour = embcol))

        else:

            try:

                if "@" in message.content:

                    searchterm = message.content.lower().split(" ", 2)[2]

                else:

                    searchterm = message.content.lower().split(" ", 1)[1]

            except IndexError:

                searchterm = "Search term not found"

            if searchterm != "Search term not found" and searchterm in str(kinkdata[1]).lower():

                kinkssearched = []

                kinkindexes = []

                for c in range(len(kinkdata[1])):

                    if searchterm in kinkdata[1][c].lower():

                        kinkssearched.append("`" + str(len(kinkindexes) + 1) + "`: " + kinkdata[1][c]) 

                        kinkindexes.append(c)

                if len(kinkindexes) > 1:

                    await message.channel.send(embed = discord.Embed(title = "Multiple kinks found matching that search:", description = "Choose the number of the one you want:\n\n" + "\n".join(kinkssearched) + "\n\nThis message will timeout after 30 seconds.", colour = embcol))

                    try:
                        
                        msg = await client.wait_for('message', timeout = 30, check = check(message.author))

                        try:

                            kinksel = kinkssearched[int(msg.content) - 1].split(": ")[1]

                            kinkindex = kinkindexes[int(msg.content) - 1]

                        except IndexError:

                            kinksel = "Fail"

                        await msg.delete()

                    except asyncio.TimeoutError:

                        await message.channel.send("Message timed out")

                        kinksel = "Fail"

                    except ValueError:

                        await message.channel.send("That isn't a valid integer")

                        kinksel = "Fail"

                        await msg.delete()

                else:

                    kinksel = kinkssearched[0].split(": ")[1]

                    kinkindex = kinkindexes[0]

                if kinksel != "Fail":

                    pref = "Fail"

                    if kinkindex > 3 and not "Role" in kinksel:
                        
                        embedstring = f"{message.author.name}, you currently have {kinksel} as: {kinkdata[a][kinkindex]}. What would you like to change this to?\n\n"
                        for z in range(0, len(kinkOptions)): #Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                        embedstring = embedstring + "\n\nThis message will timeout in 30 seconds."
                        await message.channel.send(embed = discord.Embed(title = "Editing " + kinksel, description = embedstring, colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                #options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]

                                pref = kinkOptions[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif "Role" in kinksel:
                        embedstring = f"{message.author.name}, {kinksel}\n\nCurrently, this is set as: {kinkdata[a][kinkindex]}. What would you like to change this to?\n\n"
                        for z in range(0, len(participationOptions)): #Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {participationOptions[z]}\n"
                        embedstring = embedstring + "\n\nThis message will timeout in 30 seconds."
                        await message.channel.send(embed = discord.Embed(title = "Editing role in " + kinksel.rsplit(" ", 1)[0], description = embedstring, colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                #options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = participationOptions[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif kinksel == "Pronouns":

                        await message.channel.send(embed = discord.Embed(title = "Editing your pronouns", description = message.author.name + ", your pronouns are currently " + kinkdata[a][kinkindex] + ". What would you like to change them to?\n\nThe format should ideally be the same as He/Him, so Personal Subject Pronoun/ Personal Object Pronoun.\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = checkAuthor(message.author))

                            pref = msg2.content


                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                    else:

                        await message.channel.send("That isn't a kink you can edit")

                    if pref != "Fail":

                        playerKinkData[kinkindex] = pref
                        await message.channel.send(embed = discord.Embed(title = "Edited " + kinkdata[1][kinkindex], description = "You have set it to: " + pref, colour = embcol))
                        sheet.values().update(spreadsheetId = kinksheet, range = str(f"A{playerIndex + 1}"), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[playerKinkData])).execute()

                        await message.delete()

                else:

                    await message.channel.send("Something went wrong")

            #Edit by menu

            elif searchterm == "Search term not found":
                               
                categories, kinksPerCategory, CategoryIndex, playerInformationEntries = await getCategoryData(kinkdata)
                CategoryIndex[0] = CategoryIndex[0] -1  #To include Pronouns in General Preferences
                embedstring = "Choose one of the following categories:\n\n"
                optionCounter = 1
                for kink in categories:
                    embedstring = embedstring + f"`{optionCounter}`: {kink}\n"
                    optionCounter += 1
                embedstring = embedstring + "\nThis message will timeout after 30 seconds."
                await message.channel.send(embed = discord.Embed(title = "Which kink would you like to edit?", description = embedstring, colour = embcol))

                try:
                        
                    msg = await client.wait_for('message', timeout = 30, check = check(message.author))

                    try:

                        #kinkcat = ["General Preferences", "Body Parts", "Relationships", "Physical Domination", "Mental Domination", "Clothing and Toys", "Kinkyplay", "Transformation", "Mind Control", "Monster Fucking", "Extreme Kinkplay", "Additional Kinks and Limits"]

                        kinksel = categories[int(msg.content) - 1]

                    except IndexError:

                        kinksel = "Fail"

                    await msg.delete()

                except asyncio.TimeoutError:

                    await message.channel.send("Message timed out")

                    kinksel = "Fail"

                except ValueError:

                    await message.channel.send("That isn't a valid integer")

                    kinksel = "Fail"

                    await msg.delete()

                if kinksel != "Fail":

                    
                    kinkselector = int(msg.content)
                    kinkrange = [CategoryIndex[categories.index(kinksel)], CategoryIndex[categories.index(kinksel) + 1] - 1]

                    kinktitles = []

                    kinkindex = []

                    for c in range(len(kinkdata[1])):

                        if kinkrange[0] <= c and kinkrange[1] >= c:

                            kinktitles.append("`" + str(len(kinkindex) + 1) + "`: " + kinkdata[1][c])

                            kinkindex.append(c)

                    await message.channel.send(embed = discord.Embed(title = "Editing " + kinksel, description = "Choose the data you wish to edit:\n\n" + "\n".join(kinktitles) + "\n\nThis message will timeout in 30 seconds.", colour = embcol))

                    kinktoedit = "Fail"

                    kinkindex0 = -1

                    try:

                        msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                        msg = int(msg2.content)

                        try:

                            kinktoedit = kinktitles[msg - 1].split(": ")[1]

                            kinkindex0 = int(kinkindex[msg - 1])

                            await msg2.delete()

                        except IndexError:

                            await message.channel.send("That isn't a valid option.")

                    except asyncio.TimeoutError:

                        await message.channel.send("Message timed out")

                    pref = "Fail"

                    if kinkindex0 > 3 and not "Role" in kinktoedit:

                        embedstring = f"{message.author.name}, you currently have {kinktoedit} as: {playerKinkData[kinkindex0]}. What would you like to change this to?\n\n"
                        for z in range(0, len(kinkOptions)): #Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                        embedstring = embedstring + "\n\nThis message will timeout in 30 seconds."

                        await message.channel.send(embed = discord.Embed(title = "Editing " + kinktoedit, description = embedstring, colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                #options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]

                                pref = kinkOptions[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif "Role" in kinktoedit:
                        
                        embedstring = f"{message.author.name}, {kinksel}\n\nCurrently, this is set as: {playerKinkData[kinkindex0]}. What would you like to change this to?\n\n"
                        for z in range(0, len(participationOptions)): #Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {participationOptions[z]}\n"
                        embedstring = embedstring + "\n\nThis message will timeout in 30 seconds."
                        await message.channel.send(embed = discord.Embed(title = "Editing role in " + kinktoedit.rsplit(" ", 1)[0], description = embedstring, colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                #options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = participationOptions[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif kinktoedit == "Pronouns":

                        await message.channel.send(embed = discord.Embed(title = "Editing your pronouns", description = message.author.name + ", your pronouns are currently " + kinkdata[a][kinkindex0] + ". What would you like to change them to?\n\nThe format should ideally be the same as He/Him, so Personal Subject Pronoun/ Personal Object Pronoun.\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = checkAuthor(message.author))

                            pref = msg2.content

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                    if pref != "Fail":

                        playerKinkData[kinkindex0] = pref
                        await message.channel.send(embed = discord.Embed(title = "Edited " + kinkdata[1][kinkindex0], description = "You have set it to: " + pref, colour = embcol))
                        sheet.values().update(spreadsheetId = kinksheet, range = str(f"A{playerIndex + 1}"), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[playerKinkData])).execute()

                        await message.delete()

#Takes a kink as a second input and outputs people who like that kink.
async def kinkplayers(message):
    kinkdata, namestr, targname = await getKinkData(message)

    if not str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

    else:

        kinkcolumnindex = []

        for c in range(len(kinkdata[1])):

            if message.content.split(" ", 1)[1].lower() in kinkdata[1][c].lower():

                kinkcolumnindex.append(c)

        if len(kinkcolumnindex) == 0:

            await message.channel.send(embed = discord.Embed(title = "We couldn't find a kink matching that search term.", description = "You could try looking through your own `%kinklist` to check which are available?", colour = embcol))

        else:

            if len(kinkcolumnindex) > 1:

                kinktitle = []

                for d in range(len(kinkcolumnindex)):

                    kinktitle.append("`" + str(d + 1) + "`: " + kinkdata[1][kinkcolumnindex[d]])

                await message.channel.send(embed = discord.Embed(title = "We found multiple kinks matching that search term.", description = "Which are you looking for?\n\n" + "\n".join(kinktitle) + "\n\nThis message will timeout in 30 seconds.", colour = embcol))

                msg = await client.wait_for('message', timeout = 30, check = check(message.author))

                try:

                    sel = int(msg.content) - 1

                except ValueError:

                    sel = 0

                await msg.delete()

            else:

                sel = 0

            kinkhavers = []

            if message.channel.id == 1009522511844749342:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Fave":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a fave:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append("<@" + str(kinkdata[e][2]) + ">")

                        break

                await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a fave:", description = ", ".join(kinkhavers), colour = embcol))

                await message.delete()

            else:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Fave":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a fave:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append(kinkdata[e][1])

                await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a fave:", description = ", ".join(kinkhavers), colour = embcol))

                await message.delete()

            kinkhavers = []

            if message.channel.id == 1009522511844749342:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Kink":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they kink:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append("<@" + str(kinkdata[e][2]) + ">")

                        break

                await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they kink:", description = ", ".join(kinkhavers), colour = embcol))

            else:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Kink":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they kink:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append(kinkdata[e][1])

                await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they kink:", description = ", ".join(kinkhavers), colour = embcol))

            kinkhavers = []

            if message.channel.id == 1009522511844749342:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Like":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append("<@" + str(kinkdata[e][2]) + ">")

                        break

                await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

            else:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Like":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append(kinkdata[e][1])

                await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

#Finds a room and an encounter for the specified person.
async def kinkencounter(message):
    if ("lorekeeper" in str(message.author.roles).lower() or message.author.name == "C_allum"):
        kinkdata, namestr, targname = await getKinkData(message)

        if not str(targname) in str(kinkdata):

            await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

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
async def kinksurvey(message):
    
    kinkdata, namestr, targname = await getKinkData(message)
    if str(message.channel.id) != kinkcreatechannel:
        await message.channel.send(embed = discord.Embed(title = "This is not the place to talk about that.", description = f"We will gladly talk about your deepest desires, <@{targname.id}>. We prefer a bit of privacy for that however. Please use the <#{kinkcreatechannel}> channel to call this command."))
        return
    if str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "We already know your deepest desires", description = f"Your kinklist is already registered with us, <@{targname.id}>. If you want to edit it, use %kinkedit"))
        return


    threadid = await message.create_thread(name= "Kinklist entry: " + str(len(kinkdata) - 1))

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = f"Welcome to the kink survey! We will ask you to give us a rating on all sorts of kinks in just a moment. We will go through a couple of categories with plenty of kinks, and when we are done you can look at your kinklist with the %kinklist command, or edit it with the %kinkedit command. Furthermore you can search for users with a certain kink using the %kinkplayers [kink] command, or look at someone else's list with %kinklist [@username]. \n\n **Please note that we go to sleep around <t:1670025600:T> on the night from sunday to monday every week. If you don't finish before that, your progress will be lost!** \n\n Okay, with the formalities out of the way, let us begin..."))
    

    #--------------Prepare variables---------------
    newKinklist = [str(datetime.now()), f"{targname.name}#{targname.discriminator}", f"{targname.id}"] #Contains kink data, will be written into the sheet.
    processFailed = False #Indicates if there was a problem during the process. Prevents writing to the sheet if true
    categories, kinksPerCategory, categoryIndex, playerInformationEntries = await getCategoryData(kinkdata)

    #--------------Collect information from the user-------------
    #Request user's pronouns.
    try:
        await threadid.send(embed = discord.Embed(title = "Pronouns", description = "First of all: What are your preferred pronouns?"))
        messagefound = False
        while messagefound == False:
            msg = await client.wait_for('message',  check = checkAuthor(message.author))
            if msg.channel == threadid:
                messagefound = True
        newKinklist.append(msg.content)
    except asyncio.TimeoutError:

        await threadid.channel.send("Message timed out")
        processFailed = True
        kinksel = "Fail"
        return

    except ValueError:

        await threadid.channel.send("Something went wrong! ValueError.")
        processFailed = True
        kinksel = "Fail"

        await msg.delete()
        return
    
    await threadid.send(embed = discord.Embed(title = "Pronouns", description = f"Pronouns set as: {msg.content}"))
    
    #Now ask for the remaining things.
    kinkindex = playerInformationEntries #Start at the first kink, not the player info.
    for x in range (0, len(categories)): #Go over all categories

        categoryName = categories[x]
        categoryKinkCount = kinksPerCategory[x]
        categorySection = False #Check if this is the part of the survey about the categories. Need to list the involved kinks for those.
        if categoryName == "Categories":
            categorySection = True

        for y in range(0, categoryKinkCount): #Go over each kink in a category
            kinkname = kinkdata[1][kinkindex]

            #Ask the player about the kink
            if not "Role" in kinkname and not "Additional" in kinkname:   #Everything but the "If you are Role" questions
                if (categorySection == False):  #Every category but "Categories"
                    embedstring = f"What are your feelings about {kinkname}?\n\n"

                    for z in range(0, len(kinkOptions)): #Add the answer options to the embed
                        embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                    await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, colour = embcol))

                else:   #"Categories" category needs to list kinks in the message so users understand what is part of the category
                    categoryID = categories.index(kinkname) #Find the index of the category we are asking about to get the amount of kinks in that category.
                    embedstring = f"What are your feelings about {kinkname}? \nThis includes things such as:\n"

                    for z in range(1, kinksPerCategory[categoryID]):    #Add the kinks of the category to the list in the embed.
                        embedstring = embedstring + f"- {kinkdata[1][categoryIndex[categoryID] + z]}\n"

                    embedstring = embedstring + "You will be able to rate each kink individually later.\n\n"

                    for z in range(0, len(kinkOptions)):#Add the answer options to the embed
                        embedstring = embedstring + f"`{z+1}`: {kinkOptions[z]}\n"
                
                    await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, colour = embcol))

                try:
                    messagefound = False
                    while messagefound == False:
                        msg2 = await client.wait_for('message', check = check(message.author))
                        if msg2.channel == threadid:
                            messagefound = True
                    
                    msg = int(msg2.content)

                    try:
                        #options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]
                        pref = kinkOptions[msg - 1]
                        await msg2.delete()

                    except IndexError:
                        await threadid.send("That isn't a valid option. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                        processFailed = True
                        return

                except asyncio.TimeoutError:
                    await threadid.send("Message timed out. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                    processFailed = True
                    return

                except ValueError:
                    await threadid.send("That isn't a valid integer. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                    await msg2.delete()
                    processFailed = True
                    return

            elif "Role" in kinkname:

                splitName = kinkname.rsplit(" ", 1)[0]
                embedstring = f"{message.author.name}, what is your preferred role in {splitName}\n\n"
                for z in range(0, len(participationOptions)): #Add the answer options to the embed
                            embedstring = embedstring + f"`{z+1}`: {participationOptions[z]}\n"
                await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}) \nKink {y+1}/{categoryKinkCount}: {kinkname}", description = embedstring, colour = embcol))
                try:
                    messagefound = False
                    while messagefound == False:
                        msg2 = await client.wait_for('message',  check = check(message.author))
                        if msg2.channel == threadid:
                            messagefound = True

                    msg = int(msg2.content)

                    try:
                        #options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]
                        pref = participationOptions[msg - 1]
                        await msg2.delete()


                    except IndexError:
                        await threadid.send("That isn't a valid option. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                        processFailed = True
                        return

                except asyncio.TimeoutError:
                    await threadid.send("Message timed out. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                    processFailed = True
                    return

                except ValueError:
                    await threadid.send("That isn't a valid integer. Kink survey cancelled. Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum.")
                    await msg2.delete()
                    processFailed = True
                    return

            elif "Additional" in kinkname: #Additional kinks/limits section
                try:
                    await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}): {kinkname}", description = f"Do you have any {kinkname} you want to add? List them here!"))
                    messagefound = False
                    while messagefound == False:
                        msg2 = await client.wait_for('message',  check = check(message.author))
                        if msg2.channel == threadid:
                            messagefound = True
                    pref = str(msg2.content)
                except asyncio.TimeoutError:
                
                    await threadid.channel.send("Message timed out")
                    processFailed = True
                    kinksel = "Fail"
                    return

                except ValueError:
                
                    await threadid.channel.send("Something went wrong! ValueError.")
                    processFailed = True
                    kinksel = "Fail"

                    await msg2.delete()
                    return

            await threadid.send(embed = discord.Embed(description = f"Registered {kinkname} as {pref}.", colour = embcol))
            newKinklist.append(pref)

            #Increment kinkindex
            kinkindex += 1

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "That concludes the kink survey! Thank you for your time. If you change your mind on anything I just asked you about, you can request us to change it with %kinkedit."))

    if processFailed == False: #This means nothing went wrong! We can write the results into the kink sheet.
        kinkdata, namestr, targname = await getKinkData(message)
        sheet.values().update(spreadsheetId = kinksheet, range = f"A{len(kinkdata)+1}", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[newKinklist])).execute()

    else:
        await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "Something went wrong... Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum."))

    return



#---------------------------Helper Functions---------------------------------

#Fetches name and ID of author, and loads the kinkdata from the sheet.
async def getKinkData(message):
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:GZ2000", majorDimension='ROWS').execute().get("values")
    if "@" in message.content:

        targid = int(str(message.content.split("@")[1]).split(" ")[0].replace("!","").replace("&","").replace(">",""))

        targname = await client.fetch_user(targid)
    else:

        targname = message.author

    namestr = str(targname.name + "#" + targname.discriminator)
    return kinkdata, namestr, targname

#Converts loaded kinkdata into numerical values.
async def getKinkDataNumerical(kinkdata, targname):
    for a in range(len(kinkdata)):
            if a != 0:
                if str(targname) == str(kinkdata[a][1]):
                    #Convert to Numbers
                    kinkdatanum = copy.deepcopy(kinkdata[a])
                    for b in range(4, len(kinkdata[1])):
                        try:
                            if kinkdata[a][b] == "Absolute Limit":
                                kinkdatanum[b] = -3
                            elif kinkdata[a][b] == "Hard Limit":
                                kinkdatanum[b] = -2
                                
                            elif kinkdata[a][b] ==  "Soft Limit":
                                kinkdatanum[b] = -1
                            
                            elif kinkdata[a][b] == "No Strong Emotions or Mixed":
                                kinkdatanum[b] = 0
                            
                            elif kinkdata[a][b] == "Unsure or Exploring":
                                kinkdatanum[b] = 1
                            
                            elif kinkdata[a][b] == "Likes":
                                kinkdatanum[b] = 2
                            
                            elif kinkdata[a][b] == "Kink":
                                kinkdatanum[b] = 3
                            else:
                                kinkdatanum[b] = 0
                        except IndexError:
                            kinkdatanum[b] = 0
                    break
    return kinkdatanum, a

#Returns valuable information about the kinklist itself like categories, kinks per category, the index of each category in the overall kinks and the amount of player information entries.
async def getCategoryData(kinkdata):

    categories = kinkdata[0] #Categories for embed titles. Contains a lot of empty entries at this point.
    kinksPerCategory = [] #Counts the kinks per category.
    categoryIndex = [4] #Contains the index of the first element of the category. 4 is the index of the first kink after the user data
    playerInformationEntries = 1

    
    while ("" == categories[playerInformationEntries]):
        playerInformationEntries += 1
    
    #Count the amount of kinks per category and write index of the category index.
    i = 0
    for x in range(playerInformationEntries + 1, len(kinkdata[0])):
        i += 1
        if (kinkdata[0][x] != ""):
        
            kinksPerCategory.append(i)
            categoryIndex.append(categoryIndex[-1] + i)
            i = 0
            if (kinkdata[0][x] == "Additional Kinks and Limits"):
                break
    print(f"kinkdata[1]: {kinkdata[1]}, kinkdata[0] length: {len(kinkdata[0])}, kinkdata[1] length: {len(kinkdata[1])}")
    kinksPerCategory.append(len(kinkdata[1]) - len(kinkdata[0]) + 1) #Length of last category has to be figured out this way because of index bounds.
    categoryIndex.append(categoryIndex[-1] + len(kinkdata[1]) - len(kinkdata[0]) + 1)

    while ("" in categories): #Removes the empty entries from the category row so we can use the category list length properly
        categories.remove("")
    categories.remove("Player Information")
    print(f"categories: {categories} \n\n kinksPerCategory: {kinksPerCategory} \n\n categoryIndex: {categoryIndex} \n\n playerInformationEntries: {playerInformationEntries}")
 
    return categories, kinksPerCategory, categoryIndex, playerInformationEntries