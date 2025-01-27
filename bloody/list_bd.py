# list_bd.py
import discord

async def register_list_bd(bot, games):
    @bot.tree.command(name="list_bd", description="List all ongoing Bloody Dotty games.")
    async def list_bd(interaction: discord.Interaction):
        if not games:
            await interaction.response.send_message("There are no ongoing games at the moment.", ephemeral=True)
            return

        game_list = []
        for game_id, game in games.items():
            if hasattr(game, 'host') and hasattr(game, 'opponent'):
                if game.host and game.opponent:
                    game_list.append(f"{game.host.mention} vs {game.opponent.mention}")

        if not game_list:
            await interaction.response.send_message("There are no ongoing games at the moment.", ephemeral=True)
            return

        game_list_message = "\n".join(game_list)
        await interaction.response.send_message(f"Ongoing games:\n{game_list_message}", ephemeral=False)
