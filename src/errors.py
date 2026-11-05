#Hierarki custom exception untuk sistem Rental Kendaraan.

class RentalError(Exception):
    """Base exception untuk seluruh kesalahan pada proses rental.

    Atribut konteks: message (teks pesan kesalahan).
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# [BARU] Turunan 1: data tidak valid.
# Konteks: field (nama atribut yang salah) dan value (nilai yang ditolak).
class InvalidDataError(RentalError):
    """Data yang dimasukkan tidak sesuai ketentuan."""

    def __init__(self, field: str, value, message: str):
        self.field = field
        self.value = value
        super().__init__(message)


# [BARU] Turunan 2: kendaraan tidak ditemukan. Konteks: plate_number.
class VehicleNotFoundError(RentalError):
    """Kendaraan yang dicari tidak terdaftar."""

    def __init__(self, plate_number: str, message: str = ""):
        self.plate_number = plate_number
        super().__init__(message or f"Kendaraan dengan plat {plate_number} tidak ditemukan.")


# [BARU] Turunan 3: kendaraan sedang disewa / belum disewa. Konteks: plate_number.
class VehicleUnavailableError(RentalError):
    """Kendaraan sedang disewa atau statusnya tidak sesuai."""

    def __init__(self, plate_number: str, message: str = ""):
        self.plate_number = plate_number
        super().__init__(message or f"Kendaraan {plate_number} tidak tersedia untuk operasi ini.")


# [BARU] Turunan 4: transaksi rental tidak ditemukan. Konteks: rental_id.
class RentalNotFoundError(RentalError):
    """Transaksi rental tidak ditemukan."""

    def __init__(self, rental_id: str, message: str = ""):
        self.rental_id = rental_id
        super().__init__(message or f"Rental {rental_id} tidak ditemukan.")


# [BARU] Turunan 5: status transaksi tidak sesuai. Konteks: rental_id dan status.
class RentalStateError(RentalError):
    """Operasi tidak sesuai dengan status transaksi rental."""

    def __init__(self, rental_id: str, status: str, message: str = ""):
        self.rental_id = rental_id
        self.status = status
        super().__init__(message or f"Rental {rental_id} berstatus {status}, operasi tidak dapat dilakukan.")
