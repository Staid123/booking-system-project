from enum import Enum


class RoomType(Enum):
    SINGLE = "Одноместный"
    DOUBLE = "Двухместный"
    SUITE = "Люкс"
    FAMILY = "Семейный"
    DELUXE = "Делюкс"


class RoomStatus(Enum):
    AVAILABLE = "available" # доступен
    BOOKED = "booked" # забронирован
    MAINTENANCE = "maintenance" # обслуживается
    OCCUPIED = "occupied" # занят
    CLEANING = "cleaning" # уборка


class BookingStatus(Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    FINISHED = "finished"