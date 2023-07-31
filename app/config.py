from typing import Any
from typing import Optional
from urllib.parse import quote_plus as urlquote

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, case_sensitive=True):
    POSTGRE_SERVER: str
    POSTGRE_USER: str
    POSTGRE_PASSWORD: str
    POSTGRE_DB: str
    POSTGRE_PORT: Optional[int] = 5432

    # here we can choose to save all the user uploaded files including profile_pictures
    # recommended: attach an external storage (a NAS disk or a storage bucket as filesystem)
    # or the local disk storage might run out
    # example:
    # fs_mount_path: Optional[str] = "/custom/filesystem/"
    fs_mount_path: Optional[str] = ""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    def assemble_db_connection(self) -> Any:
        pg_server = self.POSTGRE_SERVER
        pg_user = self.POSTGRE_USER
        pg_password = urlquote(self.POSTGRE_PASSWORD)
        pg_port = self.POSTGRE_PORT
        pg_db = self.POSTGRE_DB

        uri = f"postgresql://{pg_user}:{pg_password}" \
              f"@{pg_server}:{pg_port}/{pg_db}"
        return uri


settings = Settings()
