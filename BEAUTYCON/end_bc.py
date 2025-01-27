import discord
from discord.ext import commands
from discord import app_commands
from BEAUTYCON.beauty_contest import players_scores, hosted_game_active, host_channel, tree  # Import necessary variables from main.py

@tree.command(name="end_bc", description="Vote to end the current beauty contest game.")
async def end_game_vote(interaction: discord.Interaction):
    if not hosted_game_active:
        await interaction.response.send_message("No game is currently active.")
        return

    end_message = await host_channel.send(
        "Do you want to end the current beauty contest game? React with ✅ to end or ❌ to continue."
    )
    await end_message.add_reaction("✅")
    await end_message.add_reaction("❌")

    def check(reaction, user):
        return (
            user != interaction.user
            and str(reaction.emoji) in ["✅", "❌"]
            and user in players_scores
        )

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        await process_end_game_votes(interaction, end_message)
    except asyncio.TimeoutError:
        await host_channel.send("No decision made. The game will continue.")

async def process_end_game_votes(interaction, message):
    message = await host_channel.fetch_message(message.id)
    end_votes = sum(user.id in players_scores for user in message.reactions[0].users() if user != bot.user)
    continue_votes = sum(user.id in players_scores for user in message.reactions[1].users() if user != bot.user)

    if end_votes > continue_votes:
        await host_channel.send("The game has ended based on majority vote.")
        await end_game(interaction)
    elif continue_votes > end_votes:
        await host_channel.send("The game will continue.")
    else:
        await host_channel.send("No clear majority. The game will continue.")

async def end_game(interaction):
    global hosted_game_active
    hosted_game_active = False
    winner = list(players_scores.keys())[0]
    await host_channel.send(f'{winner.mention} wins the game! Thanks for playing Beauty Contest.')
    players_scores.clear()

# Register the command
async def register_end_game_commands(bot):
    bot.tree.add_command(end_game_vote)
    