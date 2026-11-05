# Parent class (abstract) semua kendaraan.

import re
from abc import ABC, abstractmethod
# [BARU] Import custom exception dari errors.py.
from errors import InvalidDataError, VehicleUnavailableError

class Vehicle(ABC):
    TYPE_NAME = "Kendaraan"
    _total_created = 0

    def _init_(self, plate_number: str, brand: str, daily_rate: int):
        # [UBAH] Sebelumnya: Vehicle.is_valid_plate(...) + raise ValueError.
        # Sekarang: self.is_valid_plate(...) + raise InvalidDataError (pesan ditambah contoh format).
        # Aturan bisnis #1: plat nomor harus valid.
        if not self.is_valid_plate(plate_number):
            raise InvalidDataError("plate_number", plate_number, f"Format plat nomor tidak valid: {plate_number!r}. Contoh: DK 1234 AB.")
        self.__plate_number = plate_number
        self.brand = brand
        self.daily_rate = daily_rate
        self.__available = True
        Vehicle._total_created += 1

    @property
    def plate_number(self) -> str:
        return self.__plate_number

    @property
    def brand(self) -> str:
        return self.__brand

    @brand.setter
    def brand(self, value: str) -> None:
        # [UBAH] Kondisi sama, yang berubah: ValueError -> InvalidDataError.
        # Aturan bisnis #2: merek tidak boleh kosong.
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("brand", value, "Merek kendaraan tidak boleh kosong.")
        self.__brand = value.strip()

    @property
    def daily_rate(self) -> int:
        return self.__daily_rate

    @daily_rate.setter
    def daily_rate(self, value: int) -> None:
        # [UBAH] Ditambah isinstance(value, bool) supaya True/False tidak lolos sebagai angka
        # (bool adalah turunan int di Python). ValueError -> InvalidDataError.
        # Aturan bisnis #2: harga sewa harus bilangan bulat positif.
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise InvalidDataError("daily_rate", value, f"Harga sewa harus bilangan bulat positif, bukan {value!r}.")
        self.__daily_rate = value

    @property
    def is_available(self) -> bool:
        return self.__available

    @classmethod
    def get_total_created(cls) -> int:
        return Vehicle._total_created

    @staticmethod
    def is_valid_plate(plate_number: str) -> bool:
        # [UBAH] Ditambah isinstance(plate_number, str) agar input bukan string (mis. None/angka)
        # menghasilkan False, bukan crash TypeError di re.fullmatch.
        return isinstance(plate_number, str) and re.fullmatch(r"[A-Z]{1,2} \d{1,4} [A-Z]{1,3}", plate_number) is not None

    def mark_rented(self) -> None:
        # [UBAH] RuntimeError -> VehicleUnavailableError.
        # Aturan bisnis #6: kendaraan yang sedang disewa tidak boleh disewa lagi.
        if not self.__available:
            raise VehicleUnavailableError(self.plate_number, f"{self.brand} ({self.plate_number}) sedang disewa.")
        self.__available = False

    def mark_returned(self) -> None:
        # [UBAH] RuntimeError -> VehicleUnavailableError.
        # Aturan bisnis #7: kendaraan hanya bisa dikembalikan jika sedang disewa.
        if self.__available:
            raise VehicleUnavailableError(self.plate_number, f"{self.brand} ({self.plate_number}) tidak sedang disewa.")
        self.__available = True

    def describe(self) -> str:
        return f"{self.TYPE_NAME} {self.brand} | Plat: {self.plate_number} | {self._extra_info()}"

    @abstractmethod
    def _extra_info(self) -> str:
        """Wajib di-override oleh subclass."""

    def _str_(self) -> str:
        return self.describe()

    def _repr_(self) -> str:
        return f"{type(self)._name_}(plate_number={self.plate_number!r}, brand={self.brand!r})"

    def _eq_(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.plate_number == other.plate_number

    def _hash_(self) -> int:
        return hash(self.plate_number)