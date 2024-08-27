from . import views
from django.urls import path

urlpatterns = [
    path('rec/', views.receipes),
    path("delect-recepie/<id>",views.delete_receipe,name="delete_receipe"),
    
]
