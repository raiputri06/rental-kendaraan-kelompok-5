#Data pelanggan.

from errors import InvalidDataError

class Customer:
    def __init__(self, customer_id: str, name: str, phone: str):
        # [BARU] Validasi ID pelanggan. Sebelumnya langsung `self.__customer_id = customer_id`
        # tanpa pengecekan. Sekarang ID kosong/bukan string -> InvalidDataError.
        if not isinstance(customer_id, str) or not customer_id.strip():
            raise InvalidDataError("customer_id", customer_id, "ID pelanggan tidak boleh kosong.")
        self.__customer_id = customer_id.strip()
        self.name = name
        self.phone = phone

    @property
    def customer_id(self) -> str:
        return self.__customer_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        # [UBAH] ValueError -> InvalidDataError (pesan: 'Nama pelanggan tidak boleh kosong.').
        # Aturan bisnis #3: nama tidak boleh kosong.
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("name", value, "Nama pelanggan tidak boleh kosong.")
        self.__name = value.strip()

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        # [UBAH] Sebelumnya `Customer.is_valid_phone` + ValueError; sekarang `self.is_valid_phone`
        # + InvalidDataError. Aturan bisnis #3: nomor telepon 10-13 digit angka.
        if not self.is_valid_phone(value):
            raise InvalidDataError("phone", value, f"Nomor telepon tidak valid: {value!r} (harus 10-13 digit angka).")
        self.__phone = value

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return isinstance(phone, str) and phone.isdigit() and 10 <= len(phone) <= 13

    @classmethod
    def from_string(cls, customer_id: str, text: str) -> "Customer":
        # [BARU] Validasi format teks. di code Sebelumnya langsung di-split, sehingga format salah
        # memunculkan error bawaan Python. Sekarang -> InvalidDataError dengan pesan jelas.
        if not isinstance(text, str) or text.count(";") != 1:
            raise InvalidDataError("customer_text", text, "Format untuk pelanggan harus 'Nama;NomorTelepon'.")
        name, phone = text.split(";")
        return cls(customer_id, name.strip(), phone.strip())

    def __str__(self) -> str:
        return f"{self.customer_id} - {self.name} ({self.phone})"

    def __repr__(self) -> str:
        return f"Customer(customer_id={self.customer_id!r}, name={self.name!r})"
