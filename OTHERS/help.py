import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get help on commands and games")
    async def help(self, interaction: discord.Interaction):
        view = HelpView()
        await interaction.response.send_message("Choose an option:", view=view)

class HelpView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="About Command", style=discord.ButtonStyle.primary, custom_id="help_about_command_btn")
    async def about_command(self, interaction: discord.Interaction, button: Button):
        command_info = (
            "```/Host_unravel - to host a game of Unravel\n"
            "/Code_unravel - to submit your code for the Unravel game\n"
            "/Guess_unravel - to guess the number in Unravel\n"
            "/List_unravel - to check the ongoing Unravel games\n"
            "/Check_moves - to check the moves one has made in the game\n"
            "/Resign_unravel - to resign a game of Unravel\n"
            "/Cancel_unravel - to cancel a pending challenge of Unravel\n"
            "/Setaslogging - to set a channel for Unravel logs\n"
            "/Host_bd - to host a game of Bloody Dotty\n"
            "/Guess_bd - to guess the sum in Bloody Dotty\n"
            "/Code_bd - to submit your code in Bloody Dotty\n"
            "/List_bd - to check the ongoing Bloody Dotty games\n"
            "/Resign_bd - to resign a game of Bloody Dotty\n"
            "/Host_bc - to host a game of Beauty Contest\n"
            "/Code_bc - to submit codes for Beauty Contest\n"
            "/Leave_bc - to leave a game of Beauty Contest\n"
            "/help - To know more about the bot\n"
            "/feedback - to submit your suggestions or report a bug of the bot\n"
            "/End_bc - to end the current Beauty Contest game```"
        )
        await interaction.response.send_message(command_info, ephemeral=False)

    @discord.ui.button(label="About Games", style=discord.ButtonStyle.secondary, custom_id="help_about_games_btn")
    async def about_games(self, interaction: discord.Interaction, button: Button):
        game_view = GameInfoView()
        await interaction.response.send_message("Choose a game to learn more:", view=game_view)

class GameInfoView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Unravel", style=discord.ButtonStyle.primary, custom_id="gameinfo_unravel_info_btn")
    async def unravel_info(self, interaction: discord.Interaction, button: Button):
        unravel_description = (
            "━━━━━━━━━━━━━━━━━━\n"
            "The goal of the game is to guess a secret 4-digit number chosen by the other player.\n"
            "\n"
            "**Setup:**\n"
            "Choose a secret 4-digit number with no repeating digits. The chosen number will be sent to the referee.\n"
            "\n"
            "**Gameplay:**\n"
            "Players take turns making guesses. ** Referees will provide feedback**.\n"
            "After each guess, **the referee** provides feedback in terms of \"Fames\" and \"Dots.\"\n"
            "\"Fames\" represent correct digits in the correct position.\n"
            "\"Dots\" represent correct digits in the wrong position.\n"
            "\n"
            "**Example:**\n"
            "Player A chooses the secret number \"0348.\"\n"
            "Player B's guess is \"0123.\"\n"
            "**Referee** feedback: 1 Fame (digit 0 is in the correct position), 1 Dot (digit 3 is correct but in the wrong position).\n"
            "Players continue taking turns until the correct number is guessed (4 Fames). The player that guesses the number of the other player first wins.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await interaction.response.send_message(unravel_description, ephemeral=False)

    @discord.ui.button(label="Bloody Dotty", style=discord.ButtonStyle.primary, custom_id="gameinfo_bloody_dotty_info_btn")
    async def bloody_dotty_info(self, interaction: discord.Interaction, button: Button):
        bloody_dotty_description = (
            "**Bloody Dotty**\n"
            "Difficulty: Beginner-Hell (Depends on Players skill level)\n"
            "Game Type: Intelligence, psychological\n"
            "\n"
            "Rules:\n"
            "- Players DM a referee a number from 1-10\n"
            "- Players take turns on guessing sum of the number\n"
            "- First player to guess the sum of the number wins\n"
            "- No decimals or loopholes\n"
            "- Players are NOT allowed to guess impossible numbers e.g. if you have 7 you cannot guess >18 because your opponent cannot be 11. However, if you deduce your opponent number to let’s say 1-5, you are still allowed to guess 6+ because the number is still possible for your opponent’s POV"
        )
        await interaction.response.send_message(bloody_dotty_description, ephemeral=False)

    @discord.ui.button(label="Beauty Contest", style=discord.ButtonStyle.primary, custom_id="gameinfo_beauty_contest_info_btn")
    async def beauty_contest_info(self, interaction: discord.Interaction, button: Button):
        beauty_contest_description = (
            "# Beauty Contest\n"
            "- Players choose a number from 0 to 100\n"
            "- They have to guess the average of all numbers multiplied by 0.8\n"
            "- The person who is closest to the number will not lose any points but everyone except that person will lose 1 point.\n"
            "- The person who loses 5 points first gets eliminated.\n"
            "\n"
            "Then we repeat the process until one person is left."
        )
        await interaction.response.send_message(beauty_contest_description, ephemeral=False)

async def register_help_commands(bot):
    await bot.add_cog(Help(bot))
