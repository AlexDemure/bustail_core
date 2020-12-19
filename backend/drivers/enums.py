from enum import Enum


class TransportType(Enum):
    car = "car"
    minubus = "minibus"
    bus = "bus"

    @property
    def description(self):
        if self is self.car:
            return "Транспорт до 8 мест."
        elif self is self.minubus:
            return "Транспорт свыше 8 и не более 20 мест."
        elif self is self.bus:
            return "Транспорт свыше 20 мест."


class DriverErrors(Enum):
    driver_already_exist = "Карточка водителя была ранее создана."

