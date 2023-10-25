# Molten main audio

from typing import Literal, cast
from disnake import CommandInter
import disnake
from disnake.ext.commands import Cog, slash_command
from mafic import SearchType
from ..components.track_list import TrackList
from ..bot import Molten
from ..player import Player


class Melted(Cog):
    def __init__(self, bot: Molten) -> None:
        self.bot = bot

    @slash_command(dm_permission=False)
    async def stop(inter: CommandInter) -> None:
        """Force the bot to stop playing and leave"""

        if not inter.author.voice or not inter.author.voice.channel:
            await inter.send("You must be in the same channel as me to stop the track.")
            return
        if inter.author.voice.channel:
            if inter.author.voice.channel.id != inter.me.voice.channel.id:
                await inter.send("You must be in the same channel as me to stop the track.")
                return

        player = cast(Player, inter.guild.voice_client)
        await player.stop()
        await player.disconnect()

    @slash_command(
        dm_permission=False
    )
    async def play(
        self,
        inter: CommandInter,
        source: Literal['youtube', 'spotify'],
        query: str,
        replace: bool = False
    ) -> None:
        """Start playing music in a channel

        Parameters
        ----------
        source: The source which to play from
        query: What song to play
        replace: Whether to replace the currently playing track (if any)
        """
        await inter.response.defer()

        if source == 'youtube':
            search = SearchType.YOUTUBE
        else:
            search = SearchType.SPOTIFY_SEARCH

        if not inter.author.voice or not inter.author.voice.channel:
            await inter.send("Cannot start playing without a channel to play in")
            return

        if not inter.guild.voice_client:
            player = await inter.author.voice.channel.connect(cls=Player)
        else:
            player = inter.guild.voice_client

        print(f'\n\na: {player.queue}\n\n')

        tracks = await player.fetch_tracks(query, search_type=search)

        if tracks is None:
            await inter.send("Sorry, I couldn't find any results for this song")
            return

        view = disnake.ui.View()
        view.add_item(TrackList(tracks, source, replace))

        await inter.send("Here are the options I found for this query:", view=view)

def setup(bot: Molten) -> None:
    bot.add_cog(Melted(bot))
