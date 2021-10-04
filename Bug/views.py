import random
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import *
import csv
def index(request):
    if request.user.is_authenticated:
        g = GeoIP2()
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            ip = xff.split(',')[0]
            country = g.country(ip)
            city = g.city(ip)
            lat, long = g.lat_lon(ip)
        else:
            ip = request.META.get('REMOTE_ADDR', None)
            country = 'Your Country Name'
            city='Your City'
            lat,long = 'Your Latitude','Your Longitiude'
        location={
            "ip":ip,
            "country":country,
            "city":city,
            "lat":lat,
            "lon":long
        }
        if location["country"]=="Your Country Name":
            location=False
        return render(request, "Bug/index.html",{"location":location})
    else:
        return HttpResponseRedirect(reverse("login"))

# API
# https://www.inaturalist.org/pages/api+reference#get-observations-taxon_stats
# https://www.inaturalist.org/places.json?taxon=Coleoptera&latitude=20.6536704&longitude=-101.3710848&per_page=50
# https://www.inaturalist.org/taxa/48662-Danaus-plexippus

# https://mol.org/species/map/Grus_japonensis

def species(request):
    with open("Bug/mexico/Mexico.csv") as f:
        reader = csv.reader(f)
        next(reader)
        i=0
        animals=[]
        for row in reader:
            push ={}
            for cell in row:
                if row.index(cell) == 0:
                    push["Name"]=cell
                elif row.index(cell)==1:
                    push["CommonName"]=cell
                elif row.index(cell)==2:
                    push["Family"]=cell
                elif row.index(cell)==3:
                    push["TaxonomicGroup"]=cell
            animals.append(push)
            print(animals)
            i+=1
            if i >= 50:
                break
        del animals[0]
        del animals[0]
        del animals[0]
        return JsonResponse(animals, safe=False)


def logind(request):
    if request.method=="GET":
        return render(request,"Bug/login.html")
    elif request.method=="POST":
        if request.POST["confirmation"]:
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "network/register.html", {
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
          # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "network/login.html", {
                    "message": "Invalid username and/or password."
                })  
def logoutd(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def me(request,user):
    pass

def Saw(request):
    pass

def Species(request):
    pass

def rightNow(request):
    pass
