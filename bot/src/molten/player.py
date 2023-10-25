from typing import Any
import mafic
from mafic.__libraries import Connectable
from mafic.node import Node


class Player(mafic.Player):
    def __init__(self, client: Any, channel: Connectable, *, node: Node | None = None) -> None:
        super().__init__(client, channel, node=node)
        self.continuous = False
        self.queue: list[mafic.Track] = []
        self.queue_just_skipped = False
