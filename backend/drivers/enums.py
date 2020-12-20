from enum import Enum


class TransportType(Enum):
    car = "car"
    minubus = "minibus"
    bus = "bus"
    other = "other"

    @property
    def description(self):
        if self is self.car:
            return "Транспорт до 8 мест."
        elif self is self.minubus:
            return "Транспорт свыше 8 и не более 20 мест."
        elif self is self.bus:
            return "Транспорт свыше 20 мест."
        elif self is self.other:
            return "Другое."


class DriverErrors(Enum):
    driver_already_exist = "Карточка водителя была ранее создана."
    transport_already_exist = "Транспорт с такими данными уже есть в системе."
    car_not_belong_to_driver = "Данный транспорт не принадлежит текущему пользователю."
