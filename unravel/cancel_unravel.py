import discord

async def register_cancel_command(bot, games, player_games):
    @bot.tree.command(name="cancel_unravel", description="Cancel your ongoing Unravel challenge")
    async def cancel_unravel(interaction: discord.Interaction):
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You are not in an ongoing challenge.", ephemeral=True)
            return

        game_id = player_games[interaction.user.id]
        game = games[game_id]

        if game['player1'] != interaction.user:
            await interaction.response.send_message("Only the player who initiated the challenge can cancel it.", ephemeral=True)
            return

        opponent = game['player2']
        games.pop(game_id)
        player_games.pop(game['player1'].id)
        player_games.pop(game['player2'].id)

        await interaction.response.send_message(f"The challenge against {opponent.display_name} has been canceled.", ephemeral=True)
