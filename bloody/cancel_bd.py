import discord

async def register_cancel_bd(bot, challenge_requests, games, player_games):
    @bot.tree.command(name="cancel_bd", description="Cancel your Bloody Dotty challenge.")
    async def cancel_bd(interaction: discord.Interaction):
        user_id = interaction.user.id

        # Check if the user is currently in an active game
        if user_id in player_games:
            await interaction.response.send_message(
                "You are currently in an active game. Use the 'resign_bd' command to conclude it before canceling a challenge.",
                ephemeral=True
            )
            return

        # Check if the user has any pending challenges
        if user_id not in challenge_requests:
            await interaction.response.send_message("You have no pending challenges to cancel.", ephemeral=True)
            return

        # Remove the challenge
        opponent_id = challenge_requests.pop(user_id)
        game_id = f"{user_id}-{opponent_id}"

        # Check if the game was initiated but not accepted
        if game_id in games and not games[game_id].game_active:
            # Remove game and update player games
            games.pop(game_id, None)
            player_games.pop(user_id, None)
            player_games.pop(opponent_id, None)

            # Notify both the host and the opponent
            opponent = await bot.fetch_user(opponent_id)
            await interaction.response.send_message(
                f"Your challenge to {opponent.mention} has been successfully canceled.",
                ephemeral=False
            )
            await opponent.send(
                f"{interaction.user.mention} has canceled their challenge. The challenge was never accepted.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("The challenge cannot be canceled as it has already been accepted.", ephemeral=True)
