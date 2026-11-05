# Rincian biaya.
# KONSEP: Invoice adalah BAGIAN dari Rental (composition): dibuat di dalam
# constructor Rental dan ikut hilang bersama Rental.



# Mendefinisikan class Invoice.
class Invoice:
    # Rincian biaya. Dibuat oleh Rental dan ikut hilang bersama Rental.

    # Mendefinisikan method/fungsi __init__.
    def __init__(self, rent_cost: int, insurance_cost: int):
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__rent_cost = rent_cost
        # Mengisi atau memperbarui nilai variabel/atribut.
        self.__insurance_cost = insurance_cost

    # Mendefinisikan method/fungsi rent_cost.
    @property
    def rent_cost(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__rent_cost

    # Mendefinisikan method/fungsi insurance_cost.
    @property
    def insurance_cost(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__insurance_cost

    # Mendefinisikan method/fungsi total.
    @property
    def total(self) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return self.__rent_cost + self.__insurance_cost

    # @staticmethod: fungsi biasa di dalam class; tidak butuh 'self' maupun 'cls'.
    # Mendefinisikan method/fungsi to_rupiah.
    @staticmethod
    def to_rupiah(amount: int) -> str:
        """350000 -> Rp350.000"""
        # Mengembalikan hasil dari method/fungsi.
        return "Rp" + f"{amount:,}".replace(",", ".")

    # __str__: teks yang tampil saat objek di-print atau di-str().
    # Mendefinisikan method/fungsi __str__.
    def __str__(self) -> str:
        # Mengembalikan hasil dari method/fungsi.
        return (
            f"Biaya Sewa   : {Invoice.to_rupiah(self.rent_cost)}\n"
            f"Asuransi     : {Invoice.to_rupiah(self.insurance_cost)}\n"
            f"Total Biaya  : {Invoice.to_rupiah(self.total)}"
        )
