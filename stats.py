import discord
import json
import os
import aiohttp
import io
from PIL import Image, ImageDraw, ImageFont
from discord import app_commands
from discord.ui import View, Select

async def register_stats_commands(bot):
    class StatsSelect(discord.ui.Select):
        def __init__(self, interaction, target_user):
            self.interaction = interaction
            self.target_user = target_user

            options = [
                discord.SelectOption(label="Total", description="View total stats", value="total"),
                discord.SelectOption(label="Unravel", description="View Unravel stats", value="unravel"),
                discord.SelectOption(label="Bloody Dotty", description="View Bloody Dotty stats", value="bloody_dotty"),
            ]

            super().__init__(placeholder="Select an option...", min_values=1, max_values=1, options=options)

        async def callback(self, interaction: discord.Interaction):
            stat_type = self.values[0]
            await send_stats(interaction, self.target_user, stat_type)

    class StatsView(View):
        def __init__(self, interaction, target_user):
            super().__init__()
            self.add_item(StatsSelect(interaction, target_user))

    async def send_stats(interaction, target_user, stat_type):
        user_data_file = f'{target_user.id}_stats.json'
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as file:
                stats = json.load(file)
        else:
            stats = {
                'total': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
                'unravel': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0},
                'bloody_dotty': {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0}
            }

        # Ensure the stat_type exists in the stats
        if stat_type not in stats:
            stats[stat_type] = {'games_won': 0, 'games_lost': 0, 'games_drawn': 0, 'total_games': 0}

        stat = stats[stat_type]

        # Ensure "total" stats are calculated correctly
        if stat_type != "total":
            total_stat = stats['total']
            total_stat['games_won'] = stats['unravel']['games_won'] + stats['bloody_dotty']['games_won']
            total_stat['games_lost'] = stats['unravel']['games_lost'] + stats['bloody_dotty']['games_lost']
            total_stat['games_drawn'] = stats['unravel']['games_drawn'] + stats['bloody_dotty']['games_drawn']
            total_stat['total_games'] = total_stat['games_won'] + total_stat['games_lost'] + total_stat['games_drawn']

        win_rate = stat['games_won'] / stat['total_games'] * 100 if stat['total_games'] > 0 else 0

        background_images = {
            "total": "total.jpg",
            "unravel": "unravelst.jpg",
            "bloody_dotty": "bdst.jpg"
        }

        background_image = Image.open(background_images[stat_type]).convert("RGBA")
        main_image = Image.new("RGBA", background_image.size)
        main_image.paste(background_image, (0, 0))

        draw = ImageDraw.Draw(main_image)

        header_font = ImageFont.truetype("SoloLevelDemo.ttf", 70)
        stat_font = ImageFont.truetype("Mirage final.ttf", 29)
        value_font = ImageFont.truetype("Mirage final.ttf", 25)

        headers = {
            "total": "Game Stats",
            "unravel": "Unravel Stats",
            "bloody_dotty": "Bloody Dotty Stats"
        }

        header_text = headers[stat_type]
        header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
        header_width = header_bbox[2] - header_bbox[0]
        header_x = (main_image.width - header_width) / 2
        draw.text((header_x, 30), header_text, font=header_font, fill=(255, 255, 255))

        stats_text = [
            ("Games Won", stat['games_won']),
            ("Games Lost", stat['games_lost']),
            ("Games Drawn", stat['games_drawn']),
            ("Total Games", stat['total_games']),
            ("Win Rate", f"{win_rate:.2f}%")
        ]

        y_offset = 120
        for stat_name, stat_value in stats_text:
            draw.text((70, y_offset), stat_name, font=stat_font, fill=(255, 255, 255))
            draw.text((320, y_offset), str(stat_value), font=value_font, fill=(255, 255, 255))
            y_offset += 40

        bar_x = 70
        bar_y = y_offset + 20
        bar_width = 300
        bar_height = 25

        progress = win_rate / 100
        progress_width = int(bar_width * progress)

        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline=(255, 255, 255), width=2)
        draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height], fill=(0, 102, 204))

        with io.BytesIO() as image_binary:
            main_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename='stats.png')

        await interaction.response.send_message(file=file)

    @bot.tree.command(name="stats", description="Check your game stats")
    async def stats(interaction: discord.Interaction, target: discord.User = None):
        target_user = target if target else interaction.user
        view = StatsView(interaction, target_user)
        await interaction.response.send_message("Select the type of stats to view:", view=view)
