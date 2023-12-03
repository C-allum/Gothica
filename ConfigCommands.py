from CommonDefinitions import *
import json
import yaml
import GlobalVars


async def print_config(message):
    try:
        with open(config_file_path, 'r') as config_file:
            GlobalVars.config = yaml.safe_load(config_file)
            embed_str = ""

            for entry in GlobalVars.config:
                embed_str += "**__" + entry + "__**" + "\n"
                for subentry in GlobalVars.config[entry]:
                    embed_str += "\u1CBC\u1CBC" + "**" + subentry + "**" +": " + str(GlobalVars.config[entry][subentry]) + "\n"
        await message.channel.send(embed = discord.Embed(title = "My Config File", description = embed_str))
    except FileNotFoundError:
        print(f"Config file not found: {config_file_path}")
    except yaml.error.YAMLError:
        print(f"Error parsing yaml in config file: {config_file_path}")

async def print_config_raw(message):
    try:
        with open(config_file_path, 'r') as config_file:
            GlobalVars.config = yaml.safe_load(config_file)
            output =yaml.dump(GlobalVars.config, indent=4)
            output = output.replace(" ", "\u1CBC")
            await message.channel.send(embed = discord.Embed(title = "My Config File", description = yaml.dump(GlobalVars.config, indent=4)))

    except FileNotFoundError:
        print(f"Config file not found: {config_file_path}")
    except yaml.error.YAMLError:
        print(f"Error parsing yaml in config file: {config_file_path}")



async def edit_config(message):
    await message.channel.send("Previous file:")
    await print_config(message)
    await message.channel.send("Editing file...")
    try:
        with open(config_file_path, 'r') as config_file:
            GlobalVars.config = yaml.safe_load(config_file)

        # Split the input string into parts
        parts = message.content.split(maxsplit=3)

        category = parts[1]
        variable = parts[2]
        new_value = parts[3]

        try:
            result = literal_eval(new_value)

            # Check the type of the result
            if isinstance(result, (int, float, str, list, dict)):
                new_value = result
            else:
                new_value = type(result).__name__
        except (SyntaxError, ValueError):
            new_value = new_value



        if category not in GlobalVars.config:
            await message.channel.send(embed = discord.Embed(title = "Error", description = f"Category '{category}' not found in the config"))
            raise ValueError(f"Category '{category}' not found in the config")

        if variable not in GlobalVars.config[category]:
            await message.channel.send(embed = discord.Embed(title = "Error", description = f"Variable '{variable}' not found in the '{category}' category"))
            raise ValueError(f"Variable '{variable}' not found in the '{category}' category")

        # Update the value in the yaml data
        GlobalVars.config[category][variable] = new_value

        # Write the updated data back to the file
        with open(config_file_path, 'w') as config_file:
            yaml.dump(GlobalVars.config, config_file, indent=4)

        print(f"Updated '{variable}' in '{category}' to '{new_value}'")
    except FileNotFoundError:
        print(f"Config file not found: {config_file_path}")
        return
    except yaml.error.YAMLError:
        print(f"Error parsing yaml in config file: {config_file_path}")
        return
    except ValueError as e:
        print(f"Error: {str(e)}")
        return
    await message.channel.send("File editing successful. New file:")
    await print_config(message)
    await message.channel.send("Reloading Config...")
    await reload_config()
    await message.channel.send("Reload completed.")



async def reload_config():
    with open('config.yaml', 'r') as config_file:
        GlobalVars.config = yaml.safe_load(config_file)

    with open('config.yaml', 'w') as yaml_file:
        yaml.dump(GlobalVars.config, yaml_file, default_flow_style=False)
    return
