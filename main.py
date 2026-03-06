import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Naka-login bilang {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        source_channel_name = "🛠️-gear-stock"
        target_channel_name = "🌎-globalchat"

        if message.channel.name == source_channel_name:
            target_channel = discord.utils.get(message.guild.text_channels, name=target_channel_name)
            if not target_channel:
                print(f"Channel '{target_channel_name}' hindi makita!")
                return

            # Prepare message content safely
            content_to_send = message.content if message.content else None

            # Send embeds if they exist
            if message.embeds:
                for embed in message.embeds:
                    # Clone embed
                    new_embed = discord.Embed(
                        title=embed.title or discord.Embed.Empty,
                        description=embed.description or discord.Embed.Empty,
                        url=embed.url or discord.Embed.Empty,
                        color=embed.color or discord.Embed.Empty,
                        timestamp=embed.timestamp or None
                    )
                    for field in embed.fields:
                        new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
                    if embed.footer.text:
                        new_embed.set_footer(text=embed.footer.text, icon_url=embed.footer.icon_url)
                    if embed.image.url:
                        new_embed.set_image(url=embed.image.url)
                    if embed.thumbnail.url:
                        new_embed.set_thumbnail(url=embed.thumbnail.url)
                    if embed.author.name:
                        new_embed.set_author(name=embed.author.name, url=embed.author.url, icon_url=embed.author.icon_url)

                    await target_channel.send(content=content_to_send, embed=new_embed)
                    content_to_send = None  # avoid sending text again for multiple embeds

            # If only text or attachments
            elif content_to_send:
                await target_channel.send(content_to_send)

            # Forward attachments (images/files)
            for attachment in message.attachments:
                await target_channel.send(file=await attachment.to_file())

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('TOKEN')