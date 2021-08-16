import os
import random

from discord.ext import commands
from dotenv import load_dotenv

# Loading environmental variable
load_dotenv('discord.env')
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!")


# Command to roll the dice

@bot.command()
async def d(ctx, dice, howManyRolls="", modifier="", advantage=""):
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
            choice = random.choices(seq, weights)
            roll = "" + str(choice[0])

        else:
            i = 0
            roll = 0
            while i < int(howManyRolls):
                choice = random.choices(seq, weights)
                roll = roll + choice[0]
                i += 1

        if modifier != "":
            if modifier[0] == "+":
                roll = roll + int(modifier[1:])
            else:
                roll = roll - int(modifier[1:])

        if advantage == "A":
            choice1 = random.choices(seq, weights)
            choice2 = random.choices(seq, weights)
            if choice1 > choice2:
                roll = choice1
            elif choice2 > choice1:
                roll = choice2
            elif choice2 == choice1:
                roll = choice2

        elif advantage == "D":
            choice1 = random.choices(seq, weights)
            choice2 = random.choices(seq, weights)
            if choice1 > choice2:
                roll = choice2
            elif choice2 > choice1:
                roll = choice1
            elif choice2 == choice1:
                roll = choice2

        await ctx.send(roll)


bot.run(TOKEN)
