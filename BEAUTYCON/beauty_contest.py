import discord
import asyncio
from discord.ext import tasks
from discord import app_commands

# BEAUTY CONTEST

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.dm_messages = True
intents.message_content = True  # Enable message content intent

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

players_scores = {}
game_active = False
hosted_game_active = False
player_guesses = {}
reaction_message_id = None
players_in_game = []
host_channel = None
afk_check_task = None

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

def find_closest(players, target):
    closest_players = []
    closest_diff = float('inf')
    for player, guess in players.items():
        diff = abs(guess - target)
        if diff < closest_diff:
            closest_diff = diff
            closest_players = [player]
        elif diff == closest_diff:
            closest_players.append(player)
    return closest_players

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Sov's Gambit"))
    await tree.sync()

@tree.command(name="host_bc", description="Start a game of beauty contest.")
async def host_game(interaction: discord.Interaction):
    global hosted_game_active, reaction_message_id, players_in_game, host_channel
    if hosted_game_active:
        await interaction.response.send_message("A hosted game is already in progress!")
        return

    hosted_game_active = True
    players_in_game = []
    host_channel = interaction.channel

    embed = discord.Embed(title="Beauty Contest", description="Those who want to play Beauty Contest, react to this message.")
    message = await interaction.channel.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    reaction_message_id = message.id
    await asyncio.sleep(40)  # wait 40 seconds for players to react

    message = await interaction.channel.fetch_message(reaction_message_id)
    for reaction in message.reactions:
        if reaction.emoji == "✅":
            async for user in reaction.users():
                if not user.bot:
                    players_in_game.append(user)

    if len(players_in_game) < 3:
        await interaction.channel.send("Not enough players joined the game.")
        hosted_game_active = False
    else:
        lives = 3 if len(players_in_game) < 5 else 5
        global players_scores
        players_scores = {player: lives for player in players_in_game}
        await start_hosted_round(interaction)

async def start_hosted_round(interaction):
    global player_guesses, afk_check_task
    player_guesses = {}
    for player in players_scores.keys():
        try:
            await player.send("Send your secret number (0-100) using the /code_bc command.")
        except discord.Forbidden:
            await interaction.channel.send(f"{player.mention}, please enable DMs from server members to participate in the game.")

    # Start a task to check for AFK players after 2 minutes
    afk_check_task = asyncio.create_task(afk_check(interaction))

async def afk_check(interaction):
    await asyncio.sleep(180)  # Wait 2 minutes
    if len(player_guesses) < len(players_scores):
        await prompt_afk_elimination(interaction)

async def prompt_afk_elimination(interaction):
    afk_players = [player for player in players_scores.keys() if player not in player_guesses]
    if afk_players:
        afk_message = await host_channel.send(f"{afk_players[0].mention} has not submitted a code. Should they be eliminated?")
        await afk_message.add_reaction("✅")
        await afk_message.add_reaction("❌")

        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) in ["✅", "❌"] and user in players_scores

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            if str(reaction.emoji) == "✅":
                await host_channel.send(f"Waiting for 1 minute to see if {afk_players[0].mention} submits their code.")
                await asyncio.sleep(60)  # Wait 1 more minute
                if afk_players[0] not in player_guesses:
                    await host_channel.send(f"{afk_players[0].mention} has been eliminated.")
                    del players_scores[afk_players[0]]
                    if len(players_scores) == 1:
                        await end_game(interaction)
                    else:
                        await process_hosted_guesses(interaction)
                else:
                    await host_channel.send(f"{afk_players[0].mention} submitted their code in time.")
            else:
                await host_channel.send(f"{afk_players[0].mention} is still in the game.")
        except asyncio.TimeoutError:
            await host_channel.send("No decision made. The game will continue without eliminating the player.")

@tree.command(name="code_bc", description="Submit your code for the beauty contest game.")
async def submit_code(interaction: discord.Interaction, number: float):
    global player_guesses
    if interaction.user not in players_scores:
        await interaction.response.send_message("You are not a part of the game.")
        return

    if players_scores[interaction.user] <= 0:
        await interaction.response.send_message("You have been eliminated and cannot submit a code.")
        return

    if interaction.user in player_guesses:
        await interaction.response.send_message("You have already submitted your code. Wait for the result and submit your code in the next round.")
        return

    if number < 0 or number > 100:
        await interaction.response.send_message("The number must be between 0 and 100.")
        return

    if len(players_scores) == 2 and number != int(number):
        await interaction.response.send_message("In a 1v1 situation, decimals are not allowed.")
        return

    player_guesses[interaction.user] = number
    await interaction.response.send_message("Code submitted successfully, wait for other players.")

    if len(player_guesses) == len(players_scores):
        await process_guesses(interaction)

async def process_guesses(interaction):
    global player_guesses, players_scores, hosted_game_active, afk_check_task

    if afk_check_task:
        afk_check_task.cancel()

    if len(players_scores) == 2:
        await process_1v1_guesses(interaction)
    else:
        await process_hosted_guesses(interaction)

async def process_hosted_guesses(interaction):
    global player_guesses, players_scores, hosted_game_active, afk_check_task

    if afk_check_task:
        afk_check_task.cancel()

    average = calculate_average(player_guesses.values())
    target = average * 0.8

    closest_players = find_closest(player_guesses, target)
    eliminated_player = None

    for player in list(players_scores.keys()):
        if player not in closest_players:
            players_scores[player] -= 1
            if players_scores[player] <= 0:
                await host_channel.send(f'{player.mention} is eliminated.')
                eliminated_player = player

    if eliminated_player:
        del players_scores[eliminated_player]

    scores_message = f'- All codes received, the target was {target:.2f}.\n'
    scores_message += '# Feedback:\n'
    for player, guess in player_guesses.items():
        scores_message += f'{player.mention}: {guess}\n'
    if len(closest_players) == 1:
        scores_message += f'# Closest to target was {closest_players[0].mention}.\n # Hence He/She Won This Round\n # Sov On Top 🗿☝🏻'
    else:
        scores_message += '# Closest to target were:\n'
        for player in closest_players:
            scores_message += f'{player.mention}\n'
        scores_message += '# Hence, they won this round\n'
    scores_message += '# Leaderboard:\n'
    for player, score in players_scores.items():
        scores_message += f'{player.mention}: {score} lives\n'
    scores_message += '- The next round will begin 20 seconds after this feedback.'

    await host_channel.send(scores_message)

    if len(players_scores) == 1:
        await end_game(interaction)
    elif len(players_scores) == 2:
        await interaction.channel.send("Special rules for 1v1 situation: \n- 100 beats 0 \n- No decimals allowed \n- Any other number except 0 beats 100\n send the code after 20 seconds")
        player_guesses.clear()
        await asyncio.sleep(20)  # 20 seconds delay before the next round
        await start_1v1_round(interaction)
    else:
        player_guesses.clear()
        await asyncio.sleep(20)  # 20 seconds delay before the next round
        await start_hosted_round(interaction)

async def start_1v1_round(interaction):
    global player_guesses, afk_check_task
    player_guesses = {}
    for player in players_scores.keys():
        try:
            await player.send("Send your secret number (0-100) using the /code_bc command. No decimals allowed in             your submission.")
        except discord.Forbidden:
            await interaction.channel.send(f"{player.mention}, please enable DMs from server members to participate in the game.")

    # Start a task to check for AFK players after 2 minutes
    afk_check_task = asyncio.create_task(afk_check(interaction))

async def process_1v1_guesses(interaction):
    global player_guesses, players_scores, hosted_game_active, afk_check_task

    if afk_check_task:
        afk_check_task.cancel()

    if len(player_guesses) < 2:
        return

    # Retrieve guesses
    player1, player2 = list(player_guesses.keys())
    guess1, guess2 = player_guesses[player1], player_guesses[player2]

    # Determine the winner and loser based on guesses
    winner = None
    loser = None

    if guess1 == 100 and guess2 == 0:
        winner, loser = player1, player2
    elif guess2 == 100 and guess1 == 0:
        winner, loser = player2, player1
    elif guess1 != 100 and guess2 == 100:
        winner, loser = player1, player2
    elif guess2 != 100 and guess1 == 100:
        winner, loser = player2, player1
    elif guess1 < guess2:
        winner, loser = player1, player2
    elif guess2 < guess1:
        winner, loser = player2, player1

    if winner and loser:
        # Update scores based on the round result
        players_scores[loser] -= 1
        if players_scores[loser] <= 0:
            if len(players_scores) == 2:
                # If this is the last round, end the game
                await host_channel.send(f'{winner.mention} with code {player_guesses[winner]} wins the game! Congratulations!🎉🎉🎉\n'
                        f'{loser.mention} loses☠️ with code {player_guesses[loser]} has {players_scores[loser]} lives remaining.')

                await end_game(interaction)
                return
            else:
                # Continue to the next round if there are still more players
                player_guesses.clear()
                await asyncio.sleep(20)  # 20 seconds delay before the next round
                await start_1v1_round(interaction)
        else:
            # Continue to the next round if there are still lives remaining for the loser
            await host_channel.send(f'{loser.mention} loses the round with code {player_guesses[loser]} and now has {players_scores[loser]} lives remaining.\n'
                                         f'{winner.mention} wins the round with code {player_guesses[winner]} and now send the next code after 20 seconds')
            player_guesses.clear()
            await asyncio.sleep(20)  # 20 seconds delay before the next round
            await start_1v1_round(interaction)


async def end_game(interaction):
    global hosted_game_active
    hosted_game_active = False
    winner = list(players_scores.keys())[0]
    await host_channel.send(f'{winner.mention} wins the game! Thanks for playing Beauty Contest.')
    players_scores.clear()
    player_guesses.clear()
    players_in_game.clear()

async def register_beauty_contest_commands(bot):
    bot.tree.add_command(host_game)
    bot.tree.add_command(submit_code)

