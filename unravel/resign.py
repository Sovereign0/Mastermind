import discord
import json
import os

async def update_stats(user, game_type, won=False, lost=False, draw=False):
    user_data_file = f'{user.id}_stats.json'

    # Load existing stats or initialize them
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            stats = json.load(file)
    else:
        stats = {
            'total': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
            'unravel': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
            'bloody_dotty': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0}
        }

    if game_type not in stats:
        stats[game_type] = {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0}

    if won:
        stats[game_type]['games_won'] += 1
        stats['total']['games_won'] += 1
    if lost:
        stats[game_type]['games_lost'] += 1
        stats['total']['games_lost'] += 1
    if draw:
        stats[game_type]['games_drawn'] += 1
        stats['total']['games_drawn'] += 1

    stats[game_type]['total_games'] += 1
    stats['total']['total_games'] += 1

    # Save the updated stats back to the file
    with open(user_data_file, 'w') as file:
        json.dump(stats, file)

async def register_resign_command(bot, games, player_games, end_game):
    @bot.tree.command(name="resign_unravel", description="Resign from your ongoing Unravel game")
    async def resign_unravel(interaction: discord.Interaction):
        if interaction.user.id not in player_games:
            await interaction.response.send_message("You are not in a game.", ephemeral=True)
            return

        game_id = player_games[interaction.user.id]
        game = games[game_id]
        opponent = game['player1'] if interaction.user == game['player2'] else game['player2']

        # Update stats
        await update_stats(interaction.user, game_type='unravel', lost=True)
        await update_stats(opponent, game_type='unravel', won=True)

        await interaction.channel.send(f"{interaction.user.display_name} has resigned. {opponent.display_name} wins!")  # Public message
        await end_game(game_id, winner=opponent, loser=interaction.user)  # Pass the correct loser
