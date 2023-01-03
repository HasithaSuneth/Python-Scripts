import requests_with_caching    #use request and request.get() with api key
import json

def get_movies_from_tastedive(film_req):
    param = {"q": film_req, "type": "movies", "limit": 5}
    taste_data = requests_with_caching.get("https://tastedive.com/api/similar", params=param)
    result_get = taste_data.json()
    return result_get

def extract_movie_titles(res_taste):
    taste_result_list = []
    for i in res_taste["Similar"]["Results"]:
        taste_result_list.append(i["Name"])
    return taste_result_list

def get_related_titles(title_list):
    related_list = []
    for i in title_list:
        for x in extract_movie_titles(get_movies_from_tastedive(i)):
            if x not in related_list:
                related_list.append(x)
    return related_list

def get_movie_data(omd_film_req):
    param = {"t": omd_film_req, "r": "json"}
    omd_data = requests_with_caching.get("http://www.omdbapi.com/", params=param)
    omd_result_get = omd_data.json()
    return omd_result_get

def get_movie_rating(res_omd):
    for i in res_omd["Ratings"]:
        if i["Source"] == "Rotten Tomatoes":
            return int(i["Value"][:-1])
    return 0

def get_sorted_recommendations(movie_title_list):
    lst1 = get_related_titles(movie_title_list)
    lst_final_res = []
    lst_final_list3 = []
    for i in lst1:
        rank = get_movie_rating(get_movie_data(i))
        lst_final_res.append((i,rank))
    lst_final_list2 = sorted(lst_final_res,  key=lambda x: -x[1])
    print(lst_final_list2)
    for i in lst_final_list2:
        lst_final_list3.append(i[0])
    return lst_final_list3
    
