from django.urls import path
from . import views

app_name = "mypage"

urlpatterns = [
    path('', views.mypageview, name='home'),
    path('trajectory', views.FatlossjourneyView, name='trajectory'),
    path('addFatLossJourneyForm', views.newfatlossjourneyform, name='addFatLossJourneyForm'),
]
