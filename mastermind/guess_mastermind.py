import discord

async def register_guess_mastermind(bot, games, player_games):
    @bot.tree.command(name="guess_mastermind", description="Submit your guess for Mastermind")
    async def guess_mastermind(interaction: discord.Interaction, guess: str):
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You are not in a game.", ephemeral=True)
            return

        game_id = player_games[interaction.user.id]
        game = games[game_id]

        if interaction.user != game['turn']:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        secret_code = game['code2'] if interaction.user == game['player1'] else game['code1']

        fames = 0
        dots = 0
        for i in range(len(secret_code)):
            if guess[i] == secret_code[i]:
                fames += 1
            elif guess[i] in secret_code:
                dots += 1

        await interaction.response.send_message(f'**YOUR GUESS: {guess}**\n**Fames: {fames} | Dots: {dots}**')

        game['guesses'][interaction.user] += 1
        game['guesses_list'][interaction.user].append(guess)

        if guess == secret_code:
            await interaction.channel.send(f'🎉 {interaction.user.mention} guessed it right! Congratulations! 🎉')
            # Logic to handle game end or further turns based on rules.

        # Handle timeout and turn change if necessary
        game['turn'] = game['player1'] if interaction.user == game['player2'] else game['player2']
        await interaction.channel.send(f"Now it's {game['turn'].mention}'s turn to guess!")
        