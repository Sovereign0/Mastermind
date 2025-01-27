import discord
from discord.ext import commands
from discord import app_commands
from BEAUTYCON.beauty_contest import players_scores, hosted_game_active, host_channel, tree  # Correct import path


@tree.command(name="leave_bc", description="Leave the current beauty contest game.")
async def leave_game(interaction: discord.Interaction):
    global players_scores, hosted_game_active

    if interaction.user not in players_scores:
        await interaction.response.send_message("You are not part of the game.")
        return

    # Set the player's lives to 0 to eliminate them
    players_scores[interaction.user] = 0
    await host_channel.send(f'{interaction.user.mention} has exited the game and is eliminated.')

    # Check if this elimination ends the game
    if len(players_scores) == 1:
        await end_game(interaction)

async def end_game(interaction):
    global hosted_game_active
    hosted_game_active = False
    winner = list(players_scores.keys())[0]
    await host_channel.send(f'{winner.mention} wins the game! Thanks for playing Beauty Contest.')
    players_scores.clear()

# Register the command
async def register_leave_game_commands(bot):
    bot.tree.add_command(leave_game)