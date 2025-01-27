import json
import os
import discord

log_file = 'unravel_logs.json'

def load_log_channels():
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return json.load(f)
    return {}

def save_log_channels(log_channels):
    with open(log_file, 'w') as f:
        json.dump(log_channels, f)

async def register_log_commands(bot):

    @bot.tree.command(name="setaslogging", description="Set the current channel as the logging channel for Unravel game results")
    async def setaslogging(interaction: discord.Interaction):
        log_channels = load_log_channels()
        guild_id = str(interaction.guild.id)
        log_channels[guild_id] = interaction.channel.id
        save_log_channels(log_channels)
        await interaction.response.send_message(f"This channel has been set as the logging channel for Unravel game results.", ephemeral=True)

async def log_game_result(bot, game_summary, player1, player2, winner):
    log_channels = load_log_channels()
    guild_id = str(player1.guild.id)

    if guild_id in log_channels:
        channel_id = log_channels[guild_id]
        channel = bot.get_channel(channel_id)

        if channel:
            if winner:
                description = f"{winner.mention} won"
                match_status = f"{winner.mention} won"
            else:
                description = "The game ended in a draw"
                match_status = "Draw"

            embed = discord.Embed(title="Unravel Match Summary", description=description, color=0x00ff00)
            embed.add_field(name="Match Status", value=match_status)
            embed.add_field(name="Players", value=f"{player1.mention} and {player2.mention}")
            embed.add_field(name=f"{player1.display_name}'s Number", value=game_summary['code1'])
            embed.add_field(name=f"{player2.display_name}'s Number", value=game_summary['code2'])
            embed.add_field(name="Total Guesses Made", value=game_summary['total_guesses'])
            embed.add_field(name=f"Number of Guesses Made by {player1.display_name}", value=game_summary['guesses'][player1])
            embed.add_field(name=f"Number of Guesses Made by {player2.display_name}", value=game_summary['guesses'][player2])
            embed.add_field(name=f"Guesses Made by {player1.display_name}", value=', '.join(game_summary['guesses_list'][player1]))
            embed.add_field(name=f"Guesses Made by {player2.display_name}", value=', '.join(game_summary['guesses_list'][player2]))

            await channel.send(embed=embed)
