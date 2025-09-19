import discord
from discord.ext import commands
import asyncio
import random

# ANSI escape code for red text
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"

# Display the ASCII art in red on startup
print(f"""{RED_COLOR}
@@@@@@  @@@@@@@@ @@@@@@@@ @@@      @@@ @@@  @@@ @@@@@@@@
@@!  @@@ @@!      @@!      @@!      @@! @@!@!@@@ @@!
@!@  !@! @!!!:!   @!!!:!   @!!      !!@ @!@@!!@! @!!!:!
!!:  !!! !!:      !!:      !!:      !!: !!:  !!! !!:
 : :. :   :        :       : ::.: : :   ::    :  : :: :::

@@@@@@@   @@@@@@  @@@@@@@                                
@@!  @@@ @@!  @@@   @@!                                  
@!@!@!@  @!@  !@!   @!!                                  
!!:  !!! !!:  !!!   !!:                                  
:: : ::   : :. :     :
{RESET_COLOR}
""")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Permission management
permitted_users = set()
ffa_mode = False

def has_permission():
    async def predicate(ctx):
        return ffa_mode or ctx.author.id in permitted_users
    return commands.check(predicate)

# Embed colors
EMBED_SUCCESS = 0x00FF00  # Green
EMBED_WARNING = 0xFFFF00  # Yellow
EMBED_ERROR = 0xFF0000    # Red

# ...

# Add command permissions
@bot.command()
@has_permission()
async def addCmdPerms(ctx, user: discord.Member):
    permitted_users.add(user.id)
    embed = discord.Embed(description=f"Granted command permissions to user {user.mention}.", color=EMBED_SUCCESS)
    await ctx.send(embed=embed)

# Remove command permissions
@bot.command()
@has_permission()
async def removeCmdPerms(ctx, user: discord.Member):
    if user.id in permitted_users:
        permitted_users.remove(user.id)
        embed = discord.Embed(description=f"Revoked command permissions from user {user.mention}.", color=EMBED_SUCCESS)
    else:
        embed = discord.Embed(description=f"User {user.mention} does not have command permissions.", color=EMBED_WARNING)
    await ctx.send(embed=embed)

# Ban command
@bot.command()
@has_permission()
async def ban(ctx, user: discord.Member):
    if user.id in permitted_users:
        permitted_users.remove(user.id)
        print(f"Removed command permissions from user {user.name} ({user.id}) as they were banned.")
    if user.id in permitted_users or user.id == bot.user.id:
        await timeout_user(ctx, ctx.author, 300)  # Timeout the user for 5 minutes (300 seconds)
        embed = discord.Embed(description=f"You are not allowed to ban users with command permissions or the bot.", color=EMBED_WARNING)
    else:
        try:
            await ctx.guild.ban(user)
            embed = discord.Embed(description=f"User {user.mention} has been banned!", color=EMBED_SUCCESS)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"Could not ban user {user.mention} due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Kick command
@bot.command()
@has_permission()
async def kick(ctx, user: discord.Member):
    if user.id in permitted_users or user.id == bot.user.id:
        await timeout_user(ctx, ctx.author, 300)  # Timeout the user for 5 minutes (300 seconds)
        embed = discord.Embed(description=f"You are not allowed to kick users with command permissions or the bot.", color=EMBED_WARNING)
    else:
        try:
            await user.kick()
            embed = discord.Embed(description=f"User {user.mention} has been kicked!", color=EMBED_SUCCESS)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"Could not kick user {user.mention} due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Timeout command
@bot.command()
@has_permission()
async def time(ctx, user: discord.Member, duration: str):
    if user.id in permitted_users or user.id == bot.user.id:
        await timeout_user(ctx, ctx.author, 300)  # Timeout the user for 5 minutes (300 seconds)
        embed = discord.Embed(description=f"You are not allowed to timeout users with command permissions or the bot.", color=EMBED_WARNING)
    else:
        try:
            time_seconds = parse_time_duration(duration)
            if time_seconds is None:
                raise ValueError("Invalid time format")
            await user.edit(timeout=discord.utils.utcnow() + datetime.timedelta(seconds=time_seconds))
            embed = discord.Embed(description=f"User {user.mention} has been timed out for {duration}!", color=EMBED_SUCCESS)
        except (ValueError, discord.errors.Forbidden):
            embed = discord.Embed(description=f"Could not timeout user {user.mention}.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Change nickname command
@bot.command()
@has_permission()
async def nick(ctx, user: discord.Member, nickname: str):
    try:
        await user.edit(nick=nickname)
        embed = discord.Embed(description=f"Changed nickname of user {user.mention} to {nickname}.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not change nickname of user {user.mention} due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Spam command
@bot.command()
@has_permission()
async def spam(ctx, message: str, times: int):
    if times <= 0 or times > 100:
        embed = discord.Embed(description="The number of times to spam must be between 1 and 100.", color=EMBED_WARNING)
    else:
        for _ in range(times):
            await ctx.send(message)
        embed = discord.Embed(description=f"Spammed the message {times} times.", color=EMBED_SUCCESS)
    await ctx.send(embed=embed)

# Purge command
@bot.command()
@has_permission()
async def purge(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(description=f"Deleted {amount} messages.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not delete messages due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Preset nuke command
@bot.command()
@has_permission()
async def presetNuke(ctx):
    # Perform preset nuke actions
    # ...
    embed = discord.Embed(description="Executed preset nuke!", color=EMBED_SUCCESS)
    await ctx.send(embed=embed)

# Nuke command
@bot.command()
@has_permission()
async def nuke(ctx):
    # Ask questions in the bot console for the nuke
    # ...
    embed = discord.Embed(description="Executed custom nuke!", color=EMBED_SUCCESS)
    await ctx.send(embed=embed)

# Rename channel command
@bot.command()
@has_permission()
async def renameChannel(ctx, new_name: str):
    try:
        await ctx.channel.edit(name=new_name)
        embed = discord.Embed(description=f"Renamed the channel to {new_name}.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not rename the channel due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Delete channel command
@bot.command()
@has_permission()
async def deleteChannel(ctx):
    try:
        await ctx.channel.delete()
        embed = discord.Embed(description="Deleted the channel.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not delete the channel due to insufficient permissions.", color=EMBED_ERROR)
        await ctx.send(embed=embed)

# Create channel command
@bot.command()
@has_permission()
async def createChannel(ctx, name: str):
    try:
        await ctx.guild.create_text_channel(name)
        embed = discord.Embed(description=f"Created a new channel named {name}.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not create a new channel due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Rename server command
@bot.command()
@has_permission()
async def renameServer(ctx, new_name: str):
    try:
        await ctx.guild.edit(name=new_name)
        embed = discord.Embed(description=f"Renamed the server to {new_name}.", color=EMBED_SUCCESS)
    except discord.errors.Forbidden:
        embed = discord.Embed(description=f"Could not rename the server due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Assign role command
@bot.command()
@has_permission()
async def assignRole(ctx, user: discord.Member, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        embed = discord.Embed(description=f"Role '{role_name}' not found.", color=EMBED_ERROR)
    else:
        try:
            await user.add_roles(role)
            embed = discord.Embed(description=f"Assigned role {role_name} to user {user.mention}.", color=EMBED_SUCCESS)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"Could not assign role {role_name} to user {user.mention} due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Remove role command
@bot.command()
@has_permission()
async def removeRole(ctx, user: discord.Member, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        embed = discord.Embed(description=f"Role '{role_name}' not found.", color=EMBED_ERROR)
    else:
        try:
            await user.remove_roles(role)
            embed = discord.Embed(description=f"Removed role {role_name} from user {user.mention}.", color=EMBED_SUCCESS)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"Could not remove role {role_name} from user {user.mention} due to insufficient permissions.", color=EMBED_ERROR)
    await ctx.send(embed=embed)

# Toggle FFA mode command
@bot.command()
@has_permission()
async def toggleFFA(ctx):
    global ffa_mode
    ffa_mode = not ffa_mode
    if ffa_mode:
        embed = discord.Embed(description="FFA mode enabled. All users can now use bot commands.", color=EMBED_SUCCESS)
    else:
        embed = discord.Embed(description="FFA mode disabled. Only users with command permissions can use bot commands.", color=EMBED_SUCCESS)
    await ctx.send(embed=embed)

# Timeout utility function
async def timeout_user(ctx, user: discord.Member, duration: int):
    try:
        await user.edit(timeout=discord.utils.utcnow() + datetime.timedelta(seconds=duration))
        print(f"User {user.name} ({user.id}) has been timed out for {duration} seconds.")
        invite = await ctx.channel.create_invite(max_age=300, max_uses=1, unique=True)
        print(f"Invite link: {invite.url}")
    except discord.errors.Forbidden:
        print(f"Could not timeout user {user.name} ({user.id}) due to insufficient permissions.")
    except Exception as e:
        print(f"Error timing out user {user.name} ({user.id}): {e}")

# Time duration parsing function
def parse_time_duration(duration: str):
    pattern = re.compile(r'(\d+)([smhdw])')
    match = pattern.match(duration)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        elif unit == 'd':
            return value * 86400
        elif unit == 'w':
            return value * 604800
    return None

# ...

def interactive_setup():
    bot_token = input("Bot Token: ")
    server_id = input("Server ID: ")
    user_id = int(input("User ID: "))
    return {
        'bot_token': bot_token,
        'server_id': int(server_id),
        'user_id': user_id
    }

# Run the bot with interactive setup
settings = interactive_setup()
SERVER_ID = settings['server_id']
permitted_users.add(settings['user_id'])
bot.run(settings['bot_token'])
