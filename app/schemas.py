from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class WidgetCreate(WidgetBase):
    pass


class WidgetUpdate(BaseModel):
    title: Optional[str] = None
    widget_type: Optional[str] = None
    data: Optional[dict] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    z_index: Optional[int] = None
    visible: Optional[bool] = None


class WidgetResponse(WidgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
