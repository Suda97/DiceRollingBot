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

@bot.command()
async def d(ctx, die):
    i = 0
    dice = ""
    howManyRolls = ""
    modifier = ""
    modifierTest = True
    advantageTest = 0
    while i < len(die):
        if die[i] == "d":
            i += 1
            while i < len(die):
                if die[i] == "+":
                    modifierTest = True
                    i += 1
                    while i < len(die):
                        if die[i] == "A" or die[i] == "a":
                            advantageTest = 1
                        elif die[i] == "D" or die[i] == "d":
                            advantageTest = 2
                        else:
                            modifier = modifier + die[i]
                        i += 1
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

                else:
                    dice = dice + die[i]
                i += 1
        else:
            howManyRolls = howManyRolls + die[i]
        i += 1

    output = ""
    roll = 0

    # Checking if dice isn't too big
    if int(dice) > 100:
        await ctx.send("To big dice to roll!")
    else:
        # Creating sequence of values from dice to set their weights for random.choices
        seq = []
        weights = []
        weight = 100 / int(dice)
        for i in range(1, int(dice) + 1):
            seq.append(i)
            weights.append(weight)

        # Checking if second argument is empty (yes: roll only once, no: roll (howManyRolls) many times)
        if howManyRolls == "":
            if advantageTest == 1 or advantageTest == 2:
                if howManyRolls != "2":
                    await ctx.send("You should roll only 2 dices when doing advantage check!")
            else:
                choice = random.choices(seq, weights)
                roll = roll + choice[0]
                output = output + str(roll)
        # Rolling and summing results
        else:
            if advantageTest == 1 or advantageTest == 2:
                if howManyRolls != "2":
                    await ctx.send("You should roll only 2 dices when doing advantage check!")
                else:
                    choice = random.choices(seq, weights)
                    adv1 = choice[0]
                    choice = random.choices(seq, weights)
                    adv2 = choice[0]
                    if advantageTest == 1:
                        if adv1 > adv2:
                            roll = roll + adv1
                        else:
                            roll = roll + adv2
                    elif advantageTest == 2:
                        if adv1 < adv2:
                            roll = roll + adv1
                        else:
                            roll = roll + adv2
                    output = "First roll: " + str(adv1) + "\nSecond roll: " + str(adv2) + "\n(" + str(roll) + ")"
            else:
                output = "("
                i = 1
                choice = random.choices(seq, weights)
                roll = roll + choice[0]
                output = output + str(choice[0])
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
        if (advantageTest == 1 or advantageTest == 2) and howManyRolls == "2":
            embed = discord.Embed(title="Bot Roll", color=0x874efe)
            embed.add_field(name="Your roll: ", value=output, inline=False)
            await ctx.send(embed=embed)
        elif advantageTest == 0:
            embed = discord.Embed(title="Bot Roll", color=0x874efe)
            embed.add_field(name="Your roll: ", value=output, inline=False)
            await ctx.send(embed=embed)


bot.run(TOKEN)
