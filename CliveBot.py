import discord 
import responses
import os

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_responses(user_message)
        if response:
            await message.author.send(response) if is_private else await message.channel.send(message.author.mention + response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN:
        raise ValueError("No Discord bot token found in environment variables")

    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print('Rock Solid. {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said : '{user_message}' ({channel})")
        
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)   
