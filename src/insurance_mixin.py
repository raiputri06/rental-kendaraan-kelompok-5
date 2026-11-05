# Mixin asuransi.
# KONSEP: Mixin = class kecil berisi satu kemampuan tambahan yang 'ditempelkan'
# ke class lain lewat multiple inheritance (dipakai Car dan Van, bukan Motorcycle).



# Mendefinisikan class InsuranceMixin.
class InsuranceMixin:
    # Mixin: menambah kemampuan hitung asuransi. Tidak dipakai berdiri sendiri.

    # Mengisi atau memperbarui nilai variabel/atribut.
    INSURANCE_RATE = 0.05  # class attribute: asuransi 5% dari harga sewa per hari

    # Mendefinisikan method/fungsi insurance_fee.
    def insurance_fee(self, days: int) -> int:
        # Mengembalikan hasil dari method/fungsi.
        return round(self.daily_rate * self.INSURANCE_RATE * days)
