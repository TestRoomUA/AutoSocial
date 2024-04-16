from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    coadmin_id: int
    content_path: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            coadmin_id=env.int("COADMIN_ID"),
            content_path=env.str("CONTENT_PATH")
        )
    )


settings = get_settings('input')