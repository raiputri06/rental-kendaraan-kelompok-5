# Subclass Van.

from insurance_mixin import InsuranceMixin
from vehicle import Vehicle
# [BARU] Import custom exception dari errors.py.
from errors import InvalidDataError

class Van(InsuranceMixin, Vehicle):
    TYPE_NAME = "Van"

    def __init__(self, plate_number: str, brand: str, daily_rate: int, capacity: int):
        super().__init__(plate_number, brand, daily_rate)
        self.capacity = capacity

    @property
    def capacity(self) -> int:
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        # [UBAH] Ditambah cek `bool`; ValueError -> InvalidDataError.
        # Aturan bisnis #4: kapasitas van harus bilangan bulat lebih dari 0.
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise InvalidDataError("capacity", value, f"Kapasitas harus bilangan bulat lebih dari 0, bukan {value!r}.")
        self.__capacity = value

    def _extra_info(self) -> str:
        return f"Kapasitas: {self.capacity} orang"
