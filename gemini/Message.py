from dataclasses import dataclass

@dataclass
class Message:
    message: str
    channel: str
    username: str

@dataclass
class MessageList:
    history: []
    messages_array: []