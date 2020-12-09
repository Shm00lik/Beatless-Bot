import discord
from discord.ext import commands
import random
import asyncio

bot = commands.Bot(command_prefix="b!", description="Play with me something")

@bot.event
async def on_ready():
    print("Bot is ready.")
    bot.options = ['r r r', 'r r b', 'r b r', 'r b b', 'b r r', 'b r b', 'b b r', 'b b b']
    bot.colors = ['r', 'b']
    bot.stats = [0, 0]

@bot.command()
async def play(ctx):
    p1 = ctx.author
    
    embed = discord.Embed(title="Game Starts!", description="Please response with your choice.")

    msg = await ctx.send(embed=embed)

    def check(message):
        return message.content in bot.options

    try:
        response = await bot.wait_for('message', check=check, timeout=30)

    except asyncio.TimeoutError:
        await ctx.send("I waited too long. Game canceled.")

    else:
        choice = response.content.split(' ')

        middle = choice[1]

        if middle == 'r':
            middle = 'b'
        elif middle == 'b':
            middle = 'r'

        comp_choice = [middle, choice[0], choice[1]]
        
        embed = discord.Embed(title="Playing a game...", description=f"Your Choice: `{' '.join(choice)}`\nMy Choice: `{' '.join(comp_choice)}`")

        await msg.edit(embed=embed)

        current_description = f"Your Choice: `{' '.join(choice)}`\nMy Choice: `{' '.join(comp_choice)}`\nCalculating"

        await asyncio.sleep(0.4)
        embed = discord.Embed(title="Playing a game...", description=current_description)

        await msg.edit(embed=embed)

        for x in range(0, 3):
            await asyncio.sleep(0.3)
            current_description += '.'

            embed = discord.Embed(title="Playing a game...", description=current_description)

            await msg.edit(embed=embed)

        await asyncio.sleep(0.75)

        rand_choices = random.choices(bot.colors, k=3)
        print("\n\n\n")

        while True:
            rand_together = ' '.join(rand_choices)
            print(rand_together)

            embed = discord.Embed(title="Playing a game...", description=f"Your Choice: `{' '.join(choice)}`\nMy Choice: `{' '.join(comp_choice)}`\n\nRandom Choices: {rand_together}")

            await msg.edit(embed=embed)

            if check_in(rand_together, ' '.join(choice)):
                await msg.add_reaction("\N{CONFETTI BALL}")
                await asyncio.sleep(3)

                a = await win(msg, rand_together, ' '.join(choice), choice, comp_choice)

                a.title = "\nYou Won!"
                await msg.edit(embed=a)
                
                bot.stats[1] = bot.stats[1] + 1
                break

            elif check_in(rand_together, ' '.join(comp_choice)):
                await msg.add_reaction("\N{CONFETTI BALL}")
                await asyncio.sleep(3)

                a = await win(msg, rand_together, ' '.join(comp_choice), choice, comp_choice)

                a.title = "\nI Won!"
                await msg.edit(embed=a)

                bot.stats[0] = bot.stats[0] + 1
                break

            else:
                rand_choices.append(random.choice(bot.colors))
                await asyncio.sleep(1)

def check_in(rand, choices):
    return choices in rand

async def win(msg, rand, choices, choice, comp_choice):
    _rand = rand.replace(choices, f'**{choices}**')

    for k in range(0, 5):
        embed = discord.Embed(title="Playing a game...", description=f"Your Choice: `{' '.join(choice)}`\nMy Choice: `{' '.join(comp_choice)}`\n\nRandom Choices: {rand if k % 2 == 0 else _rand}")

        await msg.edit(embed=embed)
        await asyncio.sleep(0.3)

    return discord.Embed(title="Playing a game...", description=f"Your Choice: `{' '.join(choice)}`\nMy Choice: `{' '.join(comp_choice)}`\n\nRandom Choices: {_rand}")

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title="Bot Stats", description=f"Victories: {bot.stats[0]}\nLosses: {bot.stats[1]}")
    await ctx.send(embed=embed)
    
bot.run(TOKEN)
