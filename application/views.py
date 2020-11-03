from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings as st
import json
import os

# main page function

def index(request):
    # if not request.user.is_authenticated:
    #     return redirect("login")
    return render(request, 'main.html')


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

def makeIcon(any):
    if any == "T":
        return "done"
    else:
        return "clear"

def read_csv_file(file_name, word):
    full_path = os.path.join(os.path.join(st.BASE_DIR, "static"), file_name)
    container = []
    data = open(full_path, "r")
    x = 0
    for i in data:
        single = i.replace("\n", "").split(",")

        if single[2] != word:
            continue
    
        if x != 0:
            single[4:12] = list(map(lambda x: makeIcon(x), single[4:12]))

        container.append(single)

        x += 1
    return container

def getProject(request):
    output = {}
    if request.method == "GET" and request.is_ajax():
        # get project details here
        word = request.GET.get("project_number")
        data = read_csv_file("data2.csv", word)
        if len(data) > 0:
            output['status'] = True
            output['data'] = data
        else:
            output['status'] = False

    return JsonResponse(output)