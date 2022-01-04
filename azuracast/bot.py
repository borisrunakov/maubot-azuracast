import logging
from typing import Type
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from azuracast.radio import RadioInfo

logger = logging.getLogger(__name__)


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("radio_api_address")
        helper.copy("radio_idx")


class AzuracastBot(Plugin):
    config: Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()
        self.radio = RadioInfo(self.config["radio_api_address"], self.config["radio_idx"])

    def on_external_config_update(self) -> None:
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.new("radio", aliases=['r'])
    async def radio(self) -> None:
        pass

    @radio.subcommand("listeners", aliases=['ls'], help="Current listeners counter.")
    async def handler(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        await self.radio.update()
        await evt.reply(self.radio.get_listeners(), allow_html=True)

    @radio.subcommand("now", help="Playing now.")
    async def handler(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        await self.radio.update()
        await evt.reply(self.radio.get_now_playing(), allow_html=True)

    @radio.subcommand("next", help="Playing next.")
    async def handler(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        await self.radio.update()
        await evt.reply(self.radio.get_next_playing(), allow_html=True)

    @radio.subcommand("streamer", aliases=['str'], help="Who's the streamer yo.")
    async def handler(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        await self.radio.update()
        await evt.reply(self.radio.get_streamer(), allow_html=True)

    @radio.subcommand("all", aliases=['a'], help="Print all available radio information.")
    async def handler(self, evt: MessageEvent) -> None:
        await evt.mark_read()
        await self.radio.update()
        await evt.reply(self.radio.get_all(), allow_html=True)
