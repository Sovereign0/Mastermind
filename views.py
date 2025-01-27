import discord

class ChallengeView(discord.ui.View):
    def __init__(self, host, player, game_name, bot, games):
        super().__init__(timeout=60)
        self.host = host
        self.player = player
        self.game_name = game_name
        self.bot = bot
        self.games = games

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.player:
            await interaction.response.send_message("You can't accept a challenge that isn't yours!", ephemeral=True)
            return

        if self.game_name == "Bloody Dotty":
            self.games[interaction.channel.id] = {
                'player1': self.host,
                'player2': self.player,
                'turn': self.host,
                'code1': None,
                'code2': None,
                'game_name': "Bloody Dotty"
            }
        elif self.game_name == "Unravel":
            self.games[interaction.channel.id] = {
                'player1': self.host,
                'player2': self.player,
                'turn': self.host,
                'code1': None,
                'code2': None,
                'game_name': "Unravel"
            }

        await interaction.response.send_message(f'{self.host.mention} and {self.player.mention} have started a game of {self.game_name}!')
        await interaction.followup.send('Both players, please check your DMs and submit your secret codes.')

        await self.host.send(f"You are now playing {self.game_name} against {self.player.display_name}. Submit your code in the channel using `/code_{self.game_name.lower()} <digit>`")
        await self.player.send(f"You are now playing {self.game_name} against {self.host.display_name}. Submit your code in the channel using `/code_{self.game_name.lower()} <digit>`")

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.player:
            await interaction.response.send_message("You can't decline a challenge that isn't yours!", ephemeral=True)
            return

        await interaction.response.send_message(f'{self.player.mention} has declined the challenge from {self.host.mention}.')
