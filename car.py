# Subclass Car.
# KONSEP: multiple inheritance (InsuranceMixin + Vehicle), super().__init__(),
# override method, setter dengan validasi.


# Mengimpor modul atau class yang digunakan file ini.
from insurance_mixin import InsuranceMixin
# Mengimpor modul atau class yang digunakan file ini.
from vehicle import Vehicle


# Mendefinisikan class Car.
class Car(InsuranceMixin, Vehicle):
    # Mengisi atau memperbarui nilai variabel/atribut.
    TYPE_NAME = "Mobil"

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, plate_number: str, brand: str, daily_rate: int, seats: int):
        # Menjalankan pemanggilan fungsi atau method.
        super().__init__(plate_number, brand, daily_rate)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.seats = seats  # lewat setter

    # Mendefinisikan method/fungsi seats.
    @property
    def seats(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__seats

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi seats.
    @seats.setter
    def seats(self, value: int) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(value, int) or value <= 0:
            # Menghentikan proses dengan melempar error.
            raise ValueError(f"Jumlah kursi harus lebih dari 0, bukan {value!r}.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__seats = value

    # Mendefinisikan method/fungsi _extra_info.
    def _extra_info(self) -> str:  # override
        # Mengembalikan hasil dari method/fungsi.
        return f"Kursi: {self.seats} orang"
