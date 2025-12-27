"""Watchtower utilities."""

from watchtower.utils.windows import (
    is_windows,
    get_data_directory,
    send_notification,
    create_scheduled_task,
    remove_scheduled_task,
    open_with_default_app,
    copy_to_clipboard,
    get_clipboard,
    play_sound,
)

__all__ = [
    "is_windows",
    "get_data_directory",
    "send_notification",
    "create_scheduled_task",
    "remove_scheduled_task",
    "open_with_default_app",
    "copy_to_clipboard",
    "get_clipboard",
    "play_sound",
]
