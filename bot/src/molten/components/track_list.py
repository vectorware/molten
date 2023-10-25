from typing import Literal, cast
import disnake
from disnake.ui import StringSelect
from disnake import SelectOption
from mafic import Track

from .playing import PlayingView
from ..player import Player


class TrackList(StringSelect):
    def __init__(self, tracks: list[Track], type: Literal['youtube', 'spotify'], replace: bool) -> None:
        self.tracks = tracks
        self.track_type = type
        self.replace = replace

        def option(track: Track) -> SelectOption:
            label = f'{track.title} [{track.author}]'

            if len(label) >= 100:
                label = label[:97] + '...'

            return SelectOption(
                label=label,
                value=track.identifier
            )

        options = [
            option(track) for track in tracks
        ]
        super().__init__(
            placeholder='Which track should I play?',
            options=options
        )

    async def callback(self, inter: disnake.MessageInteraction) -> None:
        await inter.response.defer()
        track_iden = self.values[0]

        track = None

        for maybe_track in self.tracks:
            if maybe_track.identifier == track_iden:
                track = maybe_track
                break

        # can't happen
        if track is None:
            return

        if inter.guild.voice_client is None:
            await inter.send("This query was made for a different session. Please make a new query to instantiate a new session!")
            return

        player = cast(Player, inter.guild.voice_client)

        print(f'\n\na: {player.queue}\n\n')

        if player.current is None:
            await player.play(track, volume=50)
        elif self.replace is True:
            player.queue_just_skipped = True
            await player.play(track, volume=50)
        else:
            player.queue.append(track)
            await inter.send(
                f"Queued `{track.title}` by `{track.author}` ([Source]({track.uri}))",
            )
            return

        print(f'\n\na: {player.queue}\n\n')

        await inter.send(
            f"Now playing `{player.current.title}` by `{player.current.author}` ([Source]({player.current.uri}))",
            view=PlayingView(current=player.current)
        )
