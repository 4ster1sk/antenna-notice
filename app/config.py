import dataclasses

@dataclasses.dataclass
class Config:
    discord_webhook: str
    host: str
    token: str
    antenna_id: str
    deny_filter: list
    accept_filter: list