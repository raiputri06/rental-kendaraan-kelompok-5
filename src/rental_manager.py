# Pengelola kendaraan dan transaksi.

from customer import Customer
from invoice import Invoice
from rental import Rental
from vehicle import Vehicle
# [BARU] Import custom exception dari errors.py.
from errors import InvalidDataError, VehicleNotFoundError, RentalNotFoundError

class RentalManager:
    def __init__(self):
        self.__vehicles = {}   # plat nomor -> Vehicle
        self.__rentals = {}    # ID rental  -> Rental
        self.__next_rental_no = 1

    def add_vehicle(self, vehicle: Vehicle) -> None:
        # [BARU] Hanya objek Vehicle yang boleh didaftarkan.
        if not isinstance(vehicle, Vehicle):
            raise InvalidDataError("vehicle", vehicle, "Hanya objek kendaraan yang dapat didaftarkan.")
        # [BARU] Cek plat duplikat. Aturan bisnis #1: plat nomor harus unik.
        if vehicle.plate_number in self.__vehicles:
            raise InvalidDataError("plate_number", vehicle.plate_number,
                                   f"Kendaraan dengan plat {vehicle.plate_number} sudah terdaftar.")
        self.__vehicles[vehicle.plate_number] = vehicle

    def find_vehicle(self, plate_number: str) -> Vehicle:
        # [UBAH] Gaya EAFP ("Easier to Ask Forgiveness than Permission"): langsung ambil
        # dari dict, tangani KeyError jika tidak ada. Sebelumnya: loop + pengecekan satu per satu (LBYL).
        try:
            return self.__vehicles[plate_number]
        except (KeyError, TypeError) as error:
            # `from error` menyambungkan exception asli sebagai penyebab (__cause__).
            raise VehicleNotFoundError(plate_number) from error

    def rent_vehicle(self, plate_number: str, customer: Customer, days: int) -> Rental:
        # [BARU] Validasi data pelanggan sebelum membuat transaksi.
        if not isinstance(customer, Customer):
            raise InvalidDataError("customer", customer, "Penyewaan harus memiliki data pelanggan yang valid.")
        vehicle = self.find_vehicle(plate_number)
        rental = Rental(f"R{self.__next_rental_no:03d}", customer, vehicle, days)
        # Catatan: jika start() gagal, transaksi belum disimpan ke daftar.
        rental.start()
        self.__rentals[rental.rental_id] = rental
        self.__next_rental_no += 1
        return rental

    def return_vehicle(self, rental_id: str) -> Rental:
        rental = self.__find_rental(rental_id)
        rental.finish()
        return rental

    def __find_rental(self, rental_id: str) -> Rental:
        # [UBAH] EAFP + raise ... from, sama seperti find_vehicle().
        try:
            return self.__rentals[rental_id]
        except (KeyError, TypeError) as error:
            raise RentalNotFoundError(rental_id) from error

    def show_vehicles(self) -> None:
        print("\n========== DAFTAR KENDARAAN ==========")
        for number, vehicle in enumerate(self.__vehicles.values(), start=1):
            status = "Tersedia" if vehicle.is_available else "Disewa"
            print(f"{number}. {vehicle}")
            print(f"   Harga: {Invoice.to_rupiah(vehicle.daily_rate)}/hari | Status: {status}")
        print("======================================")

    def show_transactions(self) -> None:
        print("\n========== DAFTAR TRANSAKSI ==========")
        for rental in self.__rentals.values():
            print(f"{rental} | Total: {Invoice.to_rupiah(rental.total_price)}")
        print("======================================")
