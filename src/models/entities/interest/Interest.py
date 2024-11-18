class Interest():
    def __init__(self, interest_id, city_code, description, country, country_code_iso2, country_code_iso3) -> None:
        self.interest_id = interest_id
        self.city_code = city_code
        self.description = description
        self.country = country
        self.country_code_iso2 = country_code_iso2
        self.country_code_iso3 = country_code_iso3

    def to_JSON(self):
        return {
            'interest_id': self.interest_id,
            'city_code': self.city_code,
            'description': self.description,
            'country': self.country,
            'country_code_iso2': self.country_code_iso2,
            'country_code_iso3': self.country_code_iso3
        }