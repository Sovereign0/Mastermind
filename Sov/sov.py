import discord
import random

# Define the list of responses
responses = [
    "Sov On Top 🗿☝🏻",
    "Sov is better than you mofo 🗿☝🏻",
    "Sov is The Goat 🗿☝🏻",
    "Sovereign On Top 🗿☝🏻",
    "The Sovereign reigns supreme 🗿☝🏻",
    "Sov is unmatched 🗿☝🏻",
    "Sovereign rules them all 🗿☝🏻",
    "Bow down to Sov 🗿☝🏻",
    "The king is here: Sov 🗿☝🏻",
    "All hail Sovereign 🗿☝🏻",
    "Sov supremacy 🗿☝🏻",
    "The Sovereign standard 🗿☝🏻",
    "Sov, the undefeated 🗿☝🏻",
    "In Sov we trust 🗿☝🏻",
    "Sovereign over everything 🗿☝🏻",
    "Sov, the legend 🗿☝🏻",
    "Sovereign forever 🗿☝🏻",
    "Sov conquers all 🗿☝🏻",
    "Sovereign is the apex 🗿☝🏻",
    "You can't top Sov 🗿☝🏻",
    "Sov sets the bar 🗿☝🏻",
    "Sov wins again 🗿☝🏻",
    "The Sovereign is unbeatable 🗿☝🏻",
    "Sov, the ultimate 🗿☝🏻",
    "Sovereign, the undisputed 🗿☝🏻"
]


# Register the Sov command and reaction listener
async def register_sov_commands(bot):
    @bot.event
    async def on_message(message):
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return

        # Check if the message contains "Sov" or "Sovereign"
        if any(word in message.content.lower() for word in ["sov", "sovereign"]):
            # React with emojis
            await message.add_reaction("🇸")
            await message.add_reaction("🅾️")
            await message.add_reaction("🇻")
            await message.add_reaction("🔛")
            await message.add_reaction("🔝")

            # Send a random response from the list
            response = random.choice(responses)
            await message.channel.send(response)
