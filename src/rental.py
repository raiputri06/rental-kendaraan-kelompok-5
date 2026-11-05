# Satu transaksi sewa.
# KONSEP: composition (Invoice dibuat di constructor), association
# (Customer dan Vehicle diterima dari luar), class attribute untuk status.


# Mengimpor modul atau class yang digunakan file ini.
from src.customer import Customer
# Mengimpor modul atau class yang digunakan file ini.
from src.insurance_mixin import InsuranceMixin
# Mengimpor modul atau class yang digunakan file ini.
from src.invoice import Invoice
# Mengimpor modul atau class yang digunakan file ini.
from src.vehicle import Vehicle


# Mendefinisikan class Rental.
class Rental:
    # Mengisi atau memperbarui nilai variabel/atribut.
    STATUS_ACTIVE = "Aktif"    # class attribute
    # Mengisi atau memperbarui nilai variabel/atribut.
    STATUS_DONE = "Selesai"    # class attribute

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, rental_id: str, customer: Customer, vehicle: Vehicle, days: int):
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(days, int) or days <= 0:
            # Menghentikan proses dengan melempar error.
            raise ValueError("Lama sewa harus bilangan bulat lebih dari 0 hari.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__rental_id = rental_id
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__customer = customer  # ASSOCIATION: diterima dari luar
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__vehicle = vehicle    # ASSOCIATION: diterima dari luar
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__days = days
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__status = Rental.STATUS_ACTIVE
        # COMPOSITION: Invoice dibuat DI DALAM constructor Rental
        # Mengisi atau memperbarui nilai variabel/atribut.
        insurance = vehicle.insurance_fee(days) if isinstance(vehicle, InsuranceMixin) else 0
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__invoice = Invoice(vehicle.daily_rate * days, insurance)

    # Mendefinisikan method/fungsi rental_id.
    @property
    def rental_id(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__rental_id

    # Mendefinisikan method/fungsi customer.
    @property
    def customer(self) -> Customer:
        # Mengembalikan hasil dari method/fungsi.
        return self.__customer

    # Mendefinisikan method/fungsi vehicle.
    @property
    def vehicle(self) -> Vehicle:
        # Mengembalikan hasil dari method/fungsi.
        return self.__vehicle

    # Mendefinisikan method/fungsi status.
    @property
    def status(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__status

    # Mendefinisikan method/fungsi is_active.
    @property
    def is_active(self) -> bool:
        # Mengembalikan hasil dari method/fungsi.
        return self.__status == Rental.STATUS_ACTIVE

    # Mendefinisikan method/fungsi total_price.
    @property
    def total_price(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__invoice.total

    # Mendefinisikan method/fungsi start.
    def start(self) -> None:
        # Menjalankan pemanggilan fungsi atau method.
        self.__vehicle.mark_rented()

    # Mendefinisikan method/fungsi finish.
    def finish(self) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not self.is_active:
            # Menghentikan proses dengan melempar error.
            raise RuntimeError(f"Rental {self.rental_id} sudah selesai.")
        # Menjalankan pemanggilan fungsi atau method.
        self.__vehicle.mark_returned()
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__status = Rental.STATUS_DONE

    # Mendefinisikan method/fungsi receipt.
    def receipt(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return "\n".join([
            "========== STRUK RENTAL ==========",
            f"ID Rental    : {self.rental_id}",
            f"Pelanggan    : {self.customer.name}",
            f"Kendaraan    : {self.vehicle.brand} ({self.vehicle.plate_number})",
            f"Lama Sewa    : {self.__days} hari",
            str(self.__invoice),
            f"Status       : {self.status}",
            "==================================",
        ])

    # __str__: teks yang tampil saat objek di-print atau di-str().
    # Mendefinisikan method/fungsi __str__.
    def __str__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return f"[{self.rental_id}] {self.customer.name} - {self.vehicle.brand} ({self.status})"
