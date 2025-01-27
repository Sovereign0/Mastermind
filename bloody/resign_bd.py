import discord
from discord import app_commands
from utils import update_stats

async def register_resign_bd(bot, bloody_dotty, games, player_games, end_game):
    @bot.tree.command(name="resign_bd", description="Resign from your Bloody Dotty game")
    async def resign_bd(interaction: discord.Interaction):
        # Check if the user is in an active game
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You're not currently in a game.", ephemeral=True)
            return

        # Get the current game for the player
        game_id = player_games[interaction.user.id]
        current_game = games.get(game_id)

        if current_game is None:
            await interaction.response.send_message("Could not find the game.", ephemeral=True)
            return

        # Determine the opponent
        opponent = current_game.opponent if interaction.user == current_game.host else current_game.host

        # Update stats
        update_stats(opponent, game_type='bloody_dotty', won=True)
        update_stats(interaction.user, game_type='bloody_dotty', lost=True)

        # End the game and notify players
        await end_game(game_id, opponent, interaction.user)

        # Notify both players
        await interaction.channel.send(f'{interaction.user.mention} has resigned. {opponent.mention} wins!')

        # Clear player data
        player_games.pop(interaction.user.id, None)
        player_games.pop(opponent.id, None)
        games.pop(game_id, None)

        # Optionally, you might want to remove the ongoing game view or interactions if any
        # await current_game.view.stop()  # If using views

        # Acknowledge resignation
        await interaction.response.send_message(f"You have resigned. {opponent.mention} is the winner.", ephemeral=True)
