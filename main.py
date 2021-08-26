import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Loading environmental variable
load_dotenv('discord.env')
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!")


# Command to roll the dice
@bot.command(pass_context=True)
async def d(ctx, die):

    # Getting username and avatar of user which sent the message
    member = ctx.message.author
    userAvatar = member.avatar_url
    user = ctx.message.author.display_name
    await ctx.message.delete()

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

    # Checking if dice isn't too big
    if int(dice) > 100:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name=die + "Roll: ", value="Too big dice to roll! Max size of dice = 100", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
        await ctx.send(embed=embed)

    elif int(howManyRolls) > 20:
        embed = discord.Embed(color=0x874efe)
        embed.add_field(name=die + "Roll: ", value="Too big number of rolls! Max number of rolls = 20", inline=False)
        embed.set_author(name=user, icon_url=userAvatar)
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
        if howManyRolls == "" or howManyRolls == "1":
            if advantageTest == 1 or advantageTest == 2:

                # It is not possible to do adv/disadv roll when $howManyRolls is less then 2 or more then 2
                if howManyRolls != "2":
                    embed = discord.Embed(color=0x874efe)
                    embed.add_field(name=die + " Roll: ", value="You should roll 2 dices when doing adv/disadv "
                                                                "roll!",
                                    inline=False)
                    embed.set_author(name=user, icon_url=userAvatar)
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

            await ctx.send(embed=embed)
        elif advantageTest == 2 and howManyRolls == "2":
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name=die + " Disadvantage roll: ", value=output, inline=False)
            embed.set_thumbnail(url="https://via.placeholder.com/150/" + bgColor + "/FFFFFF/?text=" + str(roll))
            embed.set_author(name=user, icon_url=userAvatar)

            await ctx.send(embed=embed)
        elif advantageTest == 0:
            embed = discord.Embed(color=0x874efe)
            embed.add_field(name=die + " Roll:", value=output, inline=False)
            embed.set_thumbnail(url="https://via.placeholder.com/150/" + bgColor + "/FFFFFF/?text=" + str(roll))
            embed.set_author(name=user, icon_url=userAvatar)
            await ctx.send(embed=embed)


bot.run(TOKEN)
