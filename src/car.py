#Subclass Car.

from insurance_mixin import InsuranceMixin
from vehicle import Vehicle
# [BARU] Import custom exception dari errors.py.
from errors import InvalidDataError

class Car(InsuranceMixin, Vehicle):
    TYPE_NAME = "Mobil"

    def __init__(self, plate_number: str, brand: str, daily_rate: int, seats: int):
        super().__init__(plate_number, brand, daily_rate)
        self.seats = seats

    @property
    def seats(self) -> int:
        return self.__seats

    @seats.setter
    def seats(self, value: int) -> None:
        # [UBAH] Ditambah cek `bool`; ValueError -> InvalidDataError.
        # Aturan bisnis #4: jumlah kursi harus bilangan bulat lebih dari 0.
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise InvalidDataError("seats", value, f"Jumlah kursi harus bilangan bulat lebih dari 0, bukan {value!r}.")
        self.__seats = value

    def _extra_info(self) -> str:
        return f"Kursi: {self.seats} orang"
