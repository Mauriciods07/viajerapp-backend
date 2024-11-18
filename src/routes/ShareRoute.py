from flask import Blueprint, jsonify, request
from src.models.ProfileModel import ProfileModel
from src.models.InterestModel import InterestModel
from src.models.RecommendationModel import RecommendationModel
from src.algorithms.recommender.order_results import sort_by_distances
from src.algorithms.recommender.embedding.oneHot._simple import getVectorFromOneHot, \
                                                                simpleVectorRecomm, \
                                                                getLowestMaxFromDict
#from serpapi import GoogleSearch
from collections import Counter
from datetime import datetime
import calendar
import locale
import random


main = Blueprint('share_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

recommendationModel = RecommendationModel()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/feed', methods = ['POST'])
def feed_home():
    try:
        profile_id = request.json['profile_id']
        min_num_recommendations = request.json['min_num_recommendations']

        if (min_num_recommendations < 2):
            raise Exception('El número mínimo de recomendaciones debe ser de 2')
        
        profile_interest = InterestModel.get_interests(profile_id)
        interest = InterestModel.get_all()
        
        interest_list = [x['interest_id'] for x in interest]
        user_interest = [interest['interest_id'] for interest in profile_interest['interest_list']]
        user_interest = list(set(user_interest))
        not_user_visited = [interest['interest_id'] for interest in interest \
                              if interest['interest_id'] not in user_interest]
        
        not_interest_recomm_num = round(min_num_recommendations / 5)
        interest_recomm_num = min_num_recommendations - not_interest_recomm_num

        user_interest_list = set()
        for _ in range(interest_recomm_num):
            if (len(user_interest) > 0):
                user_interest_list.add(random.choice(user_interest))
        user_interest_list = list(user_interest_list)

        not_user_interest = []
        for _ in range(not_interest_recomm_num + (interest_recomm_num - len(user_interest_list))):
            not_user_interest.append(random.choice(not_user_visited))

        cities_information_interest = [(x['city_code'], x['description']) for x in interest if x['interest_id'] in user_interest_list]
        cities_information_not_interest = [(x['city_code'], x['description']) for x in interest if x['interest_id'] in not_user_interest]
        
        offers_interest_list = []
        for interest_recomm in cities_information_interest:
            offers_interest = recommendationModel.get_recommendation(city_code_iso3=interest_recomm[0], city=interest_recomm[1], last_id=len(offers_interest_list))
            for offer in offers_interest:
                scales_ids = [x['interest_id'] for x in interest if x['city_code'] in offer['scales']]
                offer['scales_ids'] = scales_ids
            offers_interest_list += offers_interest
        
        offers_not_interest_list = []
        for interest_recomm in cities_information_not_interest:
            offers_not_interest = recommendationModel.get_recommendation(city_code_iso3=interest_recomm[0], city=interest_recomm[1], last_id=len(offers_interest_list))
            for offer in offers_not_interest:
                scales_ids = [x['interest_id'] for x in interest if x['city_code'] in offer['scales']]
                offer['scales_ids'] = scales_ids
            offers_not_interest_list += offers_not_interest

        offer_interest_ids = [x['scales_ids'] for x in offers_interest_list]
        offer_not_interest_ids = [x['scales_ids'] for x in offers_not_interest_list]

        one_hot_interest = getVectorFromOneHot(interest_list, offer_interest_ids, [(x['data']['id'], float(x['price']), x['num_segments']) for x in offers_interest_list])
        one_hot_not_interest = getVectorFromOneHot(interest_list, offer_not_interest_ids, [(x['data']['id'], float(x['price']), x['num_segments']) for x in offers_not_interest_list])
        one_hot_recommendation = simpleVectorRecomm(interest_list)

        interest_recommendations = []
        if (len(one_hot_interest) != 0):
            interest_recommendations = sort_by_distances(user_embedding=one_hot_recommendation, offers_embeddings=one_hot_interest)
        not_interest_recommendations = []
        if (len(one_hot_not_interest) != 0):
            not_interest_recommendations = sort_by_distances(user_embedding=one_hot_recommendation, offers_embeddings=one_hot_not_interest)

        interest_recommendations += not_interest_recommendations
        offers_interest_list += offers_not_interest_list
        recommendations = []

        if (len(offers_interest_list) != 0):

            list_ids_recommendation = []
            for _ in range(interest_recomm_num):
                interest_recommendations, id_ = getLowestMaxFromDict(interest_recommendations, "MAX")
                list_ids_recommendation.append(id_)
            for _ in range(not_interest_recomm_num):
                interest_recommendations, id_ = getLowestMaxFromDict(interest_recommendations, "MIN")
                list_ids_recommendation.append(id_)
                
            for i in range(len(list_ids_recommendation)):
                recommendation = [x for x in offers_interest_list if x['data']['id'] == list_ids_recommendation[i]][0]
                recommendation['data']['id'] = str(i + 1)
                recommendations.append(recommendation)

        return jsonify({
            'recommendations': recommendations
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/get_ranking', methods = ['GET'])
def get_ranking():
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
        today = datetime.today()
        today_string = datetime.strftime(today, '%d/%m/%Y')
        full_date = datetime.strftime(today, "%A, %d de %B de %Y")
        formatted_month = datetime.strftime(today, "%B")
        init_date = datetime.strftime(today.replace(day=1), '%d/%m/%Y')
        last_day_of_month = calendar.monthrange(today.year, today.month)
        final_date = datetime.strftime(today.replace(day=last_day_of_month[1]), '%d/%m/%Y')

        rankings = InterestModel.get_flights_per_date(init_date, final_date)
        profiles = [x['profile_id'] for x in rankings]
        count_profiles = Counter(profiles).most_common(3)

        profiles_list = []
        for profile_id in count_profiles:
            profile = ProfileModel.get_profile_data(profile_id[0])
            profiles_list.append({
                'flights_count': profile_id[1],
                'name': profile['name'],
                'profile_photo': profile['profile_photo'],
            })

        ranking = []
        for profile_info in profiles_list:
            ranking.append({
                'name': profile_info['name'],
                'profile_photo': profile_info['profile_photo'],
                'flights_count': profile_info['flights_count'],
                'position': 1 + len(ranking)
            })

        return jsonify({
            'last_day': last_day_of_month[1],
            'month': today.month,
            'formatted_month': formatted_month.title(),
            'current_date': today_string,
            'current_date_formatted': full_date.title(),
            'ranking': ranking
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500