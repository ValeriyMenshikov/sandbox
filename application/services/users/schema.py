from typing import Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: Optional[str] = Field(None, description="User real name")
    login: str = Field(None, description="User real name")
    location: Optional[str] = Field(None, description="User real location")
    icq: Optional[str] = Field(None, description="User ICQ")
    skype: Optional[str] = Field(None, description="User Skype")
    info: Optional[str] = Field(None, description="User info")


class UsersSchema(BaseModel):
    users: list[UserSchema] = Field(None, description="List of users")
