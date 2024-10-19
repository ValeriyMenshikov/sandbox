from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class From(BaseModel):
    relays: Any = Field(..., alias="Relays")
    mailbox: str = Field(..., alias="Mailbox")
    domain: str = Field(..., alias="Domain")
    params: str = Field(..., alias="Params")


class ToItem(BaseModel):
    relays: Any = Field(..., alias="Relays")
    mailbox: str = Field(..., alias="Mailbox")
    domain: str = Field(..., alias="Domain")
    params: str = Field(..., alias="Params")


class Headers(BaseModel):
    content__type: List[str] = Field(..., alias="Content-Type")
    date: List[str] = Field(..., alias="Date")
    from_: List[str] = Field(..., alias="From")
    mime__version: List[str] = Field(..., alias="MIME-Version")
    message__id: List[str] = Field(..., alias="Message-Id")
    received: List[str] = Field(..., alias="Received")
    reply__to: List[str] = Field(..., alias="Reply-To")
    return__path: List[str] = Field(..., alias="Return-Path")
    subject: List[str] = Field(..., alias="Subject")
    to: List[str] = Field(..., alias="To")


class Content(BaseModel):
    headers: Headers = Field(..., alias="Headers")
    body: str = Field(..., alias="Body")
    size: int = Field(..., alias="Size")
    mime: Any = Field(..., alias="MIME")


class Raw(BaseModel):
    from_: str = Field(..., alias="From")
    to: List[str] = Field(..., alias="To")
    data: str = Field(..., alias="Data")
    helo: str = Field(..., alias="Helo")


class Item(BaseModel):
    id: str = Field(..., alias="ID")
    from_: From = Field(..., alias="From")
    to: List[ToItem] = Field(..., alias="To")
    content: Content = Field(..., alias="Content")
    created: str = Field(..., alias="Created")
    mime: Any = Field(..., alias="MIME")
    raw: Raw = Field(..., alias="Raw")


class Messages(BaseModel):
    total: Optional[int] = None
    count: Optional[int] = None
    start: Optional[int] = None
    items: Optional[List[Item]] = None
