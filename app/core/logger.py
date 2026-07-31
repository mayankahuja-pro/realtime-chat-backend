import logging
from app.core.config import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("chat_app")