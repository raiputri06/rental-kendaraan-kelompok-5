# Mixin asuransi.


from errors import InvalidDataError

class InsuranceMixin:
    INSURANCE_RATE = 0.05

    def insurance_fee(self, days: int) -> int:
        # [BARU] Validasi lama sewa (harus bilangan bulat positif) sebelum menghitung asuransi.
        # Sebelumnya tidak ada pengecekan.
        if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
            raise InvalidDataError("days", days, "Perhitungan asuransi membutuhkan lama sewa bilangan bulat positif.")
        return round(self.daily_rate * self.INSURANCE_RATE * days)