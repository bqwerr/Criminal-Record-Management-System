from django.urls import path
from  . import views
from . import api_views

urlpatterns = [
    path('', views.home, name="police_home"),
    path('citizen/<str:pk>/<str:typ>', views.citizen_profile, name="citizen_profile"),
    path('records/', views.view_records, name="view_records"),
    path('match/', views.match_face, name="match_face"),

    # api paths

    path('api/', api_views.apiOverview, name='overview'),
    path('api/description/', api_views.description, name='description'),
    path('api/records/', api_views.get_records, name='get_records'),
    path('api/add-record/', api_views.add_record, name='add_record'),
    path('api/delete-record/<str:pk>/', api_views.delete_record, name='delete_record'),
    path('api/train/', api_views.train_model, name="train_model"),
    path('api/match/', api_views.match_image, name='match_image')
]

