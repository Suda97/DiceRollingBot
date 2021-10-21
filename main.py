import os
import random
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from collections import OrderedDict

# Loading environmental variable
load_dotenv('discord.env')
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", activity=discord.Game(name="with Your lives!"), status=discord.Status.online)


@bot.event
async def on_ready():
    print("Bot connected! PeppoHi!")


# HELP!!!!!!
@bot.command()
async def fate(ctx):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    embed = discord.Embed(color=0x874efe)
    embed.add_field(name="`!fate` output:",
                    value="`!fate` - to see this message;\n"
                          "`!files` - generates server JSON file (type it in as first command!);\n"
                          "`!tracker` - to see tracker;\n"
                          "`!add [Name] [Initiative mod] [Dex score]` - to add character to the tracker (initiative roll);\n"
                          "`!delete [Name]` - to delete character from the tracker;\n"
                          "`!clear` - to clear the tracker (and end battle if it's turned on);\n"
                          "`!battle` - to turn on the battle mode (only works while tracker isn't empty);\n"
                          "`!done` - to end turn in battle mode;\n"
                          "`!r [dice]` - to roll the dice. Example: `d20`, `2d20` (two d20),"
                          "`2d20A` (advantage roll), `2d20D` (disadvantage roll), `d20+10` (roll with mod)", inline=False)
    embed.set_author(name=user, icon_url=userAvatar)
    await ctx.send(embed=embed)


# Command which is used to generate server JSON files
@bot.command()
async def files(ctx):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    serverid = ctx.message.guild.id
    if not os.path.isdir("serverfiles"):
        os.mkdir("serverfiles")
    if not os.path.isfile("serverfiles/" + str(serverid) + ".json"):
        with open("serverfiles/" + str(serverid) + ".json", "+w") as file:
            json.dump({}, file)

        with open("serverfiles/" + str(serverid) + "var.json", "+w") as varfile:
            json.dump({"battle": False, "turn": 1, "maxTurns": 0, "round": 1}, varfile)

        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="`!files` output:", value="Files created!", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Files already exist!", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)


# Command that is used to end the turn of a player
@bot.command()
async def done(ctx):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    serverid = ctx.message.guild.id
    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
        data = json.load(varfile)
    if data["maxTurns"] == 1:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Tracker is empty!\nType `!add [Name] [Initiative mod] [Dex score]` to "
                                             "add character to the tracker.", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    elif not data["battle"]:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Battle mode is turned off!\nType `!battle` to turn it on.", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    if data["turn"] == data["maxTurns"]:
        data["round"] += 1
        data["turn"] = 1
    else:
        data["turn"] += 1
    turn = data["turn"]
    with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
        json.dump(data, outfile)
    with open("serverfiles/" + str(serverid) + ".json", "r") as file:
        data = json.load(file)
        keys = list(data.keys())
    playerTurn = turn - 1
    embed = discord.Embed(color=0x874efe)
    embed.add_field(name=str(keys[playerTurn]) + "'s turn!", value="Type `!done` to end Your turn.", inline=False)
    embed.set_author(name=user, icon_url=userAvatar)
    if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
        with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
            data = json.load(varfile)
        if data["battle"]:
            embed.set_footer(
                text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                    data["round"]))
    await ctx.send(embed=embed)


# Command to clear the tracker
@bot.command()
async def clear(ctx):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    serverid = ctx.message.guild.id
    with open("serverfiles/" + str(serverid) + ".json", "w") as outfile:
        json.dump({}, outfile)
    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
        data = json.load(varfile)
    if data["battle"]:
        with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
            json.dump({"battle": False, "turn": 1, "maxTurns": 0, "round": 1}, outfile)
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="`!clear` output:", value="Tracker cleared and battle ended!", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="`!clear` output:", value="Tracker cleared!", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)


# Command that deletes one character from the tracker
@bot.command()
async def delete(ctx, name=""):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    serverid = ctx.message.guild.id

    if name == "":
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Missing [name] in command!\nType `!delete [name]` to delete character "
                                             "from the tracker", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
            if data["battle"]:
                embed.set_footer(
                    text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                        data["round"]))
        await ctx.send(embed=embed)
    else:
        with open("serverfiles/" + str(serverid) + ".json", "r") as file:
            data = json.load(file)
            keys = list(data.keys())
        i = 0
        for _ in keys:
            if name == keys[i]:
                del data[name]
                with open("serverfiles/" + str(serverid) + ".json", "w") as outfile:
                    json.dump(data, outfile)
                with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                    vardata = json.load(varfile)
                    vardata["maxTurns"] -= 1
                with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
                    json.dump(vardata, outfile)
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name="Tracker:", value=name + " deleted from the tracker!", inline=False)
                embed.set_author(name=user, icon_url=userAvatar)
                if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                        data = json.load(varfile)
                    if data["battle"]:
                        embed.set_footer(
                            text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                                data["round"]))
                await ctx.send(embed=embed)
                return 0
            else:
                i += 1
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="There is no character named: `" + name + "`!", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
            if data["battle"]:
                embed.set_footer(
                    text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                        data["round"]))
        await ctx.send(embed=embed)


# Command that shows tracker
@bot.command()
async def tracker(ctx):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    serverid = ctx.message.guild.id
    if not os.path.isfile("serverfiles/" + str(serverid) + ".json"):
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Cannot find server files!\nType `!files` to generate server files.",
                        inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    else:
        with open("serverfiles/" + str(serverid) + ".json", "r") as file:
            data = json.load(file)
            keys = list(data.keys())
        if keys:
            text = ""
            counter = 0
            for key in keys:
                counter += 1
                text = text + str(counter) + ". " + key + "\n"
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name="Tracker: ", value=text, inline=False)
            embed.set_author(name=user, icon_url=userAvatar)
            if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                    data = json.load(varfile)
                if data["battle"]:
                    embed.set_footer(
                        text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                            data["round"]))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name="Error:", value="Tracker is empty!\nType `!add [Name] [Initiative mod] [Dex score]` "
                                                 "to add character to the tracker.", inline=False)
            embed.set_author(name=user, icon_url=userAvatar)
            await ctx.send(embed=embed)


# Command for initiative roll and adding to tracker
@bot.command()
async def add(ctx, name="", initiative="", dexScore=""):
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()

    if name == "" or initiative == "" or dexScore == "":
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Arguments are empty!\nType `!add [Name] [Initiative mod] [Dex score]` to "
                                             "add character to the tracker.", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        serverid = ctx.message.guild.id
        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
            if data["battle"]:
                embed.set_footer(
                    text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                        data["round"]))
        await ctx.send(embed=embed)
    else:
        serverid = ctx.message.guild.id
        roll = random.randint(1, 20)
        entry = {
            name: {
                "Initiative": roll + int(initiative),
                "DexScore": int(dexScore)
            }
        }

        if os.path.isfile("serverfiles/" + str(serverid) + ".json"):
            with open("serverfiles/" + str(serverid) + ".json", "r") as file:
                data = json.load(file)
                dictout = data | entry
                sorted_dict = OrderedDict()
                sorted_keys = sorted(dictout, key=lambda x: (dictout[x]["Initiative"], dictout[x]["DexScore"]),
                                     reverse=True)
                for key in sorted_keys:
                    sorted_dict[key] = dictout[key]

            with open("serverfiles/" + str(serverid) + ".json", "w") as outfile:
                json.dump(sorted_dict, outfile)

            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
                data["maxTurns"] += 1

            with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
                json.dump(data, outfile)
        else:
            with open("serverfiles/" + str(serverid) + ".json", "+w") as file:
                json.dump({}, file)

            with open("serverfiles/" + str(serverid) + "var.json", "+w") as varfile:
                json.dump({"battle": False, "turn": 1, "maxTurns": 1, "round": 1}, varfile)

            with open("serverfiles/" + str(serverid) + ".json", "r") as file:
                data = json.load(file)
                dictout = data | entry

            with open("serverfiles/" + str(serverid) + ".json", "w") as outfile:
                json.dump(dictout, outfile)

        embed = discord.Embed(color=0x874efe)
        embed.add_field(name=name + " added to tracker: ",
                        value="Initiative: (" + str(roll) + ")+" + initiative + "=" + str(
                            roll + int(initiative)) + "\n Dexterity score: " + dexScore, inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
            if data["battle"]:
                embed.set_footer(
                    text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                        data["round"]))
        await ctx.send(embed=embed)


# Command to turn on battle mode
@bot.command()
async def battle(ctx):
    serverid = ctx.message.guild.id
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()
    if not os.path.isfile("serverfiles/" + str(serverid) + ".json"):
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Cannot find server files!\n Type `!files` to generate server files.",
                        inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)
    else:
        with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
            data = json.load(varfile)
        if data["battle"]:
            with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
                json.dump({"battle": False, "turn": 1, "maxTurns": 0, "round": 1}, outfile)
            with open("serverfiles/" + str(serverid) + ".json", "w") as outfile:
                json.dump({}, outfile)
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name="`!battle` output:", value="It's the end...", inline=False)
            embed.set_author(name=user, icon_url=userAvatar)
            await ctx.send(embed=embed)
        else:
            with open("serverfiles/" + str(serverid) + ".json", "r") as file:
                data = json.load(file)
                keys = list(data.keys())
            if keys:
                with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                    data = json.load(varfile)
                data["battle"] = True
                with open("serverfiles/" + str(serverid) + "var.json", "w") as outfile:
                    json.dump(data, outfile)
                with open("serverfiles/" + str(serverid) + ".json", "r") as file:
                    data = json.load(file)
                    keys = list(data.keys())
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name=str(keys[0]) + "'s turn!", value="Type `!done` to end Your turn", inline=False)
                embed.set_author(name=user, icon_url=userAvatar)
                if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                        data = json.load(varfile)
                    if data["battle"]:
                        embed.set_footer(
                            text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                                data["round"]))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name="Error:", value="Tracker is empty!\nType `!add [Name] [Initiative mod] [Dex "
                                                     "score]` to add character to the tracker.", inline=False)
                embed.set_author(name=user, icon_url=userAvatar)
                await ctx.send(embed=embed)


# Command to roll the dice
@bot.command(pass_context=True)
async def r(ctx, die=""):
    # Getting username and avatar of user which sent the message
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()

    if die == "":
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name="Error:", value="Argument is empty!\n Type `!r 2d20` to roll the dice", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        serverid = ctx.message.guild.id
        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                data = json.load(varfile)
            if data["battle"]:
                embed.set_footer(
                    text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                        data["round"]))
        await ctx.send(embed=embed)
    else:
        # Variables
        i = 0
        dice = ""
        howManyRolls = ""
        modifier = ""
        modifierTest = True
        advantageTest = 0
        natural = 0
        # Filling all the variables
        while i < len(die):
            if die[i] == "d":
                i += 1
                while i < len(die):

                    # Checking (+ Modifier)
                    if die[i] == "+":
                        modifierTest = True
                        i += 1
                        while i < len(die):

                            # Checking if it should be adv or disadv roll
                            if die[i] == "A" or die[i] == "a":
                                advantageTest = 1
                            elif die[i] == "D" or die[i] == "d":
                                advantageTest = 2
                            else:
                                modifier = modifier + die[i]
                            i += 1

                    # Checking (- Modifier)
                    elif die[i] == "-":
                        modifierTest = False
                        i += 1
                        while i < len(die):
                            if die[i] == "A" or die[i] == "a":
                                advantageTest = 1
                            elif die[i] == "D" or die[i] == "d":
                                advantageTest = 2
                            else:
                                modifier = modifier + die[i]
                            i += 1

                    # How big is dice for example d20 or d4
                    else:
                        if die[i] == "A" or die[i] == "a":
                            advantageTest = 1
                        elif die[i] == "D" or die[i] == "d":
                            advantageTest = 2
                        else:
                            dice = dice + die[i]
                    i += 1

            # How many dices to roll
            else:
                howManyRolls = howManyRolls + die[i]
            i += 1

        output = ""
        roll = 0

        if howManyRolls == "":
            howManyRolls = "1"

        # Checking if dice isn't too big
        if int(dice) > 100:
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name=die + "Roll: ", value="Too big dice to roll! Max size of dice = 100", inline=False)
            embed.set_author(name=user, icon_url=userAvatar)
            serverid = ctx.message.guild.id
            if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                    data = json.load(varfile)
                if data["battle"]:
                    embed.set_footer(
                        text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                            data["round"]))
            await ctx.send(embed=embed)
            return 0
        if int(howManyRolls) > 20:
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name=die + "Roll: ", value="Too big number of rolls! Max number of rolls = 20",
                            inline=False)
            embed.set_author(name=user, icon_url=userAvatar)
            serverid = ctx.message.guild.id
            if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                    data = json.load(varfile)
                if data["battle"]:
                    embed.set_footer(
                        text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                            data["round"]))
            await ctx.send(embed=embed)
        else:

            # Creating sequence of values from dice to set their weights for random.choices
            seq = []
            weights = []
            weight = 100 / int(dice)
            for i in range(1, int(dice) + 1):
                seq.append(i)
                weights.append(weight)

            # Checking if second argument is empty (yes: roll only once, no: roll (howManyRolls) many times)
            if howManyRolls == "1":
                if advantageTest == 1 or advantageTest == 2:

                    # It is not possible to do adv/disadv roll when $howManyRolls is less then 2 or more then 2
                    if howManyRolls != "2":
                        embed = discord.Embed(color=0x874efe)
                        embed.add_field(name=die + " Roll: ", value="You should roll 2 dices when doing adv/disadv "
                                                                    "roll!",
                                        inline=False)
                        embed.set_author(name=user, icon_url=userAvatar)
                        serverid = ctx.message.guild.id
                        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                                data = json.load(varfile)
                            if data["battle"]:
                                embed.set_footer(
                                    text="Turn: " + str(data["turn"]) + "/" + str(
                                        data["maxTurns"]) + " | Round: " + str(
                                        data["round"]))
                        await ctx.send(embed=embed)
                else:
                    choice = random.choices(seq, weights)
                    if int(dice) == choice[0]:
                        natural = 1
                    elif choice[0] == 1:
                        natural = 2
                    roll = roll + choice[0]
                    output = output + str(roll)

            # Rolling and summing results
            elif int(howManyRolls) > 1:
                if advantageTest == 1 or advantageTest == 2:

                    # It is not possible to do adv/disadv roll when $howManyRolls is less then 2 or more then 2
                    if howManyRolls != "2":
                        embed = discord.Embed(color=0x874efe)
                        embed.add_field(name=die + " Roll: ", value="You should roll 2 dices when doing adv/disadv "
                                                                    "roll!",
                                        inline=False)
                        embed.set_author(name=user, icon_url=userAvatar)
                        serverid = ctx.message.guild.id
                        if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                            with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                                data = json.load(varfile)
                            if data["battle"]:
                                embed.set_footer(
                                    text="Turn: " + str(data["turn"]) + "/" + str(
                                        data["maxTurns"]) + " | Round: " + str(
                                        data["round"]))
                        await ctx.send(embed=embed)

                    # Adv/disadv roll
                    else:
                        choice = random.choices(seq, weights)
                        adv1 = choice[0]
                        choice = random.choices(seq, weights)
                        adv2 = choice[0]

                        if advantageTest == 1:
                            if adv1 > adv2:
                                roll = roll + adv1
                                if adv1 == int(dice):
                                    natural = 1
                                elif adv1 == 1:
                                    natural = 2
                            elif adv2 > adv1:
                                roll = roll + adv2
                                if adv2 == int(dice):
                                    natural = 1
                                elif adv2 == 1:
                                    natural = 2
                            else:
                                roll = roll + adv1
                                if adv1 == int(dice):
                                    natural = 1
                                elif adv1 == 1:
                                    natural = 2

                        elif advantageTest == 2:
                            if adv1 < adv2:
                                roll = roll + adv1
                                if adv1 == int(dice):
                                    natural = 1
                                elif adv1 == 1:
                                    natural = 2
                            elif adv2 < adv1:
                                roll = roll + adv2
                                if adv2 == int(dice):
                                    natural = 1
                                elif adv2 == 1:
                                    natural = 2
                            else:
                                roll = roll + adv1
                                if adv1 == int(dice):
                                    natural = 1
                                elif adv1 == 1:
                                    natural = 2
                        output = "First roll: " + str(adv1) + "\nSecond roll: " + str(adv2) + "\n(" + str(roll) + ")"
                else:
                    output = "("
                    i = 1
                    choice = random.choices(seq, weights)
                    roll = roll + choice[0]
                    output = output + str(choice[0])

                    # Rolling $howManyRolls times and summing all of the results
                    while i < int(howManyRolls):
                        choice = random.choices(seq, weights)
                        roll = roll + choice[0]
                        output = output + "+" + str(choice[0])
                        i += 1
                    output = output + ")"

            # Adding modifier to roll
            if modifier != "":
                if modifierTest:
                    roll = roll + int(modifier)
                    output = output + "+" + str(modifier)
                else:
                    roll = roll - int(modifier)
                    output = output + "-" + str(modifier)

            output = output + "=" + str(roll)
            serverid = ctx.message.guild.id

            if natural == 1:
                bgColor = "00ff00"
            elif natural == 2:
                bgColor = "ff0000"
            else:
                bgColor = "34363C"

            if advantageTest == 1 and howManyRolls == "2":
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name=die + " Advantage roll: ", value=output, inline=False)
                embed.set_thumbnail(url="https://via.placeholder.com/150/" + bgColor + "/FFFFFF/?text=" + str(roll))
                embed.set_author(name=user, icon_url=userAvatar)
                if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                        data = json.load(varfile)
                    if data["battle"]:
                        embed.set_footer(
                            text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                                data["round"]))
                await ctx.send(embed=embed)
            elif advantageTest == 2 and howManyRolls == "2":
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name=die + " Disadvantage roll: ", value=output, inline=False)
                embed.set_thumbnail(url="https://via.placeholder.com/150/" + bgColor + "/FFFFFF/?text=" + str(roll))
                embed.set_author(name=user, icon_url=userAvatar)
                if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                        data = json.load(varfile)
                    if data["battle"]:
                        embed.set_footer(
                            text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                                data["round"]))
                await ctx.send(embed=embed)
            elif advantageTest == 0:
                embed = discord.Embed(color=0x874efe)
                embed.add_field(name=die + " Roll:", value=output, inline=False)
                embed.set_thumbnail(url="https://via.placeholder.com/150/" + bgColor + "/FFFFFF/?text=" + str(roll))
                embed.set_author(name=user, icon_url=userAvatar)
                if os.path.isfile("serverfiles/" + str(serverid) + "var.json"):
                    with open("serverfiles/" + str(serverid) + "var.json", "r") as varfile:
                        data = json.load(varfile)
                    if data["battle"]:
                        embed.set_footer(
                            text="Turn: " + str(data["turn"]) + "/" + str(data["maxTurns"]) + " | Round: " + str(
                                data["round"]))
                await ctx.send(embed=embed)


bot.run(TOKEN)
