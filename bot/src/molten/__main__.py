import logging
from os import environ
from typing import cast
from disnake import VoiceChannel

from mafic import TrackEndEvent
from molten.components.playing import PlayingView
from molten.player import Player
from molten.bot import Molten
from dotenv import load_dotenv

load_dotenv()

bot = Molten()


@bot.listen("on_track_end")
async def on_track_end(event: TrackEndEvent) -> None:
    player = cast(Player, event.player)
    if player.continuous:
        await player.play(event.track)
    else:
        if player.queue != [] and not player.queue_just_skipped:
            track = player.queue[0]
            player.queue.remove(track)
            await player.play(track)
            channel = cast(VoiceChannel, player.channel)
            await channel.send(
                f"Now playing `{player.current.title}` by `{player.current.author}` ([Source]({player.current.uri}))",
                view=PlayingView(current=player.current)
            )
        if player.queue_just_skipped:
            player.queue_just_skipped = False

logging.basicConfig(level=logging.DEBUG)

bot.load_extension('molten.cogs.melted')

bot.run(environ["TOKEN"])
