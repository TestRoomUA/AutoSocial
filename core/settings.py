from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    provider_token: str
    admin_id: int
    coadmin_id: int


@dataclass
class Media:
    content: str
    post_media_max: int


@dataclass
class Channel:
    id: int


@dataclass
class Settings:
    bots: Bots
    bots2: Bots
    media: Media
    channel: Channel


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots2=Bots(
            bot_token=env.str("TOKEN2"),
            provider_token=env.str("PROVIDER_TOKEN2"),
            admin_id=env.int("ADMIN_ID"),
            coadmin_id=env.int("COADMIN_ID"),
        ),
        bots=Bots(
            bot_token=env.str("TOKEN"),
            provider_token=env.str("PROVIDER_TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            coadmin_id=env.int("COADMIN_ID"),
        ),
        media=Media(
            content=env.str("CONTENT_PATH"),
            post_media_max=env.int("POST_MEDIA_MAX")
        ),
        channel=Channel(
            id=env.int("CHANNEL_ID")
        )
    )


settings = get_settings('input')