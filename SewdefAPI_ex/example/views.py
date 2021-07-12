from django.shortcuts import render
from .forms import *
import requests
import ast
from .models import SewDefToken
import datetime
from django.shortcuts import redirect

# Create your views here.

#here we have a variable with the base SewDefAPI url for ease of use
APIURL ="https://sewdef.inlocrobotics.com/v1/api/"


def index(request):
    #############################
    # IMPORTANT: Here you should be filtering the tokens by YOUR users to ensure each uses their own tokens
    token = SewDefToken.objects.all()
    #############################
    # here we check if we have a token which is still valid
    # if we don't, then we will have to generate a new one, and probably you should delete the old ones
    token = token.exclude(expireDate__lte=datetime.datetime.now())
    if len(token)<1:
        return redirect('login')  # redirect to the login view to generate a new token
    #############################
    else:
        return render(request, "index.html")


def login(request):  # view to login to the SewDefAPI to generate a new token
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            #############################
            # here we make the request to the SewDefAPI to login and generate a token
            r = requests.request(method="POST", url=APIURL+"login", params={"username": username, "password": password})
            dict_str = r.content.decode("UTF-8")
            rc = ast.literal_eval(dict_str)

            if rc["status"] == 200:
                message = "Login Successful"
                tok = SewDefToken()
                #############################
                # here we save the string which is the token itself
                tok.token = rc["token"]
                #############################
                # here we save the estimated expiration date after which the token will not be valid anymore
                tok.expireDate = datetime.datetime.now() + datetime.timedelta(hours=1)
                #############################
                # IMPORTANT: When saving a token you should also save a relationship to which of YOUR users it pertains
                #            We don't do it here as this is just an example app to demonstrate API calls to SewDef
                #############################
                tok.save()  # here we save the object to the database
                return redirect('index')
            elif rc["status"] == 401:
                message = "Incorrect Password"

    form = LoginForm()
    context = {
        "form": form,
        "message": message
    }
    return render(request=request, template_name="login.html", context=context)


def contracts(request):
    ###############
    # as we have seen in the index view here we look for a valid token
    token = SewDefToken.objects.all()
    token = token.exclude(expireDate__lte=datetime.datetime.now())
    if len(token)<1:
        return redirect('login')  # redirect to the login view to generate a new token
    #############################
    else:
        tok = token[0].token
        #############################
        # here we do the request to the SewdefAPI to get information of the user's contracts
        r = requests.request(method="GET", url=APIURL + "contracts", headers={"x-access-token": tok})
        #############################
        return render(request, 'contracts.html', context=r.json())

def jobs(request):
    ###############
    # as we have seen in the index view here we look for a valid token
    token = SewDefToken.objects.all()
    token = token.exclude(expireDate__lte=datetime.datetime.now())
    if len(token)<1:
        return redirect('login')  # redirect to the login view to generate a new token
    #############################
    else:
        tok = token[0].token
        #############################
        # here we do the request to the SewdefAPI to get information of the user's jobs
        r = requests.request(method="GET", url=APIURL + "jobs", headers={"x-access-token": tok}, params={"lang": "en"})
        #############################
        jobsc = r.json()

        return render(request, 'jobs.html', context=jobsc)

