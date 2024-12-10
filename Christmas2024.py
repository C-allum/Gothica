import sqlite3
from enum import Enum
from CommonDefinitions import *
import discord
from discord import app_commands
import EconomyV2
import TupperDatabase


async def naughty_vote(target:discord.user, voter:discord.user, message:discord.message) -> bool:
    message_id = message.id
    if target == voter:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = f"{voter.display_name}, we know you are naughty, but...", description = f"{voter.mention} tried to vote themselves onto our naughty list.", colour = embcol, url = message.jump_url))

    # Check if that person has reacted to that post before
    check = await check_already_voted(voter, message_id)
    if check == True:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = f"Trying to mess with our naughty list, {voter.name}?", description = f"{voter.mention} tried to vote {target.mention} onto the naughty list twice on the same post. We only allow that once per post and person.", colour = embcol, url = message.jump_url))

        return False
    
    # Add the vote to the database if they have not.
    await addVote(target.name, voter.name, datetime.now(), Vote.Naughty, message_id)
    print(f"Naughty vote added to {target.name}")
    return True


async def nice_vote(target:discord.user, voter:discord.user, message:discord.message) -> bool:
    message_id = message.id
    if target == voter:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = f"{voter.display_name}, this wasn't nice!", description = f"{voter.mention} tried to vote themselves onto our nice list. We *should* put them onto our naughty list instead!", colour = embcol, url = message.jump_url))

    # Check if that person has reacted to that post before
    check = await check_already_voted(voter, message_id)
    if check == True:
        await client.get_channel(botchannel).send(embed=discord.Embed(title = f"Trying to mess with our nice list, {voter.name}?", description = f"{voter.mention} tried to vote {target.mention} onto the nice list twice on the same post. We only allow that once per post and person.", colour = embcol, url = message.jump_url))
        return False
    
    # Add the vote to the database if they have not.
    await addVote(target.name, voter.name, datetime.now(), Vote.Nice, message_id)
    #await client.get_channel(botchannel).send(embed=discord.Embed(title = f"{message.author.mention} is apparently too nice for the nice list...", description = f"{voter.mention} tried to vote {message.author.mention} onto the nice list twice on the same post. We only allow that once per post and person.", colour = embcol, url = message.jump_url))
    print(f"Nice vote added to {target.name}")
    return True


@staffgroup.command(
        name="print-christmas-results",
        description="Print NiceNaughtyList"
)
@app_commands.checks.has_role("Verified")
async def show_nice_naughty_results(interaction: discord.Interaction) -> list[(str, int, int)]:
    interaction.response.defer()
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        nice_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = 1 GROUP BY Person ORDER BY Person").fetchall()
        naughty_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = -1 GROUP BY Person ORDER BY Person").fetchall()
        print("Naughty Data:")
        for entry in naughty_data:
            print(entry)
        print("\nNice Data:")
        for entry in nice_data:
            print(entry)
        users = list(set([user for (user, value) in naughty_data + nice_data]))
        scores = []
        for user in users:
            try:
                naughty_score = [-naughty[1] for naughty in naughty_data if naughty[0] == user][0]
            except:
                naughty_score = 0

            try:
                nice_score = [nice[1] for nice in nice_data if nice[0] == user][0]
            except:
                nice_score = 0
                
            scores.append((user, naughty_score, nice_score))
        print("\nMerged Data (user, naughty, nice):")
        for entry in scores:
            print(entry)

    except sqlite3.Error as error:
        print('Error occured fetching list data - ', error)
        
    desc = []
    if not scores:
        desc = ["The Naughty and Nice List is empty!"]
    else:
        user_name_max_length = len(max(users, key=lambda x: len(x)))
        naughty_score_max_length = len(str(max(scores, key=lambda x: len(str(x[1])))[1]))
        nice_score_max_length = len(str(max(scores, key=lambda x: len(str(x[2])))[2]))
        scores.sort(key= lambda x: x[0])
        desc.append("Each players scores for being naughty or being nice:\n\n")
        for (name, naughty, nice) in scores:
            entry = f"```{name:<{user_name_max_length}}  {"Naughty:"} {str(naughty):>{naughty_score_max_length}}  {"Nice:"} {str(nice):>{nice_score_max_length}}\n```"
            if len(desc[-1] + entry) < 4096: 
                desc[-1] += entry
            else:
                desc.append(entry)
            print(entry.strip("`"))

    desc_index = 0
    emb = []
    for elem in desc:
        if desc_index == 0:
            emb.append(discord.Embed(title = "Naughty and Nice List", description = desc[desc_index], colour = embcol))
        else:
            emb.append(discord.Embed(description = desc[desc_index], colour = embcol))
        desc_index += 1
    
    await interaction.response.send_message(embeds=emb)
    return scores


@staffgroup.command(
        name="print-christmas-results_naughty",
        description="Print NaughtyList"
)
@app_commands.checks.has_role("Verified")
async def show_naughty_results(interaction: discord.Interaction) -> list[(str, int)]:
    interaction.response.defer()
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        nice_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = 1 GROUP BY Person ORDER BY Person").fetchall()
        naughty_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = -1 GROUP BY Person ORDER BY Person").fetchall()
        print("Naughty Data:")
        for entry in naughty_data:
            print(entry)
        users = list(set([user for (user, value) in naughty_data + nice_data]))
        scores = []
        for user in users:
            try:
                naughty_score = [-naughty[1] for naughty in naughty_data if naughty[0] == user][0]
            except:
                naughty_score = 0
                
            scores.append((user, naughty_score))
        print("\nMerged Data (user, naughty):")
        for entry in scores:
            print(entry)

    except sqlite3.Error as error:
        print('Error occured fetching list data - ', error)
        
    desc = []
    if not scores:
        desc = ["The Naughty List is empty!"]
    else:
        user_name_max_length = len(max(users, key=lambda x: len(x)))
        naughty_score_max_length = len(str(max(scores, key=lambda x: len(str(x[1])))[1]))
        scores.sort(key= lambda x: x[1], reverse= True)
        desc.append("Each players score for being naughty:\n\n")
        for (name, naughty) in scores:
            entry = f"```{name:<{user_name_max_length}}  {"Naughty:"} {str(naughty):>{naughty_score_max_length}}\n```"
            if len(desc[-1] + entry) < 4096: 
                desc[-1] += entry
            else:
                desc.append(entry)
            print(entry.strip("`"))

    desc_index = 0
    emb = []
    for elem in desc:
        if desc_index == 0:
            emb.append(discord.Embed(title = "Naughty List", description = desc[desc_index], colour = embcol))
        else:
            emb.append(discord.Embed(description = desc[desc_index], colour = embcol))
        desc_index += 1
    
    await interaction.response.send_message(embeds=emb)
    return scores


@staffgroup.command(
        name="print-christmas-results_nice",
        description="Print NiceList"
)
@app_commands.checks.has_role("Verified")
async def show_nice_results(interaction: discord.Interaction) -> list[(str, int)]:
    interaction.response.defer()
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        nice_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = 1 GROUP BY Person ORDER BY Person").fetchall()
        naughty_data = transactionsCursor.execute("SELECT Person, SUM(Vote) FROM NiceNaughtyList WHERE Vote = -1 GROUP BY Person ORDER BY Person").fetchall()
        print("Nice Data:")
        for entry in nice_data:
            print(entry)
        users = list(set([user for (user, value) in naughty_data + nice_data]))
        scores = []
        for user in users:
            try:
                nice_score = [nice[1] for nice in nice_data if nice[0] == user][0]
            except:
                nice_score = 0
                
            scores.append((user, nice_score))
        print("\nMerged Data (user, nice):")
        for entry in scores:
            print(entry)

    except sqlite3.Error as error:
        print('Error occured fetching list data - ', error)
        
    desc = []
    if not scores:
        desc = ["The Nice List is empty!"]
    else:
        user_name_max_length = len(max(users, key=lambda x: len(x)))
        nice_score_max_length = len(str(max(scores, key=lambda x: len(str(x[1])))[1]))
        scores.sort(key= lambda x: x[1], reverse= True)
        desc.append("Each players score for being nice:\n\n")
        for (name, nice) in scores:
            entry = f"```{name:<{user_name_max_length}}  {"Nice:"} {str(nice):>{nice_score_max_length}}\n```"
            if len(desc[-1] + entry) < 4096: 
                desc[-1] += entry
            else:
                desc.append(entry)
            print(entry.strip("`"))

    desc_index = 0
    emb = []
    for elem in desc:
        if desc_index == 0:
            emb.append(discord.Embed(title = "Nice List", description = desc[desc_index], colour = embcol))
        else:
            emb.append(discord.Embed(description = desc[desc_index], colour = embcol))
        desc_index += 1
    
    await interaction.response.send_message(embeds=emb)
    return scores


async def roll_for_christmas_dez_reward_item(reacter:discord.user, message:discord.message, amount_gifted:int):
    gifts_to_add = 0
    percent_chance = int((amount_gifted / 10) * 5)
    while percent_chance >= 100:
        percent_chance -= 100
        gifts_to_add += 1
    
    random_percent = random.randint(0,100)
    if percent_chance >= random_percent:
        gifts_to_add += 1
    
    if gifts_to_add > 0:
        await add_christmas_dez_reward_item(reacter, message, gifts_to_add)

    return


async def add_christmas_dez_reward_item(reacter:discord.user, message:discord.message, amount:int):
    target = message.author

    if target.bot:
        if message.author.id == 876440980356755456:
            await client.get_channel(botchannel).send(embed=discord.Embed(title = f"Do not feed us gifts either.", description = "We will get tummy aches.", colour = embcol, url = message.jump_url))
            return

        #Check if tupper img id in database, if not, check if name + player id combination is. If name + playerid is, update image.
        tup_image_url = message.author.display_avatar
        try:
            playerID, imgURL, charName = await TupperDatabase.lookup(tup_image_url, message)
        except TypeError:
            giver = reacter
            await client.get_channel(botchannel).send(embed=discord.Embed(title = str(giver.display_name) + ": We didn't find the tupper in our database.", description = "The first time a character is awarded dezzies, the post has to be rather new and can't be a long, edited post! Try awarding a different, unedited post of that character. If the issue persists, contact the bot gods. (Note from Kendrax: This is a known bug and I have no clue why this happens.)", colour = embcol, url = message.jump_url))
            return
        target = await client.fetch_user(playerID)

    # Fetch list of christmas items
    item_list = ["spellScroll001", "spellScroll002", "spellScroll003", "spellScroll004"]
    # Choose one of the items at random
    items_to_gift = []
    for i in range(0, amount):
        item = random.choice(item_list) # Choose amount *different* items to gift to reduce duplicates
        while item in items_to_gift:    # Make sure items are different.
            item =  random.choice(item_list)
        items_to_gift.append(item)


    # Add the item to the inventory of the target
    for item_id in items_to_gift:
        item_database_info = [x for x in GlobalVars.itemdatabase[0] if item_id in x][0]
        target_inv_index = GlobalVars.inventoryData.index([x for x in GlobalVars.inventoryData if str(target.id) in x][0])
        item_name = item_database_info[0]
        await EconomyV2.addItemToInventory(target_inv_index, item_id, 1, "", "")
        await EconomyV2.writeInvetorySheet(GlobalVars.inventoryData)

        await client.get_channel(botchannel).send(embed=discord.Embed(title = f"{reacter.name} found an item and gifted it to {target.name} along with the dezzies!", description = f"{target.mention} received 1x {item_name}", colour = embcol, url = message.jump_url))

    
    return


async def check_already_voted(user:discord.User, message_id:int) -> bool:
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        data = transactionsCursor.execute("SELECT Voter FROM NiceNaughtyList WHERE PostID = ? AND Voter = ?", (message_id, user.name,)).fetchall()
        
        # A lists boolean is false if it is empty
        if data:
            return True
        else:
            return False

    except sqlite3.Error as error:
        print('Error occured fetching transaction data - ', error)


# ------------- Database interface ---------------

class Vote(Enum):
    Nice = 1        #nice vote
    Naughty = -1    #naughty vote


#Initialize the Christmas Event database: connect and create a cursor
def initChristmasDataBase():
    print("Initializing Christmas Event database...")    
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        table = """ CREATE TABLE IF NOT EXISTS NiceNaughtyList (
                    Person TEXT NOT NULL,
                    Voter TEXT NOT NULL,
                    Date TEXT NOT NULL,
                    Vote INT NOT NULL,
                    PostID INT NOT NULL
        );"""

        transactionsCursor.execute(table)
        transactionsConnection.commit()
        transactionsConnection.close()

        print("Christmas Event Database initialized.\n")
    
    except sqlite3.Error as error:
        print('Error occured while initializing Christmas Event database - ', error)


@staffgroup.command(
        name="clear-nice-naughty-list",
        description="Clear NiceNaughtyList"
)
@app_commands.checks.has_role("Verified")
#Clear the database
async def clearVotes(interaction):
    #if input("Clear table NiceNaughtyList? (y/[n])").lower() == 'y':
    await interaction.response.defer(ephemeral=True, thinking=False)
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        transactionsCursor.execute("DELETE FROM NiceNaughtyList")
        transactionsConnection.commit()
        transactionsConnection.close()
        
        print("Christmas Event database cleared.\n\n")

    except sqlite3.Error as error:
            print('Error occured while clearing database - ', error)

    await interaction.followup.send("Successfully finished the task!")
    # else:
    #     print("Clearing aborted.")


#Add a vote to the database: Takes a person, a vote, a post ID anda date in datetime format to write to the Database
async def addVote(target:str, voter:str, date:datetime, vote:int, postID:int):
    try:
        transactionsConnection = sqlite3.connect('ChristmasList.db')
        transactionsCursor = transactionsConnection.cursor()

        if date == None:
            date = datetime.now()

        transactionsCursor.execute(f'''INSERT INTO NiceNaughtyList VALUES ('{target}', '{voter}', '{date}', '{vote.value}', '{postID}')''')
        transactionsConnection.commit()
        transactionsConnection.close()

    except sqlite3.Error as error:
        print('Error occured while adding an entry to the database - ', error)

