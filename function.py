"""
title: Keep Only Last N Images
author: open-webui community
version: 1.0
description: Automatically drops older image attachments from chat history to keep local GPU inference fast.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        max_images: int = Field(
            default=2, description="Number of recent images to keep in context."
        )

    def __init__(self):
        self.valves = self.Valves()

    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        messages = body.get("messages", [])
        image_count = 0

        for message in reversed(messages):
            content = message.get("content", "")

            if isinstance(content, list):
                for item in list(content):
                    if item.get("type") == "image_url":
                        image_count += 1
                        if image_count > self.valves.max_images:
                            content.remove(item)

        return body
