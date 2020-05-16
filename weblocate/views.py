from django.shortcuts import render
from django.views.generic import TemplateView
from decouple import config

import requests as rq
import json
import socket
from datetime import datetime


class ipToLocation(TemplateView):
    template_name = "ip/index.html"

    def __init__(self):
        self.address = '0'
        self.data = '0'

    def get(self, request):
        return render(request, 'ip/index.html', {'name': self.data, 'ip': self.address})

    def post(self, request):
        self.address = request.POST['search']
        self.addressValidator(request)
        if self.address != '0':
            self.data = {}
            baseurl = config('baseurl1_ip')
            apikey = config('apikey_ipdetail1')
            params = {'apiKey': apikey,
                      'ip': self.address}
            res = rq.get(baseurl, params)
            res = json.loads(res.text)
            try:
                self.data['Time'] = time(res['time_zone']['current_time'])
                self.data['IP Address'] = self.address
                self.data['ISP'] = res['isp']
                self.data['Organization'] = res['organization']
                if self.data['Organization'] == "":
                    self.data['Organization'] = self.data['ISP']
                self.data['Full Address'] = location(
                    res['latitude'], res['longitude'])
                self.data['Area'] = res['district']
                try:
                    if self.data['Area'] == "":
                        self.data['Area'] = ','.join(self.data['Full Address'].split(
                            ',')[0:2])
                except:
                    pass
                self.data['City'] = res['city']
                self.data['Country'] = res['country_name']
                self.data['Continent'] = res['continent_name']
            except:
                self.data = '0'
                pass
        request.session['name'] = self.data
        return render(request, 'ip/index.html', {'name': self.data, 'ip': self.address})

    def addressValidator(self, request):
        try:
            if self.address.lower() in ['my', 'own', 'current']:
                self.address = request.META.get(
                    'HTTP_X_FORWARDED_FOR').split(',')[0]
        except:
            self.address = '0'
        else:
            try:
                self.address = self.address.split('://')[1].split('/')[0]
            except:
                self.address = self.address.split('/')[0]
            try:
                self.address = socket.getaddrinfo(self.address, 80)[0][4][0]
            except:
                self.address = '0'


def time(dtime):
    try:
        time = datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S.%f%z')
        now = time.strftime("%d-%b-%Y %A %I:%M%p")
    except:
        try:
            time = datetime.strptime(dtime, '%Y-%m-%d %I:%M:%S.%f%z')
            now = time.strftime("%d-%b-%Y %A %I:%M%p")
        except:
            return None
    return now


def location(lat, long):
    baseurl = config('baseurl2_ip')
    geoad = str(lat)+','+str(long)
    apikey = config('apikey_ipdetail2')
    params = {'q': geoad, 'key': apikey,
              'language': 'en', 'pretty': '1'}
    res = rq.get(baseurl, params)
    try:
        return json.loads(res.text)['results'][0]['formatted']
    except:
        return 0


def print_pdf(request):
    return render(request, 'ip/pdf.html', {'name': request.session['name']})
