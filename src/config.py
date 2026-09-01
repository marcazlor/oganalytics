"""
Configuración centralizada de OGAnalytics.

Los valores que cambian según el entorno (local, Docker, producción)
se leen de variables de entorno o del fichero .env. Las rutas del
proyecto se calculan desde la ubicación de este archivo, para que
funcionen se ejecute desde donde se ejecute.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py está en src/ → un nivel por debajo de la raíz
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Rutas del proyecto. No son configuración de entorno: son iguales
# en cualquier máquina y se derivan de la estructura del repositorio.
RAW_DIR = PROJECT_ROOT / 'data' / 'raw'
MODELS_DIR = PROJECT_ROOT / 'models'
MODEL_PATH = MODELS_DIR / 'ridge_spread.pkl'


class Settings(BaseSettings):
    """Variables de entorno del proyecto."""

    database_url: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


# Instancia única, importable desde el resto del proyecto.
settings = Settings()