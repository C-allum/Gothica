from CommonDefinitions import *

#Displays the kinklist of the author, or another user if they are tagged.
async def kinklist(message):
    kinkdata, namestr, targname = await getKinkData(message)

    if not str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

    else:
        kinkdatanum = await getKinkDataNumerical(kinkdata, targname)

        #Show all kinks
        kinksec = -1

        kinks = []

        kinklist = []

        kinksegment = []

        kinksegplay = []

        kinkavg = 0

        kinktot = 0

        kinksum = 0

        segid = -2

        kinkavgs = 0

        for b in range(len(kinkdata[1])):

            try:

                if kinkdata[0][b] != "":

                    kinklist.append("\n".join(kinks))

                    kinks = ""

                    kinks = []

                    if kinktot == 0:

                        kinkres = "No Strong Emotions"

                    else:

                        kinkavg =kinksum/kinktot

                        if float(kinkavg) >= 2.5:

                            kinkres = "Kink"

                        elif float(kinkavg) >= 1.5:

                            kinkres = "Likes"

                        elif float(kinkavg) >= 0.5:

                            kinkres = "Unsure or Exploring"

                        elif float(kinkavg) >= -0.5:

                            kinkres = "No Strong Emotions"

                        elif float(kinkavg) >= -1.5:

                            kinkres = "Soft Limit"

                        elif float(kinkavg) >= -2.5:

                            kinkres = "Hard Limit"

                        else:

                            kinkres = "Absolute Limit"

                    kinktot = 0

                    kinksum = 0

                    kinksec += 1

                    if segid > 2 and segid != 11:

                        kinksegment.append("`" + str(segid) + "`: " + str(kinkdata[0][b] + " - " + str(kinkdata[a][segid+9].replace("Kink", "**Kink**").replace("Hard Limit", "__Hard Limit__").replace("Absolute Limit", "__Absolute Limit__"))))

                        if segid > 3:

                            kinksegment[int(segid)-2] = kinksegment[int(segid)-2] + " (" + kinkres + ")"

                    elif segid > 0:

                        kinksegment.append("`" + str(segid) + "`: " + str(kinkdata[0][b]))

                    segid += 1

                if kinktot == 0:

                    kinkres = "No Strong Emotions"

                else:

                    kinkavg =kinksum/kinktot

                    if float(kinkavg) >= 2.5:

                        kinkres = "Kink"

                    elif float(kinkavg) >= 1.5:

                        kinkres = "Likes"

                    elif float(kinkavg) >= 0.5:

                        kinkres = "Unsure or Exploring"

                    elif float(kinkavg) >= -0.5:

                        kinkres = "No Strong Emotions"

                    elif float(kinkavg) >= -1.5:

                        kinkres = "Soft Limit"

                    elif float(kinkavg) >= -2.5:

                        kinkres = "Hard Limit"

                    else:

                        kinkres = "Absolute Limit"

            except IndexError:

                pass

            try:
                
                kinksum += int(kinkdatanum[b])

                kinktot += 1

            except ValueError:

                pass

            kinks.append("*" + kinkdata[1][b] + ":* " + str(kinkdata[a][b]).replace("Kink", "**Kink**").replace("Hard Limit", "__Hard Limit__").replace("Absolute Limit", "__Absolute Limit__"))

        if kinktot == 0:

            kinkres = "No Strong Emotions"

        else:

            kinkavg =kinksum/kinktot

            if float(kinkavg) >= 2.5:

                kinkres = "Kink"

            elif float(kinkavg) >= 1.5:

                kinkres = "Likes"

            elif float(kinkavg) >= 0.5:

                kinkres = "Unsure or Exploring"

            elif float(kinkavg) >= -0.5:

                kinkres = "No Strong Emotions"

            elif float(kinkavg) >= -1.5:

                kinkres = "Soft Limit"

            elif float(kinkavg) >= -2.5:

                kinkres = "Hard Limit"

            else:

                kinkres = "Absolute Limit"

            kinksegment[-2] = kinksegment[-2] + " (" + kinkres + ")"

        kinklist.append("\n".join(kinks))

        kinkemb = discord.Embed(title = namestr.split("#")[0] + "'s kink list:", description = "**General Preferences:**\n\n" + str(kinklist[2]) + "\n\n**Kink Overview:**\n" + namestr.split("#")[0] + "'s general thoughts on each category of kink are shown below. We have then taken their average response in each category, and included that information in brackets.\n*As always, you should check with your rp partners regarding hard and soft limits for any particular scene.*\n\n*To see more detail on any of the below categories, type the corresponding number*\n\n" + "\n".join(kinksegment), colour = embcol)

        await message.channel.send(embed = kinkemb)

        await message.delete()

        msg = await client.wait_for('message', timeout = 30, check = check(message.author))

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
        kinkdatanum = await getKinkDataNumerical(kinkdata, targname)

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

            if searchterm in str(kinkdata[1]).lower():

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

                    if kinkindex > 3 and not "into it" in kinksel:

                        await message.channel.send(embed = discord.Embed(title = "Editing " + kinksel, description = message.author.name + ", you currently have " + kinksel + " as: " + kinkdata[a][kinkindex] + ". What would you like to change this to?\n\n`1`: Kink\n`2`: Likes\n`3`: Unsure or Exploring\n`4`: No Strong Emotions\n`5`: Soft Limit\n`6`: Hard Limit\n`7`: Absolute Limit\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]

                                pref = options[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif "into it" in kinksel:

                        await message.channel.send(embed = discord.Embed(title = "Editing role in " + kinkdata[0][kinkindex], description = message.author.name + ", " + kinksel + "\n\nCurrently, this is set as: " + kinkdata[a][kinkindex] + ". What would you like to change this to?\n\n`1`: For my characters (Submissive)\n`2`: For other people's characters (Dominant)\n`3`: To watch between other characters (Voyeur)\n`4`: All of the above (Switch)\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = options[msg - 1]

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

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = options[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                    else:

                        await message.channel.send("That isn't a kink you can edit")

                    if pref != "Fail":

                        column_int = kinkindex

                        start_index = 0

                        letter = ""

                        while column_int > 25 + start_index:

                            letter += chr(65 + int((column_int-start_index)/26) - 1)

                            column_int = column_int - (int((column_int-start_index)/26))*26

                        letter += chr(65 - start_index + (int(column_int)))

                        await message.channel.send(embed = discord.Embed(title = "Edited " + kinkdata[1][kinkindex], description = "You have set it to: " + pref, colour = embcol))

                        sheet.values().update(spreadsheetId = kinksheet, range = str(letter + str(a+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[pref]])).execute()

                        await message.delete()

                else:

                    await message.channel.send("Something went wrong")

            #Edit by menu

            elif searchterm == "Search term not found":

                await message.channel.send(embed = discord.Embed(title = "Which kink would you like to edit?", description = "Choose one of the following categories:\n\n`0`: General Preferences\n`1`: Body Parts\n`2`: Relationships\n`3`: Physical Domination\n`4`: Mental Domination\n`5`: Clothing and Toys\n`6`: Kinkyplay\n`7`: Transformation\n`8`: Mind Control\n`9`: Monster Fucking\n`10`: Extreme Kinkplay\n`11`: Additional Kinks and Limits\n\nThis message will timeout after 30 seconds", colour = embcol))

                try:
                        
                    msg = await client.wait_for('message', timeout = 30, check = check(message.author))

                    try:

                        kinkcat = ["General Preferences", "Body Parts", "Relationships", "Physical Domination", "Mental Domination", "Clothing and Toys", "Kinkyplay", "Transformation", "Mind Control", "Monster Fucking", "Extreme Kinkplay", "Additional Kinks and Limits"]

                        kinksel = kinkcat[int(msg.content)]

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

                    if kinkselector == 0:

                        kinkrange = [3, 20]

                    elif kinkselector == 1:

                        kinkrange = [21, 44]

                    elif kinkselector == 2:

                        kinkrange = [45, 56]

                    elif kinkselector == 3:

                        kinkrange = [57,67]

                    elif kinkselector == 4:

                        kinkrange = [68, 74]

                    elif kinkselector == 5:

                        kinkrange = [75, 89]

                    elif kinkselector == 6:

                        kinkrange = [90, 103]

                    elif kinkselector == 7:

                        kinkrange = [104, 119]

                    elif kinkselector == 8:

                        kinkrange = [120, 137]

                    elif kinkselector == 9:

                        kinkrange = [138, 153]

                    elif kinkselector == 10:

                        kinkrange = [154, 167]

                    elif kinkselector == 11:

                        kinkrange = [168, 169]

                    kinktitles = []

                    kinkindex = []

                    for c in range(len(kinkdata[1])):

                        if kinkrange[0] <= c and kinkrange[1] >= c:

                            kinktitles.append("`" + str(len(kinkindex) + 1) + "`: " + kinkdata[1][c])

                            kinkindex.append(c)

                    await message.channel.send(embed = discord.Embed(title = "Editing " + kinksel, description = "Choose the data you wish to edit:\n\n" + "\n".join(kinktitles) + "\n\nThis message will timeout in 30 seconds.", colour = embcol))

                    kinktoedit = "Fail"

                    kinkindex0 = ""

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

                    if kinkindex0 > 3 and not "into it" in kinktoedit:

                        await message.channel.send(embed = discord.Embed(title = "Editing " + kinktoedit, description = message.author.name + ", you currently have " + kinktoedit + " as: " + kinkdata[a][kinkindex0] + ". What would you like to change this to?\n\n`1`: Kink\n`2`: Likes\n`3`: Unsure or Exploring\n`4`: No Strong Emotions\n`5`: Soft Limit\n`6`: Hard Limit\n`7`: Absolute Limit\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]

                                pref = options[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif "into it" in kinksel:

                        await message.channel.send(embed = discord.Embed(title = "Editing role in " + kinkdata[0][kinkindex0], description = message.author.name + ", " + kinktoedit + "\n\nCurrently, this is set as: " + kinkdata[a][kinkindex0] + ". What would you like to change this to?\n\n`1`: For my characters (Submissive)\n`2`: For other people's characters (Dominant)\n`3`: To watch between other characters (Voyeur)\n`4`: All of the above (Switch)\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = options[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                        except ValueError:

                            await message.channel.send("That isn't a valid integer")

                            await msg2.delete()

                    elif kinksel == "Pronouns":

                        await message.channel.send(embed = discord.Embed(title = "Editing your pronouns", description = message.author.name + ", your pronouns are currently " + kinkdata[a][kinkindex0] + ". What would you like to change them to?\n\nThe format should ideally be the same as He/Him, so Personal Subject Pronoun/ Personal Object Pronoun.\n\nThis message will timeout in 30 seconds.", colour = embcol))

                        try:

                            msg2 = await client.wait_for('message', timeout = 30, check = check(message.author))

                            msg = int(msg2.content)

                            try:

                                options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]

                                pref = options[msg - 1]

                                await msg2.delete()

                            except IndexError:

                                await message.channel.send("That isn't a valid option.")

                        except asyncio.TimeoutError:

                            await message.channel.send("Message timed out")

                    if pref != "Fail":

                        column_int = kinkindex0

                        start_index = 0

                        letter = ""

                        while column_int > 25 + start_index:

                            letter += chr(65 + int((column_int-start_index)/26) - 1)

                            column_int = column_int - (int((column_int-start_index)/26))*26

                        letter += chr(65 - start_index + (int(column_int)))

                        await message.channel.send(embed = discord.Embed(title = "Edited " + kinkdata[1][kinkindex0], description = "You have set it to: " + pref, colour = embcol))

                        sheet.values().update(spreadsheetId = kinksheet, range = str(letter + str(a+1)), valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[[pref]])).execute()

                        await message.delete()


#Takes a kink as a second input and outputs people who like that kink.
async def kinkplayers(message):
    kinkdata, namestr, targname = await getKinkData(message)

    if not str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "Could not find " + targname.split("#")[0] + "'s kink list", description = "Make sure that <@" + str(targname.id) + "> has completed the (as yet unreleased) kink survey."))

    else:
        kinkdatanum = await getKinkDataNumerical(kinkdata, targname)

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

                    if kinkdata[e][kinkcolumnindex[sel]] == "Kink":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a kink:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append("<@" + str(kinkdata[e][2]) + ">")

                        break

                await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a kink:", description = ", ".join(kinkhavers), colour = embcol))

                await message.delete()

            else:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Kink":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a kink:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append(kinkdata[e][1])

                await message.channel.send(embed = discord.Embed(title = "People who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as a kink:", description = ", ".join(kinkhavers), colour = embcol))

                await message.delete()

            kinkhavers = []

            if message.channel.id == 1009522511844749342:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Likes":

                        if len(", ".join(kinkhavers)) > 3800:

                            await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

                            kinkhavers = []

                        kinkhavers.append("<@" + str(kinkdata[e][2]) + ">")

                        break

                await message.channel.send(embed = discord.Embed(title = "Additionally, people who have " + kinkdata[1][kinkcolumnindex[sel]] + " listed as something they like:", description = ", ".join(kinkhavers), colour = embcol))

            else:

                for e in range(len(kinkdata)):

                    if kinkdata[e][kinkcolumnindex[sel]] == "Likes":

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
            kinkdatanum = await getKinkDataNumerical(kinkdata, targname)

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

                    kinksreq = kinkneeded.split(", ")

                    kinkthoughts = []

                    for d in range(len(kinkdata[1])):

                        for e in range(len(kinksreq)):

                            if kinkdata[1][d] == kinksreq[e]:

                                kinkthoughts.append(kinkdata[1][d] + ": " + kinkdata[a][d])

                    kinkinfo = "\n\n" + str(targname) + "'s kinks for this encounter:\n\n" + "\n".join(kinkthoughts)

                encounter = encounters[colsel][rowsel].replace("{random race}", random.choice(["dragonborn", "dwarf", "elf", "gnome", "half-elf", "halfling", "half-orc", "human", "tiefling", "leonin", "satyr", "owlin", "aarakocra", "aasimar", "air genasi", "bugbear", "centaur", "changeling", "deep gnome", "duergar", "earth genasi", "eladrin", "fairy", "firbolg", "fire genasi", "githyanki", "githzerai", "goblin", "goliath", "harengon", "hobgoblin", "kenku", "kobold", "lizardfolk", "minotaur", "orc", "sea elf", "shadar-kai", "shifter", "tabaxi", "tortle", "triton", "water genasi", "yuan-ti", "kalashtar", "warforged", "astral elf", "autognome", "giff", "hadozee", "plasmoid", "loxodon", "simic hybrid", "vedalken", "verdan", "locathah", "grung", "babbage", "seedling", "chakara"])).replace("dwarfs", "dwarves").replace("elfs", "elves").replace("fairys", "fairies").replace("githyankis", "githyanki").replace("githzerais", "githzerai").replace("lizardfolks", "lizardfolk").replace("shadar-kais", "shadar-kai").replace("yuan-tis", "yuant-ti").replace("locathahs", "locathah").replace("grungs", "grung").replace("{1d4}", str(random.randint(1,4))).replace("{1d6}", str(random.randint(1,6))).replace("{1d8}", str(random.randint(1,8))).replace("{1d10}", str(random.randint(1,10))).replace("{1d12}", str(random.randint(1,12))).replace("{1d20}", str(random.randint(1,20))).replace("{2d4}", str(random.randint(2,8))).replace("{2d6}", str(random.randint(2,12))).replace("{3d4}", str(random.randint(3,12)))

                await message.channel.send(embed = discord.Embed(title = "Random Encounter for " + str(targname) + " in " + room, description = encounter + kinkinfo, colour = embcol))

            else:

                await message.channel.send("Room not found")

#Assist the author in generating their kinklist if they don't already have one.
async def kinkgenerate(message):
    
    kinkdata, namestr, targname = await getKinkData(message)
    if str(message.channel.id) != kinkcreatechannel:
        await message.channel.send(embed = discord.Embed(title = "This is not the place to talk about that.", description = f"We will gladly talk about your deepest desires, <@{targname.id}>. We prefer a bit of privacy for that however. Please use the <#{kinkcreatechannel}> channel to call this command."))
        return
    if str(targname) in str(kinkdata):

        await message.channel.send(embed = discord.Embed(title = "We already know your deepest desires", description = f"Your kinklist is already registered with us, <@{targname.id}>. If you want to edit it, use %kinkedit"))
        return


    threadid = await message.create_thread(name= "Kinklist entry: " + str(len(kinkdata) - 1))

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "Welcome to the kink survey! We will ask you to give us a rating on all sorts of kinks in just a moment. We will go through a couple of categories with plenty of kinks, and when we are done you can look at your kinklist with the %kinklist command, or edit it with the %kinkedit command. Furthermore you can search for users with a certain kink using the %kinkplayers [kink] command, or look at someone else's list with %kinklist [@username]. \n\n Okay, with the formalities out of the way, let us begin..."))
    

    #--------------Prepare variables---------------
    newKinklist = [str(datetime.now()), f"{targname.name}#{targname.discriminator}", f"{targname.id}"] #Contains kink data, will be written into the sheet.
    processFailed = False #Indicates if there was a problem during the process. Prevents writing to the sheet if true
    categories = kinkdata[0] #Categories for embed titles. Contains a lot of empty entries at this point.
    kinksPerCategory = [] #Counts the kinks per category. Needed for category display reasons later.
    kinks = kinkdata[1] #List of all entries of data. CAREFUL! 0-3 ARE NOT KINKS BUT PLAYER INFO.
    #count the entries before "General Preferences" as those are not kinks. Needed to later start the survey at the rightpoint.
    playerInformationEntries = 0
    while ("General Preferences" != categories[playerInformationEntries]):
        playerInformationEntries += 1


    #Count the amount of kinks per category
    i = 0
    for x in range(playerInformationEntries + 1, len(kinkdata[0])):
        i += 1
        if (kinkdata[0][x] != ""):
        
            kinksPerCategory.append(i)
            i = 0
            if (kinkdata[0][x] == "Additional Kinks and Limits"):
                break

    kinksPerCategory.append(len(kinkdata[1]) - len(kinkdata[0]) + 1) #Length of last category has to be figured out this way because of index bounds.
    

    while ("" in categories): #Removes the empty entries from the category row so we can use the category list length properly
        categories.remove("")
    categories.remove("Player Information")


    #--------------Collect information from the user-------------
    #Request user's pronouns.
    try:
        await threadid.send(embed = discord.Embed(title = "Pronouns", description = "First of all: What are your preferred pronouns?\n\nThis message will timeout in 120 seconds."))
        msg = await client.wait_for('message', timeout = 120, check = checkAuthor(message.author))
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

        for y in range(0, categoryKinkCount): #Go over each kink in a category
            kinkname = kinkdata[1][kinkindex]

            print(kinkname)
            #Ask the player about the kink
            if not "into it" in kinkname and not "Additional" in kinkname:   #Everything but the "If you are into it" questions

                await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}), Kink {y+1}/{categoryKinkCount}: {kinkname}", description = f"What are your feelings about {kinkname}?\n\n`1`: Kink\n`2`: Likes\n`3`: Unsure or Exploring\n`4`: No Strong Emotions\n`5`: Soft Limit\n`6`: Hard Limit\n`7`: Absolute Limit\n\nThis message will timeout in 120 seconds.", colour = embcol))

                try:
                    msg2 = await client.wait_for('message', timeout = 120, check = check(message.author))
                    msg = int(msg2.content)

                    try:
                        options = ["Kink", "Likes", "Unsure or Exploring", "No Strong Emotions", "Soft Limit", "Hard Limit", "Absolute Limit"]
                        pref = options[msg - 1]
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

            elif "into it" in kinkname:
                await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}), Kink {y+1}/{categoryKinkCount}: {kinkname}", description = f"{message.author.name}, {kinkname}\n\n`1`: For my characters (Submissive)\n`2`: For other people's characters (Dominant)\n`3`: To watch between other characters (Voyeur)\n`4`: All of the above (Switch)\n\nThis message will timeout in 120 seconds.", colour = embcol))
                try:

                    msg2 = await client.wait_for('message', timeout = 120, check = check(message.author))

                    msg = int(msg2.content)

                    try:
                        options = ["For my characters (Submissive)", "For other people's characters (Dominant)", "To watch between other characters (Voyeur)", "All of the above (Switch)"]
                        pref = options[msg - 1]
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
                print("why am I here.")
                try:
                    await threadid.send(embed = discord.Embed(title = f"{categoryName} ({x+1}/{len(categories)}): {kinkname}", description = f"Do you have any {kinkname} you want to add? List them here!\n\nThis message will timeout in 120 seconds."))
                    msg = await client.wait_for('message', timeout = 120, check = checkAuthor(message.author))
                    pref = str(msg.content)
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

            await threadid.send(embed = discord.Embed(description = f"Registered {kinkname} as {pref}.", colour = embcol))
            newKinklist.append(pref)

            #Increment kinkindex
            kinkindex += 1

    await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "That concludes the kink survey! Thank you for your time. If you change your mind on anything I just asked you about, you can request us to change it with %kinkedit."))

    if processFailed == False: #This means nothing went wrong! We can write the results into the kink sheet.
        sheet.values().update(spreadsheetId = kinksheet, range = f"A{len(kinkdata)+1}", valueInputOption = "USER_ENTERED", body = dict(majorDimension='ROWS', values=[newKinklist])).execute()

    else:
        await threadid.send(embed = discord.Embed(title = "Kink Survey", description = "Something went wrong... Please try again. If this happens again and you don't figure out why, please contact Kendrax or Callum."))

    return



#---------------------------Helper Functions---------------------------------


#Fetches name and ID of author, and loads the kinkdata from the sheet.
async def getKinkData(message):
    kinkdata = sheet.values().get(spreadsheetId = kinksheet, range = "A1:FN2000", majorDimension='ROWS').execute().get("values")
    if "@" in message.content:

        targid = int(str(message.content.split("@")[1]).split(" ")[0].replace("!","").replace("&","").replace(">",""))

        targname = await client.fetch_user(targid)
    else:

        targname = message.author

    namestr = str(targname)
    return kinkdata, namestr, targname


#Converts loaded kinkdata into numerical values.
async def getKinkDataNumerical(kinkdata, targname):
    for a in range(len(kinkdata)):
            if a != 0:
                if str(targname) == str(kinkdata[a][1]):
                    #Convert to Numbers
                    kinkdatanum = copy.deepcopy(kinkdata[a])
                    for b in range(len(kinkdata[1])):
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

    return kinkdatanum