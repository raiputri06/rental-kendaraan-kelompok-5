# Rincian biaya transaksi.

from errors import InvalidDataError

class Invoice:
    def __init__(self, rent_cost: int, insurance_cost: int):
        # [BARU] Loop validasi: biaya sewa & asuransi harus bilangan bulat dan tidak negatif.
        # Sebelumnya nilai ini langsung disimpan tanpa pengecekan.
        for label, amount in (("Biaya sewa", rent_cost), ("Biaya asuransi", insurance_cost)):
            if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
                raise InvalidDataError(label, amount, f"{label} tidak boleh negatif dan harus berupa bilangan bulat.")
        self.__rent_cost = rent_cost
        self.__insurance_cost = insurance_cost

    @property
    def rent_cost(self) -> int:
        return self.__rent_cost

    @property
    def insurance_cost(self) -> int:
        return self.__insurance_cost

    @property
    def total(self) -> int:
        return self.__rent_cost + self.__insurance_cost

    @staticmethod
    def to_rupiah(amount: int) -> str:
        return "Rp" + f"{amount:,}".replace(",", ".")

    def __str__(self) -> str:
        return (f"Biaya Sewa   : {self.to_rupiah(self.rent_cost)}\n"
                f"Asuransi     : {self.to_rupiah(self.insurance_cost)}\n"
                f"Total Biaya  : {self.to_rupiah(self.total)}")
