class CountriesInterest():
    def __init__(self, interest_id, country, code_iso2, code_iso3) -> None:
        self.interest_id = interest_id
        self.country = country
        self.code_iso2 = code_iso2
        self.code_iso3 = code_iso3

    def to_JSON(self):
        return {
            'interest_id': self.interest_id,
            'country': self.country,
            'code_iso2': self.code_iso2,
            'code_iso3': self.code_iso3
        }