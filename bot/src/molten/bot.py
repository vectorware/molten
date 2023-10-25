from os import environ
from disnake.ext.commands import AutoShardedInteractionBot
import mafic
import redis.asyncio as redis


class Molten(AutoShardedInteractionBot):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.pool = mafic.NodePool(self)
        self.loop.create_task(self.add_nodes(), name="Add required nodes")
        # self.redis = redis.from_url(environ["REDIS_URI"])

    # this only supports one node rn, but I doubt we will ever have to scale beyond that.
    async def add_nodes(self):
        await self.pool.create_node(
            host=environ["LAVALINK_HOST"],
            port=int(environ["LAVALINK_PORT"]),
            label="MAIN",
            password=environ["LAVALINK_PASSWORD"],
        )
