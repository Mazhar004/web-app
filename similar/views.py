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
                self.data = get_sorted_recommendations(
                    self.movie_name.split(','))
            except:
                pass
        return render(request, 'similar/index.html', {'data': self.data})


def similar_movie(a):
    baseurl = config('baseurl1_movie')
    d = {'q': a, 'limit': 5,
         'k': config('apikey_movie'), 'verbose': 1}
    x = json.loads(rq.get(baseurl, params=d).text)
    return x


def extract_movie_titles(a):
    x = []
    for i in a['Similar']['Results']:
        x.append([i['Name'], i['yUrl']])
    return x


def get_related_titles(a):
    y = []
    for i in a:
        x = extract_movie_titles(similar_movie(i))
        for j in x:
            if j not in y:
                y.append(j)
    return y


def get_movie_data(a):
    baseurl = config('baseurl2_movie')
    d = {'t': a[0], 'r': 'json', 'apikey': config('apikey_moviedetail2')}
    x = json.loads(rq.get(baseurl, params=d).text)
    data = {'Year': x['Year'], 'Genre': x['Genre'].split(',')[:4], 'Poster': x['Poster'], 'imdbRating': x['imdbRating'], 'imdbVotes': float(
        x['imdbVotes'].replace(',', ''))/10000, 'Link': a[1], 'Type': x['Type']}
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


def get_sorted_recommendations(a):
    x = get_related_titles(a)
    result = {}
    for i in x:
        try:
            result[i[0]] = get_movie_data(i)
        except:
            pass
    b = sorted(result, key=lambda x: (
        float(result[x]['imdbRating']), float(result[x]['imdbVotes'])), reverse=True)
    res = {}
    for i in b:
        res[i] = result[i]
    return res
