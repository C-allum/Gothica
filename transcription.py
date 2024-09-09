from CommonDefinitions import *
from discord import app_commands
from discord import SyncWebhook
import aiohttp

async def transcribe(targetThreadId:str, destinationThreadId:str, message=None):
    if not message == None:
        await message.channel.send("Processing, please wait")

    if targetThreadId.startswith("https"):
        targetThreadId = targetThreadId.split("/")[-1]
    elif targetThreadId.startswith("<"):
        targetThreadId = targetThreadId.split("#")[-1].rstrip(">")

    if destinationThreadId.startswith("https"):
        destinationThreadId = destinationThreadId.split("/")[-1]
    elif destinationThreadId.startswith("<"):
        destinationThreadId = destinationThreadId.split("#")[-1].rstrip(">")

    chan = client.get_channel(int(targetThreadId))
    dest = client.get_channel(int(destinationThreadId))
    print("Copying from " + str(chan) + " to " + str(dest))

    messageHistory = [joinedMessages async for joinedMessages in chan.history(limit = None, oldest_first= True)]
    messageHistory.sort(key=lambda x: x.created_at)

    hook = await dest.parent.create_webhook(name= "Clonehook")
    lock = asyncio.Lock()
    
    async with aiohttp.ClientSession() as session:
        whook = SyncWebhook.from_url(hook.url)
        for i in range(len(messageHistory)):
            try:
                if not messageHistory[i].content.startswith("%clone"):
                    whook.send(messageHistory[i].content, username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = dest)
                else:
                    break
            except discord.errors.HTTPException:
                pass
            if messageHistory[i].attachments:
                for b in range(len(messageHistory[i].attachments)):
                    whook.send(messageHistory[i].attachments[b].url, username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = dest)
            if messageHistory[i].embeds:
                whook.send(embed= messageHistory[i].embeds[0], username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = dest)

    await session.close()
    await hook.delete()
    
    if not message == None:
        await message.channel.send("Complete")