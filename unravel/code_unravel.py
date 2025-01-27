import discord
import random

async def register_code_unravel(bot, games, player_games):
    @bot.tree.command(name="code_unravel", description="Submit your code for Unravel")
    async def code_unravel(interaction: discord.Interaction, code: str):
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You are not in a game.", ephemeral=True)
            return

        game_id = player_games[interaction.user.id]
        game = games[game_id]

        if game['code1'] is not None and game['code2'] is not None:
            await interaction.response.send_message("Wait for the result and submit your code in the next round.", ephemeral=True)
            return

        if len(code) != 4 or not code.isdigit() or len(set(code)) != 4:
            await interaction.response.send_message("Invalid code. Please enter a 4-digit number with no repeating digits.", ephemeral=True)
            return

        if interaction.user == game['player1']:
            game['code1'] = code
        else:
            game['code2'] = code

        await interaction.response.send_message("Code submitted successfully, wait for the other player.", ephemeral=True)

        if game['code1'] is not None and game['code2'] is not None:
            channel = bot.get_channel(game['channel_id'])  # Get the channel using stored channel_id
            game['guesses'] = {game['player1']: 0, game['player2']: 0}  # Initialize guess counts
            game['guesses_list'] = {game['player1']: [], game['player2']: []}  # Initialize guesses list
            game['extra_turn'] = None  # Initialize extra turn flag

            # Randomly select who goes first
            game['turn'] = random.choice([game['player1'], game['player2']])

            await channel.send('Both codes received! Start guessing! (Use /guess_unravel <your_guess>)')
            await channel.send(f"It's {game['turn'].mention}'s turn to guess!")
