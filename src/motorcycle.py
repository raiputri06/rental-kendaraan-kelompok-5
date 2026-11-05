#Subclass Motorcycle.

from vehicle import Vehicle
# [BARU] Import ini custom exception dari errors.py.
from errors import InvalidDataError

class Motorcycle(Vehicle):
    TYPE_NAME = "Motor"

    def __init__(self, plate_number: str, brand: str, daily_rate: int, motor_type: str):
        super().__init__(plate_number, brand, daily_rate)
        # [UBAH] Sebelumnya `self.__motor_type = motor_type` (tanpa validasi).
        # Sekarang dia lewat setter agar nilai divalidasi.
        self.motor_type = motor_type

    @property
    def motor_type(self) -> str:
        return self.__motor_type

    # [BARU] Setter motor_type (sebelumnya hanya getter). Jenis motor kosong -> InvalidDataError.
    @motor_type.setter
    def motor_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("motor_type", value, "Jenis motor tidak boleh kosong.")
        self.__motor_type = value.strip()

    def _extra_info(self) -> str:
        return f"Jenis: {self.motor_type}"
