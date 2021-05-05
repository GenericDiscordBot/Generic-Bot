from __future__ import annotations

import logging
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord import Webhook


class WebhookHandler(logging.Handler):
    def __init__(self, webhook: Webhook, levels):
        self.webhook = webhook
        self.levels = [level.upper() for level in levels]

        super().__init__()

    def emit(self, record: logging.LogRecord):
        if record.levelname in self.levels:
            asyncio.create_task(self.webhook.send(record.getMessage()))
