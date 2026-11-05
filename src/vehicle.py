# Parent class (abstract) semua kendaraan.
# KONSEP: abstract class, encapsulation (private + @property + setter validasi),
# class attribute, @classmethod, @staticmethod, __str__/__repr__/__eq__/__hash__.


# Mengimpor modul atau class yang digunakan file ini.
import re
# Mengimpor modul atau class yang digunakan file ini.
from abc import ABC, abstractmethod


# Mendefinisikan class Vehicle.
class Vehicle(ABC):
    # Cetakan umum semua kendaraan. Tidak bisa dibuat objek langsung.

    # Mengisi atau memperbarui nilai variabel/atribut.
    TYPE_NAME = "Kendaraan"  # class attribute: ditimpa oleh subclass
    # Mengisi atau memperbarui nilai variabel/atribut.
    _total_created = 0       # class attribute (protected): jumlah objek yang dibuat

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, plate_number: str, brand: str, daily_rate: int):
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not Vehicle.is_valid_plate(plate_number):
            # Menghentikan proses dengan melempar error.
            raise ValueError(f"Format plat nomor tidak valid: {plate_number!r}")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__plate_number = plate_number  # instance attribute (private)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.brand = brand                  # lewat setter (ada validasi)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.daily_rate = daily_rate        # lewat setter (ada validasi)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__available = True
        # Mengisi atau memperbarui nilai variabel/atribut.
        Vehicle._total_created += 1         # mengubah class attribute

    # ---------- property (getter / setter) ----------
    # Mendefinisikan method/fungsi plate_number.
    @property
    def plate_number(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__plate_number

    # Mendefinisikan method/fungsi brand.
    @property
    def brand(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__brand

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi brand.
    @brand.setter
    def brand(self, value: str) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(value, str) or not value.strip():
            # Menghentikan proses dengan melempar error.
            raise ValueError("Merek tidak boleh kosong.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__brand = value.strip()

    # Mendefinisikan method/fungsi daily_rate.
    @property
    def daily_rate(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__daily_rate

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi daily_rate.
    @daily_rate.setter
    def daily_rate(self, value: int) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(value, int) or value <= 0:
            # Menghentikan proses dengan melempar error.
            raise ValueError(f"Harga sewa harus bilangan bulat positif, bukan {value!r}.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__daily_rate = value

    # Mendefinisikan method/fungsi is_available.
    @property
    def is_available(self) -> bool:
        # Mengembalikan hasil dari method/fungsi.
        return self.__available

    # ---------- classmethod & staticmethod ----------
    # Mendefinisikan method/fungsi get_total_created.
    @classmethod
    def get_total_created(cls) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return Vehicle._total_created

    # @staticmethod: fungsi biasa di dalam class; tidak butuh 'self' maupun 'cls'.
    # Mendefinisikan method/fungsi is_valid_plate.
    @staticmethod
    def is_valid_plate(plate_number: str) -> bool:
        """Format plat Indonesia sederhana, contoh: DK 1234 AB."""
        # Mengembalikan hasil dari method/fungsi.
        return re.fullmatch(r"[A-Z]{1,2} \d{1,4} [A-Z]{1,3}", plate_number) is not None

    # ---------- perilaku ----------
    # Mendefinisikan method/fungsi mark_rented.
    def mark_rented(self) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not self.__available:
            # Menghentikan proses dengan melempar error.
            raise RuntimeError(f"{self.brand} ({self.plate_number}) sedang disewa.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__available = False

    # Mendefinisikan method/fungsi mark_returned.
    def mark_returned(self) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if self.__available:
            # Menghentikan proses dengan melempar error.
            raise RuntimeError(f"{self.brand} ({self.plate_number}) tidak sedang disewa.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__available = True

    # Mendefinisikan method/fungsi describe.
    def describe(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return (
            f"{self.TYPE_NAME} {self.brand} | "
            f"Plat: {self.plate_number} | {self._extra_info()}"
        )

    # Mendefinisikan method/fungsi _extra_info.
    @abstractmethod
    def _extra_info(self) -> str:
        """Wajib di-override oleh subclass."""

    # ---------- magic method ----------
    # Mendefinisikan method/fungsi __str__.
    def __str__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.describe()

    # __repr__: teks 'resmi' untuk developer (repr(objek), debugging).
    # Mendefinisikan method/fungsi __repr__.
    def __repr__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return f"{type(self).__name__}(plate_number={self.plate_number!r}, brand={self.brand!r})"

    # __eq__: menentukan arti '==' antar dua objek.
    # Mendefinisikan method/fungsi __eq__.
    def __eq__(self, other: object) -> bool:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(other, Vehicle):
            # Mengembalikan hasil dari method/fungsi.
            return NotImplemented
        # Mengembalikan hasil dari method/fungsi.
        return self.plate_number == other.plate_number  # plat sama = kendaraan sama

    # __hash__: wajib ada kalau __eq__ dibuat, agar objek tetap bisa masuk set/dict.
    # Mendefinisikan method/fungsi __hash__.
    def __hash__(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return hash(self.plate_number)
