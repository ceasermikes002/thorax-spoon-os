import os


class Settings:
    def __init__(self):
        self.env = os.getenv("APP_ENV", "development")
        self.debug = os.getenv("DEBUG", "0") == "1"
        self.smtp_host = os.getenv("SMTP_HOST", "")


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

