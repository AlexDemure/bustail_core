from enum import Enum


class ApplicationStatus(Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    rejected = "rejected"


class ApplicationTypes(Enum):
    wedding = "wedding"
    watch = "watch"
    other = "other"
