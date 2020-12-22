# Work with Python 3.6
import discord
from discord.utils import get

from table import table

TOKEN = 'Nzg2NjU0OTkyNTQ3MDUzNTkw.X9JjjQ.RUMEFuoa0KnIfWRapG4wuebyOAA'

client = discord.Client()


def string_full():
    g = ''
    for i in range(len(sample.group)):
        for j in range(len(sample.group[i])):
            if sample.binary[i][j] == 'norm':
                g = g + '\t\t' + sample.group[i][j]
            elif sample.binary[i][j] == 'bold':
                g = g + '\t\t' + '**' + sample.group[i][j] + '**'
            elif sample.binary[i][j] == 'ulin':
                g = g + '\t\t' + '__' + sample.group[i][j] + '__'
            elif sample.binary[i][j] == 'evil':
                g = g + '\t\t' + '||' + sample.group[i][j] + '||'
        g = g + '\n'
    return g


def string_part():
    g = ''
    for i in range(len(sample.group)):
        for j in range(len(sample.group[i])):
            g = g + '\t\t' + sample.group[i][j]
        g = g + '\n'
    return g


def string_part_reveal():
    g = ''
    for i in range(len(sample.group)):
        for j in range(len(sample.group[i])):
            r = sample.group[i][j]
            if sample.reveal[i][j] > 0:
                r = '~~' + r + '~~'
                if sample.binary[i][j] == 'norm':
                    r = r
                if sample.binary[i][j] == 'bold':
                    r = '**' + r + '**'
                if sample.binary[i][j] == 'ulin':
                    r = '__' + r + '__'
                if sample.binary[i][j] == 'evil':
                    r = '||' + r + '||'
            g = g + '\t\t' + r
        g = g + '\n'
    return g


def string_full_reveal():
    g = ''
    for i in range(len(sample.group)):
        for j in range(len(sample.group[i])):
            r = sample.group[i][j]
            if sample.binary[i][j] == 'norm':
                r = r
            if sample.binary[i][j] == 'bold':
                r = '**' + r + '**'
            if sample.binary[i][j] == 'ulin':
                r = '__' + r + '__'
            if sample.binary[i][j] == 'evil':
                r = '||' + r + '||'
            if sample.reveal[i][j] > 0:
                r = '~~' + r + '~~'
            g = g + '\t\t' + r
        g = g + '\n'
    return g


@client.event
async def on_message(message):
    var = ['one', 'two', 'three', 'four', 'siddanda',
           'rohit', 'alan', 'sonic', 'five', 'tshk',
           'do', 'will', 'bill', 'salty', 'type',
           'hash', 'table', 'set', 'let', 'edward',
           'utter', 'otter', 'guess', 'help', 'uno']
    global sample
    global data
    global team
    global started
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!load_data'):
        started = False
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        with open('data.txt', 'r') as file:
            data = file.read().split('\n')

    if message.content.startswith('!start'):
        team = 'bold'
        started = True
        sample = table(var, 9, 8, 1, 25)
        sample.generate()
        sample.print()
        print(sample.binary)
        await message.channel.send(string_part_reveal())
        await message.channel.send("It's bold team's turn now")

    if message.content.startswith('!spy_master'):
        await message.author.send(string_full_reveal())

    if message.content.startswith('!tap'):
        word = message.content.split(' ', 1)
        test = word[1]
        if any(test in sublist for sublist in sample.group) :
            sample.revealing(test)
            msg = ('{0.author.mention} tapped ' + sample.find_recent()).format(message)
            await message.channel.send(msg)
            await message.channel.send(string_part_reveal())
            if sample.binary[sample.find_recent_x()][sample.find_recent_y()] == 'evil':
                await message.channel.send('{0.author.mention} lost the game'.format(message))
            if team == 'bold':
                if sample.binary[sample.find_recent_x()][sample.find_recent_y()] == 'bold':
                    await message.channel.send('{0.author.mention} hit a bold word; keep going bold team'.format(message))
                else:
                    await message.channel.send('{0.author.mention} did not hit a bold word; ulin team turn'.format(message))
                    team = 'ulin'
            else:
                if sample.binary[sample.find_recent_x()][sample.find_recent_y()] == 'ulin':
                    await message.channel.send('{0.author.mention} hit a ulin word; keep going ulin team'.format(message))
                else:
                    await message.channel.send('{0.author.mention} did not hit a ulin word; bold team turn'.format(message))
                    team = 'bold'
            msg = (str(sample.bold_left()) + " bold words are left").format(message)
            await message.channel.send(msg)
            msg = (str(sample.ulin_left()) + " ulin words are left").format(message)
            await message.channel.send(msg)
        else:
            await message.channel.send("{0.author.mention}, " + test + " is not a word in the list".format(message))

    if message.content.startswith('!pass'):
        msg = ('{0.author.mention} passed for ' + team + ' team').format(message)
        await message.channel.send(msg)
        if team == 'bold':
            team = 'ulin'
        else:
            team = 'bold'
        msg = ('It is now ' + team + " team's turn").format(message)
        await message.channel.send(msg)
        msg = (str(sample.bold_left()) + " bold words are left").format(message)
        await message.channel.send(msg)
        msg = (str(sample.ulin_left()) + " ulin words are left").format(message)
        await message.channel.send(msg)

    if message.content.startswith('!left'):
        msg = (str(sample.bold_left()) + " bold words are left").format(message)
        await message.channel.send(msg)
        msg = (str(sample.ulin_left()) + " ulin words are left").format(message)
        await message.channel.send(msg)

    if message.content.startswith('!team'):
        await message.channel.send(team + "'s turn right now")

    if message.content.startswith("!bold_op"):
        role = get(message.author.guild.roles, name='Bold Operative')
        await message.author.add_roles(role)
        await message.channel.send("{0.author.mention}" + " is now a bold operative")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
