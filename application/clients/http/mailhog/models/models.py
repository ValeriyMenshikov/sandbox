from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class From(BaseModel):
    relays: Any = Field(None, alias="Relays")
    mailbox: str = Field(None, alias="Mailbox")
    domain: str = Field(None, alias="Domain")
    params: str = Field(None, alias="Params")


class ToItem(BaseModel):
    relays: Any = Field(None, alias="Relays")
    mailbox: str = Field(None, alias="Mailbox")
    domain: str = Field(None, alias="Domain")
    params: str = Field(None, alias="Params")


class Headers(BaseModel):
    content__type: List[str] = Field(None, alias="Content-Type")
    date: List[str] = Field(None, alias="Date")
    from_: List[str] = Field(None, alias="From")
    mime__version: List[str] = Field(None, alias="MIME-Version")
    message__id: List[str] = Field(None, alias="Message-Id")
    received: List[str] = Field(None, alias="Received")
    reply__to: List[str] = Field(None, alias="Reply-To")
    return__path: List[str] = Field(None, alias="Return-Path")
    subject: List[str] = Field(None, alias="Subject")
    to: List[str] = Field(None, alias="To")


class Content(BaseModel):
    headers: Headers = Field(None, alias="Headers")
    body: str = Field(None, alias="Body")
    size: int = Field(None, alias="Size")
    mime: Any = Field(None, alias="MIME")


class Raw(BaseModel):
    from_: str = Field(None, alias="From")
    to: List[str] = Field(None, alias="To")
    data: str = Field(None, alias="Data")
    helo: str = Field(None, alias="Helo")


class Item(BaseModel):
    id: str = Field(None, alias="ID")
    from_: From = Field(None, alias="From")
    to: List[ToItem] = Field(None, alias="To")
    content: Content = Field(None, alias="Content")
    created: str = Field(None, alias="Created")
    mime: Any = Field(None, alias="MIME")
    raw: Raw = Field(None, alias="Raw")


class Messages(BaseModel):
    total: Optional[int] = None
    count: Optional[int] = None
    start: Optional[int] = None
    items: Optional[List[Item]] = None
