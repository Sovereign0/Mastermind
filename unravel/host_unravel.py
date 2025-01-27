import discord
from discord import app_commands
from views import ChallengeView

async def register_host_unravel(bot, bloody_dotty, games, player_games):
    game_id_counter = [1]  # Use a list so the counter is mutable within the function

    @bot.tree.command(name="host_unravel", description="Host a game of Unravel")
    async def host_unravel(interaction: discord.Interaction, player: discord.Member):
        if interaction.user.id in bloody_dotty.players or player.id in bloody_dotty.players:
            await interaction.response.send_message("One of the players is already playing Bloody Dotty. Finish that game first.", ephemeral=True)
            return

        if player == bot.user:
            await interaction.response.send_message("I can't play against myself, silly!", ephemeral=True)
            return

        if interaction.user.id in player_games or player.id in player_games:
            await interaction.response.send_message("You or the player are already in a game. Finish the current game first.", ephemeral=True)
            return

        game_id = game_id_counter[0]
        game_id_counter[0] += 1

        games[game_id] = {
            'player1': interaction.user,
            'player2': player,
            'code1': None,
            'code2': None,
            'turn': interaction.user,
            'correct_guesser': None,
            'guesses': {},
            'guesses_list': {},
            'channel_id': interaction.channel_id  # Store the channel ID
        }
        player_games[interaction.user.id] = game_id
        player_games[player.id] = game_id

        challenge_message = await interaction.channel.send(f'{player.mention}, do you want to play Unravel with {interaction.user.mention}?', view=ChallengeView(interaction.user, player, "Unravel", bot, games))
