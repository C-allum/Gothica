from CommonDefinitions import *
from discord import app_commands
import json

#READ THIS!
#To have the persistent view work, add client.add_view(tickets.Ticket_Spawn_Button_View()) to the startup routine

@staffgroup.command(name="generate-ticket-embed", description="Sets up an embed that spawns tickets.")
@app_commands.describe(title = "Title of the embed under which the ticket button will appear")
@app_commands.describe(description = "Description of the embed under which the ticket button will appear")
@app_commands.describe(ticket_title = "Title of the embed in the generated ticket")
@app_commands.describe(ticket_description = "Description of the embed in the generated ticket")
@app_commands.describe(ticket_category_id = "Channel category in which the tickets will appear. Should be only for tickets!")
@app_commands.describe(roles = "The roles that get to see the ticket by default. @ **all** relevant roles.")
@app_commands.describe(current_ticket_number = "The number from which the tickets will start to count (Default 0)")
@discord.app_commands.checks.has_role("Staff")
async def generate_ticket_embed(interaction, title:str, description:str, ticket_category_id:str, ticket_title:str, ticket_description:str, roles:str, current_ticket_number:int = 0):
    await interaction.response.defer(ephemeral=True, thinking=False)

    roles = roles.replace('@', '').replace('&', '').replace('<', '').replace('>', ',').replace(' ', '')[:-1]

    #Check if category ID is valid
    myGuild = client.get_guild(guildid)
    category = myGuild.get_channel(int(ticket_category_id))
    if category is None:
        await interaction.followup.send("The ticket channel category ID is not valid. Try again.")
        return
    
    #Figure out which channel we are in
    current_channel = interaction.channel

    #Generate the custom ID
    custom_id = -1
    views = load_ticket_views()
    for view in views:
        if int(custom_id) < int(view["custom_id"]):
            custom_id = int(view["custom_id"])
    custom_id += 1
    custom_id = str(custom_id)

    member = interaction.user.id
    button_view = Ticket_Spawn_Button_View(int(ticket_category_id), current_ticket_number, ticket_title, ticket_description, custom_id, roles, member)
    save_single_ticket_view(ticket_category_id, current_ticket_number, ticket_title, ticket_description, custom_id, roles, member, "ticket_spawn")
    await current_channel.send(embed=discord.Embed(title=title, description=description, colour = embcol), view=button_view)
    await interaction.followup.send("Success!")

    return


#--- Ticket spawn view ---
class Ticket_Spawn_Button(discord.ui.Button):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        #Make sure custom_id is not something another bot might use as well!
        super().__init__(label=":envelope_with_arrow: Ticket", style=discord.ButtonStyle.green, custom_id=f"ticket_module:{custom_id}")
        self.category_ID = int(category_ID)
        self.current_ticket_number = int(current_ticket_number)
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Generate the new channel
        myGuild = interaction.guild
        category = myGuild.get_channel(self.category_ID)

        if category is None or not isinstance(category, discord.CategoryChannel):
            await interaction.followup.send("Category not found or invalid!", ephemeral=True)
            return

        # Increase the ticket count
        self.current_ticket_number += 1

        # Get member entry
        member_obj = interaction.user

        # Generate the permission override
        overwrites = {
            myGuild.default_role: discord.PermissionOverwrite(read_messages=False),  # Hide for @everyone
            member_obj: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Allow the member to see and interact
        }
        role_ids = self.roles.split(',')
        roles = [myGuild.get_role(role_id) for role_id in role_ids]
        for role in roles:
            if role is not None:  # Ensure the role exists in the guild
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)


        # Create the ticket channel in the category
        new_ticket_channel = await myGuild.create_text_channel(
            name=f"ticket-{self.current_ticket_number}",
            category=category,
            overwrites=overwrites
        )

        # Send the default message in the new channel
        embed = discord.Embed(title=self.default_embed_title, description=self.default_embed_description, color=embcol)
        #Generate the custom ID
        new_custom_id = -1
        views = load_ticket_views()
        for view in views:
            if int(new_custom_id) < int(view["custom_id"]):
                new_custom_id = int(view["custom_id"])
        new_custom_id += 1
        new_custom_id = str(new_custom_id)
        ticket_view = Ticket_Button_View(int(self.category_ID), self.current_ticket_number, "", "", new_custom_id, self.roles, interaction.user.id)
    	
        await new_ticket_channel.send(embed=embed, view=ticket_view)
        increment_ticket_number(self.custom_id)
        save_single_ticket_view(self.category_ID, self.current_ticket_number, "", "", new_custom_id, self.roles, interaction.user.id, "ticket_close")
        await interaction.followup.send(f"Ticket created: {new_ticket_channel.mention}", ephemeral=True)

class Ticket_Spawn_Button_View(discord.ui.View):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        super().__init__(timeout=None)
        self.category_ID = category_ID
        self.current_ticket_number = current_ticket_number
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

        # Pass necessary information to the button
        self.add_item(Ticket_Spawn_Button(self.category_ID, self.current_ticket_number, self.default_embed_title, self.default_embed_description, custom_id, roles, self.member))


#--- Ticket View ---
#Views
class Ticket_Close_Button(discord.ui.Button):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        #Make sure custom_id is not something another bot might use as well!
        super().__init__(label="Close Ticket (Add lock emoji)", style=discord.ButtonStyle.blurple, custom_id=f"ticket_module:{custom_id}")
        self.category_ID = int(category_ID)
        self.current_ticket_number = int(current_ticket_number)
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Generate the new channel
        myGuild = interaction.guild
        category = myGuild.get_channel(self.category_ID)
        channel = interaction.channel

        # Keep existing overwrites, but reset and modify as needed
        new_overwrites = {
            myGuild.default_role: discord.PermissionOverwrite(read_messages=False),  # Deny @everyone access
        }

        role_ids = self.roles.split(',')
        roles = [myGuild.get_role(role_id) for role_id in role_ids]
        for role in roles:
            if role is not None:  # Ensure the role exists in the guild
                new_overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Send the closure message
        embed = discord.Embed(title="Ticket Closed!",description=f"*{interaction.user.name} closed the ticket.*", color=embcol)
        # Only let the default roles see the channel anymore
        await interaction.channel.edit(overwrites=new_overwrites, name=f"Closed-{self.current_ticket_number}")
        # Edit the embed to make the button disappear
        await interaction.message.edit(embed=interaction.message.embeds[0], view=None)
        # Delete the button from the json file
        delete_ticket_entry(self.custom_id)

        #TODO: ADD THE DELETE, REOPEN AND TRANSCRIBE BUTTON VIEW AND GENERATE IT HERE
        #Generate the custom ID
        new_custom_id = -1
        views = load_ticket_views()
        for view in views:
            if int(new_custom_id) < int(view["custom_id"]):
                new_custom_id = int(view["custom_id"])
        new_custom_id += 1
        new_custom_id = str(new_custom_id)
        ticket_closed_view = Ticket_Closed_Button_View(int(self.category_ID), self.current_ticket_number, "", "", new_custom_id, self.roles, self.member)
        view = ticket_closed_view
        save_single_ticket_view(self.category_ID, self.current_ticket_number, "", "", new_custom_id, self.roles, self.member, "ticket_delete_reopen_tanscribe")
        await channel.send(embed=embed, view=view)
        await interaction.followup.send(f"ticket closed", ephemeral=True)

class Ticket_Button_View(discord.ui.View):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        super().__init__(timeout=None)
        self.category_ID = category_ID
        self.current_ticket_number = current_ticket_number
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

        # Pass necessary information to the button
        self.add_item(Ticket_Close_Button(self.category_ID, self.current_ticket_number, self.default_embed_title, self.default_embed_description, custom_id, roles, self.member))


# --- Closed Ticket button view ---
class Ticket_Delete_Button(discord.ui.Button):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        #Make sure custom_id is not something another bot might use as well!
        super().__init__(label="Delete Ticket (Add Stopsign emoji)", style=discord.ButtonStyle.blurple, custom_id=f"ticket_module:{custom_id}")
        self.category_ID = int(category_ID)
        self.current_ticket_number = int(current_ticket_number)
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Generate the new channel
        myGuild = interaction.guild

        channel = interaction.channel

        # Send the closure message
        embed = discord.Embed(title="Deleting ticket!",description=f"*{interaction.user.name} deleted the ticket. Ticket will disappear in 10 seconds.*", color=embcol)
        await channel.send(embed=embed)
        await myGuild.get_channel(logchannel).send(f"{interaction.user.name} deleted Ticket-{self.current_ticket_number}.")
        await asyncio.sleep(10)
        # Delete the button from the json file
        custom_id = self.custom_id.split(":")[1]
        delete_ticket_entry(custom_id)

        await interaction.followup.send(f"ticket closed", ephemeral=True)

        # Delete Channel
        await interaction.channel.delete()

class Ticket_Reopen_Button(discord.ui.Button):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        #Make sure custom_id is not something another bot might use as well!
        super().__init__(label="Reopen Ticket (Add ...some emoji)", style=discord.ButtonStyle.blurple, custom_id=f"ticket_module:{custom_id}")
        self.category_ID = int(category_ID)
        self.current_ticket_number = int(current_ticket_number)
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Generate the new channel
        myGuild = interaction.guild

        channel = interaction.channel
        await interaction.message.edit(embed=interaction.message.embeds[0], view=None)

        # Delete the button from the json file
        custom_id = self.custom_id.split(":")[1]
        delete_ticket_entry(custom_id)

        # Send the reopening message and add button to close again
         #Generate the custom ID
        new_custom_id = -1
        views = load_ticket_views()
        for view in views:
            if int(new_custom_id) < int(view["custom_id"]):
                new_custom_id = int(view["custom_id"])
        new_custom_id += 1
        new_custom_id = str(new_custom_id)
        view = Ticket_Button_View(int(self.category_ID), self.current_ticket_number, "", "", new_custom_id, self.roles, self.member)
        embed = discord.Embed(title="Reopening Ticket!",description=f"*{interaction.user.name} reopened the ticket.*", color=embcol)
        save_single_ticket_view(self.category_ID, self.current_ticket_number, "", "", new_custom_id, self.roles, self.member, "ticket_close")
        await channel.send(embed=embed, view=view)

        # Add the person that opened the ticket back into the channel
        current_overwrites = channel.overwrites

        member_obj = myGuild.get_member(self.member)
        new_overwrites = {
            myGuild.default_role: discord.PermissionOverwrite(read_messages=False),  # Hide for @everyone
            member_obj: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Allow the member to see and interact
        }
        await channel.edit(overwrites={**current_overwrites, **new_overwrites})   

        await interaction.followup.send(f"ticket reopened", ephemeral=True)

class Ticket_Transcribe_Button(discord.ui.Button):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        #Make sure custom_id is not something another bot might use as well!
        super().__init__(label="Transcribe Ticket (Add pencil emoji)", style=discord.ButtonStyle.blurple, custom_id=f"ticket_module:{custom_id}")
        self.category_ID = int(category_ID)
        self.current_ticket_number = int(current_ticket_number)
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Generate the new channel
        myGuild = interaction.guild

        channel = interaction.channel

        # Send the transcription message
        embed = discord.Embed(title="Transcribing ticket!",description=f"*{interaction.user.name} requested a transcription of the ticket. Please let me know which channel / thread we should transcribe into (use #channel-name).*", color=embcol)
        await channel.send(embed=embed)
        try:
            msg = await client.wait_for('message', timeout = 90, check = checkAuthor(interaction.user))
            newdata = msg.content
        except asyncio.TimeoutError:
            await interaction.channel.send("Message timed out")
            return
        print(msg.content)

        # Call the transcribe function with the appropriate channels
        target_channel = msg.content.replace('<', '').replace('>', '').replace('#','')
        source_channel = interaction.channel.id

        await interaction.followup.send(f"ticket transcription successful.", ephemeral=True)


class Ticket_Closed_Button_View(discord.ui.View):
    def __init__(self, category_ID, current_ticket_number, default_embed_title, default_embed_description, custom_id, roles, member):
        super().__init__(timeout=None)
        self.category_ID = category_ID
        self.current_ticket_number = current_ticket_number
        self.default_embed_title = default_embed_title
        self.default_embed_description = default_embed_description
        self.custom_id = custom_id
        self.roles = roles
        self.member = member

        # Pass necessary information to the buttons
        self.add_item(Ticket_Delete_Button(self.category_ID, self.current_ticket_number, self.default_embed_title, self.default_embed_description, f"ticket_bot_del:{custom_id}", roles, member))
        self.add_item(Ticket_Reopen_Button(self.category_ID, self.current_ticket_number, self.default_embed_title, self.default_embed_description, f"ticket_bot_reopen:{custom_id}", roles, member))
        self.add_item(Ticket_Transcribe_Button(self.category_ID, self.current_ticket_number, self.default_embed_title, self.default_embed_description, f"ticket_bot_transcribe:{custom_id}", roles, member))

#------ Json file management functions for saving and loading ------
def save_single_ticket_view(category_ID, current_ticket_number, embed_title, embed_description, custom_id, roles, member, view_type):
    data = {
        "category_ID": category_ID,
        "current_ticket_number": current_ticket_number,
        "embed_title": embed_title,
        "embed_description": embed_description,
        "custom_id": custom_id,
        "roles": roles,
        "member": member,
        "view_type": view_type
    }

    # Save to a JSON file (you can also use a database if preferred)
    with open("persistent_views.json", "a") as file:
        json.dump(data, file)
        file.write("\n")  # Separate each record with a new line

# Function to save all ticket data back to the JSON file
def save_all_ticket_views(ticket_data):
    with open("persistent_views.json", "w") as file:
        for entry in ticket_data:
            json.dump(entry, file)
            file.write("\n")

def load_ticket_views():
    views = []
    try:
        with open("persistent_views.json", "r") as file:
            for line in file:
                data = json.loads(line.strip())
                views.append(data)
    except FileNotFoundError:
        print("No persistent views found.")
    
    return views


# Function to edit the current_ticket_number for a given custom_id
def edit_ticket_number(custom_id, new_ticket_number):
    tickets = load_ticket_views()
    ticket_found = False

    for ticket in tickets:
        if f"ticket_module:{ticket['custom_id']}" == f"ticket_module:{custom_id}":
            ticket["current_ticket_number"] = str(new_ticket_number)
            ticket_found = True
            break
    
    if ticket_found:
        save_all_ticket_views(tickets)
    else:
        print(f"Ticket with custom_id {custom_id} not found.")

# Function to edit the current_ticket_number for a given custom_id
def increment_ticket_number(custom_id):
    tickets = load_ticket_views()
    ticket_found = False

    for ticket in tickets:
        if f"ticket_module:{ticket['custom_id']}" == f"ticket_module:{custom_id}":
            ticket["current_ticket_number"] = str(int(ticket["current_ticket_number"]) + 1)
            ticket_found = True
            break
    
    if ticket_found:
        save_all_ticket_views(tickets)
    else:
        print(f"Ticket with custom_id {custom_id} not found.")

# Function to delete a ticket entry for a given custom_id
def delete_ticket_entry(custom_id):
    tickets = load_ticket_views()
    updated_tickets = [ticket for ticket in tickets if f"ticket_module:{ticket['custom_id']}" != f"ticket_module:{custom_id}"]
    
    if len(tickets) != len(updated_tickets):
        save_all_ticket_views(updated_tickets)
    else:
        print(f"Ticket with custom_id {custom_id} not found.")