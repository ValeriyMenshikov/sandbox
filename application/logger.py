import sys
import traceback
from collections import namedtuple
from enum import Enum
from typing import Optional

import loguru
import orjson
from pydantic_settings import BaseSettings


class LogLevelEnum(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LoggerSettings(BaseSettings):
    log_json: bool = True
    log_level: LogLevelEnum = LogLevelEnum.DEBUG


TraceInfo = namedtuple("TraceInfo", ["trace_id", "span_id"])


def serialize(record: dict) -> str:
    trace_info: TraceInfo = record["extra"].pop("trace_info", TraceInfo("0", "0"))
    log_direction = record["extra"].pop("log_direction", "all")
    subset = {
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "function": f'{record["name"]}.{record["function"]}:{record["line"]}',
        "message": record["message"],
        "level": record["level"].name,
        "log-direction": log_direction,
        "trace_id": trace_info.trace_id,
        "span_id": trace_info.span_id,
        "extra": record.get("extra", {}),
        "exception": (traceback.format_exception(*record["exception"]) if record["exception"] else None),
        "process": f"PID={record['process'].id} name={record['process'].name}",
    }

    return orjson.dumps(subset, default=str).decode("utf-8")


def patching(record: dict) -> None:
    record["serialized"] = serialize(record)  # type: ignore[typeddict-unknown-key]


def build_root_logger(log_settings: Optional[LoggerSettings] = None):  # type: ignore[no-untyped-def]
    log_settings_ = log_settings or LoggerSettings()
    loguru.logger.remove()
    if log_settings_.log_json:
        loguru.logger.configure(patcher=patching)  # type: ignore[arg-type]
        loguru.logger.add(
            sys.stdout,
            level=log_settings_.log_level.value,
            format=lambda _: "{serialized}\n",
            backtrace=False,
            diagnose=False,
            serialize=False,
        )
    else:
        loguru.logger.add(
            sys.stdout,
            level=log_settings_.log_level.value,
        )

    return loguru.logger


LOGGER = build_root_logger()


def get_logger(name: str):  # type: ignore[no-untyped-def]
    return loguru.logger.bind(logger_name=name)
