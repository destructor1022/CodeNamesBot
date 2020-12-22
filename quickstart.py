# Work with Python 3.6
import discord
from discord.utils import get

import deck

TOKEN = 'Nzg2NjU0OTkyNTQ3MDUzNTkw.X9JjjQ.RUMEFuoa0KnIfWRapG4wuebyOAA'

client = discord.Client()

players = []
playing = False
turn = "bold"


@client.event
async def on_message(message):
    global data, game
    global playing
    global turn
    global players
    var = ['one', 'two', 'three', 'four', 'siddanda',
           'rohit', 'alan', 'sonic', 'five', 'tshk',
           'do', 'will', 'bill', 'salty', 'type',
           'hash', 'table', 'set', 'let', 'edward',
           'utter', 'otter', 'guess', 'help', 'uno']

    if message.content.startswith('!load data'):
        playing = False
        with open('data.txt', 'r') as file:
            data = file.read().split('\n')
        await message.channel.send("Loaded in data")

    if message.content.startswith('!start'):
        turn = "bold"
        playing = True
        game = deck.Deck(data)
        await message.channel.send(game.generate())
        await message.channel.send(game.deck_print(False))
        await message.channel.send("It's " + turn + " team's turn now")
        await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
        await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
        await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")

    if message.content.startswith("!print deck"):
        if playing is True:
            if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                await message.author.send(game.deck_print(True))
            elif "uline spymaster" in [y.name.lower() for y in message.author.roles]:
                await message.author.send(game.deck_print(True))
            else:
                await message.channel.send(game.deck_print(False))
            await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
            await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
            await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")

    if message.content.startswith('!flip'):
        if playing is True:
            word = message.content.split(' ', 1)[1]
            if game.is_in_deck(word):
                if "bold operative" in [y.name.lower() for y in message.author.roles] and turn == "bold":
                    await message.channel.send(("{0.author.mention} " + game.flip(word)).format(message))
                    if game.most_recent.team == "bold":
                        await message.channel.send(("{0.author.mention} " + "hit a good card; go again").format(message))
                        await message.channel.send(game.deck_print(False))
                        await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
                        await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
                        await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")
                    elif game.most_recent.team == "bad":
                        await message.channel.send(
                            ("{0.author.mention} " + "hit a bad card and lost the game").format(message))
                        await message.channel.send("Bold loses; call the end game command")
                    else:
                        await message.channel.send(
                            ("{0.author.mention} " + "hit a " + game.most_recent.team + " card and ended the turn").format(
                                message))
                        turn = 'uline'
                        if game.count_left("uline") == 0:
                            await message.channel.send("Bold loses; call the end game command")
                        else:
                            await message.channel.send("It is now uline team's turn")
                            await message.channel.send(game.deck_print(False))
                            await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
                            await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
                            await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")
                if "uline operative" in [y.name.lower() for y in message.author.roles] and turn == "uline":
                    await message.channel.send(("{0.author.mention} " + game.flip(word)).format(message))
                    if game.most_recent.team == "uline":
                        await message.channel.send(("{0.author.mention} " + "hit a good card; go again").format(message))
                        await message.channel.send(game.deck_print(False))
                        await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
                        await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
                        await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")
                    elif game.most_recent.team == "bad":
                        await message.channel.send(
                            ("{0.author.mention} " + "hit a bad card and lost the game").format(message))
                        await message.channel.send("Uline loses; call the end game command")
                    else:
                        await message.channel.send(
                            ("{0.author.mention} " + "hit a " + game.most_recent.team + " card and ended the turn").format(
                                message))
                        turn = 'bold'
                        if game.count_left("bold") == 0:
                            await message.channel.send("Uline loses; call the end game command")
                        else:
                            await message.channel.send("It is now bold team's turn")
                            await message.channel.send(game.deck_print(False))
                            await message.channel.send("There are " + str(game.count_left("bold")) + " bold cards left")
                            await message.channel.send("There are " + str(game.count_left("uline")) + " uline cards left")
                            await message.channel.send("There are " + str(game.count_left("bad")) + " bad cards left")

    if message.content.startswith("!pass"):
        if turn == "bold":
            turn = "uline"
            await message.channel.send("It is now uline team's turn")
        else:
            turn = "bold"
            await message.channel.send("It is now bold team's turn")

    if message.content.startswith("!end game"):
        playing = False
        for i in players:
            if "bold operative" in [y.name.lower() for y in i.roles]:
                role = get(message.guild.roles, name='bold operative')
                await i.remove_roles(role)
            if "uline operative" in [y.name.lower() for y in i.roles]:
                role = get(message.guild.roles, name='uline operative')
                await i.remove_roles(role)
            if "bold spymaster" in [y.name.lower() for y in i.roles]:
                role = get(message.guild.roles, name='bold spymaster')
                await i.remove_roles(role)
            if "uline spymaster" in [y.name.lower() for y in i.roles]:
                role = get(message.guild.roles, name='uline spymaster')
                await i.remove_roles(role)
        players.clear()

    if message.content.startswith("!bold operative"):
        if playing is not True:
            players.append(message.author)
            if "bold operative" in [y.name.lower() for y in message.author.roles]:
                await message.channel.send("{0.author.mention} was already a bold operative".format(message))
            else:
                role = get(message.author.guild.roles, name='bold operative')
                await message.author.add_roles(role)
                await message.channel.send("{0.author.mention} is now a bold operative".format(message))
                if "uline operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='uline operative')
                    await message.author.remove_roles(role)
                if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold spymaster')
                    await message.author.remove_roles(role)
                if "uline spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='uline spymaster')
                    await message.author.remove_roles(role)

    if message.content.startswith("!uline operative"):
        if playing is not True:
            players.append(message.author)
            if "uline operative" in [y.name.lower() for y in message.author.roles]:
                await message.channel.send("{0.author.mention} was already a uline operative".format(message))
            else:
                role = get(message.author.guild.roles, name='uline operative')
                await message.author.add_roles(role)
                await message.channel.send("{0.author.mention} is now a uline operative".format(message))
                if "bold operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold operative')
                    await message.author.remove_roles(role)
                if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold spymaster')
                    await message.author.remove_roles(role)
                if "uline spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='uline spymaster')
                    await message.author.remove_roles(role)

    if message.content.startswith("!bold spymaster"):
        if playing is not True:
            players.append(message.author)
            if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                await message.channel.send("{0.author.mention} was already a bold spymaster".format(message))
            else:
                role = get(message.author.guild.roles, name='bold spymaster')
                await message.author.add_roles(role)
                await message.channel.send("{0.author.mention} is now a bold spymaster".format(message))
                if "bold operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold operative')
                    await message.author.remove_roles(role)
                if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold spymaster')
                    await message.author.remove_roles(role)
                if "uline operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='uline operative')
                    await message.author.remove_roles(role)

    if message.content.startswith("!uline spymaster"):
        if playing is not True:
            players.append(message.author)
            if "uline spymaster" in [y.name.lower() for y in message.author.roles]:
                await message.channel.send("{0.author.mention} was already a uline spymaster".format(message))
            else:
                role = get(message.author.guild.roles, name='uline spymaster')
                await message.author.add_roles(role)
                await message.channel.send("{0.author.mention} is now a uline spymaster".format(message))
                if "bold operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold operative')
                    await message.author.remove_roles(role)
                if "bold spymaster" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='bold spymaster')
                    await message.author.remove_roles(role)
                if "uline operative" in [y.name.lower() for y in message.author.roles]:
                    role = get(message.guild.roles, name='uline operative')
                    await message.author.remove_roles(role)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
