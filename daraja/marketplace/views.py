from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

############# api libraries#############
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

import uuid
########################################

########## global variable #######
base_url = 'https://12ba-197-248-162-150.ngrok-free.app'
key = 'nAbuuqCD0dMH3uhXSO5A2yY7rd1HACYE'
secret = '3ZnvWnVqFqPgvUXF'
####################################


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

################# ACCOUNTS ########################
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'login success')
            return redirect('index')  # Redirect to profile page after registration
    else:
        form = UserCreationForm()
        context = {"form":form, "error":form.errors}
    context = {"form":form}
    return render(request, 'accounts/register.html', context)

# Login user
def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a specific URL after login
            return redirect('index')  # Replace 'home' with your desired URL name
        else:
            # Handle invalid login
            # Add error message or other handling as needed
            messages.error(request,'invalid username or password')
            return redirect('login')
    else:
        # Display login form
        message = messages.get_messages(request)
        return render(request, 'accounts/login.html', {'messages':message})

# Logout 
def logout_view(request):
    logout(request)
    # Redirect to a success page
    return redirect('index')

######################## END ACCOUNTS ########################################


######################### ACCESS TOKEN ##################################
def get_access_token():
    consumer_key = key
    consumer_secret = secret
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']

########################## END ACCESS TOKEN #############################



######################### STK #################################
def stkpush(request):
    phone = request.POST.get('phone')
    amount = request.POST.get('amount')

    # if form.is_valid():
        

    return render(request, 'stk.html', )


def init_stk(request):
    
    phone = request.POST.get('phone')
    amount = request.POST.get('amount')

    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = get_access_token()
    headers = { "Authorization": f"Bearer {access_token}" }
    my_endpoint = base_url 
    Timestamp = datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
    datapass = base64.b64encode(password.encode('utf-8')).decode('utf-8')  # Decode to string
    # print(datapass)

    data = {
        "BusinessShortCode": "174379",
        "Password": datapass,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline", # for paybill - CustomerPayBillOnline
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone, # fill with your phone number
        "CallBackURL": my_endpoint + "/mpesa-express-callback",
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }
    res = requests.post(endpoint, json=data, headers=headers)
    response = res.json()
    # print(response)
    # error = response["errorMessage"]
    # print("success")
    context = { "response":response }

    return render(request, 'stkresult.html', context)   
    # if response['ResponseCode'] == 0:
    #     return HttpResponse("success")
    # else:
    #     return HttpResponse(response['errorMessage'])


####################### END STK ###############################
