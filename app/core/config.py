from functools import lru_cache
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AURUM Sweet Alchemy API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    frontend_origins: str = "http://localhost:5173"
    db_server: str = "localhost"
    db_name: str = "AurumSweetAlchemyDB"
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_trusted_connection: bool = True
    db_encrypt: bool = False
    db_trust_server_certificate: bool = True
    db_user: str = ""
    db_password: str = ""
    jwt_secret: str = "CAMBIA_ESTA_CLAVE"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self):
        return [x.strip() for x in self.frontend_origins.split(",") if x.strip()]

    @property
    def database_url(self):
        parts = [f"DRIVER={{{self.db_driver}}}", f"SERVER={self.db_server}", f"DATABASE={self.db_name}"]
        if self.db_trusted_connection:
            parts.append("Trusted_Connection=yes")
        else:
            parts.extend([f"UID={self.db_user}", f"PWD={self.db_password}"])
        parts.extend([
            f"Encrypt={'yes' if self.db_encrypt else 'no'}",
            f"TrustServerCertificate={'yes' if self.db_trust_server_certificate else 'no'}",
        ])
        return "mssql+pyodbc:///?odbc_connect=" + quote_plus(";".join(parts))

@lru_cache
def get_settings(): return Settings()
settings=get_settings()
