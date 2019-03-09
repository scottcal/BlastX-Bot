import discord, json, requests
from discord.ext import commands
from utils import parsing, mysql_module

mysql = mysql_module.Mysql()

class Deposit:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def deposit(self, ctx):
        """ Display my public wallet address to deposit funds  """
        channel_name = ctx.message.channel.name
        allowed_channels = parsing.parse_json('config.json')['command_channels'][ctx.command.name]
        if channel_name not in allowed_channels:
            return

        user = ctx.message.author
        # Check if user exists in db
        mysql.check_for_user(user.id)
        user_addy = mysql.get_address(user.id)
        await self.bot.say(user.mention + "'s Deposit Address: `" + str(user_addy) + "`" + "\n\nRemember to use !balance to check your balance and not an explorer. The address balance and your actual balance are not always the same!\n\n:warning: DISCLAIMER: This is BETA software! Do not send large amounts of BLAST! The developers are not reliable for any lost BLAST! :warning:")

def setup(bot):
    bot.add_cog(Deposit(bot))
