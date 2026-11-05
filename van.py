# Subclass Van (memakai mixin asuransi seperti Car).

# Mengimpor modul atau class yang digunakan file ini.
from insurance_mixin import InsuranceMixin
# Mengimpor modul atau class yang digunakan file ini.
from vehicle import Vehicle


# Mendefinisikan class Van.
class Van(InsuranceMixin, Vehicle):
    # Mengisi atau memperbarui nilai variabel/atribut.
    TYPE_NAME = "Van"

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, plate_number: str, brand: str, daily_rate: int, capacity: int):
        # Menjalankan pemanggilan fungsi atau method.
        super().__init__(plate_number, brand, daily_rate)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.capacity = capacity  # lewat setter

    # Mendefinisikan method/fungsi capacity.
    @property
    def capacity(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__capacity

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi capacity.
    @capacity.setter
    def capacity(self, value: int) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(value, int) or value <= 0:
            # Menghentikan proses dengan melempar error.
            raise ValueError(f"Kapasitas harus lebih dari 0, bukan {value!r}.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__capacity = value

    # Mendefinisikan method/fungsi _extra_info.
    def _extra_info(self) -> str:  # override
        # Mengembalikan hasil dari method/fungsi.
        return f"Kapasitas: {self.capacity} orang"
