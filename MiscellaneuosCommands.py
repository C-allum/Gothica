from CommonDefinitions import *

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