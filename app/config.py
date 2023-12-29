"""
path: config/config.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """"
    Settings class to load environment variables from .env file
    """
    # Email configurations
    EMAIL_ADDRESS: str = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD')
    IMAP_SERVER: str = os.getenv('IMAP_SERVER')
    WORD_IN_SUBJECT: str = os.getenv('WORD_IN_SUBJECT')

    # Google Sheets congifurations
    CREDENTIALS_FILE_PATH: str = os.getenv('CREDENTIALS_FILE_PATH')

    # Scheduler configurations (if any specifi configs are needed)
    SCHEDULE_TIME: str = os.getenv('SCHEDULE_TIME')
    SHEET_NAME: str = os.getenv('SHEET_NAME')
    SPREADSHEET_NAME: str = os.getenv('SPREADSHEET_NAME', "Invoice Data")

    PDF_DIR: str = os.getenv('PDF_DIR', "pdfs")
    TEMPLATES_DIR: str = os.getenv('TEMPLATES_DIR', "templates")

    USERNAME: str = os.getenv('USERNAME')
    PASSWORD: str = os.getenv('PASSWORD')

    SUPPER_USER: str = os.getenv('SUPPER_USER')
    SUPPER_USER_PASSWORD: str = os.getenv('SUPPER_USER_PASSWORD')

    class Config:
        """
        Config class to load environment variables from .env file
        """
        env_file = ".env"

settings = Settings()
