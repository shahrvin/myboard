from datetime import datetime
from typing import Optional

from alembic.environment import Any
from pydantic import BaseModel, Field

from app.enums import BoardVisibility, WidgetType


class AdminCreate(BaseModel):
    username: str
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class WidgetBase(BaseModel):
    title: str = ""
    widget_type: str = "note"
    data: dict = {}
    position_x: float = 0.0
    position_y: float = 0.0
    z_index: int = 0
    visible: bool = True


class WidgetCreate(BaseModel):
    widget_type: WidgetType
    title: str = ""
    data: dict[str, Any] = Field(default_factory=dict)

    position_x: float = 0
    position_y: float = 0

    width: float = 320
    height: float = 240

    z_index: int = 0
    rotation: float = 0


class WidgetUpdate(BaseModel):
    title: str | None = None
    data: dict[str, Any] | None = None

    position_x: float | None = None
    position_y: float | None = None

    width: float | None = None
    height: float | None = None

    z_index: int | None = None
    rotation: float | None = None

    visible: bool | None = None
    locked: bool | None = None

    version: int

class WidgetResponse(WidgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}



class WidgetPosition(BaseModel):
    x: float
    y: float
    z_index: int = 0


class WidgetSize(BaseModel):
    width: float = Field(gt=0)
    height: float = Field(gt=0)


class BoardCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    visibility: BoardVisibility = BoardVisibility.PRIVATE


class BoardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    visibility: BoardVisibility | None = None
    is_archived: bool | None = None
    version: int


class WidgetLayoutUpdate(BaseModel):
    id: int
    position_x: float
    position_y: float
    width: float
    height: float
    z_index: int
    rotation: float


class BoardLayoutUpdate(BaseModel):
    widgets: list[WidgetLayoutUpdate]