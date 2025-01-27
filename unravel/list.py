import discord

async def register_list_command(bot, games):
    @bot.tree.command(name="list_unravel", description="Show ongoing Unravel games")
    async def list_unravel(interaction: discord.Interaction):
        if not games:
            await interaction.response.send_message("There are no ongoing Unravel games.", ephemeral=True)
            return

        ongoing_games = [f"{game['player1'].display_name} vs {game['player2'].display_name}" for game in games.values()]
        game_list = "\n".join(ongoing_games)
        await interaction.response.send_message(f"Ongoing Unravel games:\n{game_list}", ephemeral=False)
        