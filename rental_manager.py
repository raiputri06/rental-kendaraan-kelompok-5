# Pengelola kendaraan dan transaksi.
# KONSEP: aggregation (Vehicle diterima dari luar lewat add_vehicle),
# class pengatur yang menghubungkan class-class lain.


# Mengimpor modul atau class yang digunakan file ini.
from customer import Customer
from invoice import Invoice
from rental import Rental
from vehicle import Vehicle


# Mendefinisikan class RentalManager.
class RentalManager:
    # Mendefinisikan method/fungsi __init__.
    def __init__(self):
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__vehicles = []  # AGGREGATION: Vehicle diterima dari luar (add_vehicle)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__rentals = []
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__next_rental_no = 1

    # Mendefinisikan method/fungsi add_vehicle.
    def add_vehicle(self, vehicle: Vehicle) -> None:
        # Menjalankan pemanggilan fungsi atau method.
        self.__vehicles.append(vehicle)

    # Mendefinisikan method/fungsi find_vehicle.
    def find_vehicle(self, plate_number: str) -> Vehicle:
        # Mengulang proses untuk setiap item dalam koleksi.
        for vehicle in self.__vehicles:
            # Memeriksa kondisi sebelum menjalankan blok berikutnya.
            if vehicle.plate_number == plate_number:
                # Mengembalikan hasil dari method/fungsi.
                return vehicle
        # Menghentikan proses dengan melempar error.
        raise ValueError(f"Kendaraan dengan plat {plate_number} tidak ditemukan.")

    # Mendefinisikan method/fungsi rent_vehicle.
    def rent_vehicle(self, plate_number: str, customer: Customer, days: int) -> Rental:
        # Mengisi atau memperbarui nilai variabel/atribut.
        vehicle = self.find_vehicle(plate_number)
        # Mengisi atau memperbarui nilai variabel/atribut.
        rental = Rental(f"R{self.__next_rental_no:03d}", customer, vehicle, days)
        # Menjalankan pemanggilan fungsi atau method.
        rental.start()  # gagal di sini -> belum ada data yang tersimpan
        # Menjalankan pemanggilan fungsi atau method.
        self.__rentals.append(rental)
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__next_rental_no += 1
        # Mengembalikan hasil dari method/fungsi.
        return rental

    # Mendefinisikan method/fungsi return_vehicle.
    def return_vehicle(self, rental_id: str) -> Rental:
        # Mengisi atau memperbarui nilai variabel/atribut.
        rental = self.__find_rental(rental_id)
        # Menjalankan pemanggilan fungsi atau method.
        rental.finish()
        # Mengembalikan hasil dari method/fungsi.
        return rental

    # Mendefinisikan method/fungsi __find_rental.
    def __find_rental(self, rental_id: str) -> Rental:
        # Mengulang proses untuk setiap item dalam koleksi.
        for rental in self.__rentals:
            # Memeriksa kondisi sebelum menjalankan blok berikutnya.
            if rental.rental_id == rental_id:
                # Mengembalikan hasil dari method/fungsi.
                return rental
        # Menghentikan proses dengan melempar error.
        raise ValueError(f"Rental {rental_id} tidak ditemukan.")

    # Mendefinisikan method/fungsi show_vehicles.
    def show_vehicles(self) -> None:
        # Menjalankan pemanggilan fungsi atau method.
        print("\n========== DAFTAR KENDARAAN ==========")
        # Mengulang proses untuk setiap item dalam koleksi.
        for number, vehicle in enumerate(self.__vehicles, start=1):
            # Mengisi atau memperbarui nilai variabel/atribut.
            status = "Tersedia" if vehicle.is_available else "Disewa"
            # Menjalankan pemanggilan fungsi atau method.
            print(f"{number}. {vehicle}")
            # Menjalankan pemanggilan fungsi atau method.
            print(f"   Harga: {Invoice.to_rupiah(vehicle.daily_rate)}/hari | Status: {status}")
        # Menjalankan pemanggilan fungsi atau method.
        print("======================================")

    # Mendefinisikan method/fungsi show_transactions.
    def show_transactions(self) -> None:
        # Menjalankan pemanggilan fungsi atau method.
        print("\n========== DAFTAR TRANSAKSI ==========")
        # Mengulang proses untuk setiap item dalam koleksi.
        for rental in self.__rentals:
            # Menjalankan pemanggilan fungsi atau method.
            print(f"{rental} | Total: {Invoice.to_rupiah(rental.total_price)}")
        # Menjalankan pemanggilan fungsi atau method.
        print("======================================")
