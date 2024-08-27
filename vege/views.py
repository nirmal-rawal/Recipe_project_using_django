from django.shortcuts import render, redirect, get_object_or_404
from .models import Recp
from django.http import HttpResponse

# Create your views here.

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

def update_receipe(request,id):
    queryset=get_object_or_404(Recp,id=id)

    if request.method=="POST":
        data=request.POST
        data = request.POST
        recepie_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description

        if recepie_image:
            queryset.receipe_image=recepie_image

        queryset.save()
        return redirect("/r/rec/")
    return render(request,'vege/update.html',{"receipe":queryset} )

def delete_receipe(request, id):
    queryset = get_object_or_404(Recp, id=id)
    queryset.delete()
    return redirect("/r/rec/")


