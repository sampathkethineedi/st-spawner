# IMPORTANT
# rename this file to config.py and add the details

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = ""
    API_URL: str = ""
