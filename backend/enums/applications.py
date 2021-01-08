from enum import Enum


class ApplicationStatus(Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    completed = "completed"
    rejected = "rejected"
    expired = "expired"

    @property
    def description(self):
        if self is self.waiting:
            return "В ожидании"
        elif self is self.confirmed:
            return "Подтверждена"
        elif self is self.rejected:
            return "Отменена"
        elif self is self.expired:
            return "Истекла"
        elif self is self.completed:
            return "Выполнена"


class ApplicationTypes(Enum):
    wedding = "wedding"
    watch = "watch"
    tour = "tour"
    intercity = "intercity"
    other = "other"

    @property
    def description(self):
        if self is self.wedding:
            return "Свадьба"
        elif self is self.watch:
            return "Вахта"
        elif self is self.tour:
            return "Путешествие"
        elif self is self.intercity:
            return "Междугородние"
        elif self is self.other:
            return "Другое"


class ApplicationErrors(Enum):
    to_go_when_wrong_format = "Дата назначения поездки должна быть больше текущей."
    application_does_not_belong_this_user = "Заявки не принадлежит данному пользователю."
    application_has_ended_status = "Заявка переведена в промежуточный или конечный статус."
