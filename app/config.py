import dataclasses

@dataclasses.dataclass
class Config:
    discord_webhook: str
    host: str
    token: str
    antenna_id: str
    deny_filter: list
    allow_filter: list
    filter_default_mode: str = 'deny'
    loglevel: str = 'INFO'

    @property
    def is_filter_allow_mode(self) -> bool:
        return self.filter_default_mode.lower() == 'allow'