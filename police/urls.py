from django.urls import path
from  . import views


urlpatterns = [
    path('', views.home, name="police_home"),
    path('citizen/<str:pk>/<str:typ>', views.citizen_profile, name="citizen_profile"),
    path('records/', views.view_records, name="view_records"),
]

