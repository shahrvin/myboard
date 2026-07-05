from datetime import datetime, timedelta, timezone
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.encryption import EncryptedJSON, EncryptedString
from app.enums import BoardVisibility

tz_teh = timezone(timedelta(hours=3, minutes=30))


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    avatar_url = Column(Text, nullabale=True)
    is_active = Column(Boolean, default=True, nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.tz_teh),
        onupdate=lambda: datetime.now(timezone.tz_teh),
        nullable=False,
    )
    boards = relationship("Board", back_populates="admin", cascade="all, delete-orphan")
    vault_folders = relationship("VaultFolder", back_populates="admin", cascade="all, delete-orphan")
    # widgets = relationship("Widget", back_populates="admin", cascade="all, delete-orphan")


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    title = Column(EncryptedString, nullable=False, default="Untitled Board")
    description = Column(EncryptedString, nullable=True)

    visibility = Column(
        StrEnum(BoardVisibility, name="board_visibility"), nullable=False, default=BoardVisibility.PRIVATE, index=True
    )
    is_archived = Column(Boolean, nullable=False, default=False)

    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    owner_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True)
    owner = relationship("Admin", back_populates="boards")

    widgets = relationship("Widget", back_populates="board", cascade="all, delete-orphan", order_by="Widget.z_index")

    members = relationship("BoardMember", back_populates="board", cascade="all, delete-orphan")

    share_links = relationship("BoardShareLink", back_populates="board", cascade="all, delete-orphan")


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)

    widget_type = Column(String(50), nullable=False, index=True)

    title = Column(EncryptedString, nullable=False, default="")

    data = Column(EncryptedJSON, nullable=False, default=dict)

    position_x = Column(Float, nullable=False, default=0.0)

    position_y = Column(Float, nullable=False, default=0.0)

    width = Column(Float, nullable=False, default=320.0)

    height = Column(Float, nullable=False, default=240.0)

    z_index = Column(Integer, nullable=False, default=0)

    rotation = Column(Float, nullable=False, default=0.0)

    visible = Column(Boolean, nullable=False, default=True)

    locked = Column(Boolean, nullable=False, default=False)

    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    board = relationship("Board", back_populates="widgets")

    __table_args__ = Index("ix_widgets_board_updated", "board_id", "updated_at")


class BoardRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class BoardMember(Base):
    __tablename__ = "board_members"

    id = Column(Integer, primary_key=True)

    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(StrEnum(BoardRole, name="board_role"), nullable=False, default=BoardRole.VIEWER)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    board = relationship("Board", back_populates="members")

    admin = relationship("Admin")

    __table_args__ = UniqueConstraint("board_id", "admin_id", name="uq_board_member")


class BoardShareLink(Base):
    __tablename__ = "board_share_links"

    id = Column(Integer, primary_key=True)

    token_hash = Column(String(255), nullable=False, unique=True, index=True)

    can_edit = Column(Boolean, nullable=False, default=False)

    is_active = Column(Boolean, nullable=False, default=True)

    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    board = relationship("Board", back_populates="share_links")


class VaultFolder(Base):
    __tablename__ = "vault_folders"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(EncryptedString, nullable=False)

    icon = Column(String(50), nullable=True)

    sort_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True)
    admin = relationship("Admin", back_populates="vault_folders")

    entries = relationship("VaultEntry", back_populates="folder", cascade="all, delete-orphan")


class VaultEntry(Base):
    __tablename__ = "vault_entries"

    id = Column(Integer, primary_key=True)

    entry_type = Column(String(50), nullable=False)

    title = Column(EncryptedString, nullable=False)

    data = Column(EncryptedJSON, nullable=False, default=dict)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    folder_id = Column(Integer, ForeignKey("vault_folders.id", ondelete="CASCADE"), nullable=False, index=True)
    folder = relationship("VaultFolder", back_populates="entries")
