# Program utama simulasi rental kendaraan.
# Menjalankan proses pembuatan objek, penyewaan, validasi,
# pengembalian kendaraan, dan pengecekan MRO.

# Mengimpor modul atau class yang digunakan file ini.
from car import Car
from customer import Customer
from invoice import Invoice
from motorcycle import Motorcycle
from rental_manager import RentalManager
from van import Van
from vehicle import Vehicle


if __name__ == "__main__":
    # Membuat objek pengelola rental dan beberapa kendaraan.
    print("===== 1. MEMBUAT OBJEK =====")
    manager = RentalManager()

    avanza = Car("DK 1234 AB", "Toyota Avanza", 350000, 7)
    brio = Car("DK 2345 CD", "Honda Brio", 300000, 5)
    scoopy = Motorcycle("DK 5678 EF", "Honda Scoopy", 100000, "Matic")
    hiace = Van("DK 9876 IJ", "Toyota HiAce", 800000, 15)

    # Mendaftarkan kendaraan ke dalam sistem rental.
    for item in (avanza, brio, scoopy, hiace):
        manager.add_vehicle(item)

    # Membuat data pelanggan menggunakan constructor dan class method.
    budi = Customer("P001", "Budi Santoso", "081234567890")
    siti = Customer.from_string("P002", "Siti Aminah;082345678901")

    print(f"Jumlah kendaraan dibuat : {Vehicle.get_total_created()}")
    print(f"Pelanggan 1             : {budi}")
    print(f"Pelanggan 2             : {siti}")
    print(f"Informasi kendaraan     : {avanza!r}")
    manager.show_vehicles()

    # Menyewakan kendaraan kepada pelanggan dan menampilkan bukti sewa.
    print("\n===== 2. PROSES PENYEWAAN =====")
    rental_1 = manager.rent_vehicle("DK 1234 AB", budi, 3)
    print(rental_1.receipt())

    rental_2 = manager.rent_vehicle("DK 5678 EF", siti, 2)
    print(rental_2.receipt())

    # Menguji setter untuk memastikan nilai yang tidak valid ditolak.
    print("\n===== 3. VALIDASI SETTER (NILAI TIDAK VALID) =====")
    try:
        avanza.daily_rate = -5000
    except ValueError as error:
        print(f"Ditolak: {error}")

    try:
        budi.phone = "abc"
    except ValueError as error:
        print(f"Ditolak: {error}")

    try:
        avanza.seats = 0
    except ValueError as error:
        print(f"Ditolak: {error}")

    print(f"Harga Avanza tetap      : {Invoice.to_rupiah(avanza.daily_rate)}")

    # Membandingkan objek berdasarkan aturan perbandingan yang dibuat di class.
    print("\n===== 4. PERBANDINGAN OBJEK DENGAN == =====")
    avanza_copy = Car("DK 1234 AB", "Toyota Avanza (salinan)", 350000, 7)
    print(f"avanza == avanza_copy   : {avanza == avanza_copy}")
    print(f"avanza == brio          : {avanza == brio}")
    print(f"Jumlah kendaraan dibuat : {Vehicle.get_total_created()}")

    # Memastikan kendaraan yang sedang disewa tidak dapat disewa kembali.
    print("\n===== 5. SEWA KENDARAAN YANG SEDANG DISEWA =====")
    try:
        manager.rent_vehicle("DK 1234 AB", siti, 1)
    except RuntimeError as error:
        print(f"Gagal: {error}")

    # Mengembalikan kendaraan dan menguji penolakan pengembalian berulang.
    print("\n===== 6. PENGEMBALIAN =====")
    manager.return_vehicle("R001")
    print(f"Setelah dikembalikan    : {rental_1}")

    try:
        manager.return_vehicle("R001")
    except RuntimeError as error:
        print(f"Gagal: {error}")

    manager.show_vehicles()
    manager.show_transactions()

    # Menampilkan urutan pewarisan class (MRO) dan biaya asuransi.
    print("\n===== 7. METHOD RESOLUTION ORDER (MRO) =====")
    print("MRO Car        : " + " -> ".join(c.__name__ for c in Car.__mro__))
    print("MRO Motorcycle : " + " -> ".join(c.__name__ for c in Motorcycle.__mro__))
    print(f"Asuransi Avanza 3 hari  : {Invoice.to_rupiah(avanza.insurance_fee(3))}")