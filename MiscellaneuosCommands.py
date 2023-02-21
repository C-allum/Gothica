from CommonDefinitions import *
import random

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

async def wildlust(message):
    if isbot:
        auth = message.author.name
    elif message.author.nick:
        auth = message.author.nick
    else:
        auth = message.author.name
    lewdtable = "Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls|Your arousal increases to its maximum value and you immediately begin making climax saving throws.|Your clothes and armor disappear until you complete a long rest. You are unaware of this fact, and utterly deny any suggestions to the contrary, or attempts to make you wear clothes.|Your body begins to compulsively masturbate. For the next minute, you must succeed on a DC 15 strength check at the start of each of your turns, or spend the turn pleasuring yourself to the best of your ability.|You cast Enlarge/Reduce on your genitals or other sexual traits. Roll 1d6: on a roll of 1-3, you enlarge these parts of your body; on a roll of 4-6 you reduce these parts of your body.|For the next hour whenever you open your mouth to speak, you experience the sensation and of a phantom cock in your mouth.|The last creature you had sexual intercourse with immediately climaxes, and is aware of the source of their climax.|You are petrified for 1d6 hours. While petrified in this way, your erogenous zones remain soft and fleshy, and you experience stimulation as normal.|You immediately grow a 12 inch cock if you do not already have one. If you already have a cock, ignore this result and roll again. This effect lasts until you climax.|For the next 1d6 hours, you can see the genitals and sexual characteristics of other creatures through their clothes.|For the next hour, anytime you climax, all other creatures within 30 ft must also make a climax saving throw, regardless of their current arousal.|You gain a powerful fetish for a random body part. For the next 24 hours, sexual acts or advances using that body part are made against you with advantage.|You lose any and all sexual characteristics, including genitals, until you complete a long rest. While transformed in this way, you may gain arousal, but automatically succeed on climax saving throws|Your pubic hair grows to a length of 12 inches, and is silky soft. It cannot be cut until you complete a long rest, after which it falls out and returns to its natural state.|Your erogenous zones become fully and almost painfully erect for the next 4 hours.|You are infatuated by the next creature you see for 1 hour, or until you climax.|A tiny fey appears on your shoulder and proceeds to kink-shame you for the next 24 hours.|A tiny imp appears on your shoulder and verbally encourages your most perverted sexual appetites for the next 24 hours.|Your breasts increase in size by one size category and begin lactating at high volume and pressure for the next 1d4 hours.|For next 1d4 hours, an ethereal squirrel proceeds to whisper your darkest sexual fantasies into the ear of any creature within 20 ft of you. If the squirrel is killed, 2 more take its place.|For the next 24 hours, you find yourself aroused by the silliest of things. Each time you hear a joke, pun, or other comedic retort, you gain 1d4 psychic arousal.|An illusionary copy of you appears within 5 ft of your current position, and lasts for 1d8 hours. The duplicate shares your appearance, but none of your ingame statistics, and is only interested in helping you get laid.|1d12 spectres appear at random locations within 20 ft of you. They move with you, and perform no actions other than watching you and pleasuring themselves.|For the next hour, the only words you can speak or write in any language are “Fuck Me”|For the next 24 hours, each time you climax, each creature within a 10ft cone must succeed on a dexterity saving throw or be covered in cum and gain 2d6 acid stimulation.|You smell strongly of sex for the next 24 hours. Any attempt to clean or remove this smell instead makes it stronger.|A magical seal appears above your genitals. For the next 1d6 days, you automatically succeed on climax saving throws.|You climax immediately, and the sound and image of your climax is magically broadcast to every creature of age within 1 mile.|A powerful fey appears at a point within 20 ft of you and demands to be brought to climax. If you fail to fulfil their request, they cast bestow curse upon you. If you succeed, they may grant you some form of boon or aid.|Your clothes magically transform to resemble a sexy maid’s outfit. For the next 24 hours, you feel the magical compulsion to cook and clean, after which your clothes return to normal|You cast Arcane Eye. The magical sensor appears within 10 ft a creature currently engaged in sexual intercourse, regardless of range, and projects it’s observations 5 ft in front of you for all to see.|The lower half of your clothes fall to the ground or are otherwise doffed, leaving your naked from the waist down.|If you have a cock, it is transformed into an enormous limp noodle for the next 1d6 hours. If you do not have a cock, ignore this result and roll again.|For the next hour, each of your fingers becomes tipped with a tiny cock|For the next 24 hours, any container you open contains an erect disembodied cock, in addition to any other contents.|A small rainstorm of flexible dildos falls on you, striking you for 1d4 bludgeoning damage. The dildos disappear shortly after falling to the ground.|You cast Grease, centred on yourself|If you have balls, they burst into harmless magical flame. For the next 24 hours, you produce powerful alcoholic drink in place of semen, after which your balls return to normal. If you do not have balls, ignore this result and roll again.|If you have tits, they become covered in a thin layer of frost, and feel cool to the touch. For the next 24 hours, squeezing them causes you to lactate ice-cream, after which your tits return to normal if you do not have tits, ignore this result and roll again.|Your senses are magically altered. For the next minute, you treat damage done to you as stimulation, and stimulation done to you as damage.|You gain the cock of a dragon or similarly sized monster, chosen by the DM. This lasts for 1 hour.|For the next 24 hours, each time you succeed on a knowledge check, you must make a climax saving throw, regardless of your current arousal.|Each creature within 20 ft of you must succeed on a wisdom saving throw or become hyperaroused for 1d4 rounds.|Even the lightest touch thrills your mind with mental pleasure. You gain an extra 1d6 psychic stimulation whenever you gain stimulation from a physical source.|Your hair transforms into 1d4 tentacles for the next hour. These tentacles act on your initiative each round. If you do not command them, they make a sexual act against the nearest creature, or you, if there are no other targets.|You and a random creature within 30 ft swap genitals for the next hour. Stimulation and other sensations affect the original owner of the genitals, rather than the current owner|Your genitals detach from your body and become a tiny creature with the statistics of a homunculus. They reattach or reappear after 24 hours, or if reduced to 0 hit points|For the next 24 hours, your skin flashes through vibrant colors to display your emotions and arousal. Insight checks against you are made at advantage.|For the next 1d6 days, each time you climax, your cum animates into a small elemental sprite with the statistics of a water mephit.|For the next 24 hours, when you climax, your genitals release a small cloud of colourful confetti and the sound of a birthday cheer in place of cum. |You and all creatures within 30 ft of you must succeed on a constitution saving throw or become intoxicated for the next minute|You Cast Evards Black Tentacles centered on yourself. The tentacles deal stimulation instead of damage.|Your Cast the Light Spell targeted on your erogenous zones.|Your Clothes Animate and begin pleasuring you. You gain 1d6 bludgeoning stimulation at the start of each of your turns. This effect lasts until you remove your clothes by succeeding on a strength saving throw.|You Grow Animal Ears and a tail. For the next 24 hours, your speech is magically altered to include cute animal noises and puns, after which the tail and ears disappear.|You transform into a gargantuan dildo for one minute.|For the next minute, if you move more than 5 ft on your turn, your ass cheeks cast the thundeclap cantrip as a free action.|A pair of phallic horns appear on your head, crowned with a halo of flames. These horns remain for one hour, after which they disappear|14 werewolves appear at random points within 30 ft of you. They are fully erect and violently horny.|You cast charm person, targeting a random creature within range.|It all goes to your hips. For the next minute, your size category increases by one, and your intelligence score becomes 8|A large, phallic mushroom bursts from the ground at a point within 5 ft of you. If touched, it moans loudly.|For the next hour, you can only speak or vocalize in animal noises. This does not impact your ability to cast spells with verbal components Wild and Lustful Magic|You cast entangle, centered on yourself. Creatures that end their turn within the spell’s area take 1d4 bludgeoning stimulation.|Your undergarments teleport to the top of your head. If you are not wearing undergarments, someone else’s undergarments teleport to the top of your head.|Error 404, your sex is missing|A succubus appears at a point within 20 ft of you, and makes it their personal mission to seduce you into lecherous acts.|You regain your virginity. You lose proficiency with all sexual implements (including your natural implements) until you cause another creature to climax.|For the next 24 hours, faint and seductive music can be heard playing by any creature within 30 ft of you. Nice.|Your tongue grows to a length of 2 ft, and counts as a +1 sexual implement for the next hour.|You cast Time Stop. Sexual acts you perform while under the effects of this spell do not cause the spell to end.|A wolf or other large canine appears at a point within 5 ft of you and immediately attempts to hump your leg|A random object within 30 ft of you becomes a mimic.|You cast prestidigitation, soiling the pants of the nearest creature other than yourself that is wearing pants.|A market stall full of bread appears within 30 ft of you. Everyone is uncomfortable.|A Ghost appears at a point within 5 ft of you and proceeds to perform oral sex on you for the next minute, or until you climax.|You are showered with the loose pages of a large journal. Each page contains a beautifully rendered images of feet|Sexually degrading writing appears all over your body. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.|You cast Enthral, targeting all creatures within range.|2d6 poisonous snakes appear within 20 ft of you. They have a fly speed of 30 ft, and their bite attacks deal stimulation instead of damage.|A strange nun appears, spanking you for 1d8 bludgeoning damage before disappearing|You cast suggestion on yourself and your nearest ally. The suggestion is to kiss|You are showered in coins and tips. Gain 2cp for every sexual act or advance you have made in the past 24 hours|A bullywug appears from the nearest body of water, and attempts to persuade you into kissing it. The bullywug claims to be royalty of some sort.|You cast haste on yourself. Your skin turns blue for the duration of the spell.|Your genitals are swarmed by an array of tiny harmless lizards for the next 24 hours. The lizards spread to any creature you have sexual intercourse with.| I disembodied voice calls from the distance, encouraging you to “do it for the exposure” each creature that can hear the voice must make a performance check, and lose a number of CP equal to the result.|A for the next minute, an ethereal greatclub hovers over you, attacking any creature you can see that performs a sexual act or advance. The club uses your spell attack modifier when making attacks|If you have a pussy, it transforms into a fragrant flower for the next 1d6 hours. If you do not have a pussy, ignore this result and roll again.|An incredibly attractive goblin appears at a point within 5 ft of you, wearing leather pants and singing words of power. He claims to be a king, and will not leave until you agree to marry him.|You begin drooling uncontrollably, and are unable to close your mouth.|A random barmaid appears, slapping you for 1d4 bludgeoning damage before calling you a pig or a whore and then disappears|If you have tits, you magically grow an additional single breast|A talking squirrel appears at a point within 5 ft of you, and drunkenly accosts you for money before asking if you know where he lives. He seems to be having a very bad day.|For the next minute, any food you touch magically transforms into dick-shaped candies.|A portal to your genitals appears on a random surface within 1000 miles. The portal lasts for 24 hours, and can be used to perform sexual acts.|You cast Hypnotic pattern, centered on your nipples.|If you have a cock, it magically splits into two duplicates of itself for the next 24 hours.|A scarlet “A” appears on your left breast, and is visible through your clothing. It cannot be washed off or cleaned by mundane or magical means for the next 24 hours.|You violently climax in a burst of magical energy, regaining all expended spell slots."
    lewdroll = random.randint(0,99)
    lewdtext = lewdtable.split("|")[lewdroll]
    print(auth + " rolled on the lewd wild magic table")
    await message.delete()
    await message.channel.send(embed = discord.Embed(title= message.author.name + " rolled a " + str(lewdroll+1) + " on the Wild and Lustful Magic Table!", description= lewdtext, colour = embcol))

async def crunch(message):
    try:
        numbrolls = int(message.content.split(" ")[1])
    except IndexError:
        numbrolls = 1
    except TypeError:
        numbrolls = 1
    if numbrolls > 12:
        numbrolls = 12
    dezcost = numbrolls * 10
    userinvs = sheet.values().get(spreadsheetId = EconSheet, range = "A6:ZZ2000", majorDimension = 'ROWS').execute().get("values")
    authorindex = [row[0] for row in userinvs[::4]].index(message.author.name + "#" + message.author.discriminator)
    authorindex *= 4
    authorinv = userinvs[authorindex]
    if int(authorinv[1]) < dezcost:
        await message.channel.send(embed = discord.Embed(title= "You cannot afford this.", description= "It costs 10" + dezzieemj + " to find one of a suitable size to eat. You have only " + str(authorinv[1])))
    else:
        dezresults = []
        for a in range(numbrolls):
            rand = random.randint(0,9)
            if rand == 0:
                #Wildlust
                lustnum = random.randint(1,len(lewdtab))
                dezresults.append("You rolled a " + str(lustnum) + " on the wild magic table:\n" + lewdtab[lustnum])
            elif rand == 1:
                #Broken Tooth
                dezresults.append("You broke a tooth as you bit into the dezzie. " + random.choice(["These *are* rocks, after all.", "You may want to visit the clinic to fix that.", "The tooth fairy has been alerted to your position."]))
            elif rand == 2:
                #Mimic
                dezresults.append("The dezzie turns out to be a mimic. " + random.choice(["It bites back.", "It did not consent to voreplay.", "It seems to like being bitten.", "It tastes oddly metallic"]))
            elif rand == 3:
                #pass out
                dezresults.append(random.choice(["You awake 2 hours later, unaware of what transpired.", "You pass out for 2 hours", "You fall into a deep slumber, awakening about 2 hours later.", "The overwhelming sense of lust paralyses you for two hours."]))
            elif rand == 4:
                #Poisoned
                dezresults.append("Make a constitution save with a DC of 15. On a fail, you are poisoned for 6 hours.")
            elif rand == 5:
                #Change in senses
                dezresults.append(random.choice(["Everything appears slightly more purple.", "You can smell the odour of fresh sex.", "Everything tastes slightly saltier.", "Your egronious zones become more sensitive."]) + " This can only be undone by means of a greater restoration or wish spell")
            elif rand == 6:
                #Goblin transformation
                dezresults.append("Make an inhibition saving throw, with a DC of 14. On a failure, your skin turns pink and you are turned into a goblin for an hour.")
            elif rand == 7:
                #Nothing
                dezresults.append("Nothing seems to happen")
            elif rand == 8:
                #Orgy
                dezresults.append("You have the urge to start an orgy.")
            elif rand == 9:
                #Damage
                dezresults.append("You take 3d8 " + random.choice(["psychic", "bludgeoning", "poison", "piercing", "thunder"]) + random.choice([" damage.", " stimulation."]))
        await message.channel.send(embed = discord.Embed(title="You ate some dezzies!", description= "\n\n".join(dezresults), colour = embcol))
        sheet.values().update(spreadsheetId = EconSheet, range = "B" + str(authorindex+6), valueInputOption = "USER_ENTERED", body = dict(majorDimension='COLUMNS', values=[[(int(authorinv[1]) - dezcost)]])).execute()
