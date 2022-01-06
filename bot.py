"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

Description:
Sentinel is a fully secure password managing Discord bot.

Version: 1.0
"""

import os
import discord
from discord.ext import commands
import discord.utils
from dotenv import load_dotenv, find_dotenv
import utils.encryption as encryption, utils.load as load, utils.extraction as extraction, utils.edit as edit

load_dotenv(find_dotenv())
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=">s")

#On ready event
@client.event
async def on_ready():
    print("The bot is online!!!")

# Once the bot joins the server
@client.event
async def on_guild_join(guild):
    """
    Once the bot joind ther server, it will send
    a welcome message to the main channel and create
    a new category named sentinel and a new channel in
    that category name #sentinel-main. It will also send
    set of welcome message and instruction in the new
    #sentinel-main channel which it created.
    """

    # Embed settings
    embed_first = discord.Embed(
        title='Welcome to Sentinel!',
        description = "Sentinel is a powerful, efficient and fully secure password managing Discord Bot! With password being stored as **Cypher-text**, sentinel assures a secure environment for your password storage.\n\n**The Sentinel Enviornment**\nSentinel provides a safe and secure environment even within any Discord server by creating a private channel for every user. The private channel can only be accessed by user and the bot. Feel free to add, retrieve and update your passwords in the channel.\n\n**Commands**\n1.`>snew`: To start using sentinel, every user must have to run this command in #sentinel-main channel. This will initialise the bot and create a private channel for the user.\n2. `>sadd`: This command will allow user to add the passwords. This command takes in 3 parameters: username, password and website. Example run: `>sadd maverick presario Facebook.com`.\n3. `>sget`: This command will print all the passwords of a user in a beautiful tabular format.\n4. `>sdelete`: This command will allow the user to delete his/her desired password. This command takes 2 parameters: username and website of the desired password to be deleted. Example run: `>sdelete maverick Facebook.com`.\n5. `>sguide`: Get all commands.\n\n**Security levels**\n1. All of the data is securely converted to **Cypher-text** and stored in a secure environment.\n 2. All the password is stored registered with your unique discord ID ensuring no one can access your passwords under any circumstances.\n3. All commands can be run in a private channel allowing no one to see your messages with the bot.",
        color = discord.Color.blue()
    )

    category = discord.utils.get(guild.categories, name="sentinel")
    findChannel = discord.utils.get(guild.channels, name="sentinel-main")
    if category is None:
        categoryNew = await guild.create_category("sentinel") #Create new category
        if findChannel is None:
            channelMain = await guild.create_text_channel("sentinel_main", category=categoryNew)  #Create new main channel
            await channelMain.send(embed=embed_first)   #Main channel message

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Thank you for adding **Sentinel.** For more info, visit #sentinel-main.")
        break


@client.command(name='new')
async def serverSetup(ctx):
    """
    The new command registers a new user into the master database.
    This command also creates a private text channel where only the user
    and the bot are present. This will ensure full security while a user
    is using the bot.
    The master data is stored in binaries which makes it extremely difficult 
    to crack ensuring a first degree safety
    """

    #Embed settings
    embed_newUser = discord.Embed(
        title="Welcome to your private channel!",
        description = "You can access me anytime in this channel. All conversations here will remain between you and me, so feel secured!\n\n**Commands**\n1.`>snew`: To start using sentinel, every user must have to run this command in #sentinel-main channel. This will initialise the bot and create a private channel for the user.\n2. `>sadd`: This command will allow user to add the passwords. This command takes in 3 parameters: username, password and website. Example run: `>sadd maverick presario Facebook.com`.\n3. `>sget`: This command will print all the passwords of a user in a beautiful tabular format.\n4. `>sdelete`: This command will allow the user to delete his/her desired password. This command takes 2 parameters: username and website of the desired password to be deleted. Example run: `>sdelete maverick Facebook.com`.\n5. `>sguide`: Get all commands.",
        color = discord.Color.blue()
    )

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="sentinel")
    member = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    chan = await guild.create_text_channel('{}_sentinel'.format(ctx.author), overwrites=overwrites, category=category)
    await chan.send(embed=embed_newUser)


@client.command(name='add')
async def addPass(ctx, username, password, website):
    """
    This function will help user add a new password to the database.
    Confirmation will be asked from the user before proceeding towards
    registration process which consists of encrytion and addition of data.
    """

    # Embed settings
    ## Embed for confirmation message
    embed_conMessage = discord.Embed(
        title='Confirm details',
        description = "Please confirm the details to be added by reacting to appropriate emoji\n\n**Username:** {}\n**Password:** {}\n**Website:** {}".format(username, password, website),
        color = discord.Color.blue()
    )

    embed_conAdded = discord.Embed(
        title="Details added successfully!",
        color = discord.Color.blue()
    )

    embed_conAbort = discord.Embed(
        title="Process aborted!",
        color = discord.Color.blue()
    )    

    conMessage = await ctx.send(embed=embed_conMessage)
    await conMessage.add_reaction("✅")
    await conMessage.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and reaction.emoji
    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    if reaction.emoji == "✅" and user == ctx.author:
        encryption.decFile("utils/masterData.csv")
        refname = str(ctx.author)
        if (load.loadMaster(username, password, website, refname)):
            await conMessage.delete()
            await ctx.send(embed=embed_conAdded)
        else:
            await ctx.send("Error. Please try again later")
    elif reaction.emoji == "❌" and user == ctx.author:
        await ctx.send(embed=embed_conAbort)
    encryption.encFile("utils/masterData.csv")


@client.command(name='get')
async def getPass(ctx):
    """
    This function will extract all the passwords of the user
    and print them into a table in the channel.
    """

    refUser = str(ctx.author)
    result = extraction.releasePass(refUser)
    await ctx.send("```\n{}\n```".format(result))

@client.command(name='delete')
async def deletePass(ctx, username, website):
    """
    This function will delete the record that user dosent
    wants. It willtake username and website as parameters
    and delete the matching record. 
    """

    refUser = str(ctx.author)
    confirmResult = edit.confirmData(refUser, username, website)
    
    # Embed settings
    embed_confirmation = discord.Embed(
        title="Confirm details",
        description = "Confirm the details you want to delete by reacting to appropriate emoji\n\n```{}```".format(confirmResult),
        color = discord.Color.blue()
    )    

    conMessage = await ctx.send(embed=embed_confirmation)
    await conMessage.add_reaction("✅")
    await conMessage.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and reaction.emoji
    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    if reaction.emoji == "✅" and user == ctx.author:
        if (edit.deletePass(refUser, username, website)):
            await ctx.send("Data deleted successfully!!!")
        else:
            await ctx.send("Error. Please try again later")
    elif reaction.emoji == "❌" and user == ctx.author:
        await ctx.send("Process terminated. Record not deleted.")


@client.command(name='guide')
async def helpCommand(ctx):
    """
    A simple help command which will return bot commands and
    important links.
    """

    # Embed settings
    embed_help = discord.Embed(
        title = "Sentinel help centre",
        description = "**Commands**\n1.`>snew`: To start using sentinel, every user must have to run this command in #sentinel-main channel. This will initialise the bot and create a private channel for the user.\n2. `>sadd`: This command will allow user to add the passwords. This command takes in 3 parameters: username, password and website. Example run: `>sadd maverick presario Facebook.com`.\n3. `>sget`: This command will print all the passwords of a user in a beautiful tabular format.\n4. `>sdelete`: This command will allow the user to delete his/her desired password. This command takes 2 parameters: username and website of the desired password to be deleted. Example run: `>sdelete maverick Facebook.com`.\n5. `>sguide`: Get all commands.\n\n",
        color = discord.Color.blue()
    )

    await ctx.send(embed=embed_help)


client.run(TOKEN)