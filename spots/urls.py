from django.urls import path

from . import views

app_name = 'spots'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:spot_id>/register', views.register, name='register'),
]
