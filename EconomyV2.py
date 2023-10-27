from CommonDefinitions import *

async def shop(message):
    if message.content.split(" ", 1)[1].lower() in str(itemlists).lower():
        shopitems = []
        for a in range(len(itemlists)):
            if message.content.split(" ", 1)[1].lower() in itemlists[a].title.lower():

                if (itemlists[a].title == "Random Loot" or itemlists[a].title ==  "Event Items") and not "staff" in str(message.author.roles).lower():
                    await message.channel.send(embed = discord.Embed(title= "This is not a shop", description = "", colour = embcol))
                else:

                    shopitems.append(str(itemdatabase[a][0][15]) + "\n------------------------------------------------------------\n")
                    for b in range(len(itemdatabase[a])):
                        if b != 0:
                            nextitem = str(itemdatabase[a][1][17]) + " **" + str(itemdatabase[a][b][0]) + "**\n  *" + str(itemdatabase[a][b][2]) + "*" + dezzieemj
                            if len("\n".join(shopitems)) + len(nextitem) <= 4096:
                                shopitems.append(nextitem)
                            else:
                                await message.channel.send(embed = discord.Embed(title = str(itemdatabase[a][0][21]) + " " + itemlists[a].title + " " + str(itemdatabase[a][0][21]), description = "\n".join(shopitems), colour = int(itemdatabase[a][0][17])))
                                shopitems = []
                    await message.channel.send(embed = discord.Embed(title = str(itemdatabase[a][0][21]) + " " + itemlists[a].title + " " + str(itemdatabase[a][0][21]), description = "\n".join(shopitems), colour = int(itemdatabase[a][0][17])))
