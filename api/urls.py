from django.urls import path

from api.views import (
    GetIngredient, AddToFavorites,
    RemoveFromFavorites,
    AddToFollow, RemoveFromFollow,
    AddPurchase, RemovePurchase
)


urlpatterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('follow/', AddToFollow.as_view()),
    path('unfollow/<int:pk>/', RemoveFromFollow.as_view()),
    path('purchases/', AddPurchase.as_view()),
    path('purchases/<int:pk>/', RemovePurchase.as_view()),
    path('ingredients', GetIngredient.as_view({'get': 'list'})),
]
