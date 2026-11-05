# Subclass Motorcycle (tidak memakai mixin asuransi).

# Mengimpor modul atau class yang digunakan file ini.
from vehicle import Vehicle


# Mendefinisikan class Motorcycle.
class Motorcycle(Vehicle):
    # Mengisi atau memperbarui nilai variabel/atribut.
    TYPE_NAME = "Motor"

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, plate_number: str, brand: str, daily_rate: int, motor_type: str):
        # Menjalankan pemanggilan fungsi atau method.
        super().__init__(plate_number, brand, daily_rate)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__motor_type = motor_type

    # Mendefinisikan method/fungsi motor_type.
    @property
    def motor_type(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__motor_type

    # Mendefinisikan method/fungsi _extra_info.
    def _extra_info(self) -> str:  # override
        # Mengembalikan hasil dari method/fungsi.
        return f"Jenis: {self.motor_type}"
