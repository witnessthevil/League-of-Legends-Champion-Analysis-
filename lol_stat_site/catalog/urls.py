from django.urls import path
from . import views

urlpatterns = [
    path("",view=views.index,name="index"),
    path("v1/",view=views.v1,name="v11")
]