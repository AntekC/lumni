from django.shortcuts import render, redirect
from .models import Tutorial
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .form import NewUserForm
import readline
import socket
import sys

socket_address = '/home/pin/iBSR/backend/ibsr.sock'

# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name='main/home.html',
                  context={"tutorials": Tutorial.objects.all})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = NewUserForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})


def app(request):
    status = {}
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        try:
            sock.connect(socket_address)
            connected = True
            print(f'-- Connected to iBSR server @{socket_address}')
        except socket.error as err:
            connected = False
            print('-- Could not connect to iBSR server. Aborting shell')
        while connected:
            try:
                line = "status"
            except (KeyboardInterrupt, EOFError):
                break
            else:
                sock.sendall(line.encode('utf-8'))
                try:
                    response = sock.recv(4096).decode()
                    connected = False
                except socket.timeout:
                    print('-- No response from server')
                else:
                    if response:
                        status = response
                        print(status[0])
                    else:
                        print('-- Empty response')
        print('\n-- Bye!')
    return render(request=request,
                  template_name='main/home.html',
                  )    