import discord
from discord import app_commands
import random

async def register_host_mastermind(bot, games, player_games):
    @bot.tree.command(name="host_mastermind", description="Host a new Mastermind game")
    @app_commands.describe(
        timeout="Enable timeout",
        timeout_duration="Timeout duration in minutes (1-12)",
        code_type="Choose code type",
        start_point="Start point for alphabets (A-J)",
        end_point="End point for alphabets (M-Z)",
        code_length="Code length (4-8 digits/letters)"
    )
    async def host_mastermind(
        interaction: discord.Interaction,
        timeout: str = None,
        timeout_duration: int = None,
        code_type: str = None,
        start_point: str = None,
        end_point: str = None,
        code_length: int = 4
    ):
        # Validate and process timeout
        if timeout is None:
            await interaction.response.send_message("Please specify if the timeout is enabled or disabled.", ephemeral=True)
            return

        if timeout.lower() == 'yes' and timeout_duration is None:
            await interaction.response.send_message("Please specify the timeout duration in minutes (1-12).", ephemeral=True)
            return

        if timeout.lower() == 'yes':
            timeout_minutes = min(max(timeout_duration, 1), 12)
        else:
            timeout_minutes = None

        # Validate and process code type
        if code_type is None:
            await interaction.response.send_message("Please specify the code type: 'numbers' or 'alphabets'.", ephemeral=True)
            return

        if code_type.lower() == 'numbers':
            code_length = min(max(code_length, 4), 6)
            secret_code = "".join(random.sample("0123456789", code_length))
        elif code_type.lower() == 'alphabets':
            if start_point is None or end_point is None:
                await interaction.response.send_message("Please specify both start point and end point for alphabets.", ephemeral=True)
                return

            start_point = start_point.upper()
            end_point = end_point.upper()

            if ord(end_point) - ord(start_point) < 10:
                await interaction.response.send_message("The gap between start and end points should be at least 10 letters.", ephemeral=True)
                return

            alphabet_range = [chr(i) for i in range(ord(start_point), ord(end_point) + 1)]
            code_length = min(max(code_length, 4), 8)
            secret_code = "".join(random.sample(alphabet_range, code_length))
        else:
            await interaction.response.send_message("Invalid code type. Please choose 'numbers' or 'alphabets'.", ephemeral=True)
            return

        # Register the game
        game_id = len(games) + 1
        games[game_id] = {
            'player1': interaction.user,
            'player2': None,
            'code1': secret_code,
            'code2': None,
            'turn': interaction.user,
            'guesses': {interaction.user: 0},
            'guesses_list': {interaction.user: []},
            'timeout_enabled': timeout.lower() == 'yes',
            'timeout_minutes': timeout_minutes
        }
        player_games[interaction.user.id] = game_id

        await interaction.response.send_message(f"Mastermind game hosted successfully with ID: {game_id}. Waiting for another player to join.", ephemeral=True)
