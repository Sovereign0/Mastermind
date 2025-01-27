import discord

async def register_resign_mastermind(bot, games, player_games):
    @bot.tree.command(name="resign_mastermind", description="Resign from your current Mastermind game")
    async def resign_mastermind(interaction: discord.Interaction):
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You are not in a game.", ephemeral=True)
            return

        game_id = player_games[interaction.user.id]
        game = games[game_id]

        other_player = game['player1'] if interaction.user == game['player2'] else game['player2']
        await interaction.channel.send(f"{interaction.user.mention} has resigned! {other_player.mention} wins by default.")

        # Cleanup game data
        games.pop(game_id)
        player_games.pop(game['player1'].id)
        player_games.pop(game['player2'].id)
        