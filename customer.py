# Data pelanggan.
# KONSEP: setter validasi, @staticmethod (validasi), @classmethod (alternative constructor).



# Mendefinisikan class Customer.
class Customer:
    # Data pelanggan.

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, customer_id: str, name: str, phone: str):
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__customer_id = customer_id
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.name = name    # lewat setter
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.phone = phone  # lewat setter

    # Mendefinisikan method/fungsi customer_id.
    @property
    def customer_id(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__customer_id

    # Mendefinisikan method/fungsi name.
    @property
    def name(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__name

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi name.
    @name.setter
    def name(self, value: str) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not isinstance(value, str) or not value.strip():
            # Menghentikan proses dengan melempar error.
            raise ValueError("Nama tidak boleh kosong.")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__name = value.strip()

    # Mendefinisikan method/fungsi phone.
    @property
    def phone(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return self.__phone

    # setter: jalan otomatis saat nilai diisi (obj.atribut = nilai); nilai divalidasi dulu.
    # Mendefinisikan method/fungsi phone.
    @phone.setter
    def phone(self, value: str) -> None:
        # Memeriksa kondisi sebelum menjalankan blok berikutnya.
        if not Customer.is_valid_phone(value):
            # Menghentikan proses dengan melempar error.
            raise ValueError(f"Nomor telepon tidak valid: {value!r} (harus 10-13 digit angka).")
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__phone = value

    # @staticmethod: fungsi biasa di dalam class; tidak butuh 'self' maupun 'cls'.
    # Mendefinisikan method/fungsi is_valid_phone.
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        # Mengembalikan hasil dari method/fungsi.
        return isinstance(phone, str) and phone.isdigit() and 10 <= len(phone) <= 13

    # @classmethod: method milik CLASS (parameter pertama 'cls'), bukan milik satu objek.
    # Mendefinisikan method/fungsi from_string.
    @classmethod
    def from_string(cls, customer_id: str, text: str) -> "Customer":
        """Alternative constructor. Format teks: 'Nama;NomorTelepon'."""
        # Mengisi atau memperbarui nilai variabel/atribut.
        name, phone = text.split(";")
        # Mengembalikan hasil dari method/fungsi.
        return cls(customer_id, name.strip(), phone.strip())

    # __str__: teks yang tampil saat objek di-print atau di-str().
    # Mendefinisikan method/fungsi __str__.
    def __str__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return f"{self.customer_id} - {self.name} ({self.phone})"

    # __repr__: teks 'resmi' untuk developer (repr(objek), debugging).
    # Mendefinisikan method/fungsi __repr__.
    def __repr__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return f"Customer(customer_id={self.customer_id!r}, name={self.name!r})"
