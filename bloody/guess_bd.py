import discord
from discord import app_commands
from utils import update_stats  # Import the update_stats function

async def register_guess_bd(bot, bloody_dotty, games, player_games, end_game):
    @bot.tree.command(name="guess_bd", description="Submit your guess for Bloody Dotty")
    async def guess_bd(interaction: discord.Interaction, guess: int):
        # Check if the user is currently in a game
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You aren't in a game.", ephemeral=True)
            print(f"[DEBUG] {interaction.user.id} attempted to guess but is not in a game.")
            return

        # Retrieve the game ID from player_games
        game_id = player_games[interaction.user.id]
        print(f"[DEBUG] Player {interaction.user.id} is in game {game_id}")

        # Retrieve the current game object using the game_id
        current_game = games.get(game_id)

        if not current_game:
            await interaction.response.send_message("The game could not be found.", ephemeral=True)
            print(f"[DEBUG] No game found with ID {game_id}")
            return

        print(f"[DEBUG] Current game state: {current_game}")

        # Check if the current game's turn is None (shouldn't be the case in a normal flow)
        if current_game.turn is None:
            await interaction.response.send_message("The game state seems corrupted. Please restart.", ephemeral=True)
            print(f"[DEBUG] Game {game_id} has no current turn set. Possible corruption.")
            return

        print(f"[DEBUG] Current turn: {current_game.turn.id}")

        # Ensure it's the player's turn
        if interaction.user != current_game.turn:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            print(f"[DEBUG] Player {interaction.user.id} tried to guess, but it's {current_game.turn.id}'s turn.")
            return

        # Validate the guess
        min_sum = 2  # 1 + 1
        max_sum = 20  # 10 + 10

        # Calculate possible sum range based on the player's own number
        player_number = current_game.host_number if interaction.user.id == current_game.host.id else current_game.opponent_number
        opponent_min = 1
        opponent_max = 10

        possible_min_sum = player_number + opponent_min
        possible_max_sum = player_number + opponent_max

        # Check if the guess is within the possible bounds
        if guess < possible_min_sum or guess > possible_max_sum:
            await interaction.response.send_message(
                f"Impossible guess! Your number is {player_number}, so the sum must be between {possible_min_sum} and {possible_max_sum}. Guess again.",
                ephemeral=True
            )
            print(f"[DEBUG] Invalid guess {guess} by {interaction.user.id}. Valid range: {possible_min_sum}-{possible_max_sum}")
            return

        # Calculate the actual sum
        actual_sum = current_game.host_number + current_game.opponent_number

        if guess == actual_sum:
            await interaction.channel.send(f'🎉 {interaction.user.mention} guessed it right! The sum is {actual_sum}. Congratulations! 🎉')

            # Update the player's stats
            update_stats(interaction.user, game_type='bloody_dotty', won=True)
            opponent = current_game.opponent if interaction.user == current_game.host else current_game.host
            update_stats(opponent, game_type='bloody_dotty', lost=True)

            # End the game
            print(f"[DEBUG] Ending game {game_id} as {interaction.user.id} won.")
            await end_game(game_id, interaction.user, opponent)
            return

        # If the guess was incorrect, switch turns
        current_game.turn = current_game.opponent if interaction.user == current_game.host else current_game.host
        await interaction.channel.send(
            f'{interaction.user.mention} guessed {guess}, which is incorrect! It\'s now {current_game.turn.mention}\'s turn to guess the sum.'
        )
        print(f"[DEBUG] {interaction.user.id} guessed incorrectly. It's now {current_game.turn.id}'s turn.")
