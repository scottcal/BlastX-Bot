import discord, json, requests, math
from discord.ext import commands
from utils import rpc_module as rpc, parsing

class Masternodes:
    def __init__(self, bot):
        self.bot = bot
        self.rpc = rpc.Rpc()

    @commands.command(pass_context=True)
    async def mninfo(self, ctx):
        """Show masternodes info"""
        channel_name = ctx.message.channel.name
        allowed_channels = parsing.parse_json('config.json')['command_channels'][ctx.command.name]
        if channel_name not in allowed_channels:
            return

        mn_info = self.rpc.listmasternodes()
        block_number = self.rpc.getblockcount()
        total_mn = 0
        active_mn = 0
        curr_block_reward = 3.75  
        curr_mn_reward_percent = 0.85

        for mn in mn_info:
            if (mn["status"] == "ENABLED") or (mn["status"] == "WATCHDOG_EXPIRED"):
               active_mn += 1
            total_mn += 1

        daily_reward = (1/active_mn) * curr_block_reward * 1440 * curr_mn_reward_percent
        weekly_reward = daily_reward * 7
        monthly_reward = daily_reward * 30
        yearly_reward = daily_reward * 365

        avg_reward_freq = (active_mn * 1)/60
        avg_reward_freq_hr = math.floor(avg_reward_freq)
        avg_reward_freq_min = math.floor((avg_reward_freq - avg_reward_freq_hr)*60)
        avg_reward_freq_sec = math.floor((avg_reward_freq - avg_reward_freq_hr - (avg_reward_freq_min/60))*3600)

        roi_days = 2500/daily_reward
        roi_yearly_percent = ((daily_reward * 365)/2500)*100

        coins_locked = total_mn * 2500;

        embed= discord.Embed(colour=0x00FF00)
        embed.set_author(name='BLASTX Masternode Information', icon_url="https://blastexchange.com/Blastx_Logo.png")
        embed.add_field(name="Total Masternodes", value="{}".format(total_mn))
        embed.add_field(name="Active Masternodes", value="{}".format(active_mn))
        embed.add_field(name='\u200b',value='\u200b')
        embed.add_field(name="Daily Income", value="{0:.4f} BLASTX".format(daily_reward))
        embed.add_field(name="Monthly Income", value="{0:.4f} BLASTX".format(monthly_reward))
        embed.add_field(name="Yearly Income", value="{0:.4f} BLASTX".format(yearly_reward))
        embed.add_field(name="Reward Frequency", value="{:02}:{:02}:{:02}".format(avg_reward_freq_hr,avg_reward_freq_min,avg_reward_freq_sec))
        embed.add_field(name="Days to ROI", value="{0:.0f} days".format(roi_days))
        embed.add_field(name="Annual ROI", value="{0:.2f}%".format(roi_yearly_percent))

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Masternodes(bot))

