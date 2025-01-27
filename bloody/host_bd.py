import discord
from discord import app_commands
from bloody.view_bd import BloodyDottyChallengeView
from game import BloodyDotty  # Assuming BloodyDotty is your game class

async def register_host_bd(bot, bloody_dotty, games, player_games):
    @bot.tree.command(name="host_bd", description="Host a game of Bloody Dotty")
    async def host_bd(interaction: discord.Interaction, player: discord.Member):
        # Check if either player is already in a game
        if interaction.user.id in player_games or player.id in player_games:
            await interaction.response.send_message("One of the players is already in a game. Finish that game first.", ephemeral=True)
            return

        # Create a view for the Bloody Dotty challenge
        view = BloodyDottyChallengeView(interaction.user, player, bot, games, player_games)

        await interaction.response.send_message(
            f'{player.mention}, do you want to play Bloody Dotty with {interaction.user.mention}?',
            view=view
        )

        # Wait for the user's response with a 60-second timeout
        timed_out = await view.wait()  # Wait for the view to finish

        if timed_out and not view.is_accepted:
            await interaction.followup.send(f'{interaction.user.mention}, the challenge to {player.mention} timed out.', ephemeral=True)
        elif not view.is_accepted:
            await interaction.followup.send(f'{interaction.user.mention}, the challenge to {player.mention} was rejected.', ephemeral=True)
