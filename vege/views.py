from django.shortcuts import render, redirect, get_object_or_404
from .models import Recp
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        recepie_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        Recp.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=recepie_image,
        )
        return redirect('/r/rec/')

    queryset = Recp.objects.all()
    if request.GET.get("search"):
        queryset=queryset.filter(receipe_name__icontains=request.GET.get("search"))
    return render(request, 'vege/receipes.html', {"data": queryset})

@login_required(login_url="/login/")
def update_receipe(request, id):
    print(f"User authenticated: {request.user.is_authenticated}")
    queryset = get_object_or_404(Recp, id=id)

    if request.method == "POST":
        data = request.POST
        recepie_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if recepie_image:
            queryset.receipe_image = recepie_image

        queryset.save()
        return redirect("/r/rec/")

    return render(request, 'vege/update.html', {"receipe": queryset})

@login_required(login_url="/login/")
def delete_receipe(request, id):
    print(f"User authenticated: {request.user.is_authenticated}")
    queryset = get_object_or_404(Recp, id=id)
    if request.method == "POST":
        queryset.delete()
        return redirect("/r/rec/")
    return render(request, 'vege/confirm_delete.html', {"receipe": queryset})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid username")
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Password wrong")
            return redirect('/login/')
        else:
            login(request, user)  # Pass the request object here
            return redirect('/r/rec/')
                
    return render(request, "vege/login.html")


def logout_page(request):
    logout(request)
    return redirect('/login/')



def register(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already Exits")
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Successfully")
        return redirect("/register/")        
    return render(request,"vege/register.html")
