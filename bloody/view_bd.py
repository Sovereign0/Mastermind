import discord
from game import BloodyDotty  # Import the BloodyDotty class

class BloodyDottyChallengeView(discord.ui.View):
    def __init__(self, host, opponent, bot, games, player_games):
        super().__init__(timeout=30)
        self.host = host
        self.opponent = opponent
        self.bot = bot
        self.games = games
        self.player_games = player_games
        self.is_accepted = False  # Track if the challenge was accepted

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("You can't accept a challenge that isn't yours!", ephemeral=True)
            return

        # Mark the challenge as accepted
        self.is_accepted = True

        # Start the game because the challenge was accepted
        game_id = f"{self.host.id}-{self.opponent.id}"
        new_game = BloodyDotty()  # Create a new instance of BloodyDotty
        new_game.game_active = True
        new_game.host = self.host
        new_game.opponent = self.opponent
        new_game.players = {self.host.id, self.opponent.id}
        new_game.host_number = None
        new_game.opponent_number = None
        new_game.sums = {self.host.id: 0, self.opponent.id: 0}
        new_game.turn = None
        new_game.channel = interaction.channel

        # Track the new game instance and players
        self.games[game_id] = new_game
        self.player_games[self.host.id] = game_id
        self.player_games[self.opponent.id] = game_id

        self.stop()  # Stop the view to prevent further interactions
        await interaction.response.send_message(f"The game of Bloody Dotty has started between {self.host.mention} and {self.opponent.mention}!", ephemeral=False)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("You can't decline a challenge that isn't yours!", ephemeral=True)
            return

        self.stop()  # Stop the view to prevent further interactions
        await interaction.response.send_message(f'{self.opponent.mention} has declined the challenge from {self.host.mention}.', ephemeral=False)

async def on_timeout(self):
    if not self.is_accepted:
        self.stop()  # Stop the view to prevent further interactions
        try:
            await interaction.response.send_message(f"{self.opponent.mention} didn't respond to the challenge in time. The challenge has been canceled.", ephemeral=False)
            await interaction.response.send_message(f"You didn't respond to {self.host.mention}'s challenge in time. The challenge has been canceled.", ephemeral=False)
        except discord.Forbidden:
            # Handle permission errors, such as if the bot cannot send messages
            pass
