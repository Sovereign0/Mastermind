import discord

async def register_list_mastermind(bot, games):
    @bot.tree.command(name="list_mastermind", description="List all ongoing Mastermind games")
    async def list_mastermind(interaction: discord.Interaction):
        if not games:
            await interaction.response.send_message("No ongoing Mastermind games.", ephemeral=True)
            return

        game_list = "\n".join([f"Game {gid}: {game['player1'].mention} vs {game['player2'].mention}" for gid, game in games.items()])
        await interaction.response.send_message(f"Ongoing Mastermind games:\n{game_list}", ephemeral=True)
        