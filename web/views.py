from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def index(request):
    if(request.user.is_authenticated):
        return redirect(reverse("topics:index"))
    return login_funktion(request)


def login_funktion(request):
    if(request.user.is_authenticated):
        return redirect(reverse("topics:index"))
    L_Form = AuthenticationForm()
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=name,password=password)
        if user:
            login(request, user)
            return redirect(reverse('topics:index'))

    return render(request, 'web/login.html', {'L_Form': L_Form})

def register_funktion(request):
    if(request.user.is_authenticated):
        return redirect(reverse("topics:index"))
    R_Form = UserCreationForm()

    if request.method == "POST":
        R_Form = UserCreationForm(request.POST)
        if R_Form.is_valid():
            R_Form.save()
            
            name = R_Form.cleaned_data["username"]
            password = R_Form.cleaned_data["password1"]
            user = authenticate(request, username=name,password=password)
            if user:
                login(request, user)
                return redirect(reverse('topics:index'))

    return render(request, 'web/register.html', {'R_Form': R_Form})



def logOut_view(request):
        logout(request)
        return redirect(reverse('web:index'))