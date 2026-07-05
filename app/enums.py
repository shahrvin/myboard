from enum import Enum


class BoardVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"


class BoardRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class WidgetType(str, Enum):
    NOTE = "note"
    TODO = "todo"
    TABLE = "table"
    CALENDAR = "calendar"
    JOURNAL = "journal"
    HABIT_TRACKER = "habit_tracker"
    LINKS = "links"
    PROFILE = "profile"
    TECH_STACK = "tech_stack"
    TEXT = "text"
    IMAGE = "image"
    EMBED = "embed"