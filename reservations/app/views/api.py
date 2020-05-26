from django.shortcuts import render
from django.http import JsonResponse
import requests
import time

from rest_framework import generics, status
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from app.models.artist import Artist
from app.models.location import Location
from app.models.show import Representation
from app.models.show import Show
from app.serializers.artists import ArtistSerializer
from app.serializers.location import LocationSerializer
from app.serializers.representation import RepresentationSerializer
from app.serializers.show import ShowSerializer


class ArtistApiView (generics.ListAPIView):
    """ Comment here """  # TODO: Comment class

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('id', 'lastname')


class RepresentationApiView (generics.ListAPIView):
    """ Comment here """  # TODO: Comment class

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('id', 'location')


class ShowApiView (generics.ListAPIView):
    """ Comment here """  # TODO: Comment class

    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('id', 'title')


class LocationApiView (generics.ListAPIView):
    """ Comment here """  # TODO: Comment class

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('id', 'designation')

MAX_RETRIES = 5  # Arbitrary number of times we want to try

class ExternalAPIShowView(generics.GenericAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    # Get the list of show from Théatre de la ville de Paris
    def get(self, request, *args, **kwargs):
        data_list = []
        attempt_num = 0  # keep track of how many times we've retried
        external_api_url = "https://api.theatredelaville-paris.com/events" 
        r = requests.get(external_api_url, timeout=10)
        data_all = r.json()
        while attempt_num < MAX_RETRIES:
            if r.status_code == 200:
                for i in range(len(data_all['hydra:member'])):
                    title = data_all['hydra:member'][i]['name']
                    #slug = data_all['hydra:member'][i]['slug']
                    description = data_all['hydra:member'][i]['excerpt']
                    bookable = data_all['hydra:member'][i]['ticketingOpen']
                    price = str(data_all['hydra:member'][i]['priceRange'])
                    date_created = data_all['hydra:member'][i]['ticketingOpening']
                    image = data_all['hydra:member'][i]['image']

                    if image != None : 
                        poster = image['contentUrl']['medium']

                    # Extract the price from the string 
                    if price == 'None':
                        price = 0
                    elif price[0] == 'd' or price[0] == 'D':
                        price = price[3:5].strip()
                    else :
                        price = price[:2]
                        if price[1] == '€':
                            price = price[0]
                        else:
                            price = price.strip()
                    
                    #Convert the price in Integer
                    price = int(price)

                    data_filtered = {
                        'title' : title,
                        #'slug' : slug,
                        'description' : description,
                        'poster' : poster,
                        'bookable' : bookable,
                        'price' : price,
                        'date_created' : date_created,
                    }
                    data_list.append(data_filtered) 
                return Response(data_list, status=status.HTTP_200_OK)
            else:
                    attempt_num += 1
                    time.sleep(5)  # Wait for 5 seconds before re-trying
            return Response({"error": "Request failed"}, status=r.status_code)
    


class ExternalAPI(generics.ListAPIView):
    queryset = ''

    def get(self, request, *args, **kwargs):
        attempt_num = 0  # keep track of how many times we've retried
        external_api_url = "https://api.theatredelaville-paris.com/events" 
        r = requests.get(external_api_url, timeout=10)
        data_all = r.json()
        while attempt_num < MAX_RETRIES:
            if r.status_code == 200:
                data = data_all
                return Response(data, status=status.HTTP_200_OK)
            else:
                    attempt_num += 1
                    time.sleep(5)  # Wait for 5 seconds before re-trying
            return Response({"error": "Request failed"}, status=r.status_code)
