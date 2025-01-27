import discord
from utils import update_stats
from unravel_logs import log_game_result

async def register_guess_unravel(bot, games, player_games):
    async def end_game(game_id, winner, game):
        await log_game_result(bot, {
            'code1': game['code1'],
            'code2': game['code2'],
            'total_guesses': sum(game['guesses'].values()),
            'guesses': game['guesses'],
            'guesses_list': game['guesses_list']
        }, game['player1'], game['player2'], winner)

        games.pop(game_id)
        player_games.pop(game['player1'].id)
        player_games.pop(game['player2'].id)

    @bot.tree.command(name="guess_unravel", description="Submit your guess for Unravel")
    async def guess_unravel(interaction: discord.Interaction, guess: str):
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            await interaction.response.send_message("Invalid guess. Please enter a 4-digit number with no repeating digits.", ephemeral=True)
            return

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
        for i in range(4):
            if guess[i] == secret_code[i]:
                fames += 1
            elif guess[i] in secret_code:
                dots += 1

        await interaction.response.send_message(f'**YOUR GUESS: {guess}**\n**Fames: {fames} | Dots: {dots}**')

        game['guesses'][interaction.user] += 1
        game['guesses_list'][interaction.user].append(guess)

        if guess == secret_code:
            if 'correct_guesser' in game and game['correct_guesser'] is not None:
                if game['correct_guesser'] == interaction.user:
                    await interaction.channel.send(f'🎉 {interaction.user.mention} guessed it right again! Congratulations! 🎉')
                    # Remove the lines that update total stats separately
                    update_stats(interaction.user, game_type='unravel', won=True)
                    update_stats(game['player1'] if interaction.user == game['player2'] else game['player2'], game_type='unravel', lost=True)

                    # Other updates remain the same


                    await end_game(game_id, interaction.user, game)
                    return
                else:
                    # Check if the second player guessed it correctly within the same number of turns
                    if game['guesses'].get(game['correct_guesser'], float('inf')) > game['guesses'][interaction.user]:
                        await interaction.channel.send(f'🎉 {interaction.user.mention} wins! Congratulations! 🎉')
                        update_stats(interaction.user, game_type='unravel', won=True)
                        update_stats(game['correct_guesser'], game_type='unravel', lost=True)

                        await end_game(game_id, interaction.user, game)
                    else:
                        await interaction.channel.send(f'🎉 Both players guessed correctly! It\'s a draw! 🎉')
                        update_stats(game['player1'], game_type='unravel', draw=True)
                        update_stats(game['player2'], game_type='unravel', draw=True)

                        await end_game(game_id, None, game)
                    return
            else:
                game['correct_guesser'] = interaction.user
                other_player = game['player1'] if interaction.user == game['player2'] else game['player2']
                if game['guesses'][other_player] < game['guesses'][interaction.user]:
                    await interaction.channel.send(f"{other_player.mention} gets one more turn to guess!")
                    game['turn'] = other_player
                    game['extra_turn'] = other_player
                    return
                else:
                    await interaction.channel.send(f'🎉 {interaction.user.mention} guessed it right first and wins! Congratulations! 🎉')
                    update_stats(interaction.user, game_type='unravel', won=True)
                    update_stats(other_player, game_type='unravel', lost=True)

                    await end_game(game_id, interaction.user, game)
                    return

        if game.get('extra_turn') == interaction.user:
            other_player = game['player1'] if interaction.user == game['player2'] else game['player2']
            await interaction.channel.send(f'🎉 {other_player.mention} guessed it right first and wins! Congratulations! 🎉')
            update_stats(other_player, game_type='unravel', won=True)
            update_stats(interaction.user, game_type='unravel', lost=True)


            await end_game(game_id, other_player, game)
            return

        game['turn'] = game['player1'] if interaction.user == game['player2'] else game['player2']
        await interaction.channel.send(f"Now it's {game['turn'].mention}'s turn to guess!")
