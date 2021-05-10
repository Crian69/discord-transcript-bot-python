import re
import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', help_command=None, intents=intents)
TOKEN = ''

@client.event
async def on_ready():
    print('Bot Is Ready')


@client.command()
async def transcript(ctx: discord.ext.commands.Context):

    css = '''
        body {
        background-color: #36393e;
        color: #dcddde;
        }
        a {
            color: #0096cf;
        }
        .info {
            display: flex;
            max-width: 100%;
            margin: 0 5px 10px;
        }
        .guild-icon-container {
            flex: 0;
        }
        .guild-icon {
            max-width: 88px;
            max-height: 88px;
        }
        .metadata {
            flex: 1;
            margin-left: 10px;
        }
        .guild-name {
            font-size: 1.4em;
        }
        .channel-name {
            font-size: 1.2em;
        }
        .channel-topic {
            margin-top: 2px;
        }
        .channel-message-count {
            margin-top: 2px;
        }
        .chatlog {
            max-width: 100%;
            margin-bottom: 24px;
        }
        .message-group {
            display: flex;
            margin: 0 10px;
            padding: 15px 0;
            border-top: 1px solid;
        }
        .author-avatar-container {
            flex: 0;
            width: 40px;
            height: 40px;
        }
        .author-avatar {
            border-radius: 50%;
            height: 40px;
            width: 40px;
        }
        .messages {
            flex: 1;
            min-width: 50%;
            margin-left: 20px;
        }
        .author-name {
            font-size: 1em;
            font-weight: 500;
        }
        .timestamp {
            margin-left: 5px;
            font-size: 0.75em;
        }
        .message {
            padding: 2px 5px;
            margin-right: -5px;
            margin-left: -5px;
            background-color: transparent;
            transition: background-color 1s ease;
        }
        .content {
            font-size: 0.9375em;
            word-wrap: break-word;
        }
        .mention {
            color: #7289da;
        }
    '''

    def check_message_mention(msgs: str):
        mentions = re.findall("<@!\\d+>", msgs)
        if not mentions:
            return msgs

        else:
            msg = ''
            for mention in mentions:
                msg = msgs.replace(mention,
                                   f"<span class=\"mention\">@{client.get_user(int(mention[3:-1])).name}</span>")
            return msg

    messages: discord.TextChannel.history = await ctx.channel.history(limit=None, oldest_first=True).flatten()
    f = open(f'transcripts\\{ctx.channel}.html', 'w', encoding="utf-8")

    f.write(
        f'''
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset=utf-8>
            <meta name=viewport content="width=device-width">
            <style>
                {css}
            </style>
        </head>

        <body>
            <div class=info>
                <div class=guild-icon-container><img class=guild-icon src={ctx.guild.icon_url}></div>
                <div class=metadata>
                    <div class=guild-name>{ctx.guild.name}</div>
                    <div class=channel-name>{ctx.channel.name}</div>
                    <div class=channel-message-count>{len(messages)} messages</div>
                </div>
            </div>
        '''
    )
    for message in messages:
        if message.attachments:
            content = f"<img src=\"{message.attachments[0].url}\" width=\"200\" alt=\"embed\" \\>"

        else:
            content = check_message_mention(message.content)

        f.write(f'''
        <div class="message-group">
            <div class="author-avatar-container"><img class=author-avatar src={ctx.author.avatar_url}></div>
            <div class="messages">
                <span class="author-name" >{ctx.author.name}</span><span class="timestamp">{message.created_at.strftime("%b %d, %Y %H:%M")}</span>
                <div class="message">
                    <div class="content"><span class="markdown">{content}</span></div>
                </div>
            </div>
        </div>
        ''')
    f.write('''
            </div>
        </body>
    </html>
    ''')
    f.close()

    await ctx.channel.send(file=discord.File(f'transcripts\\{ctx.channel}.html'))

client.run(TOKEN)