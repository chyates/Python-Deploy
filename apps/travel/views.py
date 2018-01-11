# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, time, datetime
from time import strptime, strftime, localtime
import re
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Trip

# Create your views here.
# GET REQUESTS
def index(request):
    return render(request, 'travel/index.html')

def add(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'travel/add_trip.html', context)

def trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip': trip,
        'travelers': trip.travelers.all(),
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'travel/trip.html', context)

def travels(request):
    user = User.objects.get(id=request.session['id'])
    trips_joined = Trip.objects.filter(travelers=user)
    context = {
        'trips_created':Trip.objects.filter(creator=user),
        'trips_joined':Trip.objects.filter(travelers=user),
        'other_trips': Trip.objects.all().exclude(creator=user).exclude(travelers=user),
        'user': user
    }
    return render(request, 'travel/dashboard.html', context)

def join(request, trip_id):
    current_trip = Trip.objects.get(id=trip_id)
    current_user = User.objects.get(id=request.session['id'])
    current_trip.travelers.add(current_user)
    current_trip.save()
    return redirect('/travels/destination/' + trip_id)

def destroy(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('/travels')

# def admin_destroy(request, id):
#     User.objects.get(id=id).delete()
#     return redirect('/dashboard')

def leave(request, id):
    current_trip = Trip.objects.get(id=id)
    print current_trip
    current_user = User.objects.get(id=request.session['id'])
    print current_user
    current_trip.travelers.remove(current_user)
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

# POST REQUESTS
def register(request):
    result = User.objects.valid_reg(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['id'] = result.id
    return redirect('/travels')

def login(request):
    result = User.objects.valid_log(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['id'] = result.id
    return redirect('/travels')

def create(request):
    result = Trip.objects.valid_trip(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/travels/add')
    return redirect('/travels')
    