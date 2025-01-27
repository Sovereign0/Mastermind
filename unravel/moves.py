import discord

async def register_moves_command(bot, games, player_games):
    @bot.tree.command(name="check_moves", description="Check the moves of a player in the ongoing game")
    async def check_moves_target(interaction: discord.Interaction, target: discord.User = None):
        if target is None:
            target = interaction.user

        if target.id not in player_games:
            await interaction.response.send_message(f"{target.display_name} is not in an ongoing game.", ephemeral=True)
            return

        game_id = player_games[target.id]
        game = games[game_id]

        if target not in game['guesses_list']:
            await interaction.response.send_message(f"No moves recorded for {target.display_name}.", ephemeral=True)
            return

        guesses = game['guesses_list'][target]
        feedback = [f"Guess: {guess}, Fames: {sum(1 for i, j in zip(guess, game['code2']) if i == j)}, Dots: {sum(1 for ch in guess if ch in game['code2'])}" for guess in guesses]

        feedback_list = "\n".join(feedback)
        await interaction.channel.send(f"Moves by {target.display_name}:\n{feedback_list}")
