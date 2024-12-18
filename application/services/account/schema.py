from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str | None = Field(None, description="User real name", serialization_alias="Name")
    location: str | None = Field(None, description="User real location", serialization_alias="Location")
    icq: str | None = Field(None, description="User ICQ", serialization_alias="Icq")
    skype: str | None = Field(None, description="User Skype", serialization_alias="Skype")
    info: str | None = Field(None, description="User info", serialization_alias="Info")
    profile_picture_url: str | None = Field(
        None, description="Profile picture URL", serialization_alias="ProfilePictureUrl"
    )
    medium_profile_picture_url: str | None = Field(
        None, description="Medium profile picture URL", serialization_alias="MediumProfilePictureUrl"
    )
    small_profile_picture_url: str | None = Field(
        None, description="Small profile picture URL", serialization_alias="SmallProfilePictureUrl"
    )
