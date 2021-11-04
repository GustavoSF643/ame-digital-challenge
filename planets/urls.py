from django.urls import path
from .views import PlanetsRetrieveView, PlanetsView

urlpatterns = [
    path('planets/', PlanetsView.as_view()),
    path('planets/<int:id>/', PlanetsRetrieveView.as_view()),
]