import json
import os

def update_stats(user, game_type=None, won=False, lost=False, draw=False):
    user_data_file = f'{user.id}_stats.json'
    
    # Load or initialize the stats
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            stats = json.load(file)
    else:
        stats = {
            'total': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
            'unravel': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
            'bloody_dotty': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0}
        }

    # Update game-specific stats
    if game_type:
        game_stats = stats.get(game_type, {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0})
        if won:
            game_stats['games_won'] += 1
        if lost:
            game_stats['games_lost'] += 1
        if draw:
            game_stats['games_drawn'] += 1
        game_stats['total_games'] = game_stats['games_won'] + game_stats['games_lost'] + game_stats['games_drawn']
        stats[game_type] = game_stats

    # Update total stats (irrespective of the game type)
    total_stats = stats['total']
    if won:
        total_stats['games_won'] += 1
    if lost:
        total_stats['games_lost'] += 1
    if draw:
        total_stats['games_drawn'] += 1
    total_stats['total_games'] = total_stats['games_won'] + total_stats['games_lost'] + total_stats['games_drawn']
    stats['total'] = total_stats

    # Save the updated stats back to the file
    with open(user_data_file, 'w') as file:
        json.dump(stats, file)

