from lists import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='home'),
    path('linked_person/', views.linked_person, name='linked_person'),
]