from django.urls import path

from . import views

app_name = 'spots'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:spot_id>/', views.detail, name='detail'),
]
