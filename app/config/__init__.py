from loguru import logger
from helpers import EXIT
from redminelib import Redmine
from pydantic import BaseSettings, Field
from datetime import datetime, time

from .settings import RTMSettings

settings = RTMSettings()

