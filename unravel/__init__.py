from .host_unravel import register_host_unravel
from .code_unravel import register_code_unravel
from .guess_unravel import register_guess_unravel
from .list import register_list_command
from .moves import register_moves_command
from .resign import register_resign_command
from .cancel_unravel import register_cancel_command

async def register_unravel_commands(bot, bloody_dotty, games, player_games, end_game):
    await register_host_unravel(bot, bloody_dotty, games, player_games)
    await register_code_unravel(bot, games, player_games)
    await register_guess_unravel(bot, games, player_games)
    await register_list_command(bot, games)
    await register_moves_command(bot, games, player_games)
    await register_resign_command(bot, games, player_games, end_game)
    await register_cancel_command(bot, games, player_games)
    