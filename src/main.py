#Program utama simulasi rental kendaraan dengan exception handling.

from car import Car
from customer import Customer
from invoice import Invoice
from motorcycle import Motorcycle
from rental_manager import RentalManager
from van import Van
from vehicle import Vehicle
# [BARU] Import custom exception dari errors.py.
from errors import (RentalError, InvalidDataError, VehicleNotFoundError,
                    VehicleUnavailableError, RentalStateError)


# [BARU] raise ... from: mengubah ValueError bawaan Python menjadi InvalidDataError,
# sambil menyimpan error aslinya sebagai penyebab (error.__cause__).
def parse_days(text: str) -> int:
    try:
        return int(text)
    except ValueError as error:
        raise InvalidDataError("days", text, f"Lama sewa harus berupa angka, bukan {text!r}.") from error


# [BARU] except bertingkat: dari yang paling spesifik ke yang paling umum.
# Python memeriksa except dari atas; RentalError (induk) harus paling bawah,
# kalau di atas maka turunannya tidak akan pernah tertangkap blok spesifik.
def coba_sewa(manager: RentalManager, plate: str, customer: Customer, days) -> None:
    try:
        rental = manager.rent_vehicle(plate, customer, days)
    except VehicleNotFoundError as error:
        print(f"[spesifik] Plat {error.plate_number} tidak ada di sistem.")
    except VehicleUnavailableError as error:
        print(f"[spesifik] Kendaraan {error.plate_number} sedang tidak tersedia.")
    except InvalidDataError as error:
        print(f"[spesifik] Data '{error.field}' ditolak (nilai: {error.value!r}).")
    except RentalError as error:
        print(f"[umum] Kesalahan rental lain: {error}")
    else:
        print(f"[berhasil] {rental}")
    finally:
        print(f"[finally] Pemeriksaan sewa {plate} selesai.")


# [BARU] Re-raise: error dicatat (log) di sini, lalu dilempar ulang dengan `raise`
# supaya pemanggil di level atas tetap bisa menanganinya.
def sewa_dengan_log(manager: RentalManager, plate: str, customer: Customer, days: int) -> None:
    try:
        manager.rent_vehicle(plate, customer, days)
    except RentalError as error:
        print(f"[LOG] Gagal menyewa {plate}: {type(error).__name__}")
        raise

if __name__ == "__main__":
    print("===== 1. MEMBUAT OBJEK =====")
    manager = RentalManager()
    avanza = Car("DK 1234 AB", "Toyota Avanza", 350000, 7)
    brio = Car("DK 2345 CD", "Honda Brio", 300000, 5)
    scoopy = Motorcycle("DK 5678 EF", "Honda Scoopy", 100000, "Matic")
    hiace = Van("DK 9876 IJ", "Toyota HiAce", 800000, 15)

    for item in (avanza, brio, scoopy, hiace):
        manager.add_vehicle(item)

    budi = Customer("P001", "Budi Santoso", "081234567890")
    siti = Customer.from_string("P002", "Siti Aminah;082345678901")
    print(f"Jumlah kendaraan dibuat : {Vehicle.get_total_created()}")
    print(f"Pelanggan 1             : {budi}")
    print(f"Pelanggan 2             : {siti}")
    print(f"Informasi kendaraan     : {avanza!r}")
    manager.show_vehicles()

    print("\n===== 2. PROSES PENYEWAAN =====")
    # [UBAH] Sebelumnya rent_vehicle() dipanggil langsung tanpa try.
    # Sekarang try/except/else: `except RentalError` menangkap semua exception rental
    # lewat base class, `else` hanya jalan kalau tidak ada error.
    try:
        rental_1 = manager.rent_vehicle("DK 1234 AB", budi, 3)
        print(rental_1.receipt())
    except RentalError as error:
        print(f"Penyewaan gagal: {error}")
    else:
        print("Penyewaan pertama berhasil dibuat.")

    # [BARU] Ditambah blok `finally`: selalu dijalankan, ada error maupun tidak.
    try:
        rental_2 = manager.rent_vehicle("DK 5678 EF", siti, 2)
        print(rental_2.receipt())
    except RentalError as error:
        print(f"Penyewaan gagal: {error}")
    else:
        print("Penyewaan kedua berhasil dibuat.")
    finally:
        print("Proses penyewaan selesai diperiksa.")

    print("\n===== 3. PENGUJIAN DATA TIDAK VALID =====")
    # [UBAH] `except ValueError` -> `except InvalidDataError`; ditambah `else` dan `finally`.
    try:
        avanza.daily_rate = -5000
    except InvalidDataError as error:
        print(f"Data harga ditolak: {error}")
    else:
        print("Perubahan harga berhasil.")
    finally:
        print("Validasi harga selesai.")

    # [UBAH] `except ValueError` -> `except InvalidDataError`.
    try:
        budi.phone = "abc"
    except InvalidDataError as error:
        print(f"Nomor telepon ditolak: {error}")

    # [UBAH] `except ValueError` -> `except InvalidDataError`.
    try:
        avanza.seats = 0
    except InvalidDataError as error:
        print(f"Jumlah kursi ditolak: {error}")
    print(f"Harga Avanza tetap      : {Invoice.to_rupiah(avanza.daily_rate)}")

    print("\n===== 4. PERBANDINGAN OBJEK DENGAN == =====")
    avanza_copy = Car("DK 1234 AB", "Toyota Avanza (salinan)", 350000, 7)
    print(f"avanza == avanza_copy   : {avanza == avanza_copy}")
    print(f"avanza == brio          : {avanza == brio}")
    print(f"Jumlah kendaraan dibuat : {Vehicle.get_total_created()}")

    print("\n===== 5. PENGUJIAN ATURAN BISNIS =====")
    # [UBAH] Sebelumnya `except RuntimeError`. Sekarang VehicleUnavailableError (+ else & finally).
    # Menguji aturan bisnis #6: kendaraan yang sedang disewa tidak bisa disewa lagi.
    try:
        manager.rent_vehicle("DK 1234 AB", siti, 1)
    except VehicleUnavailableError as error:
        print(f"Penyewaan ditolak: {error}")
    else:
        print("Kendaraan berhasil disewa.")
    finally:
        print("Pemeriksaan ketersediaan kendaraan selesai.")

    # [BARU] Pengujian baru: plat tidak terdaftar -> VehicleNotFoundError,
    # tertangkap lewat base class RentalError.
    try:
        manager.rent_vehicle("DK 0000 ZZ", siti, 1)
    except RentalError as error:
        print(f"Pencarian kendaraan gagal: {error}")

    # [BARU] Pengujian baru: lama sewa 0 hari -> InvalidDataError (aturan bisnis #5).
    try:
        manager.rent_vehicle("DK 2345 CD", siti, 0)
    except InvalidDataError as error:
        print(f"Lama sewa ditolak: {error}")

    print("\n===== 6. PENGEMBALIAN =====")
    # [UBAH] return_vehicle() sekarang dibungkus try/except/else/finally.
    try:
        manager.return_vehicle("R001")
    except RentalError as error:
        print(f"Pengembalian gagal: {error}")
    else:
        print(f"Setelah dikembalikan: {rental_1}")
    finally:
        print("Proses pengembalian selesai.")

    # [UBAH] `except RuntimeError` -> `except RentalStateError`.
    # Menguji aturan bisnis #7: pengembalian kedua kali ditolak.
    try:
        manager.return_vehicle("R001")
    except RentalStateError as error:
        print(f"Pengembalian ulang ditolak: {error}")

    manager.show_vehicles()
    manager.show_transactions()

    print("\n===== 7. METHOD RESOLUTION ORDER (MRO) =====")
    print("MRO Car        : " + " -> ".join(c.__name__ for c in Car.__mro__))
    print("MRO Motorcycle : " + " -> ".join(c.__name__ for c in Motorcycle.__mro__))
    print(f"Asuransi Avanza 3 hari  : {Invoice.to_rupiah(avanza.insurance_fee(3))}")

    print("\n===== 8. EXCEPT BERTINGKAT, RAISE FROM, RE-RAISE, EAFP =====")
    print("--- 8a. except bertingkat (spesifik -> umum) ---")
    coba_sewa(manager, "DK 0000 ZZ", budi, 1)    # VehicleNotFoundError
    coba_sewa(manager, "DK 5678 EF", budi, 1)    # VehicleUnavailableError (Scoopy masih disewa)
    coba_sewa(manager, "DK 9876 IJ", budi, -2)   # InvalidDataError (lama sewa)
    coba_sewa(manager, "DK 9876 IJ", budi, 2)    # berhasil

    print("--- 8b. raise ... from ---")
    try:
        manager.rent_vehicle("DK 2345 CD", siti, parse_days("tiga"))
    except InvalidDataError as error:
        print(f"Ditolak: {error}")
        print(f"Penyebab asli (__cause__): {error.__cause__!r}")

    print("--- 8c. re-raise dengan `raise` ---")
    try:
        sewa_dengan_log(manager, "DK 5678 EF", budi, 1)
    except VehicleUnavailableError as error:
        print(f"Ditangani di level atas: {error}")

    print("--- 8d. Gaya EAFP ---")
    # EAFP: langsung coba menyewakan, tangani kegagalannya, tanpa mengecek is_available dulu.
    # (LBYL akan menulis `if vehicle.is_available: ...` sebelum mark_rented()).
    for percobaan in (1, 2):
        try:
            manager.find_vehicle("DK 2345 CD").mark_rented()
        except VehicleUnavailableError as error:
            print(f"Percobaan {percobaan}: gagal - {error}")
        else:
            print(f"Percobaan {percobaan}: Honda Brio berhasil ditandai disewa.")
