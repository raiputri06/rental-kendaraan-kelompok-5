# Satu transaksi sewa.

from customer import Customer
from insurance_mixin import InsuranceMixin
from invoice import Invoice
from vehicle import Vehicle
# [BARU] Import ini custom exception dari errors.py.
from errors import InvalidDataError, RentalStateError

class Rental:
    STATUS_ACTIVE = "Aktif"
    STATUS_DONE = "Selesai"

    def __init__(self, rental_id: str, customer: Customer, vehicle: Vehicle, days: int):
        # [BARU] Empat validasi berikut (rental_id, customer, vehicle, days).
        # Sebelumnya hanya `days` yang diperiksa.
        if not isinstance(rental_id, str) or not rental_id.strip():
            raise InvalidDataError("rental_id", rental_id, "ID rental tidak boleh kosong.")
        if not isinstance(customer, Customer):
            raise InvalidDataError("customer", customer, "Data pelanggan tidak valid.")
        if not isinstance(vehicle, Vehicle):
            raise InvalidDataError("vehicle", vehicle, "Data kendaraan tidak valid.")
        # [UBAH] Ditambah cek `bool`; ValueError -> InvalidDataError.
        # Aturan bisnis #5: lama sewa minimal 1 hari.
        if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
            raise InvalidDataError("days", days, "Lama sewa harus bilangan bulat lebih dari 0 hari.")
        self.__rental_id = rental_id
        self.__customer = customer
        self.__vehicle = vehicle
        self.__days = days
        self.__status = self.STATUS_ACTIVE
        insurance = vehicle.insurance_fee(days) if isinstance(vehicle, InsuranceMixin) else 0
        self.__invoice = Invoice(vehicle.daily_rate * days, insurance)

    @property
    def rental_id(self) -> str:
        return self.__rental_id

    @property
    def customer(self) -> Customer:
        return self.__customer

    @property
    def vehicle(self) -> Vehicle:
        return self.__vehicle

    @property
    def status(self) -> str:
        return self.__status

    @property
    def is_active(self) -> bool:
        return self.__status == self.STATUS_ACTIVE

    @property
    def total_price(self) -> int:
        return self.__invoice.total

    def start(self) -> None:
        # [BARU] Cek status sebelum kendaraan ditandai disewa. Sebelumnya start() langsung
        # memanggil mark_rented() tanpa cek. Gagal -> RentalStateError.
        if not self.is_active:
            raise RentalStateError(self.rental_id, self.status, f"Rental {self.rental_id} tidak dapat dimulai karena statusnya bukan Aktif.")
        self.__vehicle.mark_rented()

    def finish(self) -> None:
        # [UBAH] RuntimeError -> RentalStateError.
        # Aturan bisnis #7: transaksi yang sudah selesai tidak bisa dikembalikan dua kali.
        if not self.is_active:
            raise RentalStateError(self.rental_id, self.status, f"Rental {self.rental_id} sudah selesai dan tidak dapat dikembalikan lagi.")
        self.__vehicle.mark_returned()
        self.__status = self.STATUS_DONE

    def receipt(self) -> str:
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

    def __str__(self) -> str:
        return f"[{self.rental_id}] {self.customer.name} - {self.vehicle.brand} ({self.status})"
