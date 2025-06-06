from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class BadRequestError(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    message: Optional[str] = Field(None, description="Client message")
    invalid_properties: Optional[Dict[str, List[str]]] = Field(
        None,
        alias="invalidProperties",
        description="Key-value pairs of invalid request properties",
    )


class BbParseMode(Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class ChangeEmail(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="User login")
    password: Optional[str] = Field(None, description="User password")
    email: Optional[str] = Field(None, description="New user email")


class ChangePassword(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="User login")
    token: Optional[str] = Field(None, description="Password reset token")
    old_password: Optional[str] = Field(None, alias="oldPassword", description="Old password")
    new_password: Optional[str] = Field(None, alias="newPassword", description="New password")


class ColorSchema(Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class GeneralError(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    message: Optional[str] = Field(None, description="Client message")


class InfoBbText(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    value: Optional[str] = Field(None, description="Text")
    parse_mode: Optional[BbParseMode] = Field(None, alias="parseMode")


class LoginCredentials(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    login: Optional[str] = None
    password: Optional[str] = None
    remember_me: Optional[bool] = Field(None, alias="rememberMe")


class PagingSettings(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    posts_per_page: Optional[int] = Field(None, alias="postsPerPage", description="Number of posts on a game room page")
    comments_per_page: Optional[int] = Field(
        None,
        alias="commentsPerPage",
        description="Number of commentaries on a game or a topic page",
    )
    topics_per_page: Optional[int] = Field(
        None,
        alias="topicsPerPage",
        description="Number of detached topics on a forum page",
    )
    messages_per_page: Optional[int] = Field(
        None,
        alias="messagesPerPage",
        description="Number of private messages and conversations on dialogue page",
    )
    entities_per_page: Optional[int] = Field(
        None, alias="entitiesPerPage", description="Number of other entities on page"
    )


class Rating(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    enabled: Optional[bool] = Field(None, description="Rating participation flag")
    quality: Optional[int] = Field(None, description="Quality rating")
    quantity: Optional[int] = Field(None, description="Quantity rating")


class Registration(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="Login")
    email: Optional[str] = Field(None, description="Email")
    password: Optional[str] = Field(None, description="Password")


class ResetPassword(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="Login")
    email: Optional[str] = Field(None, description="Email")


class UserRole(Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class UserSettings(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    color_schema: Optional[ColorSchema] = Field(None, alias="colorSchema")
    nanny_greetings_message: Optional[str] = Field(
        None,
        alias="nannyGreetingsMessage",
        description="Message that user's newbies will receive once they are connected",
    )
    paging: Optional[PagingSettings] = None


class User(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="Login")
    roles: Optional[List[UserRole]] = Field(None, description="Roles")
    medium_picture_url: Optional[str] = Field(None, alias="mediumPictureUrl", description="Profile picture URL M-size")
    small_picture_url: Optional[str] = Field(None, alias="smallPictureUrl", description="Profile picture URL S-size")
    status: Optional[str] = Field(None, description="User defined status")
    rating: Optional[Rating] = None
    online: Optional[AwareDatetime] = Field(None, description="Last seen online moment")
    name: Optional[str] = Field(None, description="User real name")
    location: Optional[str] = Field(None, description="User real location")
    registration: Optional[AwareDatetime] = Field(None, description="User registration moment")


class UserDetails(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    login: Optional[str] = Field(None, description="Login")
    roles: Optional[List[UserRole]] = Field(None, description="Roles")
    medium_picture_url: Optional[str] = Field(None, alias="mediumPictureUrl", description="Profile picture URL M-size")
    small_picture_url: Optional[str] = Field(None, alias="smallPictureUrl", description="Profile picture URL S-size")
    status: Optional[str] = Field(None, description="User defined status")
    rating: Optional[Rating] = None
    online: Optional[AwareDatetime] = Field(None, description="Last seen online moment")
    name: Optional[str] = Field(None, description="User real name")
    location: Optional[str] = Field(None, description="User real location")
    registration: Optional[AwareDatetime] = Field(None, description="User registration moment")
    icq: Optional[str] = Field(None, description="User ICQ number")
    skype: Optional[str] = Field(None, description="User Skype login")
    original_picture_url: Optional[str] = Field(
        None, alias="originalPictureUrl", description="URL of profile picture original"
    )
    info: Optional[InfoBbText | str] = None
    settings: Optional[UserSettings] = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = Field(None, description="Additional metadata")


class UserEnvelope(BaseModel):
    model_config = ConfigDict(
        # extra="forbid",
    )
    resource: User = None
    metadata: dict = Field(None, description="Additional metadata")
