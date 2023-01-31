from CommonDefinitions import *
LKChannel = 912559434969022534
ModChannel = 829477815782866956
async def staffVacation(message):
    #Toggle Lorekeeper chat Permissions
    perms = client.get_channel(LKChannel).overwrites_for(message.author)
    readMessages = perms.read_messages
    sendMessages = perms.send_messages

    if "staff vacation" in str(message.author.roles).lower() and "lorekeeper" in str(message.author.roles).lower():
        if sendMessages == True and readMessages == True:
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False
            await client.get_channel(LKChannel).set_permissions(message.author, overwrite=perms)

        perms = client.get_channel(ModChannel).overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages
        if sendMessages == True and readMessages == True and "moderator" in str(message.author.roles).lower():
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False
            await client.get_channel(ModChannel).set_permissions(message.author, overwrite=perms)
        role = discord.utils.get(client.guilds[0].roles,name="Staff Vacation")
        await message.author.remove_roles(role)
        

    elif not("staff vacation" in str(message.author.roles).lower()) and "lorekeeper" in str(message.author.roles).lower():
        if sendMessages == False and readMessages == False:
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            await client.get_channel(LKChannel).set_permissions(message.author, overwrite=perms)


        perms = client.get_channel(ModChannel).overwrites_for(message.author)
        readMessages = perms.read_messages
        sendMessages = perms.send_messages
        if sendMessages == False and readMessages == False and "moderator" in str(message.author.roles).lower():
            perms.send_messages = True
            perms.read_messages = True
            perms.view_channel = True
            await client.get_channel(ModChannel).set_permissions(message.author, overwrite=perms)
        
        role = discord.utils.get(client.guilds[0].roles,name="Staff Vacation")
        await message.author.add_roles(role)

    return