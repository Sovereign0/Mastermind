import discord

async def register_moves_mastermind(bot, games, player_games):
    @bot.tree.command(name="check_moves_mastermind", description="Check the moves of a Mastermind game")
    async def check_moves_mastermind(interaction: discord.Interaction, target: discord.User = None):
        target = target or interaction.user
        if target.id not in player_games:
            await interaction.response.send_message(f"{target.mention} is not in a game.", ephemeral=True)
            return

        game_id = player_games[target.id]
        game = games[game_id]

        if target not in game['guesses_list']:
            await interaction.response.send_message(f"No moves found for {target.mention}.", ephemeral=True)
            return

        guesses = game['guesses_list'][target]
        await interaction.response.send_message(f"Guesses made by {target.mention}:\n{', '.join(guesses)}", ephemeral=True)
        