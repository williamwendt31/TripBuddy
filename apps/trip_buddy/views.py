from django.shortcuts import render, HttpResponse, redirect
from django.template.defaultfilters import date
from .models import *

def index(request):
    if 'user_id' not in request.session:
        return render(request, 'index.html')
    else:
        return redirect('/travels')

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validations(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        pwd_hash = bcrypt.hashpw(request.POST['pwd'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pwd_hash=pwd_hash)
        request.session['user_id'] = user.id
        print("here")
        return redirect('/travels')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/travels')

def travels(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "trips": Trip.objects.exclude(planned_by=User.objects.get(id=request.session['user_id'])).exclude(joined_users=User.objects.get(id=request.session['user_id']))
    }
    return render(request, 'travels.html', context)

def show(request, id):
    context = {
        "trip": Trip.objects.get(id=id)
    }
    return render(request, 'show.html', context)

def addtrip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'addtrip.html')


def processadd(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addtrip')
        Trip.objects.create(dest=request.POST['dest'], desc=request.POST['desc'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planned_by=User.objects.get(id=request.session['user_id']))
    return redirect('/travels')


def join(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    trip.joined_users.add(User.objects.get(id=request.session['user_id']))
    trip.save()
    return redirect('/travels')


def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    Trip.objects.get(id=id).delete()
    return redirect('/travels')


def cancel(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    Trip.objects.get(id=id).joined_users.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/travels')
    

def logout(request):
    request.session.clear()
    return redirect('/')