from CommonDefinitions import *
from discord import app_commands
from discord import SyncWebhook
import aiohttp

async def transcribe(sourceThreadId:str, destinationThreadId:str, message=None):
    if not message == None:
        await message.channel.send("Processing, please wait")

    if sourceThreadId.startswith("https"):
        sourceThreadId = sourceThreadId.split("/")[-1]
    elif sourceThreadId.startswith("<"):
        sourceThreadId = sourceThreadId.split("#")[-1].rstrip(">")

    if destinationThreadId.startswith("https"):
        destinationThreadId = destinationThreadId.split("/")[-1]
    elif destinationThreadId.startswith("<"):
        destinationThreadId = destinationThreadId.split("#")[-1].rstrip(">")

    chan = client.get_channel(int(sourceThreadId))
    dest = client.get_channel(int(destinationThreadId))

    print("Copying from " + str(chan) + " to " + str(dest))
    
    await copyFromTo(chan, dest)
    
    if not message == None:
        await message.channel.send("Complete")


@staffgroup.command(name="transcribe", description="Transcribes a channel or thread.")
@app_commands.describe(source = "Channel or thread to create a transcript of.")
@app_commands.describe(destination = "Destination of the transcript.")
async def transcribeSlash(interaction, 
                          source: discord.TextChannel | discord.Thread, 
                          destination: discord.TextChannel | discord.Thread):
    
    await interaction.response.defer(ephemeral = True, thinking = False)
    
    print("Copying from " + str(source) + " to " + str(destination))
    await copyFromTo(source, destination)

    await interaction.followup.send("Transcription complete!")


async def copyFromTo(source: discord.TextChannel | discord.Thread, 
                     destination: discord.TextChannel | discord.Thread):
    
    messageHistory = [joinedMessages async for joinedMessages in source.history(limit = None, oldest_first= True)]
    messageHistory.sort(key=lambda x: x.created_at)

    hook = await destination.parent.create_webhook(name= "Clonehook")
    #lock = asyncio.Lock()
    
    async with aiohttp.ClientSession() as session:
        whook = SyncWebhook.from_url(hook.url)
        for i in range(len(messageHistory)):
            try:
                if not messageHistory[i].content.startswith("%clone"):
                    whook.send(messageHistory[i].content, username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = destination)
                else:
                    break
            except discord.errors.HTTPException:
                pass
            if messageHistory[i].attachments:
                for b in range(len(messageHistory[i].attachments)):
                    whook.send(messageHistory[i].attachments[b].url, username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = destination)
            if messageHistory[i].embeds:
                whook.send(embed= messageHistory[i].embeds[0], username = messageHistory[i].author.name, avatar_url = messageHistory[i].author.avatar, thread = destination)

    await session.close()
    await hook.delete()