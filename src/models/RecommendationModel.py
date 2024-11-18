from decouple import config
import datetime
import requests
import random
import json

class RecommendationModel():
    def __init__(self) -> None:
        # "https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={originLocationCode}&destinationLocationCode={destinationCode}&departureDate={departureDate}&returnDate={returnDate}&adults={adults}&max={max}
        self.base_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        self.params = {
            'originLocationCode': 'MEX',
            'destinationLocationCode': '',
            'departureDate': '', ## 2024-11-20 | YYYY-mm-dd
            'returnDate': '',
            'adults': '2',
            'max': '5'
        }
        self.numDays = 3
        self.numAdults = 2

        with open('src/resources/files/offers.json', encoding='utf-8') as file:
            data = json.load(file)
        self.offers = data

    def get_recommendation(self, city_code_iso3: str, city: str, last_id: int = 0) -> dict[str, dict[str, str]]:
        offer_type, offer_params = random.choice(list(self.offers.items()))
        
        if (offer_type == "numDays"):
            self.numDays = random.randint(0, 20)
        elif (offer_type == "numAdults"):
            self.numAdults = random.randint(0, 5) 
        
        init_date = datetime.datetime.today()
        final_date = init_date + datetime.timedelta(days=self.numDays)
        
        init_date = datetime.datetime.strftime(init_date, '%Y-%m-%d')
        final_date = datetime.datetime.strftime(final_date, '%Y-%m-%d')
        
        self.params['destinationLocationCode'] = city_code_iso3
        self.params['departureDate'] = init_date
        self.params['returnDate'] = final_date

        url = self.base_url + "?" + '&'.join([x + "=" + self.params[x] for x in self.params.keys()])

        try:
            headers = {"Authorization": "Bearer {}".format(config("AMADEUS_API_KEY"))}
            response = requests.get(url, headers=headers).json()
            print(response)

            offers_list = []
            if (len(response) != 0):
                number_of_offers = response['meta']['count']
                offers = response['data']

                for option in offers:
                    segments = option['itineraries'][0]['segments']
                    num_segments = len(segments)
                    scales = []
                    for segment in segments:
                        scale = [segment[x]['iataCode'] for x in segment.keys() if x == 'departure' or x == 'arrival']
                        scales += scale

                    option['id'] = str(int(option['id']) + last_id)
                    price = option['price']['total']
                    currency = option['price']['currency']
                    text = offer_params['description'].format(city=city, numDays=self.numDays, numAdults=self.numAdults)

                    new_option = self.params.copy()
                    new_option_02 = {
                        'number_offers': number_of_offers,
                        'num_segments': num_segments,
                        'scales': list(set(scales)),
                        'price': price,
                        'currency': currency,
                        'currency_symbol': '€' if currency == 'EUR' else '$',
                        'text': text,
                        'data': option
                    }

                    new_option.update(new_option_02)
                    offers_list.append(new_option)

            return offers_list

        except Exception as ex:
            print(str(ex))
            return {}