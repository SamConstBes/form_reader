#config_app.py
import os

from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class SFTPConfig:
    host: str = "127.0.0.1"
    port: int = 5432
    user: str = ""
    password: str = ""


@dataclass(frozen=True)
class AppConfig:
    UPLOAD_FOLDER = os.get_env("UPLOAD_FOLDER")
    sftp: SFTPConfig = SFTPConfig (
        host=os.getenv("SFTP_HOST", "127.0.0.1"),
        port=int(os.getenv("SFTP_PORT", 5432)),
        user=os.getenv("SFTP_USER", ""),
        password=os.getenv("SFTP_PASS", "")
    )

app_config = AppConfig()