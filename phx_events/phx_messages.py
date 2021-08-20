from asyncio import Queue, Task
from dataclasses import dataclass
from enum import Enum, unique
from functools import cached_property
from logging import Logger
from typing import Any, Callable, NewType, Optional, TypedDict, Union


Topic = NewType('Topic', str)
Event = NewType('Event', str)
ChannelEvent = Union['PHXEvent', Event]
ChannelMessage = Union['PHXMessage', 'PHXEventMessage']
HandlerFunction = Callable[[ChannelMessage, Logger], None]


class EventMap(TypedDict):
    queue: Queue[ChannelMessage]
    handlers: list[HandlerFunction]
    task: Task[None]
    topic: Optional[Topic]


@unique
class PHXEvent(Enum):
    close = 'phx_close'
    error = 'phx_error'
    join = 'phx_join'
    reply = 'phx_reply'
    leave = 'phx_leave'

    # hack for typing
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class BasePHXMessage:
    topic: Topic
    ref: Optional[str]
    payload: dict[str, Any]

    @cached_property
    def subtopic(self):
        if ':' not in self.topic:
            return None

        _, subtopic = self.topic.split(':', 1)
        return subtopic


@dataclass(frozen=True)
class PHXMessage(BasePHXMessage):
    event: Event


@dataclass(frozen=True)
class PHXEventMessage(BasePHXMessage):
    event: PHXEvent
