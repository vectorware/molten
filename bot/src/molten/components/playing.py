from typing import cast
import disnake
from disnake.ui import Button, View
from disnake import Interaction
from mafic import Track
from ..player import Player


async def is_in_voice(inter: Interaction) -> bool:
    if inter.author.voice.channel is None or inter.guild.voice_client is None or inter.author.voice.channel.id != inter.guild.voice_client.channel.id:
        return False

    return True


class PlayingView(View):
    def __init__(self, *, current: Track, timeout: float | None = 3600) -> None:
        super().__init__(timeout=timeout)
        self.queue = []


    @disnake.ui.button(emoji="⏪", disabled=True)
    async def previous_track(self, button: disnake.ui.Button, inter: Interaction) -> None:
        ...


    @disnake.ui.button(emoji="⏸️")
    async def pause(self, button: disnake.ui.Button, inter: Interaction) -> None:
        await inter.response.defer()
        if not await is_in_voice(inter):
            await inter.send(f'{inter.author.mention} you are not in the same voice channel as me. I cannot pause this track.')

        player = cast(Player, inter.guild.voice_client)

        await player.pause(pause=not player.paused)
        await inter.send(f'{inter.author.mention} toggled pause')

    @disnake.ui.button(emoji="⏩")
    async def next_track(self, button: disnake.ui.Button, inter: Interaction) -> None:
        # TODO
        await inter.response.defer()
        if not await is_in_voice(inter):
            await inter.send(f'{inter.author.mention} you are not in the same voice channel as me. I cannot pause this track.')

        player = cast(Player, inter.guild.voice_client)

        if len(player.queue) < 1:
            await inter.send(f'Not enough tracks to skip forward.')
        else:
            print(f'\n\na: {player.queue}\n\n')
            track = player.queue[0]
            player.queue.remove(track)
            player.queue_just_skipped = True
            await player.play(track)
            await inter.send(
                f"Now playing `{track.title}` by `{track.author}` ([Source]({track.uri}))",
                view=PlayingView(current=player.current)
            )

    @disnake.ui.button(emoji="🔁")
    async def continuous_play(self, button: disnake.ui.Button, inter: Interaction) -> None:
        await inter.response.defer()
        if not await is_in_voice(inter):
            await inter.send(f'{inter.author.mention} you are not in the same voice channel as me. I cannot pause this track.')

        player = cast(Player, inter.guild.voice_client)
        player.continuous = not player.continuous

        await inter.send(f'Continuous play is now {"on" if player.continuous else "off"}.')
