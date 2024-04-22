from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Media:
    content: str


@dataclass
class Channel:
    id: int


@dataclass
class Settings:
    bots: Bots
    media: Media
    channel: Channel


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        ),
        media=Media(
            content=env.str("CONTENT_PATH")
        ),
        channel=Channel(
            id=env.int("CHANNEL_ID")
        )
    )


settings = get_settings('input')