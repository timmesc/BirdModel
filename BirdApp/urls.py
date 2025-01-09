from django.urls import path 
from . import views

app_name = 'BirdApp'
urlpatterns = [
    path('', views.predictor, name = 'predictor'),
    path('formInfo/', views.formInfo, name = 'formInfo')
]