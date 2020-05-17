from django.shortcuts import render
from django.views.generic import TemplateView
from decouple import config

import requests as rq
import json


class movie_recommend(TemplateView):
    template_name = "similar/index.html"

    def __init__(self):
        self.movie_name = ''
        self.data = {}

    def get(self, request):
        return render(request, 'similar/index.html', {'data': self.data})

    def post(self, request):
        self.movie_name = request.POST['search']
        if self.movie_name != '':
            try:
                self.data = get_sorted_recommendations(self.movie_name)
            except:
                pass
        return render(request, 'similar/index.html', {'data': self.data})


def similar_movie(name):
    baseurl = config('baseurl1_movie')
    params = {'q': name, 'limit': 5,
         'k': config('apikey_movie'), 'verbose': 1}
    s_title = json.loads(rq.get(baseurl, params=params).text)
    return s_title


def extract_movie_titles(name):
    info = []
    for i in name['Similar']['Results']:
        info.append([i['Name'], i['yUrl']])
    return info


def get_related_titles(name):
    titles = []
    for i in name:
        title = extract_movie_titles(similar_movie(i))
        for j in title:
            if j not in titles:
                titles.append(j)
    return titles


def get_movie_data(name_detail):
    baseurl = config('baseurl2_movie')
    params = {'t': name_detail[0], 'r': 'json', 'apikey': config('apikey_moviedetail2')}
    x = json.loads(rq.get(baseurl, params=params).text)
    data = {'Year': x['Year'], 'Genre': x['Genre'].split(',')[:4], 'Poster': x['Poster'], 'imdbRating': x['imdbRating'], 'imdbVotes': float(
        x['imdbVotes'].replace(',', ''))/10000, 'Link': name_detail[1], 'Type': x['Type']}
    for k in x['Ratings']:
        if k['Source'] == 'Rotten Tomatoes':
            data['Rotten_Tomatoes'] = k['Value']
            break
    try:
        data['BoxOffice'] = float(x['BoxOffice'][1:].replace(',', ''))/1000000
    except:
        data['BoxOffice'] = 'N/A'
        pass
    try:
        data['Total_Season'] = x['totalSeasons']
    except:
        pass
    return data


def get_sorted_recommendations(name):
    title = get_related_titles([name])
    result = {}
    for i in title:
        try:
            result[i[0]] = get_movie_data(i)
        except:
            pass
    rating_index = sorted(result, key=lambda x: (
        float(result[x]['imdbRating']), float(result[x]['imdbVotes'])), reverse=True)
    res = {}
    for i in rating_index:
        res[i] = result[i]
    return res
